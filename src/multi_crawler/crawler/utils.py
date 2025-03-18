import sqlite3

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def get_webdriver(is_headless: bool = False):
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-data-dir=/chrome-user-data")

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


def to_database(name: str, table_name: str, datas: list[any]):  # type: ignore
    conn = sqlite3.connect(f"{name}.db")

    df = pd.DataFrame(datas)

    df.to_sql(table_name, conn, if_exists="replace", index=False, chunksize=1000)
    # df.to_excel(f"{name}.xlsx", index=False)

    return df


# 허용되지 않는 문자 제거 함수
def remove_illegal_chars(text):  # type: ignore
    if isinstance(text, str):
        # 제어 문자 제거 (ASCII 0~31)
        return text.translate(str.maketrans("", "", "".join(map(chr, range(32)))))
    return text  # type: ignore


def to_excel(name: str, datas: list[any]):  # type: ignore
    df = pd.DataFrame(datas)
    df = df.map(remove_illegal_chars)

    df.to_excel(f"{name}.xlsx", index=False)


def get_text_or_empty_in_bs(bs: BeautifulSoup, selector: str):
    app_title = bs.select_one(selector)
    if app_title:
        app_title = str(app_title.text)
    else:
        app_title = ""

    return app_title
