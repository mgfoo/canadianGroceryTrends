import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from scipy.stats import f_oneway, kruskal


def cal_avg_per_region(input_file):
    """
    Calculates the average value per category per year for all provinces in each region and saves the result to a CSV file.
    """
    province_categories = {
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

    # Load the data
    data = pd.read_csv(input_file)
    data['region'] = data['province'].map(province_categories)


      # Filter for the required categories
    valid_categories = ['fruits', 'veggies', 'meat', 'dairy']
    data = data[data['category'].str.lower().isin(valid_categories)]

    # Group by region, year, and category, then calculate the average
    grouped = data.groupby(['region', 'year', 'category']).agg(
        avg_value=('avg_value', 'mean')
    ).reset_index()

    # Save the aggregated results to a new CSV file
    output_file = 'output/geo_csv/regions/avg_value_reg.csv'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    grouped.to_csv(output_file, index=False)

    print(f"Aggregated data saved to: {output_file}")
    return output_file


def pairwise_region_comparison(input_file):
    """
    Compares average values across regions for each category and year using pairwise differences.
    """
    data = pd.read_csv(input_file)
    results_list = []

    for year in data['year'].unique():
        year_data = data[data['year'] == year]
        for category in year_data['category'].unique():
            category_data = year_data[year_data['category'] == category]

            east = category_data[category_data['region'] == 'East Coast']['avg_value'].values
            west = category_data[category_data['region'] == 'West Coast']['avg_value'].values
            interior = category_data[category_data['region'] == 'Interior']['avg_value'].values

            if len(east) == 1 and len(west) == 1 and len(interior) == 1:
                diff_east_west = abs(east[0] - west[0])
                diff_east_interior = abs(east[0] - interior[0])
                diff_west_interior = abs(west[0] - interior[0])

                results_list.append({
                    'year': year,
                    'category': category,
                    'diff_east_west': diff_east_west,
                    'diff_east_interior': diff_east_interior,
                    'diff_west_interior': diff_west_interior
                })

    results_df = pd.DataFrame(results_list)
    output_file = 'output/geo_csv/pairwise_region_comparison_results.csv'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    results_df.to_csv(output_file, index=False)

    print(f"Pairwise region comparison results saved to: {output_file}")
    return results_df


def extended_region_comparison(input_file):
    """
    Performs pairwise region comparison with Kruskal-Wallis test.
    """
    data = pd.read_csv(input_file)
    results_list = []

    for category in data['category'].unique():
        category_data = data[data['category'] == category]
        east = category_data[category_data['region'] == 'East Coast']['avg_value']
        west = category_data[category_data['region'] == 'West Coast']['avg_value']
        interior = category_data[category_data['region'] == 'Interior']['avg_value']

        if not (east.empty or west.empty or interior.empty):
            kruskal_stat, kruskal_p = kruskal(east, west, interior)
            results_list.append({
                'category': category,
                'kruskal_stat': kruskal_stat,
                'kruskal_p': kruskal_p,
            })

    results_df = pd.DataFrame(results_list)
    output_file = 'output/geo_csv/extended_region_comparison_results.csv'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    results_df.to_csv(output_file, index=False)

    print(f"Extended region comparison results saved to: {output_file}")
    return results_df

def visualize_differences(input_file):
    """
    Generates create line plot & heat map
    """
    output_dir = 'output/geo_png'


    # Load the processed data
    data = pd.read_csv(input_file)

    # Convert year to string for better plotting
    data['year'] = data['year'].astype(str)

    # Line Plot: Trends of values over the years for each region and category
    plt.figure(figsize=(15, 10))
    sns.lineplot(
        data=data,
        x='year',
        y='avg_value',
        hue='region',
        style='category',
        markers=True,
        dashes=False
    )
    plt.title('Trends of Average Values Over Years by Region and Category')
    plt.xlabel('Year')
    plt.ylabel('Average Value')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    line_plot_path = os.path.join(output_dir, 'line_Regions.png')
    plt.savefig(line_plot_path)
    plt.close()
    print(f"Line plot saved to: {line_plot_path}")

    # Heatmap: Differences in average values over time by province and category
    pivot_data = data.pivot_table(
        values='avg_value',
        index=['region', 'category'],
        columns='year',
        aggfunc='mean'
    )
    plt.figure(figsize=(15, 10))
    sns.heatmap(
        pivot_data,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        linewidths=0.5,
        cbar_kws={'label': 'Average Value'}
    )
    plt.title('Heatmap of Average Values by Region and Category Over Years')
    plt.xlabel('Year')
    plt.ylabel('Region and Category')
    plt.tight_layout()
    heatmap_path = os.path.join(output_dir, 'heatmap_differences_regions.png')
    plt.savefig(heatmap_path)
    plt.close()
    print(f"Heatmap saved to: {heatmap_path}")


def main():
    input_file = 'output/geo_csv/avg_year_prov.csv'
    avg_file = cal_avg_per_region(input_file)
    pairwise_results = pairwise_region_comparison(avg_file)
    extended_results = extended_region_comparison(avg_file)
    visualize_differences(avg_file)
    print("Analysis complete.")


if __name__ == "__main__":
    main()
