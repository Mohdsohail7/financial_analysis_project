import json
import os
import pandas as pd

def load_company_data(company_id: str):
    # load json data for a comapany 
    file_path = f"data/raw_json/{company_id}.json"

    if not os.path.exists(file_path):
        return None
    
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
    

def convert_json_data_to_dataframe(section_data):
    # convert json section to dataframe 
    if not section_data or not isinstance(section_data, list):
        return pd.DataFrame()
    
    df = pd.DataFrame(section_data)
    return df


def data_clean_numeric(df: pd.DataFrame):
    # convert numeric values into columns

    for col in df.columns:
        df[col] = (
            df[col].astype(str).str.replace("%", "", regex=False).str.replace(",", "", regex=False).replace("None", None)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def extract_feature(balance_df, pl_df):
    features = {}
    try:
        net_profit = pl_df["net_profit"].iloc[0]
        equity = balance_df["equity_capital"].iloc[0] + balance_df["reserves"].iloc[0]
        features["roe"] = (net_profit / equity) * 100 if equity else None
    except Exception:
        features["roe"] = None

    try:
        debt = balance_df["borrowings"].iloc[0]
        equity = balance_df["equity_capital"].iloc[0] + balance_df["reserves"].iloc[0]
        features["debt_to_equity"] = debt / equity if equity else None
    except Exception:
        features["debt_to_equity"] = None

    try:
        latest_sales = pl_df["sales"].iloc[0]
        previous_sales = pl_df["sales"].iloc[0]
        features["sales_growth"] = (
            (latest_sales - previous_sales) / previous_sales * 100
            if previous_sales else None
        )

    except Exception:
        features["sales_growth"] = None
    
    return features



def process_company(company_id: str):
    raw_data = load_company_data(company_id)

    if not raw_data:
        return None
    
    balance_df = data_clean_numeric(
        convert_json_data_to_dataframe(raw_data.get("balancesheet"))
    )

    pl_df = data_clean_numeric(
        convert_json_data_to_dataframe(raw_data.get("profitandloss"))
    )

    features = extract_feature(balance_df, pl_df)
    features["company_id"] = company_id

    return features


def process_all_companies(company_ids):
    records = []

    for company_id in company_ids:
        print(f"Processing {company_id}...")
        features = process_company(company_id)

        if features:
            records.append(features)

    return pd.DataFrame(records)

