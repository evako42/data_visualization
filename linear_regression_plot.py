import pandas as pd

file_path = 'experiment_data.xlsx'
experimental_condition = pd.read_excel(file_path, sheet_name='data1')
control_condition = pd.read_excel(file_path, sheet_name='data2')

def make_lr_plot(x_val:str, y_val:str, dataf:object, jitter:float, plot_title:str):
            """
            This function creates a scatter plot with the linear regression model of the arguments.
            Additionally, it prints out the spearman correlation. (NB: could modify so that the function returns instead of prints, or provides this value in the title)
    
            Args:
                x_val, y_val (string): input variables; these should be column names in data.
                dataf (object): dataframe where each column is a variable and each row is an observation.
                jitter (float): add uniform random noise of this size to either the x variables. 
                plot_title (string): The desired title of the plot.
    
            """
        import seaborn as sns
        import matplotlib.pyplot as plt

        # Linear regression model
        lm = sns.lmplot(x=x_val,y=y_val, data=dataf,x_jitter=jitter)
        ax = lm.axes
        ax = ax[0,0]
        plt.ylim(-10,80)
        plt.xlim(-10,80)

        # The diagonal line
        ax.plot(ax.get_xlim(), ax.get_ylim(), ls="--", color='gray')
        plt.xlabel(f"{x_val}", size=18)
        plt.ylabel(f"{y_val}",size=18)

        # Get the stats
        from scipy.stats import linregress
        lr = linregress(dataf[x_val], dataf[y_val])
        r_value = lr[2]
        r_squared = r_value**2

        # Use spearmanr to calculate the Spearman's rank correlation
        from scipy.stats import spearmanr
        correlation, p_value = spearmanr(dataf[x_val], dataf[y_val])

        # Print the result
        print(f"Spearman's correlation: {round(correlation, 4)}")
        print(f"P-value: {round(p_value,10)}")

        ax = plt.suptitle(f'{plot_title}\nR2: {round(r_squared,3)}',size=15, style='oblique')
        plt.show()

# Merge the DataFrames based on the 'Subject' column
merged_df = pd.merge(experimental_condition, control_condition, on='Subjects')
merged_df = merged_df.drop_duplicates(subset='Subjects')

for column in merged_df.columns:
    if column != 'Subjects':
        merged_df[column] = pd.to_numeric(merged_df[column], errors='coerce')

#print(merged_df.dtypes)
print(merged_df)
condition = 5
make_lr_plot(x_val= f'{condition}_x', y_val = f'{condition}_y', dataf = merged_df , jitter = 0.5, plot_title = 'Experiment 1')
