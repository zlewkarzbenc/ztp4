# Zadanie 4. z zaawansowanych technik programowania dla bioinformatyków

Pipeline wykonuje analizy stężeń pyłów w powietrzu, przygotowuje przegląd literatury i generuje raport. 

## Uruchomienie programu

W pliku config/task4.yaml użytkownik ustawia lata, np.:

years: [2021, 2024]

Następnie wpisuje w terminalu:
```{bash}
snakemake --cores 1
```
Komenda wyszukuje plik o nazwie `Snakefile` i wykonuje workflow w nim zdefiniowany. Gdy mamy kilka rożnych workflowów,możemy wybrać ten, który chcemy wykonać za pomocą opcji `-s`. 
## Scenariusz działania

1) 

Użytkownik ustawia w pliku konfiguracyjnym:

- years: [2021, 2024]

Uruchamia:
```{bash}
snakemake --cores 1
```
Pipeline:

- uruchamia kod running_pm25.py dla lat 2021 i 2024
- uruchamia kod pubmed_fetch.py dla lat 2021 i 2024
- uruchamia kod generate_report.py i generuje raport dla {2021, 2024}

2) 

Użytkownik zmienia config na:

- years: [2019, 2024]

Uruchamia:

- `snakemake -s Snakefile_task4 --cores 1`

Pipeline:
- uruchamia kod `running_pm25.py` dla roku 2019; 2024 zostaje pominięty
- uruchamia kod `pubmed_fetch.py` dla roku 2019; 2024 zostaje pominięty
- uruchamia kod `generate_report.py` i generuje raport dla {2019, 2024}

## Weryfikacja tego, że pliki nie przeliczają się drugi raz

Przy uruchomieniu linijki:

```{bash}
snakemake --cores 1 --summary
```
Pojawia się informacja, którep pliki są aktualne, a które muszą zostać przeliczone od nowa.

Po uruchomieniu programu wyświetla się również informacja typu:

    Job stats:
    job             count
    ------------  -------
    all                 1
    pm25_metrics        2
    pubmed_fetch        2
    report              1
    total               6

Widać tutaj, że pm25_metrics i pubmed_fetch uruchamiają sie dla dwóch lat. Jeśli nie byłoby potrzeby uruchomienia ich dla któregoś roku informacja ta wyglądałaby tak:

    Job stats:
    job             count
    ------------  -------
    all                 1
    pm25_metrics        1
    pubmed_fetch        1
    report              1
    total               4

Jeśli wszystkie pliki są aktualne, po uruchomieniu programu dostajemy informację:

    Nothing to be done (all requested files are present and up to date).

## Zawartość repozytorium

Folder config zawiera plik task4.yaml. Są tam parametry do podania przez użytkownika. Użytkownik nie edytuje pozostałych plików.

Folder src zawiera kody źródłowe podzielone na 3 części: literature, pm25 i report.

-Podfolder pm25 zawiera pliki powstałe dla zadań 1 i 3 (`average_and_limits.py`, `data_loader.py` i `visualizations.py`) oraz `running_pm25.py` zawierający kod, który używa funkcji z reszty plików w sposób potrzebny do odecnego zadania.

-Podfolder literature zawiera plik `pubmed_fetch.py` pobierający dane z bazy danych PubMed.

-Podfolder report zawiera plik generate_report.py tworzący raport MarkDown z danych uzyskanych w tym zadaniu.

Folder tests zawiera plik test_pubmed_fetch.py zawierający testy pliku pubmed_fetch.py.

Plik Snakefile uruchamia pipline za pomocą Snakemake.

#### Źródła danych

[Główny Inspektorat Ochrony Środowiska – powietrze.gios.gov.pl](https://powietrze.gios.gov.pl/pjp/archives)

---------

### Autorzy: Aleksander Janowiak

---------

#### Niespodzianka dla pary 17
Pomiary uśredniane są najpierw wewnątrz stacji, a w danych GIOS występują brakujące wartości co oznacza, że niektóre stacje mają danej doby mniej pomiarów niż inne. Przez to, poszczególne pomiary nie są traktowane równocennie. Brakujących wartości nie jest bardzo dużo, ale jest ich wystarczająco by metoda uśredniania wpływała na końcowy wykres.
