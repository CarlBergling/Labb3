# Labb3
Ett repo till riskmodellering

## Överfört från labb 2

- `makeham.py`: redan kopierad, identisk med originalet i labb 2.
- `config.py`: försäkringsdata från uppgift 7 och Makeham-parametrar med full
  precision från uppgift 6b. Nya indata för labb 3 är markerade separat.
- `policy.py`: beräkning av garanterad pension (cell 41) och första ordningens
  reserv (cell 43), omgjorda till funktioner med samma beräkningslogik.
- `main3.ipynb`: körbar kontroll av pensionsbelopp, reservtabell och reservdiagram.
- `requirements.txt`: de paket som behövs för denna grund och notebooken.

Garanterad årlig pension ska bli cirka 164 404,8790 och G efter fem år cirka
2 885 198,92. Reserven är per kvarvarande försäkring, inte den förväntade
reserven för hela populationen. Populationer och transfereringar ingår ännu inte.

Öppna `Labb3` i VS Code och kör notebooken med en Pythonmiljö som har paketen i
`requirements.txt`. Kör cellerna i ordning. Labb 3-beräkningarna kräver inga
importer eller datafiler från den intilliggande labb 2-mappen.

`market_data.csv` finns redan här och är identisk med labb 2:s kopia. SCB-rådata,
hela labb 2-notebooken och de veckobaserade scenariogeneratorerna ligger kvar i
labb 2; de behövs inte för att köra de överförda beräkningarna. Parametrarnas
ursprung finns dokumenterat i `config.py` och labb 2 behöver inte skattas om.

## Återstår att implementera

`state_model.py`, `valuation.py`, `scenarios.py`, `strategies.py` och `alm.py`
är tomma platshållare. Andra ordningens reserv, omräknad pension och förväntade
kassaflöden ska senare läggas till i `policy.py`. Notebookens kontroll är en
kontroll mot labb 2, inte en lösning på labb 3:s uppgifter.
