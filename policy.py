"""Återanvända försäkringsberäkningar från labb 2, uppgift 7.

Reserven beräknas för en kvarvarande, levande försäkring. Förväntade
populationer och transfereringar kopplas in senare i labb 3.
"""

import numpy as np

import config
from makeham import survival_function_makeham


def guaranteed_yearly_payout(
    age=config.x,
    retirement_age=config.z,
    max_age=config.max_age,
    annual_premium=config.P,
    initial_reserve=config.G_0,
    guaranteed_rate=config.r_G,
    alpha=config.alpha_W,
    beta=config.beta_W,
    gamma=config.gamma_W,
):
    """Beräkna årlig garanterad pension b enligt labb 2, cell 41.

    Premier betalas i slutet av månad 1 till och med pensionsmånaden.
    Första pensionen betalas månaden därefter. Alla betalningar vägs
    med överlevnadssannolikheten och diskonteras med garantiräntan.
    """
    n_premium_months = int(round(12 * (retirement_age - age)))
    n_total_months = int(round(12 * (max_age - age)))
    delta = np.log1p(guaranteed_rate)
    l_x = survival_function_makeham(alpha, beta, gamma, age)

    pv_premium_units = 0.0
    for t in range(1, n_premium_months + 1):
        l_x_t = survival_function_makeham(alpha, beta, gamma, age + t / 12)
        pv_premium_units += (l_x_t / l_x) * np.exp(-delta * t / 12)
    pv_premiums = pv_premium_units * annual_premium / 12

    pv_payout_units = 0.0
    for t in range(n_premium_months + 1, n_total_months + 1):
        l_x_t = survival_function_makeham(alpha, beta, gamma, age + t / 12)
        pv_payout_units += (l_x_t / l_x) * np.exp(-delta * t / 12)

    return 12 * (initial_reserve + pv_premiums) / pv_payout_units


def project_first_order_reserve(
    n_months=360,
    yearly_payout=None,
    age=config.x,
    retirement_age=config.z,
    max_age=config.max_age,
    annual_premium=config.P,
    initial_reserve=config.G_0,
    guaranteed_rate=config.r_G,
    alpha=config.alpha_W,
    beta=config.beta_W,
    gamma=config.gamma_W,
):
    """Returnera G[0..n_months] enligt rekursionen i labb 2, cell 43.

    G är reserven per kvarvarande försäkring, inklusive arvsvinst.
    Ränta och riskpremie baseras på föregående månads reserv, precis
    som i labb 2. Grundinställningen återskapar dess 30-årsprojektion.
    """
    n_total_months = int(round(12 * (max_age - age)))
    if not isinstance(n_months, (int, np.integer)) or not 0 <= n_months <= n_total_months:
        raise ValueError("n_months ska vara ett heltal inom försäkringens beräkningshorisont.")

    if yearly_payout is None:
        yearly_payout = guaranteed_yearly_payout(
            age=age,
            retirement_age=retirement_age,
            max_age=max_age,
            annual_premium=annual_premium,
            initial_reserve=initial_reserve,
            guaranteed_rate=guaranteed_rate,
            alpha=alpha,
            beta=beta,
            gamma=gamma,
        )

    n_premium_months = int(round(12 * (retirement_age - age)))
    delta = np.log1p(guaranteed_rate)
    G = np.zeros(n_months + 1)
    G[0] = initial_reserve

    for t in range(1, n_months + 1):
        current_age = age + (t - 1) / 12
        premium = annual_premium / 12 if t <= n_premium_months else 0.0

        l_x_t = survival_function_makeham(alpha, beta, gamma, current_age + 1 / 12)
        l_x = survival_function_makeham(alpha, beta, gamma, current_age)
        q_m = 1 - l_x_t / l_x
        sum_at_risk = -G[t - 1]
        risk_premium = q_m / (1 - q_m) * sum_at_risk

        guaranteed_return = G[t - 1] * (np.exp(delta / 12) - 1)
        pension = 0.0 if t <= n_premium_months else yearly_payout / 12
        G[t] = G[t - 1] + premium - risk_premium + guaranteed_return - pension

    return G
