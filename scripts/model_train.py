import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import yaml
import argparse
from datetime import datetime
import joblib
def train(input_path):
    df=pd.read_csv(input_path)
    with open('param.yaml', 'r') as param_file:
        params = yaml.safe_load(param_file)
        model_param = params['Train_model']['reg']
    
    X = df.drop(columns=['Sales', 'Customers'])  # Drop the target column
    y = df['Sales']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
         
    model=RandomForestRegressor(**model_param)
    
    model.fit(X_train, y_train)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    model_path = f"{timestamp}.pkl"
    joblib.dump(model, model_path)
if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help='Path to read csv')
    
    args=parser.parse_args()
    train(args.input)