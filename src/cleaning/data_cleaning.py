

import pandas as pd
import os

# Saves dataframe as a CSV, and creates a folder if not already made
def SaveToCSV(df, file_name, folder):
    output_folder = os.path.join('./', folder)
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, file_name)
    df.to_csv(output_path, index=False)


# Generates DF and CSV for yearly average prices by location and product
def YearlyAvgFood(df):
    avg_df = df.copy() 
    avg_df['Year'] = avg_df['REF_DATE'].dt.year
    avg_df = avg_df.groupby(['Year', 'GEO', 'Products'])['VALUE'].mean().reset_index()
    avg_df = avg_df.rename(columns={'VALUE': 'Average_Price'})
    avg_df = avg_df.sort_values(by=['GEO', 'Year'], ascending=True).reset_index(drop=True)
    SaveToCSV(avg_df, "yearly_avg_prices.csv", "cleaned_data")
    return avg_df


# Generates DF and CSV for quarterly average prices by location and product
def QuarterlyAvgFood(df):
    quarter_df = df.copy()
    quarter_df['Year'] = quarter_df['REF_DATE'].dt.year
    quarter_df['Quarter'] = quarter_df['REF_DATE'].dt.quarter
    avg_df = quarter_df.groupby(['Year', 'Quarter', 'GEO', 'Products'])['VALUE'].mean().reset_index()
    avg_df = avg_df.rename(columns={'VALUE': 'Average_Price'})
    avg_df = avg_df.sort_values(by=['GEO', 'Year'], ascending=True).reset_index(drop=True)
    SaveToCSV(avg_df, "quarterly_avg_prices.csv", "cleaned_data")
    return avg_df


# Generates DF and CSV adding a column to specify pre / during / post covid decided by CIHI Timeline
def CovidPeriod(df, name):
    cov_df = df.copy()
    lockdown_start = pd.to_datetime('2020-01-01')
    lockdown_end = pd.to_datetime('2022-05-30')

    def get_period(date):
        if date < lockdown_start:
            return 'Pre-COVID'
        elif lockdown_start <= date <= lockdown_end:
            return 'During-COVID'
        else:
            return 'Post-COVID'

    cov_df['COVID_Period'] = cov_df['REF_DATE'].apply(get_period)
    cov_df = cov_df.sort_values(by=['GEO','REF_DATE',], ascending=True).reset_index(drop=True)
    SaveToCSV(cov_df, name, "cleaned_data")
    return cov_df


# Assign Coast / Region to each province location
def Coasts(df, name):
    coast_df = df[df['GEO'] != 'Canada'].copy()

    coast_mapping = {
        'British Columbia': 'West Coast',
        'Alberta': 'Interior',
        'Saskatchewan': 'Interior',
        'Manitoba': 'Interior',
        'Ontario': 'Interior',
        'Quebec': 'Interior',
        'Newfoundland and Labrador': 'East Coast',
        'Nova Scotia': 'East Coast',
        'New Brunswick': 'East Coast',
        'Prince Edward Island': 'East Coast',
    }

    coast_df['Coast'] = coast_df['GEO'].map(coast_mapping).fillna('Unknown')
    coast_df = coast_df.sort_values(by=['Coast','GEO', 'REF_DATE'], ascending=False).reset_index(drop=True)
    SaveToCSV(coast_df, name, "cleaned_data")
    return coast_df


# Gets current item prices as of August 2024
def CurrentPrices(df):
    current_df = df[df['REF_DATE'] == '2024-08'].copy()
    SaveToCSV(current_df, "current_prices.csv", "cleaned_data")
    return current_df


# Splits item list by quarter
def QuarterSplit(df, name):
    pop_df = df.copy()
    pop_df['REF_DATE'] = pd.to_datetime(pop_df['REF_DATE'])

    pop_df['Year'] = pop_df['REF_DATE'].dt.year
    pop_df['Quarter'] = pop_df['REF_DATE'].dt.quarter
    
    pop_df = pop_df.drop(columns=['REF_DATE'])

    pop_df = pop_df.sort_values(by=['GEO', 'Year'], ascending=True).reset_index(drop=True)
    SaveToCSV(pop_df, name, "cleaned_data")
    
    return pop_df


# Generates DF and CSV for quarterly average prices by location and product
def QuarterlyAvgIncome(df):
    quarter_df = df.copy()
    quarter_df['Year'] = quarter_df['REF_DATE'].dt.year
    quarter_df['Quarter'] = quarter_df['REF_DATE'].dt.quarter
    avg_df = quarter_df.groupby(['Year', 'Quarter', 'GEO'])['VALUE'].mean().reset_index()
    avg_df = avg_df.rename(columns={'VALUE': 'Average_Weekly_Income'})
    avg_df = avg_df.sort_values(by=['GEO', 'Year'], ascending=True).reset_index(drop=True)
    SaveToCSV(avg_df, "quarterly_avg_income.csv", "cleaned_data")
    return avg_df


# Function for creating custom item list CSV
def FilterIngredients(df, items):
    filtered_df = df[df['Products'].isin(items)]
    SaveToCSV(filtered_df, "filtered_items.csv", "cleaned_data")
    return filtered_df


