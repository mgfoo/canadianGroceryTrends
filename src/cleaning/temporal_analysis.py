import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.multicomp import pairwise_tukeyhsd


#Save dataframe to CSV
def SaveToCSV(df, file_name, folder):
    output_folder = os.path.join('./', folder)
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, file_name)
    df.to_csv(output_path, index=False)


#Add the YoY price increase of each ingredient as a column (all files)
def YoYPriceIncrease(folder_name):
    folder_path = os.path.join(os.getcwd(), folder_name)
    filepaths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]
    category_results = {}

    for filepath in filepaths:
        category_name = os.path.splitext(os.path.basename(filepath))[0] 
        df = pd.read_csv(filepath)
        
        if df.empty:
            continue 
        
        df['REF_DATE'] = pd.to_datetime(df['REF_DATE'])
        df['Year'] = df['REF_DATE'].dt.year
        
        yearly_avg = df.groupby('Year')['VALUE'].mean().reset_index()
        
        if yearly_avg.empty:
            continue  
        
        yearly_avg.rename(columns={'VALUE': 'Average_Price'}, inplace=True)
        
        yearly_avg['YoY_Increase'] = yearly_avg['Average_Price'].pct_change() * 100
        
        if yearly_avg['YoY_Increase'].isnull().all():
            continue
        
        category_results[category_name] = yearly_avg
    
    return category_results



# Plot the average YoY increases of food prices over time across all Provinces.
def PlotYoYIncrease(yoy_results):
                                
    plt.figure(figsize=(12, 8))
    sns.set(style="whitegrid")
    colors = sns.color_palette("tab20", len(yoy_results)) 
    
    for i, (category, data) in enumerate(yoy_results.items()):
        plt.plot(data['Year'], data['YoY_Increase'], label=category, color=colors[i], marker='o', linewidth=2)
    
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('YoY Price Increase (%)', fontsize=14)
    plt.title('Year-over-Year Price Increase by Category', fontsize=16)
    plt.legend(title="Food Categories", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
    plt.show()


#Add the YoY price increase of each ingredient as a column (Single files)
def CalculateYoYIncrease(df):
    df.loc[:, 'REF_DATE'] = pd.to_datetime(df['REF_DATE'])
    df = df.sort_values(by=['Products', 'REF_DATE'])
    df['YoY_Increase'] = df.groupby('Products')['VALUE'].pct_change() * 100
    df = df.dropna(subset=['YoY_Increase'])
    return df


#Calculate the average price increase for Covid period
def AveragePriceIncreasePeriod(df):
    df_with_yoy = CalculateYoYIncrease(df)
    avg_increase = df_with_yoy.groupby('COVID_Period')['YoY_Increase'].mean().reset_index()
    return avg_increase


#Tukey Test for Covid themed comparison.
def TukeyTest(df):
    df_with_yoy = CalculateYoYIncrease(df)
    tukey = pairwise_tukeyhsd(endog=df_with_yoy['YoY_Increase'], 
                              groups=df_with_yoy['COVID_Period'], 
                              alpha=0.05)
    
    tukey_results = pd.DataFrame(data=tukey.summary().data[1:], columns=tukey.summary().data[0])
    return tukey_results


#Add MoM price increase for each food item.
def CalculateMoMIncreaseByPeriod(df):
    df['REF_DATE'] = pd.to_datetime(df['REF_DATE'])
    df = df.sort_values(by=['Products', 'REF_DATE'])
    df['MoM_Increase'] = df.groupby('Products')['VALUE'].pct_change() * 100
    df = df.dropna(subset=['MoM_Increase'])
    return df


#Conduct pairwise t-tests for each product across all 3 covid periods
def TukeyTestPerProductCovid(df, product):
    product_df = df[df['Products'] == product]
    if product_df['COVID_Period'].nunique() != 3:
        return None
    tukey = pairwise_tukeyhsd(
        endog=product_df['MoM_Increase'],
        groups=product_df['COVID_Period'],
        alpha=0.05
    )
    tukey_results = pd.DataFrame(data=tukey.summary(), columns=['group1', 'group2', 'meandiff', 'p-adj', 'lower', 'upper', 'reject'])
    return tukey_results


#Conduct a pairwise t-test for each grouping of ingredients.
def TukeyTestAllProductsCovid(df):
    products = df['Products'].unique()
    all_results = []
    
    for product in products:
        tukey_results = TukeyTestPerProductCovid(df, product)
        
        if tukey_results is not None:
            tukey_results['Product'] = product
            all_results.append(tukey_results)
   
    if all_results:
        final_results = pd.concat(all_results, ignore_index=True)
        return final_results
    else:
        return pd.DataFrame()


#Calculate the MoM price increase per ingredient.
def CalculateMOMIncrease(df):
    df = df.sort_values(by=['Products', 'REF_DATE'])
    df['MoM_Increase'] = df.groupby('Products')['VALUE'].pct_change() * 100
    return df.dropna(subset=['MoM_Increase'])


#Conduct a pairwise t-test for each ingredient across three presidential periods.
def TukeyTestPresidency(df):
    products = df['Products'].unique()
    results = []
    
    for product in products:
        product_df = df[df['Products'] == product]
        
        if product_df['Presidency_Period'].nunique() != 3:
            continue
        
        tukey = pairwise_tukeyhsd(
            endog=product_df['MoM_Increase'],
            groups=product_df['Presidency_Period'],
            alpha=0.05
        )

        tukey_results = pd.DataFrame(data=tukey.summary().data[1:], columns=tukey.summary().data[0])
        tukey_results['Product'] = product
        results.append(tukey_results)
    
    return pd.concat(results, ignore_index=True) if results else pd.DataFrame()


yoy = YoYPriceIncrease("split_data")
PlotYoYIncrease(yoy)

file_path = os.path.join("cleaned_data", "covid_period_food.csv")
df = pd.read_csv(file_path)

avg_increase = AveragePriceIncreasePeriod(df)
print(avg_increase)

tukey_results = TukeyTest(df)
print(tukey_results)

df_mom = CalculateMoMIncreaseByPeriod(df)
final_results = TukeyTestAllProductsCovid(df_mom)
SaveToCSV(final_results, "tukey_covid.csv", "")

file_path = os.path.join("cleaned_data", "presidency.csv")
df = pd.read_csv(file_path)

df_mom = CalculateMOMIncrease(df)
tukey_results = TukeyTestPresidency(df_mom)

SaveToCSV(tukey_results, "tukey_pres.csv", "")
