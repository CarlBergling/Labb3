import numpy as np


def calculate_be(scenario, first_order_cashflow):
    """Discount future first-order cash flows using each month's zero rates."""
    maturities = [5, 10, 15, 20, 30]
    zero_rates = scenario[["Y5", "Y10", "Y15", "Y20", "Y30"]].to_numpy()
    BE = np.zeros(len(scenario))

    for t in range(len(scenario)):
        future_cashflows = first_order_cashflow[t + 1:]
        years_to_payment = np.arange(1, len(future_cashflows) + 1) / 12

        # Linear between quoted maturities, flat beyond either end.
        rates = np.interp(years_to_payment, maturities, zero_rates[t])
        discount_factors = np.exp(-rates * years_to_payment)
        BE[t] = np.sum(future_cashflows * discount_factors)

    return BE