# Splits ingredient list into groups CSVs after filtering
def SplitProducts(df):
    categories = {
        "meats": [
            "Ground beef, per kilogram",
            "Pork loin cuts, per kilogram",
            "Chicken breasts, per kilogram",
            "Bacon, 500 grams",
            "Wieners, 400 grams"
        ],
        "seafood": [
            "Salmon, per kilogram",
            "Shrimp, 300 grams",
        ],
        "meat_alts": [
            "Meatless burgers, 226 grams",
            "Tofu, 350 grams ",
            "Eggs, 1 dozen"
        ],
        "dairy": [
            "Milk, 4 litres",
            "Cream, 1 litre",
            "Butter, 454 grams",
            "Margarine, 907 grams",
            "Block cheese, 500 grams",
            "Yogurt, 500 grams"
        ],
        "fruits": [
            "Apples, per kilogram",
            "Oranges, per kilogram",
            "Bananas, per kilogram",
            "Pears, per kilogram",
            "Lemons, unit",
            "Limes, unit",
            "Grapes, per kilogram",
            "Cantaloupe, unit",
            "Avocado, unit"
        ],
        "veggies": [
            "Potatoes, per kilogram",
            "Tomatoes, per kilogram",
            "Cabbage, per kilogram",
            "Onions, per kilogram",
            "Celery, unit",
            "Cucumber, unit",
            "Iceberg lettuce, unit",
            "Broccoli, unit",
            "Peppers, per kilogram",
            "Squash, per kilogram",
        ],
        "grains": [
            "White bread, 675 grams",
            "Flatbread and pita, 500 grams ",
            "Dry or fresh pasta, 500 grams",
            "Cereal, 400 grams",
        ],
        "drinks": [
            "Apple juice, 2 litres",
            "Orange juice, 2 litres",
            "Roasted or ground coffee, 340 grams",
            "Tea (20 bags)"
        ],
        "condiments": [
            "Ketchup, 1 litre",
            "Vegetable oil, 3 litres",
            "Mayonnaise, 890 millilitres ",
            "Salsa, 418 millilitres",
            "Pasta sauce, 650 millilitres",
            "Salad dressing, 475 millilitres"
        ],
        "canned": [
            "Canned soup, 284 millilitres",
            "Canned beans and lentils, 540 millilitres",
        ],
        "nuts": [
            "Almonds, 200 grams",
            "Peanuts, 450 grams",
        ],
        "baby": [
            "Baby food, 128 millilitres",
            "Infant formula, 900 grams "
        ],
        "pantry": [
            "White sugar, 2 kilograms",
            "Wheat flour, 2.5 kilograms",
            "Brown rice, 900 grams ",
            "White rice, 2 kilograms"
        ]
    }

    for category, items in categories.items():
        category_df = df[df['Products'].isin(items)]
        SaveToCSV(category_df, f"{category}.csv", "split_data")

    all_items = [item for sublist in categories.values() for item in sublist]
    filtered_df = df[df['Products'].isin(all_items)]
    return filtered_df
    

# Filter dataset for US presidency terms, around Donald Trumps first term.
def AddPresidency(df):
    df['REF_DATE'] = pd.to_datetime(df['REF_DATE'])
    df['Presidency_Period'] = pd.cut(
        df['REF_DATE'],
        bins=[
            pd.Timestamp("2015-12-31"),
            pd.Timestamp("2017-01-20"),  
            pd.Timestamp("2021-01-20"),  
            pd.Timestamp("2024-12-31")  
        ],
        labels=["Pre-Trump", "During-Trump", "Post-Trump"]
    )
    
    return df

raw_food_data = pd.read_csv('food_prices_sample.csv')
raw_food_data = raw_food_data[['REF_DATE', 'GEO', 'Products', 'VALUE']]
raw_food_data['REF_DATE'] = pd.to_datetime(raw_food_data['REF_DATE'])

unique_foods = raw_food_data[['Products']].drop_duplicates().reset_index(drop=True)
SaveToCSV(unique_foods, "all_food_list.csv", "")

raw_food_data = SplitProducts(raw_food_data)

yearly_avg = YearlyAvgFood(raw_food_data)
quarter_avg = QuarterlyAvgFood(raw_food_data)
covid_columns = CovidPeriod(raw_food_data, "covid_period_food.csv")
coasts = Coasts(raw_food_data, "coasts.csv")
current_prices = CurrentPrices(raw_food_data)

raw_population_data = pd.read_csv('population.csv')
raw_population_data = raw_population_data[['REF_DATE', 'GEO', 'VALUE']]
raw_population_data['REF_DATE'] = pd.to_datetime(raw_population_data['REF_DATE'])

quarter_population = QuarterSplit(raw_population_data, "quarter_population.csv")

raw_income_data = pd.read_csv('income.csv')
raw_income_data = raw_income_data[['REF_DATE', 'GEO', 'VALUE']]
raw_income_data['REF_DATE'] = pd.to_datetime(raw_income_data['REF_DATE'])

quarter_income = QuarterlyAvgIncome(raw_income_data)

quarter_prices_and_income = pd.merge(quarter_avg, quarter_income, on=["Year", "Quarter", "GEO"], how="inner")
SaveToCSV(quarter_prices_and_income, "quarter_prices_and_income.csv", "cleaned_data")

quarter_prices_and_population = pd.merge(quarter_avg, quarter_population, on=["Year", "Quarter", "GEO"], how="inner")
SaveToCSV(quarter_prices_and_population, "quarter_prices_and_population.csv", "cleaned_data")

presidency = AddPresidency(raw_food_data)
SaveToCSV(presidency, "presidency.csv", "cleaned_data")

