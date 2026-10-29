import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

def expressing_alpha_beta(gamma, mortality, ages):
    m = np.sum(mortality)
    g_gamma = np.sum(mortality * np.exp(gamma * ages))
    f1 = np.sum(np.exp(gamma * ages))
    f2 = np.sum(np.exp(2 * gamma * ages))

    alpha = (m * f2 - g_gamma * f1) / (len(ages) * f2 - f1**2)
    beta = (m * f1 - len(ages) * g_gamma) / (f1**2 - len(ages) * f2)

    return alpha, beta

def gamma_equation(gamma, mortality, ages):
    alpha, beta = expressing_alpha_beta(gamma, mortality, ages)
    equation = (alpha + beta * np.exp(gamma * ages) - mortality) * ages * beta * np.exp(gamma * ages)

    return np.sum(equation)

def fit_makeham(ages, mortality):
    gamma = brentq(gamma_equation, 0.01, 0.2, args=(mortality, ages))
    alpha, beta = expressing_alpha_beta(gamma, mortality, ages)

    return alpha, beta, gamma

def survival_function_makeham(alpha, beta, gamma, ages):
    survival = np.exp(-alpha * ages - (beta * (np.exp(gamma * ages) - 1) / gamma))

    return survival
    
def remaining_survival(t, alpha, beta, gamma, age, l_x):
    l_x_t = survival_function_makeham(alpha, beta, gamma, age + t) / l_x

    return l_x_t

def life_expectancy_makeham(age, alpha, beta, gamma):
    l_x = survival_function_makeham(alpha, beta, gamma, age)
    life_expectancy, error = quad(remaining_survival, 0, 150 - age, args=(alpha, beta, gamma, age, l_x))

    return life_expectancy
