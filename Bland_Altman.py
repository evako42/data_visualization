import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import shapiro

# Load files
file_path = 'excel_data_experiment.xlsx'
control_condition = pd.read_excel(file_path, sheet_name='control_condition')
experimental_condition = pd.read_excel(file_path, sheet_name='experimental_condition')

def rand_jitter(arr):
    stdev = .1 * (max(arr) - min(arr))
    return arr + np.random.randn(len(arr)) * stdev

def bland_altman_plot(data1, data2, plot_title:str):
    """
    This function creates a Bland Altman plot. Additionally, it checks for the normal distribution of the difference data.
    
    Args:
    data1, data2: input variables; these should be column names in data.
    plot_title (string): The desired title of the plot.
    
    """
    data1 = np.asarray(data1)
    data2 = np.asarray(data2)
    mean = np.mean([data1, data2], axis=0)

    diff = data1 - data2
    diff = rand_jitter(diff)

    # Perform the Shapiro-Wilk test to check for normal distribution
    _, p_value = shapiro(diff)
    alpha = 0.05
    # Check the p-value against the significance level
    if p_value > alpha:
        print(f"The diff data appears to be normally distributed (p-value: {p_value:.4f})")
    else:
        print(f"The diff data does not appear to be normally distributed (p-value: {p_value:.4f})")

    md = np.mean(diff)                   # Mean of the difference
    sd = np.std(diff, axis=0)            # Standard deviation of the difference
    positive_lima = md + 1.96*sd         # Limits of agreement
    negative_lima = md - 1.96*sd         # Limits of agreement

    plt.scatter(mean, diff)
    plt.axhline(md, color='black', linestyle='-', label= f'Mean of the difference: {round(md,3)}')
    plt.axhline(positive_lima, color='gray', linestyle='--', label = f'Mean + 95% 2SD: {round(positive_lima, 2)}')
    plt.axhline(negative_lima, color='gray', linestyle='--', label = f'Mean - 95% 2SD: {round(negative_lima, 2)}')
    plt.ylim(-40,30)
    plt.legend()
    plt.xlabel('Mean')
    plt.ylabel(f'Difference')
    plt.title(f'{plot_title}')
    plt.show()

bland_altman_plot(control_condition['test1'], experimental_condition['test1'], 'Condition comparison with BA plot')
