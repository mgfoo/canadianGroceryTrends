import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# List of provinces with data
PROVINCES = [
    "British Columbia", "Alberta", "Manitoba", "Quebec", "Ontario",
    "Saskatchewan", "Prince Edward Island", "Newfoundland and Labrador",
    "New Brunswick", "Nova Scotia"
]

CATEGORIES = [
    "baby",
    "beans",
    "canned",
    "condiments",
    "dairy",
    "drinks",
    "frozen",
    "fruits",
    "grains",
    "meat_alts",
    "meats",
    "nuts",
    "pantry",
    "seafood",
    "snacks",
    "veggies",
]

# Create directories for organized output
CSV_OUTPUT_DIR = "output/geo_csv/years"
AVG_OUTPUT_DIR = "output/geo_csv/avg"
PNG_OUTPUT_DIR = "output/geo_png/years"

os.makedirs(CSV_OUTPUT_DIR, exist_ok=True)
os.makedirs(PNG_OUTPUT_DIR, exist_ok=True)
os.makedirs(AVG_OUTPUT_DIR, exist_ok=True)

def load_and_filter_data(filepath, usecols, provinces):
    """Load the dataset and filter by the given provinces."""
    # Load only the necessary columns
    data = pd.read_csv(filepath, usecols=usecols, low_memory=True)

    # Filter by the specified provinces
    data = data[data['GEO'].isin(provinces)].copy()

    # Rename columns
    data.rename(columns={'GEO': 'province', 'REF_DATE': 'date', 'VALUE': 'value'}, inplace=True)
    
    # Convert date to datetime and extract year
    data['date'] = pd.to_datetime(data['date'], errors='coerce')
    data['year'] = data['date'].dt.year
    
    return data

def compute_item_statistics(data):
    """mean val product listed yearly"""
    item_summary = data.groupby(['Products', 'province', 'year'])['value'].mean().reset_index()
    item_summary.rename(columns={'value': 'avg_total_yearly'}, inplace=True)
    return item_summary

def compute_average_2017_2024_per_province(data):
    """Mean value of product 2017 to 2024"""
    avg_2017_2024_per_province = ( data.groupby(['Products', 'province'])['value'].mean().reset_index() )
    avg_2017_2024_per_province.rename(columns={'value': 'avg_total'}, inplace=True)
    return avg_2017_2024_per_province

def process_files(filepaths, columns_to_load, provinces, csv_output_dir, avg_output_dir):

    for data_filepath in filepaths:
        print(f"Processing file: {data_filepath}")

        # Load and filter the data
        data = load_and_filter_data(data_filepath, columns_to_load, provinces)

        # Compute statistics for each item
        item_summary = compute_item_statistics(data)

        # Compute average value of each item from 2017 to 2024 per province
        avg_2017_2024_per_province = compute_average_2017_2024_per_province(data)

        # Save summaries to CSV files
        base_name = os.path.basename(data_filepath).replace('.csv', '')  # Get base filename without .csv

        item_summary_filepath = os.path.join(csv_output_dir, f'{base_name}_item.csv')
        avg_province_filepath = os.path.join(avg_output_dir, f'{base_name}_avg_prov.csv')

        item_summary.to_csv(item_summary_filepath, index=False)
        avg_2017_2024_per_province.to_csv(avg_province_filepath, index=False)

        print(f"File '{data_filepath}' processing complete.")

    print(f"Analysis complete for all files. Results saved to '{csv_output_dir}' and '{avg_output_dir}'.")

def main():

    # List of filepaths to the datasets
    filepaths = [
        'split_data/baby.csv',
        'split_data/beans.csv',
        'split_data/canned.csv',
        'split_data/condiments.csv',
        'split_data/dairy.csv',
        'split_data/drinks.csv',
        'split_data/frozen.csv',
        'split_data/fruits.csv',
        'split_data/grains.csv',
        'split_data/meat_alts.csv',
        'split_data/meats.csv',
        'split_data/nuts.csv',
        'split_data/pantry.csv',
        'split_data/seafood.csv',
        'split_data/snacks.csv',
        'split_data/veggies.csv',
    ]

    # Columns to load from the dataset
    columns_to_load = ['GEO', 'REF_DATE', 'VALUE', 'Products']
    process_files(filepaths, columns_to_load, PROVINCES, CSV_OUTPUT_DIR, AVG_OUTPUT_DIR)



if __name__ == "__main__":
    main()