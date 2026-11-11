"""Reused from labb2"""

import numpy as np

import config
from makeham import survival_function_makeham
from state_model import state_model


def guaranteed_yearly_payout():
    """Calculate the guaranteed annual pension."""
    premium_months = 12 * (config.z - config.x)
    total_months = 12 * (config.max_age - config.x)

    l_start = survival_function_makeham(
        config.alpha_W, config.beta_W, config.gamma_W, config.x
    )

    pv_premiums = 0.0
    for t in range(1, premium_months + 1):
        years = t / 12
        age = config.x + years
        l_t = survival_function_makeham(
            config.alpha_W, config.beta_W, config.gamma_W, age
        )
        survival = l_t / l_start
        discount = np.exp(-config.delta_G * years)
        pv_premiums += (config.P / 12) * survival * discount

    pv_pension = 0.0
    for t in range(premium_months + 1, total_months + 1):
        years = t / 12
        age = config.x + years
        l_t = survival_function_makeham(
            config.alpha_W, config.beta_W, config.gamma_W, age
        )
        survival = l_t / l_start
        discount = np.exp(-config.delta_G * years)
        pv_pension += survival * discount

    monthly_pension = (config.G_0 + pv_premiums) / pv_pension
    return 12 * monthly_pension


def project_first_order_reserve(n_months, yearly_payout):
    """Calculate G for a policy that is still active."""
    premium_months = 12 * (config.z - config.x)
    monthly_rate = np.exp(config.delta_G / 12) - 1

    G = np.zeros(n_months + 1)
    G[0] = config.G_0

    for t in range(1, n_months + 1):
        start_age = config.x + ((t - 1) / 12)
        end_age = config.x + (t / 12)

        l_start = survival_function_makeham(
            config.alpha_W, config.beta_W, config.gamma_W, start_age
        )
        l_end = survival_function_makeham(
            config.alpha_W, config.beta_W, config.gamma_W, end_age
        )
        q_month = 1 - (l_end / l_start)

        previous_reserve = G[t - 1]
        mortality_gain = (q_month / (1 - q_month)) * previous_reserve
        interest = previous_reserve * monthly_rate

        if t <= premium_months:
            premium = config.P / 12
            pension = 0.0
        else:
            premium = 0.0
            pension = yearly_payout / 12

        G[t] = previous_reserve + premium + mortality_gain + interest - pension

    return G


def prepare_first_order_policy(mortality_factor=1.0):
    """Calculate the expected reserve and cash flows up to age 120."""
    n_months = 12 * (config.max_age - config.x)

    b = guaranteed_yearly_payout()
    G = project_first_order_reserve(n_months, b)

    pop_pp, pop_po, pop_tr, pop_de, t_pp_de, t_po_de, t_pp_tr, t_pp_po = state_model(
        n_months=n_months, mortality_factor=mortality_factor
    )

    expected_G = (pop_pp + pop_po) * G

    first_order_cashflow = np.zeros(n_months + 1)
    for t in range(1, n_months + 1):
        pension = pop_po[t] * (b / 12)
        transfer = t_pp_tr[t] * G[t - 1]
        premium = pop_pp[t] * (config.P / 12)
        first_order_cashflow[t] = pension + transfer - premium

    return {
        "b": b,
        "G": G,
        "expected_G": expected_G,
        "pop_pp": pop_pp,
        "pop_po": pop_po,
        "pop_tr": pop_tr,
        "pop_de": pop_de,
        "t_pp_de": t_pp_de,
        "t_po_de": t_po_de,
        "t_pp_tr": t_pp_tr,
        "t_pp_po": t_pp_po,
        "first_order_cashflow": first_order_cashflow,
    }