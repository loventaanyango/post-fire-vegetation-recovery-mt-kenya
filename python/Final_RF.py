import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.inspection import PartialDependenceDisplay
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import make_scorer
from scipy.stats import f_oneway
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Specify the directory where the CSV files are located
data_directory = r'C:\\Users\\hp\Desktop\\PROJECT\\Revised_data'  # Replace with your actual folder path

# List all CSV files in the directory
csv_files = [f for f in os.listdir(data_directory) if f.endswith('.csv')]

# Initialize a list to hold data from all CSVs
all_years_data = []

# Iterate over the CSV files and read them into pandas DataFrames
for file_name in csv_files:
    file_path = os.path.join(data_directory, file_name)
    df = pd.read_csv(file_path)
    
    # Add the year from the file name as a column (assuming the year is part of the file name)
    year = int(file_name.split('_')[2].split('.')[0])  # Extract year from the file name (e.g., 'averaged_data_2011.csv')
    df['Year'] = year
    
    # Append the DataFrame to the list
    all_years_data.append(df)

# Combine all the data into one DataFrame
combined_data = pd.concat(all_years_data, ignore_index=True)

# Now create a column for change in NBR compared to the prefire year (2011)
prefire_data = combined_data[combined_data['Year'] == 2011][['DN', 'nbr']]
prefire_data.rename(columns={'nbr': 'nbr_prefire'}, inplace=True)

# Merge the prefire data back to the combined data to calculate the change
combined_data = pd.merge(combined_data, prefire_data[['DN', 'nbr_prefire']], on='DN', how='left')
combined_data['nbr_change'] = combined_data['nbr'] - combined_data['nbr_prefire']

# Define your features (independent variables) and target (dependent variable)
X = combined_data[['Year', 'nbr', 'dnbr', 'lst', 'mean_temp', 'max_temp', 'min_temp', 'prec_sum', 'totc', 'aspect', 'slope', 'Elevation']]
y = combined_data['nbr_change']  # Target variable is the change in NBR compared to prefire year


# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Drop rows with NaN values in the target variable y_train
X_train = X_train[~y_train.isna()]
y_train = y_train.dropna()

# Initialize and train the Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = rf_model.predict(X_test)

# Evaluate the model
rmse = mean_squared_error(y_test, y_pred, squared=False)
r2 = r2_score(y_test, y_pred)

# Print the evaluation metrics
print(f'RMSE: {rmse}')
print(f'R²: {r2}')

#Cross validation
# Define the number of folds for cross-validation
k_folds = 10  # Common choice is 5 or 10

# Define a custom scoring function for RMSE
def rmse_score(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))

rmse_scorer = make_scorer(rmse_score, greater_is_better=False)

# Initialize the k-fold object
kf = KFold(n_splits=k_folds, shuffle=True, random_state=42)

# Perform k-fold cross-validation for RMSE and R²
rmse_scores = cross_val_score(rf_model, X, y, cv=kf, scoring=rmse_scorer)
r2_scores = cross_val_score(rf_model, X, y, cv=kf, scoring='r2')

# Average metrics across folds
mean_rmse = -np.mean(rmse_scores)  # Negative because scoring function returns negative RMSE
mean_r2 = np.mean(r2_scores)

# Print cross-validation results
print(f'K-Fold Cross-Validation Results ({k_folds} Folds):')
print(f'Average RMSE: {mean_rmse:.4f}')
print(f'Average R²: {mean_r2:.4f}')


# Group data by burn severity classes
classes = combined_data['DN'].unique()
class_data = [combined_data[combined_data['DN'] == c]['nbr_change'] for c in classes]

# Perform one-way ANOVA
anova_result = f_oneway(*class_data)
print(f"F-statistic: {anova_result.statistic}, p-value: {anova_result.pvalue}")

# Filter out the '0' class from the data
filtered_data = combined_data[combined_data['DN'] != 0]

# Perform Tukey HSD test on filtered data
tukey = pairwise_tukeyhsd(filtered_data['nbr_change'], filtered_data['DN'], alpha=0.05)
print(tukey)

# Tukey HSD Test
tukey = pairwise_tukeyhsd(combined_data['nbr_change'], combined_data['DN'], alpha=0.05)
print(tukey)
tukey.plot_simultaneous()

# Label axes
plt.xlabel('Mean Difference (with 95% CI)', fontsize=12)  # X-axis: Mean Difference
plt.ylabel('Burn Severity Classes (DN)', fontsize=12)  # Y-axis: Group/Factor levels (DN)
plt.title('Tukey HSD Test for NBR Change by Burn Severity Class', fontsize=14)  # Optional Title

plt.show()

# Recovery Rates

# Define a dictionary to map DN values to class names
class_names = {
    1: 'Unburned',
    2: 'Low Severity',
    3: 'Moderate-Low Severity',
    4: 'Moderate Severity',
    5: 'Moderate-High Severity',
    6: 'High Severity',
    7: 'Very High Severity'
}

combined_data['DN'] = combined_data['DN'].map(class_names)

