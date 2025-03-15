import sqlite3
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def get_webdriver():
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--headless")  # 헤드리스 모드 실행

    # WebDriver 설정 (시스템에 설치된 ChromeDriver 사용)
    return webdriver.Chrome(options=chrome_options)


def get_text_or_empty(page: WebElement, by: str, value: str) -> str:
    elems = page.find_elements(by, value)
    return elems[0].text if elems else ""


def selected_elems(driver: WebDriver, by: str, selector: str) -> list[WebElement]:
    return WebDriverWait(driver, 3).until(
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
