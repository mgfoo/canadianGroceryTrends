# Food Prices in Canada: A Temporal and Geographic Examination

### CMPT353 Final Project By Daksh Patel and Michaela Foo
## To read our final analysis and report, please download: Analyzing_Food_Prices_in_Canada__Trends__Regional_Disparities__and_Key_Insights.pdf
---
## Overview

This study aims to understand and identify the causes or factors contributing to the rapid increase in food prices across Canada over the last seven years and to determine if any regions or food items experienced significantly different changes in price compared to the rest of Canada.

The initial focus was to examine how the cost of making a sandwich has changed over the past 10 years. However, due to data availability and the complexity of the issue, the study was expanded to analyze the average price changes of staple food items across Canada and its provinces. This redefined focus allowed for broader questions to be explored, such as identifying periods and regions of irregular growth and investigating factors that may have influenced these trends, including COVID-19 lockdowns, shifts in U.S. economic policies, and changes in demographics such as population growth and changes in average income.

---

## Data

Note: Larger data files are not uploaded to the repo due to size constraints, and were processed locally.

The data was sourced from Statistics Canada, providing monthly average prices for staple food items from January 2017 to August 2024. The dataset covers all Canadian provinces (territories excluded), and national averages were calculated across provinces. 

After removing redundant items (different quantities and varieties), the following categories and provinces were used for this analysis and report:

### **Categories**
1. Baby (food)
2. Beans
3. Canned
4. Condiments
5. Dairy
6. Drinks
7. Frozen
8. Fruits
9. Grains
10. Meat Alternatives
11. Meats
12. Nuts
13. Pantry
14. Seafood
15. Snacks
16. Vegetables

All provinces were available in the data list, including and average across Canada, but territories were not included in the Statistics Canada dataset.

### **Locations**
1. Alberta  
2. British Columbia  
3. Manitoba  
4. New Brunswick  
5. Newfoundland and Labrador  
6. Nova Scotia  
7. Ontario  
8. Prince Edward Island  
9. Quebec  
10. Saskatchewan
11. Canada

---

## Description of important folders

### src/cleaning folder

src/cleaning/data_cleaning.py: This file was used to clean and organize the original data file. A sample CSV was added to replicate how it would run normally, as the original file was too large. Simply running the script will produce all the categorized data, oh which smaller files have been included for reference.

src/cleaning/temporal_analysis.py: This files runs the temporal themed analysis on the organized data files. Due to the much smaller sampled data size, some files may come out empty. Simply running the file will generate a YoY price graph, print some Tukey test results in the terminal (used for testing), and store the results of all the analysis as CSV files.

src/cleaning/verify_cols_csv.py: Running this file will print out the header format of the original raw data, or for this repo, the smaller sample data.

src/cleaning/re_comp_cat.py: This Python script is designed for data processing and analysis of average yearly values of various grocery categories across Canadian provinces. it also processes CSV files containing yearly data for individual grocery categories and calculates the average yearly value for each category in each province.

src/cleaning/reg_comp.py: This processes grocery price data across Canadian provinces, focusing on yearly trends and regional averages for various product categories. the key functions are: Computes yearly average values for each product in each province and calculating the average values for products from 2017 to 2024 per province.

### scr/geo_analysis folder

coast_region_analysis.py: This Python script analyzes grocery data by aggregating average values per category across Canadian regions, performing statistical comparisons, and visualizing trends. It calculates yearly averages by region, conducts pairwise and Kruskal-Wallis tests for differences between regions, and generates line plots and heatmaps for insights into trends and regional variations.

income_analysis.py: This Python script analyzes the relationship between average income and category prices across Canadian provinces by merging income and item price datasets, conducting correlation analysis, and visualizing the findings. It outputs CSV files summarizing income-price trends and correlation results, along with scatterplots highlighting regional and categorical differences.

pop_analysis.py: This Python script examines the relationship between population size and average category prices across Canadian provinces by merging population and price data, conducting correlation analysis, and visualizing the trends. The analysis generates CSV outputs summarizing insights and scatterplots illustrating provincial and categorical variations.

urban_rural.py: This Python script analyzes the differences in food prices between urban and rural provinces in Canada, categorizing regions and performing statistical tests like Mann-Whitney U to identify significant price disparities. It visualizes trends and differences with line graphs and bar charts, while saving results and summaries in CSV format for further insights.

---

## Order of execution for the + files produced

# Geographic/demographic Analysis

Note: This assumes that all required csv files are uploaded/processed (from 'scr/cleaning' and 'data')

### **1. Income vs Category Prices**
#### **Execution Steps**
1. Load and preprocess income data from `data/income.csv`.
2. Load item summary data from `output/geo_csv/avg_year_prov.csv`.
3. Merge income and item data by `year` and `province`.
4. Analyze the relationship between income and category prices, saving results to a CSV file.
5. Perform correlation analysis using Spearman’s rank correlation.
6. Generate a scatterplot showing income vs average prices for each category and province.

#### **Input Files**
- `data/income.csv`: Contains income data with columns `REF_DATE`, `GEO`, and `VALUE`.
- `output/geo_csv/avg_year_prov.csv`: Summary of average prices by year, province, and category.

#### **Output Files**
- **CSV Files**:
  - `output/geo_csv/income/income_cat_analysis.csv`: Analysis of income vs category prices.
  - `output/geo_csv/income/cor_income_analysis.csv`: Correlation results for income vs prices.
- **Visualizations**:
  - `output/geo_png/income_vs_price.png`: Scatterplot of income vs category prices.

---

