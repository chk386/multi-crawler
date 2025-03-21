from __future__ import annotations

import time
from collections.abc import Callable

import icecream
import requests
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from multi_crawler.crawler.utils import (
    get_user_data_path,
    get_webdriver,
    selected_elems,
    to_database,  # type: ignore
)

categories = [
    1005,
    # 236,
    # 240,
    # 1006,
    # 1003,
    # 239,
    # 1004,
    # 237,
    # 1002,
    # 803,
    # 823,
    # 233,
    # 243,
    # 232,
    # 234,
    # 242,
    # 238,
]


# FIXME: delay_time 적용해야함
def get_all_skin_codes(is_headless: bool, delay_time: int, log) -> set[str]:  # type: ignore
    log("스킨 코드 크롤링 시작!\n")

    start_time = time.time()

    driver: WebDriver = get_webdriver(is_headless)
    skin_codes: set[str] = set()

    try:
        # 스킨 카테고리 조회 페이지
        for no in categories:
            url = f"https://d.cafe24.com/category?display=PTMD&no={no}"
            log(f"스킨 카테고리 목록 url : {url}")

            driver.get(url=url)

            # 스크롤 처리
            move_scroll(driver)

            results = get_skin_codes(driver)
            log(f"카테고리번호 [{no}] 스킨 총 카운트 : {len(results)}")

            skin_codes.update(results)

    except:
        screenshot = f"{get_user_data_path()}/screenshot-error.png"
        driver.save_screenshot(screenshot)

        log(
            f"""
            =====================================
            크롤링 과정에서 오류가 발생하였습니다.
            f"에러 스크린샷 확인 : {screenshot}"
            =====================================
        """.strip()
        )

        raise
    finally:
        end_time = time.time()
        log(f"스킨 목록 크롤링 소요시간 : {end_time - start_time:.2f}초\n")

        driver.quit()

    return skin_codes


def get_skin_codes(driver: WebDriver) -> set[str]:
    # fixme: skin_codes는 중복일 수 있다.
    skin_codes: list[str] = []
    skin_elems = selected_elems(driver, By.CSS_SELECTOR, ".items-wrap > a.link")

    for elem in skin_elems:
        skin_code = (elem.get_attribute("href") or "productCode=0").split(
            "productCode="
        )[1]

        skin_codes.append(skin_code)

    print(f"스킨 코드 목록 : {skin_codes}")

    return set(skin_codes)


def move_scroll(driver: WebDriver):
    scroll_y = 0

    while True:
        for _ in range(0, 5):
            # 스크롤 내리기
            driver.execute_script("window.scrollBy(0, 200);")

            # 페이지 로딩 대기
            time.sleep(0.1)

        current_scroll_y = int(driver.execute_script("return window.scrollY;"))  # type: ignore

        # 스크롤 변화가 없을경우 탈출
        if scroll_y == current_scroll_y:
            break

        scroll_y = current_scroll_y


def extract(line: str, sep: str) -> str:
    parts = line.split(sep)
    line.split("productName")[1]
    if len(parts) > 1:
        return parts[1].split(",")[0].replace('\\"', "").strip()

    return ""


def extract_skin_infos(codes: set[str], delay_time: int, log: Callable[[str], None]):
    datas: list[dict[str, str | int | float]] = []

    for code in codes:
        time.sleep(delay_time)
        url = f"https://d.cafe24.com/product/product_detail?productCode={code}"

        response = requests.get(
            url,
            stream=True,
        )

        # 라인별로 읽기
        for line in response.iter_lines(decode_unicode=True):
            if line:  # 빈 라인은 무시
                if "selling" in line:
                    one_line = str(line).strip()

                    left_index = one_line.rfind("self.", 0, one_line.find("sellingCnt"))
                    one_line = one_line[left_index:]
                    right_index = one_line.rfind(
                        "</script>", one_line.find("sellingCnt"), len(one_line)
                    )
                    one_line = one_line[:right_index]

                    skin_name = extract(one_line, 'productName\\":')
                    selling_cnt = extract(one_line, 'sellingCnt\\":')
                    agency_id = extract(one_line, 'agencyId\\":')
                    agency_name = extract(one_line, 'brandName\\":')
                    product_code = extract(one_line, 'productCode\\":')
                    product_price = extract(one_line, 'productPrice\\":')
                    update_at = extract(one_line, 'lastModifyDate\\":')
                    created_at = extract(one_line, 'regDate\\":')
                    hit_cnt = extract(one_line, 'hitCnt\\":')
                    design_style = extract(one_line, 'designStyle\\":')
                    layout = extract(one_line, 'layout\\":')
                    tag = extract(one_line, 'tag\\":')
                    count = extract(one_line, 'count\\":')
                    avg_rating = extract(one_line, 'avgRating\\":')
                    avg_rating = avg_rating if avg_rating != "null" else 0
                    color = extract(one_line, 'color\\":')
                    category_code1 = extract(one_line, 'categoryCode1\\":')
                    category_code2 = extract(one_line, 'categoryCode2\\":')

                    data: dict[str, str | int | float] = {
                        "skin_name": skin_name,
                        "sale_cnt": int(
                            selling_cnt.replace(",", "") if selling_cnt else 0
                        ),
                        "agency_id": agency_id,
                        "agency_name": agency_name,
                        "skin_code": product_code,
                        "skin_detail_url": url,
                        "sample_url": f"https://d.cafe24.com/sample?productCode={product_code}&frame=P",
                        "design_type": (
                            "반응형" if skin_name.__contains__("반응형") else "개별형"
                        ),
                        "design_style": design_style,
                        "layout": layout,
                        "hit_cnt": int(hit_cnt.replace(",", "") if hit_cnt else 0),
                        "product_price": product_price,
                        "tag": tag,
                        "review_cnt": int(count.replace(",", "") if count else 0),
                        "review_avg_rating": float(
                            avg_rating.replace(",", "") if avg_rating else 0
                        ),
                        "color": color,
                        "category_code1": category_code1,
                        "category_code2": category_code2,
                        "update_at": update_at,
                        "create_at": created_at,
                    }

                    log(f"스킨별 정보 추출 : {skin_name}, url : {url}")

                    datas.append(data)

    log("스킨 추출이 완료되었습니다.\n")
    log(f"총 {len(codes)} 건 추출하였습니다.")

    return datas


def extract_skins(is_headless: bool, delay_time: int, log: Callable[[str], None]):
    codes = get_all_skin_codes(is_headless, delay_time, log)
    to_database("multi-crawler", "skin_codes", codes)  # type: ignore

    skin_datas = extract_skin_infos(codes, delay_time, log)
    to_database("multi-crawler", "skin_info", skin_datas)  # type: ignore

    log("refresh")


if __name__ == "__main__":
    print("스킨 크롤링을 시작합니다.")

    extract_skins(False, 0, icecream.ic)  # type: ignore
