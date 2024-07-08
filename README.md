**Optimal Bet Allocation Tool**
Overview
This Python script helps users optimize their bet allocations across multiple betting options to maximize their utility. The script supports various utility functions, allowing users to choose the one that best matches their risk preferences. Additionally, users have the option to visualize their chosen utility function.

Prerequisites
Before running the script, ensure you have the following libraries installed:

- numpy
- pandas
- matplotlib
- scipy
You can install these libraries using pip:

bash

pip install numpy pandas matplotlib scipy

**Usage**
1. Prepare Your Data: Ensure your betting data is in a CSV file with the following columns:

probabilities: The probability of winning for each bet.
payout_ratios: The payout ratio for each bet.
correlation_indices: Indices indicating correlated bets (use 0 if there are no correlations).

2. Run the Script: Execute the script and follow the prompts:

python optimal_bet_allocation.py

Input Details:

Total Bet: Enter the total amount you want to wager.
Utility Function Choice: Select your preferred utility function from the list provided.
Utility Function Parameters: If required, provide additional parameters for the chosen utility function.
Visualization Option: Choose whether you want to see a plot of the utility function.

**Output:**
The script will display the optimal bet allocation for each bet.
If visualization is chosen, a plot of the selected utility function will be displayed.
Utility Functions Supported:

Linear: u(w) = w
Exponential: u(w) = -e^(-alpha * w)
CRRA: u(w) = (w^(1-gamma)) / (1-gamma)
Square-root: u(w) = sqrt(w)
Logarithmic: u(w) = ln(w)
Quadratic: u(w) = w - beta * w^2
Hyperbolic: u(w) = (1/y) * (alpha + beta * w)^y
Power: u(w) = (w^k) / k for k < 1
