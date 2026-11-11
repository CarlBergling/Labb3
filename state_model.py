"""
Implement the state model for the policy and plot the populations (PP, PO, TR, DE) for 
each period 50 years (600 months) into the future. 
Use the area plot to visualize the size of the populations over time.
"""

import numpy as np

import config
from makeham import survival_function_makeham


def state_model(
        n_months=600,
        age=config.x,
        retirement_age=config.z,
        transfer_rate=config.transfer_rate,
        alpha=config.alpha_W,
        beta=config.beta_W,
        gamma=config.gamma_W,
        mortality_factor=1.0
):
    """
    Calculate the monthly populations in PP, PO, TR and DE.
    The policy starts in PP. Transitions occur in the order:
    death, transfer, then start of pension payments.
    """

    # Populations
    pop_pp = np.zeros(n_months+1)
    pop_pp[0] = 1 # Everyone is policy-paying at the beginning
    pop_po = np.zeros(n_months+1)
    pop_tr = np.zeros(n_months+1)
    pop_de = np.zeros(n_months+1)

    # Transitions
    t_pp_po = np.zeros(n_months+1)
    t_pp_tr = np.zeros(n_months+1)
    t_po_de = np.zeros(n_months+1)
    t_pp_de = np.zeros(n_months+1)
    
    monthly_transfer_rate = 1 - (1 - transfer_rate) ** (1/12)
    first_payout_month = (12 * (retirement_age - age)) + 1

    for t in range(1, n_months+1):
        start_age = age + ((t-1)/12)
        end_age = age + ((t)/12)

        l_start = survival_function_makeham(alpha, beta, gamma, start_age)
        l_end = survival_function_makeham(alpha, beta, gamma, end_age)

        # probability of death
        q_month_base = 1 - (l_end/l_start)
        q_month = q_month_base * mortality_factor

        # This months transfers to death
        t_pp_de[t] = pop_pp[t-1] * q_month
        t_po_de[t] = pop_po[t-1] * q_month

        t_pp_tr[t] = (pop_pp[t-1] - t_pp_de[t]) * monthly_transfer_rate

        if t == first_payout_month:
            t_pp_po[t] = (pop_pp[t - 1] - t_pp_de[t] - t_pp_tr[t])
        
        # Update populations
        pop_pp[t] = pop_pp[t - 1] - (t_pp_de[t] + t_pp_tr[t] + t_pp_po[t])
        pop_po[t] = pop_po[t - 1] - t_po_de[t] + t_pp_po[t]
        pop_tr[t] = pop_tr[t - 1] + t_pp_tr[t]
        pop_de[t] = pop_de[t - 1] + t_pp_de[t] + t_po_de[t]
    
    return pop_pp, pop_po, pop_tr, pop_de, t_pp_de, t_po_de, t_pp_tr, t_pp_po


