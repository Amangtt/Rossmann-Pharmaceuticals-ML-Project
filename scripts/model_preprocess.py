import pandas as pd
import argparse
from sklearn.preprocessing import StandardScaler

def Feature_engeneering(input_path,output_path):
    df = pd.read_csv(input_path)
    # Ensure 'Date' is in datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    # Extract day, month, year
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['IsWeekend'] = df['DayOfWeek'].apply(lambda x: 1 if x >= 6 else 0)
    df['MonthPeriod'] = pd.cut(df['Day'], bins=[0, 10, 20, 31], labels=['Beginning', 'Mid', 'End'])
    # Get holiday dates
    holiday_dates = df.loc[df['StateHoliday'].isin(['a', 'b', 'c']), 'Date'].sort_values().unique()

    # Initialize columns for days to the next and previous holiday
    df['DaysToHoliday'] = None
    df['DaysAfterHoliday'] = None

    # Calculate DaysToHoliday and DaysAfterHoliday
    for i, current_date in df['Date'].items():
            # Skip calculations if the current date is a holiday
        if current_date in holiday_dates:
            continue

        # Calculate the difference with holidays
        diffs = [(holiday_date - current_date).days for holiday_date in holiday_dates]
            
        # Find the next holiday difference (non-negative)
        future_diffs = [d for d in diffs if d > 0]  # strictly greater than 0
        df.at[i, 'DaysToHoliday'] = min(future_diffs) if future_diffs else None

        # Find the previous holiday difference (negative)
        past_diffs = [abs(d) for d in diffs if d < 0]  # strictly less than 0
        df.at[i, 'DaysAfterHoliday'] = min(past_diffs) if past_diffs else None
    df['Quarter'] = df['Date'].dt.quarter
    col=['DaysToHoliday','DaysAfterHoliday']
    df[col]=df[col].fillna(0)
    df = df.drop(columns=['Date'], errors='ignore')
        
    df = pd.get_dummies(df, columns=['MonthPeriod','StateHoliday'], drop_first=True)
            # Scale the features
    scaler = StandardScaler()
    numeric_cols = ["Sales", "Customers", "DaysToHoliday", "DaysAfterHoliday"]
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
        # Save to CSV
    df.to_csv(output_path, index= False)
            
if __name__=="__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help='Path to read csv')
    parser.add_argument('--output', required=True, help='Path to output csv')
    args=parser.parse_args()
    Feature_engeneering(args.input,args.output)



