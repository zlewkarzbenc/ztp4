import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
"""
visualizations.py
--------------
Moduł służący do wizualizacji danych o stężeniu pyłów PM2.5.
Zawiera funkcje do generowania wykresów liniowych, map ciepła (heatmaps) 
oraz zestawień słupkowych dla wybranych stacji pomiarowych.

"""
def plot_average(monthly_df_grouped, years, cities, show=True):
    """
        Funkcja rysująca wykres liniowy pokazujący trend średnich miesięcznych wartości PM2.5 dla wybranych lat i miast  

    Args:
        monthly_df_grouped (pd.DataFrame): Zgrupowana po miastach ramka danych z uśrednionymi miesięcznymi wartościami PM2.5 
        years (list[int]): lista lat które będą analizowane  
        cities(list[str]): lista analizowanych miast 
   
    Returns:
        None
    """
    # średnie dla stacji
    colors = plt.cm.Set1.colors
    color_index = 0

    df = monthly_df_grouped[cities]
    
    for year in years:
        df_year = df.loc[year]
        for city in cities:
            plt.plot(range(1,13), df_year[city], label=f'{city} {year}', marker='o', color=colors[color_index])
            color_index += 1

    plt.xlabel('Miesiąc')
    plt.xticks(range(1,13))
    plt.ylabel('Średni poziom PM2.5')
    plt.title(f'Średni miesięczny poziom PM2.5\n w miastach: {", ".join(cities)} w latach: {", ".join(map(str, years))}')
    plt.legend()
    plt.tight_layout()
    if show:
        plt.show()
    return 

def bar_plots(norms_df, year, show=True):
    """
        Funkcja przygotowująca wykres słupkowy grupowany ze wszytkich analizowanych lat dla 3 stacji z najmniejszą i 3 z największą liczbą dni przekroczenia normy w wybranym roku, gdzie oś X – stacje,
        a oś Y – liczba dni z przekroczeniem normy
    
    Args:
        norms_df (pd.DataFrame): Dataframe z z MultiIndexem (['Miejscowość', 'Kod stacji']. 
            Kolumny to lata, wartości to liczba dni powyżej normy.
        year (int): Rok referencyjny dla wyboru stacji ekstremalnych. 
    
    Returns:
        None
    """
    min_stations = norms_df[year].nsmallest(3).index.get_level_values(1).tolist()
    max_stations = norms_df[year].nlargest(3).index.get_level_values(1).tolist()
    stations = min_stations + max_stations

    idx = pd.IndexSlice
    plot_df = norms_df.loc[idx[:, stations], :].reset_index()

    # melt, żeby mieć kolumny: miasto, stacja, rok, liczba_dni
    plot_df = plot_df.melt(id_vars=['Miejscowość', 'Kod stacji'], var_name='rok', value_name='liczba_dni')

    # połącz miasto i kod w jedną kolumnę
    plot_df['miasto_stacja'] = plot_df['Miejscowość'] + '\n' + plot_df['Kod stacji']

    # wykres
    plt.figure(figsize=(10, 6))
    sns.barplot(data=plot_df, x='miasto_stacja', y='liczba_dni', hue='rok', palette='viridis')
    plt.xticks(rotation=45)
    plt.ylabel('Liczba dni z przekroczeniem normy')
    plt.title('Dni z przekroczeniem normy PM2.5 dla wybranych stacji')
    plt.legend(title='Rok')
    plt.tight_layout()
    if show:
        plt.show()  
    return 
    
if __name__ == "__main__":
    pass