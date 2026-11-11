# Labb3
Ett repo till riskmodellering

## Överfört från labb 2

- `makeham.py`: redan kopierad, identisk med originalet i labb 2.
- `config.py`: försäkringsdata från uppgift 7 och Makeham-parametrar med full
  precision från uppgift 6b. Nya indata för labb 3 är markerade separat.
- `policy.py`: beräkning av garanterad pension (cell 41) och första ordningens
  reserv (cell 43), omgjorda till funktioner med samma beräkningslogik.
- `main3.ipynb`: tillståndsmodellens areadiagram och anrop till ALM-förberedelserna.
- `requirements.txt`: de paket som behövs för denna grund och notebooken.

Garanterad årlig pension ska bli cirka 164 404,8790 och G efter fem år cirka
2 885 198,92. Reserven är per kvarvarande försäkring, inte den förväntade
reserven för hela populationen. `prepare_first_order_policy` i `policy.py`
kopplar nu ihop reserven med tillståndsmodellen och beräknar förväntat G samt
första ordningens kassaflöde. Positiva kassaflöden betyder nettoutbetalningar.

Öppna `Labb3` i VS Code och kör notebooken med en Pythonmiljö som har paketen i
`requirements.txt`. Kör cellerna i ordning. Labb 3-beräkningarna kräver inga
importer eller datafiler från den intilliggande labb 2-mappen.

`market_data.csv` finns redan här och är identisk med labb 2:s kopia. SCB-rådata,
hela labb 2-notebooken och de veckobaserade scenariogeneratorerna ligger kvar i
labb 2; de behövs inte för att köra de överförda beräkningarna. Parametrarnas
ursprung finns dokumenterat i `config.py` och labb 2 behöver inte skattas om.

## Modellens nuvarande upplägg

- `state_model.py`: populationer och månadsvisa övergångar enligt föreläsning 12.
- `policy.py`: pension, första ordningens reserv och försäkringsunderlag fram
  till slutåldern 120 år (720 månader från start).
- `alm.py`: `prepare_alm` väljer scenariots simuleringsperiod, beräknar
  aktieavkastning och skapar startportföljen. Den hämtar även hela
  försäkringsunderlaget från `policy.py`. Standardportföljen är lika belopp
  i tio aktier, utan obligationer, för testet i uppgift 2.
- Notebooken läser scenariofilen och anropar modellfilerna. Resultatet
  `alm_inputs` innehåller bland annat `stock_returns`, `initial_holdings`
  och `policy`. I `policy` finns `b`, `G`, `expected_G`, populationer,
  övergångar och `first_order_cashflow`.

Simuleringens standardhorisont är 360 månader. Försäkringsunderlaget har
721 start- och månadsvärden även för en kortare simulering, så att framtida
utbetalningar efter simuleringsslutet kan ingå i BE.

## Återstår att implementera

`run_alm` kör nu månadsloopen för aktieportföljen i uppgift 2 och returnerar
förväntat G och V, tillgångar, BE och BOF. BE beräknas i `valuation.py`.
Diagrammet, femårstabellen och livslängds-SCR återstår, liksom strategierna
och scenarioanalysen i senare uppgifter.
