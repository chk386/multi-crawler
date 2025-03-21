import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd
from appdirs import user_data_dir  # type: ignore
from bs4 import BeautifulSoup
from icecream import ic
from pandas.errors import DatabaseError
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def get_user_data_path():
    user_data_path = str(user_data_dir("multi-crawler"))  # type: ignore
    directory_path = Path(user_data_path)
    directory_path.mkdir(parents=True, exist_ok=True)

    ic(user_data_path)

    return user_data_path


def get_webdriver(is_headless: bool = False):
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # chrome_options.add_argument(f"user-data-dir={get_user_data_path()}")

    # 브로우저가 자동 종료 방지 옵션
    chrome_options.add_experimental_option("detach", True)
    # 콘솔 출력 방지
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    if is_headless:
        chrome_options.add_argument("--headless")  # 헤드리스 모드 실행

    # WebDriver 설정 (시스템에 설치된 ChromeDriver 사용)
    return webdriver.Chrome(options=chrome_options)


def get_text_or_empty(page: WebElement, by: str, value: str) -> str:
    elems = page.find_elements(by, value)
    return elems[0].text if elems else ""


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def selected_elems(driver: WebDriver, by: str, selector: str) -> list[WebElement]:
    return WebDriverWait(driver, 10).until(
        method=ec.presence_of_all_elements_located((by, selector))
    )


def is_element_exist(driver: WebDriver, by: str, selector: str) -> bool:
    try:
        driver.find_element(by, selector)
    except NoSuchElementException:
        return False
    return True


def to_database(database: str, table_name: str, datas: list[any]):  # type: ignore
    if len(datas) == 0:
        return

    conn = sqlite3.connect(f"{database}.db")
    df = pd.DataFrame(datas)

    df.to_sql(table_name, conn, if_exists="replace", index=False, chunksize=1000)
    # df.to_excel(f"{name}.xlsx", index=False)

    return df


def get_count_table(database: str, tablename: str):
    conn = sqlite3.connect(f"{database}.db")
    cnt = 0
    try:
        df = pd.read_sql_query(con=conn, sql=f"SELECT count(*) AS cnt FROM {tablename}")
        cnt = int(df["cnt"].iloc[0])  # type: ignore
    except DatabaseError:
        ic(tablename + "추출 & 수집 전입니다.")
    finally:
        conn.close()

    return cnt


def get_text_or_empty_in_bs(bs: BeautifulSoup, selector: str):
    app_title = bs.select_one(selector)
    if app_title:
        app_title = str(object=app_title.text)
    else:
        app_title = ""

    return app_title


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
