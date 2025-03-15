import time
from datetime import datetime

# from pprint import pprint
from urllib.parse import parse_qs, urlparse

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from utils import (
    get_text_or_empty,
    get_webdriver,
    is_element_exist,
    selected_elems,
    to_database,
)

# from config.app_logging import logger
sleep_time = 0


def get_agency_info(driver: WebDriver, page: WebElement):
    agency_url = driver.current_url
    print(f"에이전시 페이지 : {agency_url}")

    url_parsed = urlparse(agency_url)
    query_params = parse_qs(url_parsed.query)
    agency_id = query_params.get("agencyId", "-")[0]

    entry_date = page.find_element(
        By.CSS_SELECTOR, "div.last > span:nth-child(2)"
    ).text.split(" ")[0]

    agency_selector = "#designer-info > dl > dd:nth-child({})"

    business_number = get_text_or_empty(
        page, By.CSS_SELECTOR, agency_selector.format("12")
    )

    business_address = get_text_or_empty(
        page, By.CSS_SELECTOR, agency_selector.format("14")
    )
    agency_info_selector = (
        "div.designer-info-content > div:nth-child(3) > dl > dd:nth-child({})"
    )
    contact_person = get_text_or_empty(
        page, By.CSS_SELECTOR, agency_info_selector.format("2")
    )

    email = get_text_or_empty(page, By.CSS_SELECTOR, agency_info_selector.format("6"))
    phone_number = get_text_or_empty(
        page, By.CSS_SELECTOR, agency_info_selector.format("8")
    )

    website_url = get_text_or_empty(
        page, By.CSS_SELECTOR, agency_info_selector.format("10")
    )

    review_count = page.find_element(By.CSS_SELECTOR, ".reviews").text.split(" ")[0]
    review_url = f"https://d.cafe24.com/designer/designer_comment?agencyId={agency_id}"

    skin_url = f"https://d.cafe24.com/designer/designer_product?productTypeCode=PTMD&agencyId={agency_id}"
    driver.get(skin_url)

    page = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, "#container"))
    )

    skin_count = get_text_or_empty(
        page, By.CSS_SELECTOR, "div.pb-10.row-c-between > div.txt-md"
    )

    skin_count = skin_count.split("개")[0] if skin_count else "0"

    data: dict[str, str | int | datetime] = {
        "agency_id": agency_id,
        "entry_date": entry_date,
        "business_number": business_number,
        "business_address": business_address,
        "contact_person": contact_person,
        "email": email,
        "phone_number": phone_number,
        "website_url": website_url,
        "review_count": int(review_count.replace(",", "") if review_count else 0),
        "review_url": review_url,
        "skin_count": int(skin_count.replace(",", "") if skin_count else 0),
        "skin_url": skin_url,
        "created_at": datetime.now(),
    }

    return data


def do_agencies_info_crawling():
    print("에이전시 크롤링을 시작합니다.")
    start_time = time.time()
    datas: list[dict[str, str | int | datetime]] = []
    driver = get_webdriver()

    try:
        # 디자이너샵(에이전시) 목록 페이지
        page_no = 1

        while True:
            url = f"https://d.cafe24.com/designer/designer_main?safety=Y&order=REG_ASC&pageNo={page_no}&isActive=T"
            print(f"페이지번호 : {page_no}, url : {url}")

            page_no += 1
            driver.get(url)

            # 목록 끝일 경우 종료
            if is_element_exist(driver, By.CLASS_NAME, "cart-none"):
                break

            designer_links = selected_elems(driver, By.CLASS_NAME, "shop-link")

            # 디자이너샵 목록 순회하여 해당 엘리먼트 클릭
            for i in range(len(designer_links)):
                # url이 변경되었다가 다시 돌아오기 때문에 다시 elements를 가져와야 함
                designer_links: list[WebElement] = selected_elems(
                    driver,
                    By.CLASS_NAME,
                    "shop-link",  # + 디자이너샵 바로가기 버튼 셀렉트
                )

                time.sleep(sleep_time)

                designer_link = designer_links[i]
                designer_link.click()

                # 디자이너샵 페이지 전환 & 랜더링 완료 대기
                WebDriverWait(driver, 10).until(ec.url_changes(url))
                page = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, "#container"))
                )

                datas.append(get_agency_info(driver, page))

                # 디자이너 목록 페이지로 이동
                driver.get(url=url)

    except:
        print("에이전시 크롤링 중 에러 발생")
        raise
    finally:
        print(f"총 {len(datas)}개의 에이전시 정보를 저장하였습니다.")
        print("에이전시 크롤링을 종료합니다.")
        end_time = time.time()
        print(f"에이전시 목록 크롤링 소요시간 : {end_time - start_time:.2f}초")
        # 브라우저 종료
        driver.quit()

    return datas


if __name__ == "__main__":

    datas: list[dict[str, str | int | datetime]] = do_agencies_info_crawling()
    to_database("multi-crawler", "agency_info", datas)
