import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s- %(levelname)s-%(message)s')
class preprocess:
    def load_data(train,test,stores_):
        logging.info('Loading data....')
        df=pd.read_csv(train)
        df_test=pd.read_csv(test)
        stores=pd.read_csv(stores_)
        return df,df_test,stores
    def missing_value(df,df_test,stores):
        logging.info('Checking for missing data....')
        print(df.isnull().sum())
        print(df_test.isnull().sum())
        print(stores.isnull().sum())
    
    def skewed(table, col):
        logging.info('plotting skewed data....')
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=table[col], color="skyblue")
        plt.title(f"Box Plot of {col}", fontsize=16)
        plt.xlabel(col, fontsize=14)
        plt.show()

    def handle_data(df,df_test,stores):
        logging.info('Handling data....')
        fill=['CompetitionDistance','CompetitionOpenSinceMonth','CompetitionOpenSinceYear','Promo2SinceWeek','Promo2SinceYear','PromoInterval']
        stores[fill]=stores[fill].fillna(0)
        df_test = df_test.dropna(subset=['Open'])
        return df,df_test,stores


