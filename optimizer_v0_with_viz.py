import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize


# Read data from CSV file
def read_csv(file_path):
    data = pd.read_csv(file_path)
    probabilities = data.iloc[:, 0].values
    payout_ratios = data.iloc[:, 1].values
    correlation_indices = data.iloc[:, 2].values
    return probabilities, payout_ratios, correlation_indices

file_path = 'test_bets_1.csv'  # Replace with CSV file path
probabilities, payout_ratios, correlation_indices = read_csv(file_path)

total_bet = float(input("How much do you want to wager in total? "))  # Total amount you're willing to wager

# Define utility functions
def u_linear(w):
    return w

def u_exponential(w, alpha):
    return -np.exp(-alpha * w)

def u_crra(w, gamma):
    if gamma != 1:
        return (w**(1-gamma)) / (1-gamma)
    else:
        return np.log(w)

def u_sqrt(w):
    return np.sqrt(w)

def u_log(w):
    return np.log(w)

def u_quadratic(w, beta):
    return w - beta * w**2

def u_hyperbolic(w, alpha, beta, y):
    return (1/y) * (alpha + beta * w)**y

def u_power(w, k):
    if k != 0:
        return (w**k) / k
    else:
        return np.log(w)  # In case k approaches 0
    
# Plot the utility function
def plot_utility_curve(utility_func, utility_name, W_range=(0.1, 100)):
    W = np.linspace(W_range[0], W_range[1], 500)
    U = utility_func(W)
    plt.figure(figsize=(10, 6))
    plt.plot(W, U, label=f'{utility_name} Utility Curve')
    plt.xlabel('Wealth (W)')
    plt.ylabel('Utility (U)')
    plt.title(f'Utility Curve for {utility_name} Function')
    plt.legend()
    plt.grid(True)
    plt.show()
    
see_visualization = input("Do you want to see a visualization of the utility function? (yes/no): ").strip().lower()

# Ask the user to choose a utility function
print("Choose a utility function:")
print("1: u(w) = w")
print("2: u(w) = -e^(-alpha * w)")
print("3: u(w) = (w^(1-gamma)) / (1-gamma)")
print("4: u(w) = sqrt(w)")
print("5: u(w) = ln(w)")
print("6: u(w) = w - beta * w^2")
print("7: u(w) = (1/y) * (alpha + beta * w)^y")
print("8: u(w) = (w^k) / k for k < 1")

utility_choice = int(input("Enter the number of your chosen utility function: "))

# Ask for necessary constant inputs
alpha, beta, gamma, y, k = None, None, None, None, None
if utility_choice == 2:
    alpha = float(input("Enter the value of alpha: "))
elif utility_choice == 3:
    gamma = float(input("Enter the value of gamma: "))
elif utility_choice == 6:
    beta = float(input("Enter the value of beta: "))
elif utility_choice == 7:
    alpha = float(input("Enter the value of alpha: "))
    beta = float(input("Enter the value of beta: "))
    y = float(input("Enter the value of y: "))
elif utility_choice == 8:
    k = float(input("Enter the value of k: "))

# Define selected utility function
def utility(w):
    if utility_choice == 1:
        return u_linear(w)
    elif utility_choice == 2:
        return u_exponential(w, alpha)
    elif utility_choice == 3:
        return u_crra(w, gamma)
    elif utility_choice == 4:
        return u_sqrt(w)
    elif utility_choice == 5:
        return u_log(w)
    elif utility_choice == 6:
        return u_quadratic(w, beta)
    elif utility_choice == 7:
        return u_hyperbolic(w, alpha, beta, y)
    elif utility_choice == 8:
        return u_power(w, k)
    
# Plot selected utility curve if the user wants to see it
W_range = (0.1, 100)
if see_visualization == 'yes':
    if utility_choice == 1:
        plot_utility_curve(u_linear, "Linear", W_range)
    elif utility_choice == 2:
        plot_utility_curve(lambda W: u_exponential(W, alpha), "Exponential", W_range)
    elif utility_choice == 3:
        plot_utility_curve(lambda W: u_crra(W, gamma), "CRRA", W_range)
    elif utility_choice == 4:
        plot_utility_curve(u_sqrt, "Square-root", W_range)
    elif utility_choice == 5:
        plot_utility_curve(u_log, "Logarithmic", W_range)
    elif utility_choice == 6:
        plot_utility_curve(lambda W: u_quadratic(W, beta), "Quadratic", W_range)
    elif utility_choice == 7:
        plot_utility_curve(lambda W: u_hyperbolic(W, alpha, beta, y), "Hyperbolic", W_range)
    elif utility_choice == 8:
        plot_utility_curve(lambda W: u_power(W, k), "Power", W_range)
        
# Define expected utility function
def expected_utility(bet_allocations):
    w = total_bet
    utility_value = 0
    n = len(bet_allocations)
    
    for i in range(n):
        bet = bet_allocations[i]
        p_win = probabilities[i]
        p_lose = 1 - p_win
        payout_ratio = payout_ratios[i]
        correlation_index = correlation_indices[i]

        # Check for correlated bets
        if correlation_index != 0:
            correlated_bets = [j for j in range(n) if correlation_indices[j] == correlation_index and j != i]
            for j in correlated_bets:
                correlated_p_win = probabilities[j]
                correlated_payout_ratio = payout_ratios[j]
                util_correlated_win = utility(w + bet * payout_ratio + bet_allocations[j] * correlated_payout_ratio)
                util_correlated_lose = utility(w - bet)
                utility_value += correlated_p_win * util_correlated_win + (1 - correlated_p_win) * util_correlated_lose
        else:
            util_win = utility(w + bet * payout_ratio)
            util_lose = utility(w - bet)
            utility_value += p_win * util_win + p_lose * util_lose
    
    return -utility_value  # Minimize negative utility --> maximize utility

# Initial guess: even distribution among all bets
initial_guess = np.full(len(probabilities), total_bet / len(probabilities))

# Bounds: bet amounts should each be between 0 and total_bet
bounds = [(0, total_bet) for _ in range(len(probabilities))]

# Constraint: sum of all bet allocations should equal total_bet
constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - total_bet}

# Optimize
result = minimize(expected_utility, initial_guess, bounds=bounds, constraints=constraints)

# Retrieve the optimal bet amounts
optimal_bets = result.x

# Print the results
for i, bet in enumerate(optimal_bets):
    print(f"Optimal bet on Bet {i+1}: ${bet:.2f}")

print(f"Total Bet: ${np.sum(optimal_bets):.2f}")
