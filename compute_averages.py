# liczenie średnich i wskazywanie dni z przekroczeniem normy
import pandas as pd

def monthly_average(data, metadata_idx=3):
    """(Zad2)
    Function used to compute monthly averages of PM2.5 concentration in Zad2.
    Averages over measurements in all stations for a given city in a given month (in a given year)
    Args:
        data (pandas.DataFrame): a dataframe of PM2.5 levels
        metadata_idx (int): index of the first non-metadata row in the `data` DataFrame

    Returns:
        result (pandas.DataFrame): a dataframe of average monthly PM2.5 in each city with MultiIndex (year, month) and cities as columns.
    """
    # add "year" an "month" columns for downstream indexing
    dt = pd.to_datetime(
        data["Miejscowość"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce"
    )

    data["year"] = dt.dt.year
    data["month"] = dt.dt.month

    ## prepare the new "city" column (used for aggregation)
    meta_cols = {"Miejscowość", "year", "month"}
    station_cols = [c for c in data.columns if c not in meta_cols]

    # construct a dictionary for mapping stations to cities
    city_names = (
        pd.Series(station_cols)
        .str.replace(r"\.\d+$", "", regex=True) # this converts eg. "Kraków.1" to "Kraków"
    )

    station_to_city = dict(zip(station_cols, city_names))

    # drop metadata, then melt
    no_metadata_df = data[metadata_idx:].drop("Miejscowość", axis=1)

    long = no_metadata_df.melt(id_vars=["year", "month"], value_vars=station_cols, var_name="station", value_name="pm2.5")

    # ensure all stations are assigned to a city
    long["city"] = long["station"].map(station_to_city)
    long.drop("station", axis=1, inplace=True)

    ## perform the actual aggregation
    long["pm2.5"] = pd.to_numeric(long["pm2.5"], errors="coerce")
    monthly_avg = long.groupby(["year", "month", "city"], as_index=False).mean(numeric_only=True)

    # pivot back to a readable format
    result = (
        monthly_avg
        .pivot(
            index=["year", "month"],
            columns="city",
            values="pm2.5"
        )
        .sort_index()
    )

    # convert Multindex from float to int
    idx = result.index

    idx = idx.set_levels(
        idx.levels[idx.names.index("year")].astype(int),
        level="year"
    )

    idx = idx.set_levels(
        idx.levels[idx.names.index("month")].astype(int),
        level="month"
    )

    result.index = idx

    return result

def count_days_over_treshold(data, treshold=15, metadata_idx=3):
    """ (Zad4)
    Function used to count days when PM2.5 concentration exceeds a given thershold for all stations in a given year.
    Args:
        data (pandas.DataFrame): a dataframe of PM2.5 levels
        treshold (int): maximum acceptable PM2.5 according to WHO 
        metadata_idx (int): index of the first non-metadata row in the `data` DataFrame

    Returns:
        exceedance_counts (pandas.DataFrame): a dataframe containing - for every station and every year - the number days where the average PM2.5 exceeded the acceptable thershold.
    """
    dt = pd.to_datetime(
    data["Miejscowość"],
    format="%Y-%m-%d %H:%M:%S",
    errors="coerce"
    )

    data["date"] = dt.dt.date
    data["year"] = dt.dt.year  

    meta_cols = {"Miejscowość", "year", "date"}
    station_cols = [c for c in data.columns if c not in meta_cols]

    ## map station column name to city, then station code to city

    # correct city names ("Kraków.1" to "Kraków")
    station_to_city = (
        pd.Series(station_cols, index=station_cols)
        .str.replace(r"\.\d+$", "", regex=True)
        .to_dict()
    )

    column_to_station = data.loc[0, station_cols].to_dict()

    # drop metadata
    df = data.iloc[metadata_idx:].copy()

    # prepare the long dataframe used for aggregation
    long = df.melt(
        id_vars=["year", "date"],
        value_vars=station_cols,
        var_name="column",
        value_name="pm25"
    )

    # eg. "station" is "MpKrakBulwar", "column" is "Kraków.1" and city is "Kraków" 
    long["station"] = long["column"].map(column_to_station)
    long["city"] = long["column"].map(station_to_city)

    long = long.drop("column", axis=1) # get rid of the intermediate column with station column names (like "Kraków.1")

    long["pm25"] = pd.to_numeric(long["pm25"], errors="coerce")

    # compute daily average PM2.5 by station
    daily  = (
        long
        .groupby(["year", "date", "city", "station"], as_index=False)
        .agg(daily_pm25=("pm25", "mean"))
    )

    daily["exceeded"] = daily["daily_pm25"] > treshold

    exceedance_counts = (
        daily
        .groupby(["year", "city", "station"], as_index=False)
        .agg(days_exceeded=("exceeded", "sum"))
    )

    # convert "year" from float to int
    exceedance_counts["year"] = exceedance_counts["year"].astype('int')

    return exceedance_counts


def main():
    print("compute_averages module. This is only to be used through an import.")

if __name__ == "__main__":
    main()