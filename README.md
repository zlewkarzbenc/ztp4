# Wizualizacja poziomu zanieczyszczeń (PM2.5)

Projekt ma na celu  wizualizację danych dotyczących poziomu zanieczyszczenia powietrza PM2.5, 
aby ułatwić analizę danych oraz przedstawić zmiany stężenia pyłu w czasie w polskich miastach. 

----------

#### Repozytorium zawiera:
* Pliki z kodem źródłowym:
  * `load_data.py` - moduł odpowiedzialny za wczytywanie i czyszczenie danych
  * `compute_averages.py` - moduł, który oblicza średnie dla miast zawartych w danych wejściowych
  * `visualizations.py` - moduł generujący wykresy i wizualizacje danych
  * `main.ipynb` - notebook, który pokazuje użycie wszystkich modułów
* Pliki danych:
  * `all_data.csv` - surowe dane wejściowe używane w późniejszych obliczeniach i ogólnej analizie
  * `monthly_average.csv` - miesięczne średnie stężenia PM2.5 w miastach, które są zawarte w pliku all_data.csv

---------

#### Jak zainstalować i uruchomić projekt?

1. Sklonuj repozytorium
```bash
git clone https://github.com/zlewkarzbenc/ztp_grupa_16
```

2. Utwórz wirtualne środowisko (zalecane)
```bash
python -m venv venv
source ./venv/bin/activate
```
3. Zainstaluj potrzebne biblioteki
```bash
pip install -r requirements.txt
```
<!-- czy to potrzebne?
4. Uruchom główny notebook
```bash
jupyter notebook
```
-->
---------

#### Źródła danych

[Główny Inspektorat Ochrony Środowiska – powietrze.gios.gov.pl](https://powietrze.gios.gov.pl/pjp/archives)

---------

### Autorzy: Aleksander Janowiak, Dominika Aniszewska

---------

#### Niespodzianka dla pary 17
Pomiary uśredniane są najpierw wewnątrz stacji, a w danych GIOS występują brakujące wartości co oznacza, że niektóre stacje mają danej doby mniej pomiarów niż inne. Przez to, poszczególne pomiary nie są traktowane równocennie. Brakujących wartości nie jest bardzo dużo, ale jest ich wystarczająco by metoda uśredniania wpływała na końcowy wykres.
