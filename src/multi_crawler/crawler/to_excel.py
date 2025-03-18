import sqlite3

import pandas as pd


# 허용되지 않는 문자 제거 함수
def remove_illegal_chars(text):
    if isinstance(text, str):
        # 제어 문자 제거 (ASCII 0~31)
        return text.translate(str.maketrans("", "", "".join(map(chr, range(32)))))
    return text


if __name__ == "__main__":
    # skin_infos
    conn = sqlite3.connect("multi-crawler.db")
    df = pd.read_sql_query("SELECT * FROM app_info", conn)
    df = df.applymap(remove_illegal_chars)

    df.to_excel("앱목록.xlsx")
