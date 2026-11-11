"""Run the ALM model for the stock portfolio in task 2."""

import numpy as np
import pandas as pd

import config
from makeham import survival_function_makeham
from policy import prepare_first_order_policy
from valuation import calculate_be


def prepare_alm(scenario, 
                n_months=360, 
                asset_columns=config.stocks,
                initial_weights=None):
    """
    Prepare stock returns, initial holdings and the first-order policy data.
    """
 
    scenario = scenario.iloc[:n_months + 1]

    stock_prices = scenario[asset_columns]
    stock_returns = stock_prices.pct_change()

    n_stocks = len(asset_columns)
    if initial_weights:
        #weight_per_stock = Här är vi
    amount_per_stock = config.A_0 / n_stocks
    initial_holdings = np.full(n_stocks, amount_per_stock)

    policy = prepare_first_order_policy()

    return {
        "n_months": n_months,
        "scenario": scenario,
        "stock_prices": stock_prices,
        "stock_returns": stock_returns,
        "initial_holdings": initial_holdings,
        "policy": policy,
    }


def run_alm(scenario, n_months=360, asset_columns=config.stocks):
    """Project the reserves, assets, BE and BOF for one scenario."""
    inputs = prepare_alm(scenario=scenario, 
                         n_months=n_months, 
                         asset_columns=asset_columns)
    stock_returns = inputs["stock_returns"]
    holdings = inputs["initial_holdings"]
    policy = inputs["policy"]

    G = policy["G"]
    b = policy["b"]
    pop_pp = policy["pop_pp"]
    pop_po = policy["pop_po"]
    t_pp_tr = policy["t_pp_tr"]

    V = np.zeros(n_months + 1)
    assets = np.zeros(n_months + 1)
    V[0] = config.V_0
    assets[0] = holdings.sum()

    first_payout_month = 12 * (config.z - config.x) + 1
    months = np.arange(len(G))
    ages = config.x + (months / 12)
    survival = survival_function_makeham(config.alpha_W, config.beta_W, config.gamma_W, ages)

    for t in range(1, n_months + 1):
        
        returns = stock_returns.iloc[t].to_numpy()
        holdings = holdings * (1 + returns)
        assets_before_cashflow = holdings.sum()
        portfolio_return = (assets_before_cashflow / assets[t - 1]) - 1


        q_month = 1 - (survival[t] / survival[t - 1])
        mortality_gain = (q_month / (1 - q_month)) * V[t - 1]
        investment_gain = V[t - 1] * portfolio_return
        premium = 0.0
        if t < first_payout_month:
            premium = config.P / 12
        reserve_before_payout = V[t - 1] + mortality_gain + investment_gain + premium

        monthly_pension = 0.0
        if t >= first_payout_month:

            remaining_years = (months[t:] - t) / 12
            survival_given_alive = survival[t:] / survival[t]
            discount = np.exp(-config.delta_p * remaining_years)
            annuity_factor = np.sum(survival_given_alive * discount)
            monthly_pension = max(b / 12, reserve_before_payout / annuity_factor)

        V[t] = reserve_before_payout - monthly_pension


        pension_cashflow = pop_po[t] * monthly_pension
        transfer_cashflow = t_pp_tr[t] * max(G[t - 1], V[t - 1])
        premium_cashflow = pop_pp[t] * premium
        cashflow = pension_cashflow + transfer_cashflow - premium_cashflow

        weights = holdings / assets_before_cashflow
        holdings = holdings - weights * cashflow
        assets[t] = holdings.sum()

    active_population = pop_pp[:n_months + 1] + pop_po[:n_months + 1]
    expected_V = active_population * V
    BE = calculate_be(inputs["scenario"], policy["first_order_cashflow"])
    BOF = assets - BE

    return pd.DataFrame({
        "Period": np.arange(n_months + 1),
        "Expected G": policy["expected_G"][:n_months + 1],
        "Expected V": expected_V,
        "Assets": assets,
        "BE": BE,
        "BOF": BOF,
    })
