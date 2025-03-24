import pandas as pd

#to print out cols names for csv files

# Paths to your datasets
food_prices_path = 'data/food_prices.csv'
income_path = 'data/income.csv'
population_path = 'data/population.csv'

# Load and print column names
food_prices = pd.read_csv(food_prices_path)
income = pd.read_csv(income_path)
population = pd.read_csv(population_path)

print("Food Prices Columns:", food_prices.columns)
print("Income Columns:", income.columns)
print("Population Columns:", population.columns)
