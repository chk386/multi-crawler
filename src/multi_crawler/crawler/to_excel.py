import sqlite3

import pandas as pd

if __name__ == "__main__":
    # skin_infos
    conn = sqlite3.connect("multi-crawler.db")
    df = pd.read_sql_query("SELECT * FROM agency_info", conn)

    df.to_excel("에이전시목록.xlsx")
