import time

import requests
from bs4 import BeautifulSoup
from icecream import ic

from multi_crawler.crawler.utils import (
    get_text_or_empty_in_bs,
    to_database,  # type: ignore
    to_excel,
)

cookies = {
    # 'fb_external_id': 'f90ba5d5f0ed6264eb726745e1c0141634ccdee35710bfd52c95ddebf7004e9a',
    # 'FROM_DCAFE': 'echosting',
    # 'fb_event_id': 'event_id.eckorea24.1.G2CJDJFMDW2JCTSDM4F1BAC9RSIW38P',
    # 'CUR_STAMP': '1737702802517',
    # 'PHPSESSID': '52e1618938d4bb5242e24253b5164c75',
    # 'analytics_session_id': 'analytics_session_id.eckorea24_1.D5CDB92.1741762564950',
    # 'analytics_longterm': 'analytics_longterm.eckorea24_1.D5CDB92.1741762564950',
    # 'myhdpharm01.cafe24.com-crema_device_token': 'GtYVEBu4a2MsYSYlx48yQjh0QNFiGm9y',
    "country_code": "CN",
    # 'ch-veil-id': '58a4308d-f479-4b8c-9ea9-0fe5f406cd78',
    # 'cafe_user_name': 'chk386%2C%EC%A1%B0%ED%98%9C%EA%B7%9C%2Cue6080.echosting.cafe24.com',
    # 'show_product_no': '29501',
}

headers = {
    "accept": "text/html, */*; q=0.01",
    "accept-language": "ko-KR,ko;q=0.7",
    "priority": "u=1, i",
    "referer": "https://store.cafe24.com/kr/category/apps?",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Brave";v="134"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}


sleep_time = 0


def extract_app_urls(page: int) -> list[str]:
    uris = list[str]()
    ic("앱 주소 조회 시작!\n")

    while True:
        time.sleep(sleep_time)

        params = {
            "page": str(page),
            "order": "SALES_DESC",
            "filter": "{}",
        }

        response = requests.get(
            "https://store.cafe24.com/kr/filter/rest/apps",
            params=params,
            cookies=cookies,
            headers=headers,
        )

        if not response.text.strip():
            ic("앱 주소 조회 - 끝!")
            ic(f"\n추출된 앱 갯수 : {len(uris)}")
            return uris

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            bs = soup.select(selector=".inner >.js-gtm-search-app")

            uri = [str(b.get("href")) for b in bs]
            ic(f"주소 추출 : {uri}")
            uris.extend(uri)

        else:
            response.raise_for_status()

        page += 1


def extrace_app_infos(app_paths: list[str]):
    datas = list[dict[str, str]]()
    ic("앱 정보 추출 시작!\n")
    for path in app_paths:
        url = f"https://store.cafe24.com{path}"
        ic(f"앱 상세 url : {url}")

        response = requests.get(
            url,
            cookies=cookies,
            headers=headers,
        )

        if response.status_code == 200:
            bs = BeautifulSoup(response.text, "html.parser")

            data = {
                "app_no": url.split("/")[-1],  # URL에서 마지막 부분을 app_no로 사용
                "app_url": url,
                "app_title": get_text_or_empty_in_bs(bs, ".infoHead > .title"),
                "partner_name": get_text_or_empty_in_bs(
                    bs, "li.partner > div > span > a"
                ),
                "review_avg_score": get_text_or_empty_in_bs(bs, ".average"),
                "review_cnt": get_text_or_empty_in_bs(bs, "span.review > a > span"),
                # "category": get_text_or_empty_in_bs(
                #     bs,
                #     "div.infoProductWrap > div.infoListArea > ul > li:nth-child(2) > p > span",
                # ),
                "faq_list": get_text_or_empty_in_bs(bs, "#app_faq_list"),
                "inquiry_list": get_text_or_empty_in_bs(bs, "#js-inquiry-list-div"),
                "recent_review_list": get_text_or_empty_in_bs(bs, "#comment_list"),
            }

            datas.append(data)

        else:
            continue

    return datas


if __name__ == "__main__":
    app_paths = extract_app_urls(page=1)
    df = to_database("multi-crawler", "app_uris", app_paths)  # type: ignore

    app_infos = extrace_app_infos(app_paths)

    to_database("multi-crawler", "app_info", app_infos)
    to_excel("app_info", app_infos)
