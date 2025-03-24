import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr

# File paths
CSV_OUTPUT_DIR = "output/geo_csv/population"
ITEM_SUMMARY_FILE = "output/geo_csv/avg_year_prov.csv"
POPULATION_FILE = "data/population.csv"

# Output directory for visualizations
PNG_OUTPUT_DIR = "output/geo_png"
os.makedirs(PNG_OUTPUT_DIR, exist_ok=True)

# List of provinces with data
PROVINCES = [
    "British Columbia", "Alberta", "Manitoba", "Quebec", "Ontario",
    "Saskatchewan", "Prince Edward Island", "Newfoundland and Labrador",
    "New Brunswick", "Nova Scotia"
]

def load_and_preprocess_population(filepath):
    """Load and preprocess the population dataset."""
    # Load population data and select relevant columns
    population = pd.read_csv(filepath, usecols=['REF_DATE', 'GEO', 'VALUE'])
    population.rename(columns={'REF_DATE': 'date', 'GEO': 'province', 'VALUE': 'population'}, inplace=True)

    # Extract the year from the date
    population['year'] = pd.to_datetime(population['date']).dt.year

    # Average population by year and province
    population_avg = population.groupby(['province', 'year'])['population'].mean().reset_index()

    # Filter for relevant provinces
    population_avg['province'] = population_avg['province'].str.strip()
    population_avg = population_avg[population_avg['province'].isin(PROVINCES)]
   
    return population_avg

def load_item_summary(filepath):
    """Load the item summary dataset."""
    item_summary = pd.read_csv(filepath)
    item_summary.rename(columns={'avg_value': 'price'}, inplace=True)
    
    return item_summary

def merge_data(item_summary, population_avg):
    """Merge item prices and population data on year and province."""
    merged = pd.merge(item_summary, population_avg, on=['year', 'province'], how='inner')

    return merged

def analyze_population_vs_category_price(data):
    """Analyze how population compares to the average price of each category."""
    comparison = data.groupby(['province', 'year', 'category']).agg({
        'price': 'mean',
        'population': 'mean'
    }).reset_index()

    # Save the analysis to a CSV file
    output_csv = os.path.join(CSV_OUTPUT_DIR, 'population_cat_analysis.csv')
    comparison.to_csv(output_csv, index=False)
    print(f"Population vs Category Price analysis saved to {output_csv}")

    return comparison

def visualize_population_vs_price(data):
    """Visualize the relationship between population and average category price."""
    plt.figure(figsize=(16, 10))
    sns.scatterplot(data=data, x='population', y='price', hue='category', style='province', palette='viridis')
    plt.title('Population vs Average Price of Categories by Province', fontsize=14)
    plt.xlabel('Average Population', fontsize=12)
    plt.ylabel('Average Price', fontsize=12)
    plt.legend(title='Category & Province', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    plt.tight_layout()

    # Save the visualization
    output_png = os.path.join(PNG_OUTPUT_DIR, 'population_vs_price.png')
    plt.savefig(output_png)
    plt.show()
    print(f"Visualization saved to {output_png}")

def correlation_analysis(data):
    """Perform correlation analysis between population and price."""
    correlation_results = []
    for category in data['category'].unique():
        category_data = data[data['category'] == category]
        correlation, p_value = spearmanr(category_data['population'], category_data['price'])
        correlation_results.append({'Category': category, 'Correlation': correlation, 'P-Value': p_value})

    # Convert to DataFrame
    correlation_df = pd.DataFrame(correlation_results)
    correlation_df.to_csv(os.path.join(CSV_OUTPUT_DIR, 'cor_population_analysis.csv'), index=False)
    print(f"Correlation analysis results saved to {os.path.join(CSV_OUTPUT_DIR, 'cor_population_analysis.csv')}")

    return correlation_df

def main():
    """Main function to execute the population vs price analysis pipeline."""
    # Load and preprocess population data
    print(f"Loading population data from: {POPULATION_FILE}")
    population_avg = load_and_preprocess_population(POPULATION_FILE)

    # Load the item summary data
    print(f"Loading item summary data from: {ITEM_SUMMARY_FILE}")
    item_summary = load_item_summary(ITEM_SUMMARY_FILE)

    # Merge datasets
    merged_data = merge_data(item_summary, population_avg)

    # Analyze population vs category price
    comparison = analyze_population_vs_category_price(merged_data)

    # Perform correlation analysis
    correlation_results = correlation_analysis(comparison)

    # Visualize the results
    visualize_population_vs_price(comparison)

if __name__ == "__main__":
    main()
