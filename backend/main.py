from services.fetch_data import (
    get_company_ids,
    get_company_data,
    validate_api_response,
    save_raw_json
)

from services.process_data import process_all_companies


EXCEL_PATH = "data/company_id.xlsx"


def main():
    company_ids = get_company_ids(EXCEL_PATH)
    print(f"Total Companies found: {len(company_ids)}")

    for company_id in company_ids:
        print(f"\nFetching data for {company_id}..")
        data = get_company_data(company_id)
        


        # if data:
        #     print("API Response Keys:", data.keys())

        if validate_api_response(data, company_id):
            save_raw_json(company_id, data)
        else:
            print(f"[SKIPPED] Invalid data for {company_id}")

        
        print(f"\nProcessing data for ml..")
        df = process_all_companies(company_ids)

        print("\nML data set ready")
        print(df.head())


if __name__ == "__main__":
    main()