### **2. Population vs Category Prices**
#### **Execution Steps**
1. Load and preprocess population data from `data/population.csv`.
2. Load item summary data from `output/geo_csv/avg_year_prov.csv`.
3. Merge population and item data by `year` and `province`.
4. Analyze the relationship between population and category prices, saving results to a CSV file.
5. Perform correlation analysis using Spearman’s rank correlation.
6. Generate a scatterplot showing population vs average prices for each category and province.

#### **Input Files**
- `data/population.csv`: Contains population data with columns `REF_DATE`, `GEO`, and `VALUE`.
- `output/geo_csv/avg_year_prov.csv`: Summary of average prices by year, province, and category.

#### **Output Files**
- **CSV Files**:
  - `output/geo_csv/population/population_cat_analysis.csv`: Analysis of population vs category prices.
  - `output/geo_csv/population/cor_population_analysis.csv`: Correlation results for population vs prices.
- **Visualizations**:
  - `output/geo_png/population_vs_price.png`: Scatterplot of population vs category prices.

---

### **3. Urban vs Rural Food Prices**
#### **Execution Steps**
1. Load item summary data from `output/geo_csv/years/food_prices_item.csv`.
2. Classify provinces as `Urban` or `Rural` and calculate regional averages.
3. Perform Mann-Whitney U tests to compare urban and rural prices.
   - Save results for all products and separately for those with negligible differences.
4. Generate visualizations:
   - A bar chart comparing urban vs rural prices.
   - A line plot showing yearly trends in average prices by region and category.

#### **Input Files**
- `output/geo_csv/years/food_prices_item.csv`: Detailed food price data by province and category.

#### **Output Files**
- **CSV Files**:
  - `output/geo_csv/urban_rural/avg_val_urban_rural.csv`: Average values by region and category.
  - `output/geo_csv/urban_rural/mannwhitneyu_results.csv`: Mann-Whitney U test results for urban vs rural prices.
  - `output/geo_csv/urban_rural/mannwhitneyu_results_small.csv`: Results for negligible differences.
  - `output/geo_csv/urban_rural/urban_vs_rural_summary.csv`: Summary of urban vs rural prices.
- **Visualizations**:
  - `output/geo_png/urban_vs_rural_prices.png`: Bar chart comparing urban vs rural prices.
  - `output/geo_png/yearly_trends_by_region_and_category.png`: Line plot showing yearly trends in average prices.

---

## Output Directories
- **CSV Files**: Saved under `output/geo_csv` in specific subfolders (`income`, `population`, `urban_rural`).
- **Visualizations**: Saved under `output/geo_png`.

---

## Notes
- Ensure all input datasets are preprocessed with the required columns and formats. Some categories may be missing due to a smaller sampled dataset.
- Install the required Python packages (ie `pandas`, `seaborn`, `matplotlib`, `scipy`) before running the scripts. The list of required packages can be found in `requirements.txt`

---
# Temporal Analysis

## **Order of Execution**

1. **Year-over-Year (YoY) Price Increase Calculation**
   - The `YoYPriceIncrease` function calculates the YoY price increase for each food category across all CSV files in the `split_data` folder.
   - The `PlotYoYIncrease` function visualizes these YoY increases for each food category over time.

2. **Average Price Increase During COVID Periods**
   - The `AveragePriceIncreasePeriod` function computes the average YoY price increase during pre-COVID, during-COVID, and post-COVID periods.
   - Results are printed to the console.

3. **Tukey Test for COVID Period Comparison**
   - The `TukeyTest` function performs a Tukey post-hoc test to identify significant differences in price increases between the COVID periods.
   - Results are printed to the console.

4. **Month-over-Month (MoM) Price Increase Calculation by COVID Period**
   - The `CalculateMoMIncreaseByPeriod` function calculates MoM price increases for each food item during COVID periods.
   - The `TukeyTestAllProductsCovid` function performs pairwise Tukey tests for each product across the three COVID periods.
   - Results are saved to `tukey_covid.csv` in the project directory using `SaveToCSV`.

5. **MoM Price Increase Calculation by Presidency Period**
   - The `CalculateMOMIncrease` function calculates MoM price increases for each food item during U.S. presidency periods.
   - The `TukeyTestPresidency` function performs pairwise Tukey tests for each product across three presidency periods (Pre-Trump, During-Trump, Post-Trump).
   - Significant results (`reject == True`) are filtered and saved to `tukey_pres.csv` in the project directory using `SaveToCSV`.

---

## **Expected Outputs**

1. **Visualizations:**
   - A line plot showing the Year-over-Year (YoY) price increase percentages for all food categories over time is displayed.

2. **CSV Outputs:**
   - `tukey_covid.csv`: Results of pairwise Tukey tests for Month-over-Month (MoM) price increases during the three COVID periods for all products.
   - `tukey_pres.csv`: Results of pairwise Tukey tests for MoM price increases during the three U.S. presidency periods (only significant results).

3. **Console Outputs:**
   - Average YoY price increase during the COVID periods (`AveragePriceIncreasePeriod`).
   - Summary of the Tukey test results for YoY price increases across COVID periods (`TukeyTest`).

---

## **Key Assumptions**
- Data files are organized in the `split_data` folder (for YoY analysis) and `cleaned_data` folder (for COVID and presidency analyses).
- Each CSV file contains columns `REF_DATE`, `VALUE`, `Products`, and either `COVID_Period` or `Presidency_Period` for grouping.
- The program assumes the input files are pre-cleaned and correctly formatted for processing (which can be founded in `cleaned_data` folder.

---
