"""Gemensamma parametrar. Belopp och räntor är årliga om inget annat anges."""

from math import log1p

# Från Labb2/main2.ipynb, uppgift 7 (cell 40).
# Samma variabelnamn som i labb 2 för att underlätta jämförelsen.
x = 60                       # Ålder vid start; försäkringen gäller en kvinna.
z = 65                       # Pensionsålder.
max_age = 120                # Slutålder för beräkningshorisonten.
u = z - x                    # År till pensionering.
s = max_age - z              # Antal år med pension.
P = 120_000                  # Årlig premie, betalas med P/12 per månad.
G_0 = 2_000_000              # Första ordningens reserv vid start.
r_G = 0.02                   # Effektiv årlig garantiränta.
delta_G = log1p(r_G)         # Motsvarande kontinuerlig ränta.

# Full precision från sparad utskrift i labb 2, uppgift 6b (cell 34).
# Kvinnans parametrar används för försäkringen; männens bevaras som referens.
alpha_W = 0.0007385920444426279
beta_W = 5.691931706360492e-07
gamma_W = 0.1363098414907224

alpha_M = 0.0011632139663998189
beta_M = 1.1569727380463711e-06
gamma_M = 0.1316502928381501

# Nya indata från labb 3-instruktionen; ingår inte i labb 2-kontrollen.
V_0 = 2_100_000              # Andra ordningens reserv vid start.
A_0 = 2_100_000              # Tillgångarnas värde vid start.
r_p = 0.02                  # Effektiv årlig prognosränta.
delta_p = log1p(r_p)
transfer_rate = 0.02         # Årlig transfersannolikhet.

# Tillgångarnas ordning från labb 2. Scenariofilerna använder Y5 i stället för Y05.
stocks = ["BA", "CAT", "KO", "DIS", "JPM", "MMM", "MSFT", "PFE", "WMT", "XOM"]
rates = ["Y05", "Y10", "Y15", "Y20", "Y30"]
