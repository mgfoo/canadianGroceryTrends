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


def calculate_avg_per_year_per_province(filepaths, output_file):
    """
    Calculates the average value per year for each province per category and saves the result to a CSV file.
    """
    # Initialize an empty list to store results
    all_results = []

    for filepath in filepaths:
        # Extract category name from the file path
        category = os.path.basename(filepath).replace('_item.csv', '')

        # Load the data
        data = pd.read_csv(filepath)

        # Group by year and province and calculate the average
        grouped = data.groupby(['year', 'province']).agg(avg_value=('avg_total_yearly', 'mean')).reset_index()

        # Add category information
        grouped['category'] = category

        # Append the result to the list
        all_results.append(grouped)

    # Concatenate all results into a single DataFrame
    final_df = pd.concat(all_results, ignore_index=True)

    # Save the final DataFrame to a CSV file
    final_df.to_csv(output_file, index=False)

    print(f"Resulting CSV file has been saved to: {output_file}")

def main():

    filepaths = [
    'output/geo_csv/years/baby_item.csv',
    'output/geo_csv/years/beans_item.csv',
    'output/geo_csv/years/canned_item.csv',
    'output/geo_csv/years/condiments_item.csv',
    'output/geo_csv/years/dairy_item.csv',
    'output/geo_csv/years/drinks_item.csv',
    'output/geo_csv/years/frozen_item.csv',
    'output/geo_csv/years/fruits_item.csv',
    'output/geo_csv/years/grains_item.csv',
    'output/geo_csv/years/meat_alts_item.csv',
    'output/geo_csv/years/meats_item.csv',
    'output/geo_csv/years/nuts_item.csv',
    'output/geo_csv/years/pantry_item.csv',
    'output/geo_csv/years/seafood_item.csv',
    'output/geo_csv/years/snacks_item.csv',
    'output/geo_csv/years/veggies_item.csv',
    ]
     # Specify the output file path
    output_file = 'output/geo_csv/avg_year_prov.csv'
    calculate_avg_per_year_per_province(filepaths, output_file)


if __name__ == "__main__":
    main()
