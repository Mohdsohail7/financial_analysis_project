import json
import os
import pandas as pd
from services.scoring_engine import score_company
from services.insight_generator import generate_insights
from services.database import save_data_in_database


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
    if df.empty:
        return df
    
    # convert numeric values into columns

    for col in df.columns:
        df[col] = (
            df[col].astype(str).str.replace("%", "", regex=False).str.replace(",", "", regex=False).replace(["None", "nan", ""], None)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def sort_by_year(df: pd.DataFrame):
    if "year" in df.columns:
        df = df.sort_values(by="year", ascending=False)
    return df


def extract_feature(balance_df, pl_df):
    features = {}
    try:
        net_profit = pl_df["net_profit"].iloc[0]
        equity = (
            balance_df["equity_capital"].iloc[0]
            + balance_df["reserves"].iloc[0]
        )
        features["roe"] = (net_profit / equity) * 100 if equity else None
    except Exception:
        features["roe"] = None

    try:
        debt = balance_df["borrowings"].iloc[0]
        equity = (
            balance_df["equity_capital"].iloc[0]
            + balance_df["reserves"].iloc[0]
        )
        features["debt_to_equity"] = debt / equity if equity else None
    except Exception:
        features["debt_to_equity"] = None

    try:
        if len(pl_df) >= 2:
            latest_sales = pl_df["sales"].iloc[0]
            previous_sales = pl_df["sales"].iloc[1]
            features["sales_growth"] = (
                (latest_sales - previous_sales) / previous_sales * 100
                if previous_sales else None
            )
        else:
            features["sales_growth"] = None
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

    balance_df = sort_by_year(balance_df)
    pl_df = sort_by_year(pl_df)

    features = extract_feature(balance_df, pl_df)
    features["company_id"] = company_id

    return features


def process_all_companies(company_ids):
    records = []

    for company_id in company_ids:
        print(f"Processing {company_id}...")
        features = process_company(company_id)

        if not features:
            continue

        score, pros_flags, cons_flags = score_company(features)
        pros_text, const_text = generate_insights(pros_flags, cons_flags)

        features["score"] = score
        features["pros_flags"] = pros_text
        features["cons_flags"] = const_text

        records.append(features)
        # save_data_in_database(features)


    df =  pd.DataFrame(records)
    #  Log cleaned ML dataset 
    if not df.empty:
        os.makedirs("data/processed", exist_ok=True)
        df.to_csv("data/processed/ml_dataset.csv", index=False)

    return df



