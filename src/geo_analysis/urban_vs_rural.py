import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, mannwhitneyu

# Group provinces into urban and rural
URBAN_PROVINCES = ["Ontario", "Quebec", "Alberta", "British Columbia", "New Brunswick", "Nova Scotia"]
RURAL_PROVINCES = [
     "Manitoba", "Saskatchewan", "Prince Edward Island",
    "Newfoundland and Labrador"
]

# Paths to CSV output files
CSV_OUTPUT_DIR = "output/geo_csv/urban_rural"
ITEM_SUMMARY_FILE = "output/geo_csv/years/food_prices_item.csv"

# Output directory for visualizations
PNG_OUTPUT_DIR = "output/geo_png"
os.makedirs(PNG_OUTPUT_DIR, exist_ok=True)

def load_data(filepath):
    """Load the item summary CSV file."""
    data = pd.read_csv(filepath)
    return data

def cal_avg_per_region(data):
    """
    Calculates the average value per category per year for all provinces in each region
    and saves the result to a CSV file.
    """
    province_categories = {
        'Ontario': 'Urban',
        'Quebec': 'Urban',
        'Alberta': 'Urban',
        'British Columbia': 'Urban',
        'New Brunswick': 'Urban',
        'Nova Scotia': 'Urban',
        'Manitoba': 'Rural',
        'Saskatchewan': 'Rural',
        'Prince Edward Island': 'Rural',
        'Newfoundland and Labrador': 'Rural',
    }

    # Map provinces to regions

    data = pd.read_csv(data)

    data['region'] = data['province'].map(province_categories)
    
      # Filter 
    valid_categories = ['fruits', 'veggies', 'meat', 'dairy']
    data = data[data['category'].str.lower().isin(valid_categories)]

    # Group by region, year, and category, then calculate the average
    grouped = data.groupby(['region', 'year', 'category']).agg(
        avg_value=('avg_value', 'mean')
    ).reset_index()

    # Save the aggregated results to a new CSV file
    output_file = os.path.join(CSV_OUTPUT_DIR, "avg_val_urban_rural.csv")
    grouped.to_csv(output_file, index=False)

    print(f"Aggregated data saved to: {output_file}")
    return grouped


def add_urban_rural_column(data):
    """Add a column categorizing provinces as urban or rural."""
    data['region_type'] = data['province'].apply(
        lambda x: 'Urban' if x in URBAN_PROVINCES else 'Rural'
    )
    return data

def compute_average_by_region(data):
    """Compute average prices by region type (urban vs rural)."""
    region_summary = data.groupby(['Products', 'region_type'])['avg_total_yearly'].mean().reset_index()
    region_summary.rename(columns={'avg_total_yearly': 'region_avg'}, inplace=True)

    return region_summary

def perform_mannwhitneyu_test(region_summary):
    """Perform Mann-Whitney U Test to compare urban and rural prices."""
    results = []

    # Pivot data to separate urban and rural columns for each product
    pivoted_summary = region_summary.pivot(index='Products', columns='region_type', values='region_avg')

    # Loop through each product
    for product in pivoted_summary.index:
        urban_price = pivoted_summary.loc[product, 'Urban']
        rural_price = pivoted_summary.loc[product, 'Rural']

        # Check if either value is missing
        if pd.isna(urban_price) or pd.isna(rural_price):
            results.append({'Product': product, 'U-Statistic': None, 'P-Value': None, 'Notes': 'Missing data'})
            continue

        # Check for very small differences
        if abs(urban_price - rural_price) < 1e-6:  # Threshold for negligible difference
            results.append({
                'Product': product,
                'U-Statistic': None,
                'P-Value': None,
                'Notes': 'Very small mean difference (treated as negligible)'
            })
            continue

        try:
            # Perform Mann-Whitney U Test
            stat, p_value = mannwhitneyu([urban_price], [rural_price], alternative='two-sided')
            results.append({'Product': product, 'U-Statistic': stat, 'P-Value': p_value})
        except Exception as inner_e:
            results.append({'Product': product, 'U-Statistic': None, 'P-Value': None, 'Notes': f'Error: {str(inner_e)}'})

    # Convert results to DataFrame
    mannwhitneyu_results = pd.DataFrame(results)
    mannwhitneyu_results.to_csv(os.path.join(CSV_OUTPUT_DIR, "mannwhitneyu_results.csv"), index=False)
    print(f"Mann-Whitney U Test results saved to: {os.path.join(CSV_OUTPUT_DIR, 'mannwhitneyu_results.csv')}")

    return mannwhitneyu_results