combined_data['RateOfChange'] = combined_data.groupby('DN')['nbr_change'].diff() / combined_data.groupby('DN')['Year'].diff()

plt.figure(figsize=(10, 6))
sns.lineplot(data=combined_data, x='Year', y='RateOfChange', hue='DN', marker='o')
plt.title('Rates of Vegetation Recovery Over Time by Burn Severity Class')
plt.xlabel('Year')
plt.ylabel('Rate of NBR Change (per year)')
plt.legend(title='Burn Severity Class')
plt.grid(True)
plt.show()


# **Recovery Plot Over the Years**

# Group the data by year and calculate the average NBR change for each year
yearly_recovery = combined_data.groupby('Year')['nbr_change'].mean()

# Plot the recovery over the years
plt.figure(figsize=(10, 6))
plt.plot(yearly_recovery.index, yearly_recovery.values, marker='o', linestyle='-', color='b')
plt.title('Post-Fire Vegetation Recovery Over the Years (Mt. Kenya)', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Average NBR Change', fontsize=12)
plt.grid(True)
plt.xticks(yearly_recovery.index)  # Ensure all years are labeled
plt.show()

# **Correlation Matrix (Heatmap)**
plt.figure(figsize=(12, 8))
correlation_matrix = combined_data[['nbr_change', 'lst', 'dnbr', 'mean_temp', 'max_temp', 'min_temp', 'prec_sum', 'totc', 'aspect', 'slope', 'Elevation']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5, fmt=".2f")
plt.title('Correlation Matrix', fontsize=14)
plt.show()

# **Pairplot or Scatterplot Matrix**
sns.pairplot(combined_data[['nbr_change', 'lst', 'dnbr', 'mean_temp', 'max_temp', 'min_temp', 'prec_sum', 'totc', 'aspect', 'slope', 'Elevation']],
             height=1.3)
plt.suptitle('Pairplot of Variables', y=1.02, fontsize=14)
plt.show()

# **Partial Dependence Plot (PDP) for LST**
plt.figure(figsize=(10, 6))
disp = PartialDependenceDisplay.from_estimator(rf_model, X_train, features=['lst'], grid_resolution=50)
disp.plot()
plt.suptitle('Partial Dependence Plot for LST', fontsize=14)
plt.show()

# Feature importances (Random Forest)
importances = rf_model.feature_importances_
print("Feature importances:", importances)

# Extract feature importance
feature_importances = rf_model.feature_importances_ 

## Create a DataFrame for better visualization
importance_df = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': feature_importances
}).sort_values(by='Importance', ascending=False)


# Plot feature importance
plt.figure(figsize=(10, 6))
plt.barh(importance_df['Feature'], importance_df['Importance'], color='skyblue')
plt.gca().invert_yaxis()  # Highest importance on top
plt.xlabel('Feature Importance')
plt.title('Feature Importance from Random Forest')
plt.show()

# **Residual Plot**
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.7, edgecolor='k')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--')
plt.title('Residual Plot', fontsize=14)
plt.xlabel('Actual Values', fontsize=12)
plt.ylabel('Predicted Values', fontsize=12)
plt.grid()
plt.show()

# **R² Visualization**
plt.figure(figsize=(8, 6))
plt.bar(['R² Score'], [r2], color='teal')
plt.title('Model R² Score', fontsize=14)
plt.ylabel('R² Value', fontsize=12)
plt.ylim(0, 1)  # Assuming R² between 0 and 1
plt.show()

# **Scatter Plots for Each Variable**
feature_columns = ['lst', 'dnbr', 'mean_temp', 'max_temp', 'min_temp', 'prec_sum', 'totc', 'aspect', 'slope', 'Elevation']
for feature in feature_columns:
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=combined_data, x=feature, y='nbr_change', alpha=0.6, edgecolor='k')
    plt.title(f'Scatter Plot: {feature} vs. NBR Change', fontsize=14)
    plt.xlabel(feature, fontsize=12)
    plt.ylabel('NBR Change', fontsize=12)
    plt.grid()
    plt.show()


# Calculate the R^2 value
r2 = r2_score(y_test, y_pred)

# Create the plot
plt.figure(figsize=(8, 6))

# Scatter plot of actual vs predicted values
plt.scatter(y_test, y_pred, alpha=0.7, edgecolor='k', label='Data Points')

# Line of best fit
coeffs = np.polyfit(y_test, y_pred, 1)  # Fit a linear model
line_of_best_fit = np.polyval(coeffs, y_test)
plt.plot(y_test, line_of_best_fit, color='blue', label=f'Best Fit Line (y={coeffs[0]:.2f}x + {coeffs[1]:.2f})')

# Identity line for reference
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--', label='Ideal Fit Line (y=x)')

# Add R^2 value as text annotation


# Add titles and labels
plt.title('Residual Plot', fontsize=14)
plt.xlabel('Actual Values', fontsize=12)
plt.ylabel('Predicted Values', fontsize=12)

# Add a legend
plt.legend(fontsize=10)

# Add grid
plt.grid(alpha=0.5)

# Show the plot
plt.show()
