import pandas as pd
import requests
from config.api_config import BASE_URL, API_KEY
import json
import os


def get_company_ids(excel_path: str):
    # get the company ids from excel file
    df = pd.read_excel(excel_path)

    if "company_id" not in df.columns:
        raise ValueError("Company id not found in Excel file.")
    
    company_ids = df["company_id"].dropna().unique().tolist()
    return company_ids


def get_company_data(company_id: str):
    # get the financial data for a single company
    params = {
        "id": company_id,
        "api_key": API_KEY
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] API call failed for {company_id}: {e}")
        return None

def validate_api_response(response: dict, company_id: str):
    # Validates api response
    if not response or "data" not in response:
        print(f"[WARRNING] No data section for {company_id}")
        return False
    
    data = response["data"]

    if not isinstance(data, dict):
        print(f"[ERROR] Invalid data format for {company_id}")
        return False

    for section  in ["balance_sheet", "profit_loss", "cash_flow"]:
        if section not in data or not data.get(section):
            print(f"[INFO] {company_id} missing or empty {section}")
            

    return True


def save_raw_json(company_id: str, response: dict):
    # Saves raw API response as JSON file.

    data = response["data"]

    os.makedirs("data/raw_json", exist_ok=True)
    file_path = f"data/raw_json/{company_id}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print (f"[SAVED] Raw data for {company_id}")