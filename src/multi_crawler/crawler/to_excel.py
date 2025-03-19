import sqlite3

import pandas as pd


# 허용되지 않는 문자 제거 함수
def remove_illegal_chars(text: str):
    if isinstance(text, str):  # type: ignore
        # 제어 문자 제거 (ASCII 0~31)
        return text.translate(str.maketrans("", "", "".join(map(chr, range(32)))))

    return text


def to_excel(sql: str, filename: str):
    conn = sqlite3.connect("multi-crawler.db")
    df = pd.read_sql_query(sql, conn)
    df = df.applymap(remove_illegal_chars)  # type: ignore

    df.to_excel(filename)
