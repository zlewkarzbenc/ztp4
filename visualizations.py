# wizualizacje
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_city_trends(monthly_df, cities=["Warszawa", "Katowice"], years=[2015, 2024], ylim=[0, 75]):
    """(Zad2)
    Plot monthly PM2.5 trends for selected cities and years.

    Args:
        monthly_df (pd.DataFrame): DataFrame with MultiIndex (year, month) and cities as columns.
        cities (list[str]): Cities to include in the plot.
        years (list[int]): Years to include in the plot.
        ylim (list[int]): Y-axis limits.

    Returns:
        ax (matplotlib.axes.Axes): the desired lineplot to be shown in Zad2
    """

    # data preparation
    df = monthly_df.loc[years, cities].reset_index()

    df_long = df.melt(
        id_vars=["year", "month"],
        var_name="city",
        value_name="pm25"
    )

    df_long["series"] = (
        df_long["city"] + " " + df_long["year"].astype(str)
    )

    # coloring
    palette = sns.color_palette("coolwarm", 4)

    city_colors = {
        cities[0]: palette[:2][::-1], # reverse the pallete here for more consistent coloring (darker lines for later years)
        cities[1]: palette[2:],
    }

    year_order = sorted(years)
    color_map = {
        f"{city} {year}": city_colors[city][i]
        for city in cities
        for i, year in enumerate(year_order)
    }

    # plotting
    fig, ax = plt.subplots(figsize=(12, 6))

    sns.lineplot(
        data=df_long,
        x="month",
        y="pm25",
        hue="series",
        palette=color_map,
        marker="o",
        alpha=0.85,
        ax=ax,
    )

    ax.set_title(f"Wykres stężenia PM2.5 (µg/m³) w {cities[0]} i {cities[-1]} w latach {years[0]} oraz {years[-1]}", fontsize=13)
    ax.set_xlabel("Miesiąc")
    ax.set_ylabel("PM2.5 (µg/m³)")
    ax.set_xlim(1, 12)
    ax.set_ylim(*ylim)

    ax.set_xticks(range(1,13))
    ax.grid(alpha=0.4)

    ax.legend(title="", frameon=False)
    fig.tight_layout()

    return ax


def plot_pm25_exceedance_bars(
    exceedance_counts: pd.DataFrame,
    top_n: int = 3,
    base_year: int = 2024,
    threshold: float = 15,
    figsize=(12, 6),
):
    """(Zad4)
    Create a grouped barplot of the number of days with average PM2.5 above who_threshold.
    Include top_n best and worst stations in terms of days over treshold in year base_year.

    Args:
        exceedance_counts (pd.DataFrame): 
        top_n (int): Number of highest and lowest exceedence stations to be displayed.
        base_year (int): year that constitues the criterion for selecting the highest and lowest exceedence stations.  
        who_threshold (int): information to be displayed on the plot

    Returns:
        ax (matplotlib.axes.Axes): the desired barplot to be shown in Zad4
    """
    # select top & bottom stations based on base_year
    exceedance_base = (
        exceedance_counts
        .loc[exceedance_counts["year"] == base_year]
        .sort_values("days_exceeded", ascending=True)
    )

    top_stations = exceedance_base["station"].tail(top_n).tolist()
    bottom_stations = exceedance_base["station"].head(top_n).tolist()
    # keep selected stations in a list for plot ordering
    selected_stations = bottom_stations + top_stations

    plot_df = (
        exceedance_counts
        .loc[exceedance_counts["station"].isin(selected_stations)]
        .copy()
    )

    # create labels for the barplot
    plot_df["label"] = (
        plot_df["city"].astype(str) + ": " + plot_df["station"].astype(str)
    )

    # build station to label mapping to make labels ordered correctly
    label_map = (
        plot_df
        .drop_duplicates("station")
        .set_index("station")["label"]
        .to_dict()
    )

    # try to make a colormap that always looks good...
    years = sorted(plot_df["year"].unique())
    palette = sns.color_palette("magma", n_colors=len(years) + 2)[2:]
    year_palette = dict(zip(years, palette))

    fig, ax = plt.subplots(figsize=figsize)

    sns.barplot(
        data=plot_df,
        x="station",
        y="days_exceeded",
        hue="year",
        order=selected_stations,
        palette=year_palette,
        ax=ax,
    )

    ax.set_xticks(range(len(selected_stations)))
    # replace x-axis labels with "city: station"
    ax.set_xticklabels(
        [label_map[s] for s in selected_stations],
        rotation=45,
        ha="right"
    )

    # styling
    ax.set_title(
        "Liczba dni z przekroczeniem normy dobowej PM2.5\n"
        f"(PM2.5 > {threshold} µg/m³, WHO)\n"
        f"{top_n} stacje z najmniejszą i {top_n} z największą liczbą dni w {base_year}",
        fontsize=13,
    )

    ax.set_xlabel("Stacja pomiarowa (miasto: kod stacji)")
    ax.set_ylabel("Liczba dni z przekroczeniem normy dobowej")
    ax.grid(axis="y", alpha=0.4)
    ax.legend(title="Rok", frameon=False)

    fig.tight_layout()
    return ax

def main():
    print("visualizations module. This is only to be used through an import.")

if __name__ == "__main__":
    main()