def perform_mannwhitneyu_test_small(region_summary):
    """Perform Mann-Whitney U Test to compare urban and rural prices, and calculate trends."""
    results = []

    # Pivot data to separate urban and rural columns for each product
    pivoted_summary = region_summary.pivot(index='Products', columns='region_type', values='region_avg')

    # Loop through each product
    for product in pivoted_summary.index:
        urban_price = pivoted_summary.loc[product, 'Urban']
        rural_price = pivoted_summary.loc[product, 'Rural']

        # Check if either value is missing
        if pd.isna(urban_price) or pd.isna(rural_price):
            results.append({'Product': product, 'U-Statistic': None, 'P-Value': None, 
                            'Effect Size': None, 'Urban-Rural Diff': None, 'Notes': 'Missing data'})
            continue

        # Calculate absolute and percentage difference
        diff = urban_price - rural_price
        percent_diff = (diff / rural_price) * 100 if rural_price != 0 else None

        try:
            # Perform Mann-Whitney U Test
            stat, p_value = mannwhitneyu([urban_price], [rural_price], alternative='two-sided')

            # Calculate effect size (absolute difference normalized by mean of both groups)
            mean_price = (urban_price + rural_price) / 2
            effect_size = diff / mean_price if mean_price != 0 else None

            results.append({
                'Product': product,
                'U-Statistic': stat,
                'P-Value': p_value,
                'Effect Size': effect_size,
                'Urban-Rural Diff': diff,
                'Percent Diff (%)': percent_diff,
            })
        except Exception as inner_e:
            results.append({'Product': product, 'U-Statistic': None, 'P-Value': None, 
                            'Effect Size': None, 'Urban-Rural Diff': None, 'Notes': f'Error: {str(inner_e)}'})

    # Convert results to DataFrame
    mannwhitneyu_results = pd.DataFrame(results)
    mannwhitneyu_results.sort_values(by='Urban-Rural Diff', ascending=False, inplace=True)  # Sort by difference
    mannwhitneyu_results.to_csv(os.path.join(CSV_OUTPUT_DIR, "mannwhitneyu_results_small.csv"), index=False)
    print(f"Mann-Whitney U Test results saved to: {os.path.join(CSV_OUTPUT_DIR, 'mannwhitneyu_results_small.csv')}")

    return mannwhitneyu_results

def visualize_yearly_trends_by_region(data):
    """
    Create a line graph showing yearly trends in average values for each category by region (urban vs rural).
    """
    # Check for required columns
    required_columns = {'year', 'region', 'category', 'avg_value'}
    if not required_columns.issubset(data.columns):
        raise ValueError(f"Data is missing required columns: {required_columns - set(data.columns)}")

    plt.figure(figsize=(16, 10))
    sns.lineplot(
        data=data,
        x='year',  # Year as the x-axis
        y='avg_value',  # Average value as the y-axis
        hue='region',  # Differentiates urban and rural regions
        style='category',  # Differentiates categories (products)
        markers=True
    )
    plt.title('Yearly Trends in Average Values by Region and Category', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Average Value ($)', fontsize=14)
    plt.legend(title='Region and Category', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to a file
    output_path = os.path.join(PNG_OUTPUT_DIR, "yearly_trends_by_region_and_category.png")
    plt.savefig(output_path)
    plt.show()


def visualize_urban_rural_differences(region_summary):
    """Create bar chart comparing urban vs rural prices for each product."""
    plt.figure(figsize=(16, 10))  # Increased figure size for better readability
    sns.barplot(data=region_summary, x='Products', y='region_avg', hue='region_type', palette='viridis')
    plt.title('Urban vs Rural Average Prices by Product', fontsize=14)
    plt.xlabel('Product', fontsize=12)
    plt.ylabel('Average Price', fontsize=12)
    plt.xticks(rotation=90, fontsize=10, ha='center')  # Rotate and align labels cleanly
    plt.legend(title='Region Type', loc='upper right', fontsize=10)
    plt.tight_layout()  # Adjust layout to prevent clipping
    plt.savefig(os.path.join(PNG_OUTPUT_DIR, "urban_vs_rural_prices.png"))
    plt.show()


def main():
    """Main function to load data, analyze, and visualize."""
    # Load the item summary data
    print(f"Loading data from: {ITEM_SUMMARY_FILE}")
    data = load_data(ITEM_SUMMARY_FILE)

    line_graph = 'output/geo_csv/avg_year_prov.csv'

    line_graph = cal_avg_per_region(line_graph)

    # Add urban vs rural classification
    data = add_urban_rural_column(data)


    # Compute average prices by region type
    region_summary = compute_average_by_region(data)

    perform_mannwhitneyu_test(region_summary)
    #preform small as vals are very close (thresholds)
    perform_mannwhitneyu_test_small(region_summary)

    # Visualize the differences
    visualize_urban_rural_differences(region_summary)

    # Visualize yearly trends
    visualize_yearly_trends_by_region(line_graph)


    # Save the summary to a CSV file
    region_summary.to_csv(os.path.join(CSV_OUTPUT_DIR, "urban_vs_rural_summary.csv"), index=False)
    print(f"Urban vs Rural summary saved to: {os.path.join(CSV_OUTPUT_DIR, 'urban_vs_rural_summary.csv')}")

if __name__ == "__main__":
    main()
