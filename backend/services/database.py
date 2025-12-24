import json
from sqlalchemy import text
from config.db_config import engine


def save_data_in_database(row):
    query = text("""
        INSERT INTO ml(
                 company_id, score, roe, debt_to_equity, sales_growth, pros, cons
        )
                 VALUES(
                 :company_id, :score, :roe, :debt, :growth, :pros, :cons
                 )
                 ON DUPLICATE KEY UPDATE
                 score = VALUES(score)
                 roe = VALUES(roe)
                 debt_to_equity = VALUES(debt_to_equity),
                sales_growth = VALUES(sales_growth),
                pros = VALUES(pros),
                cons = VALUES(cons)
""")
    
    data = {
        "company_id": row["company_id"],
        "score": int(row["score"]),
        "roe": row.get("roe"),
        "debt": row.get("debt_to_equity"),
        "growth": row.get("sales_growth"),
        "pros": json.dumps(row.get("pros", [])),
        "cons": json.dumps(row.get("cons", [])),
    }

    with engine.begin() as conn:
        conn.execute(query, data)