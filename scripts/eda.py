import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s- %(levelname)s-%(message)s')
class eda:
    def sales_per_day(self,df):
        logging.info('calculating sales per day....')
        sales=df.groupby('DayOfWeek').agg({
            'Sales':'sum',
            
        }).reset_index()
        plt.figure(figsize=(10, 6))
        plt.plot(sales['DayOfWeek'], sales['Sales'], marker='o', linestyle='-', color='b')
        plt.title('Sales by Day of the Week')
        plt.xlabel('Day of the Week')
        plt.ylabel('Sales')
        plt.xticks(ticks=[5, 6, 7], labels=['Friday', 'Saturday', 'Sunday'])  # Adjust labels if needed
        plt.grid(True)
        plt.show()
        return sales


    def holiday(self,df):
        logging.info('calculating holidays....')
        df['Date'] = pd.to_datetime(df['Date'])

        # Sort DataFrame by date and store for proper comparison
        df = df.sort_values(['Store', 'Date']).reset_index(drop=True)

        # Initialize a new column for categorization
        df['Category'] = 'Not Categorized'

        # Identify holiday dates
        holiday_dates = df[df['StateHoliday'].isin(['a', 'b', 'c'])]['Date'].tolist()

        # Iterate through each row to assign categories
        for i in range(len(df)):
            current_date = df.loc[i, 'Date']

            if current_date in holiday_dates:
                # Mark as a Holiday
                df.loc[i, 'Category'] = 'Holiday'
            else:
                # Check if it is 1 day before a holiday (and not itself a holiday)
                if (current_date + pd.Timedelta(days=1)) in holiday_dates:
                    df.loc[i, 'Category'] = 'Before Holiday'
                
                # Check if it is 1 day after a holiday (and not itself a holiday)
                if (current_date - pd.Timedelta(days=1)) in holiday_dates:
                    df.loc[i, 'Category'] = 'After Holiday'

        # Aggregate sales by category
        sales_summary = df.groupby('Category')['Sales'].sum()
        print("\nSales Summary:")
        print(sales_summary)
   

    def seasonal(self,df):
        logging.info('calculating which season has the most sales....')
        df_fil= df[df['StateHoliday'].isin(['a','b','c'])]
        
        add=df_fil.groupby('StateHoliday')['Sales'].sum().reset_index()
        plt.figure(figsize=(8, 5))
        sns.barplot(data=add, x='StateHoliday', y='Sales', palette='coolwarm')
        plt.title('Total Sales by State Holiday')
        plt.xlabel('State Holiday')
        plt.ylabel('Total Sales')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.show()
        return add
    
    def corr(self,df):
        logging.info('calculating correlation between sales and customers....')
        correlation=df['Sales'].corr(df['Customers'])
        print(correlation)
        # Create a scatter plot with a regression line
        plt.figure(figsize=(10, 6))
        sns.regplot(x='Customers', y='Sales', data=df, scatter_kws={'alpha': 0.6}, line_kws={'color': 'red'})
        plt.title('Sales vs. Customers')
        plt.xlabel('Number of Customers')
        plt.ylabel('Sales')
    
    def promo_sales(self,df):
        logging.info('Checking if promotion has an effect on sales....')
        open_stores = df[df['Open'] == 1]

        # Step 2: Group by Store and Promo, then calculate average Sales
        promo_sales = open_stores.groupby(['Store', 'Promo'])[['Sales','Customers']].mean().reset_index()
        summary= promo_sales.groupby('Promo').agg({
            'Sales':'sum',
            'Customers':'sum'
        }).reset_index()
        plt.figure(figsize=(6, 4))
        sns.barplot(data=summary, x='Promo', y='Sales', color='b', label='Sales', alpha=0.6)
        sns.barplot(data=summary, x='Promo', y='Customers', color='r', label='Customers', alpha=0.6)
        plt.title('Sales with and without Promotion')
        plt.xlabel('Promos')
        plt.ylabel('Sales')
        plt.show()
        # Step 3: Display the results
        return summary
   
    def open_weekends(self,df):
        logging.info('Which stores are open eveyday....')
        op=df[(df['DayOfWeek']==7) & (df['Open']==1)]
        stores=op['Store'].unique()
        n= df.groupby('Store')['Sales'].sum().reset_index()
        n['Check'] = n['Store'].apply(lambda x: 'Open Every Week' if x in stores else 'Closed on sunday')
        
        value=n.sort_values(by='Sales',ascending=False)
        return value
    

    def assortment_sales(self,df,stores):
        logging.info('Which assortment has the highest sales....')
        df_edited= df.groupby('Store')['Sales'].sum().reset_index()
        assoret= stores[['Store','Assortment']]
        merged_df=pd.merge(df_edited,assoret, on='Store', how='inner')
        ass=merged_df.groupby('Assortment')['Sales'].mean().reset_index()
        print(ass)
        # Step 4: Visualize the results
        plt.figure(figsize=(8, 5))
        sns.barplot(data=ass, x='Assortment', y='Sales', palette='viridis')
        plt.title('Average Sales by Assortment')
        plt.xlabel('Assortment')
        plt.ylabel('Average Sales')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.show()
   
    def comp(self,df,stores):
        logging.info('The difference in sales before and after the opening of compition....')
        fill=['CompetitionDistance','CompetitionOpenSinceMonth','CompetitionOpenSinceYear','Promo2SinceWeek','Promo2SinceYear','PromoInterval']
        stores[fill]=stores[fill].fillna(0)
        merged_df = pd.merge(stores, df, on='Store')
        smthg=merged_df[merged_df['CompetitionOpenSinceYear'] > 2013]
        smthg['Date']=pd.to_datetime(smthg['Date'])
        smthg['SalesYear'] = smthg['Date'].dt.year
        smthg['YearsSinceCompetitionOpen'] = smthg['SalesYear'] - smthg['CompetitionOpenSinceYear']

        # Step 2: Create new columns for sales before and after the competition opened
        smthg['SalesBeforeCompetition'] = smthg.apply(
            lambda x: x['Sales'] if x['YearsSinceCompetitionOpen'] < 0 else 0, axis=1
        )
        smthg['SalesAfterCompetition'] = smthg.apply(
            lambda x: x['Sales'] if x['YearsSinceCompetitionOpen'] >= 0 else 0, axis=1
        )

        
        overall=smthg['SalesAfterCompetition'].sum()
        overall2=smthg['SalesBeforeCompetition'].sum()
        print(f"Sales after competition opening: {overall}")
        print(f"sales before competition opening: {overall2}")
    
    def dis(self,df,stores):
        logging.info('Does distance between compition affect sales....')
        stores['CompetitionDistance']=stores['CompetitionDistance'].fillna(0)
        df_edited= df.groupby('Store')['Sales'].sum().reset_index()
        distance= stores[['Store','CompetitionDistance']]
        merged_df=pd.merge(df_edited,distance, on='Store', how='inner')
        correlation=merged_df['Sales'].corr(merged_df['CompetitionDistance'])
        print(correlation)
    
        
    def highest_sales(self,df):
        logging.info('the highest sales recorded in a single day....')
        highest=df.groupby('Date')['Sales'].sum().reset_index()
        sales=highest.sort_values(by='Sales',ascending= False)
        return sales