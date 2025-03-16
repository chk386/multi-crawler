from multi_crawler.crawler.agencies import (
    do_agencies_info_crawling,
    to_database,  # type: ignore
)
from multi_crawler.crawler.skins import extract_skin_infos, get_all_skin_codes

if __name__ == "__main__":
    print("크롤러 GUI 시작")

    datas = do_agencies_info_crawling()
    to_database("multi-crawler", "agency_info", datas)

    codes = get_all_skin_codes()
    to_database("multi-crawler", "skin_codes", codes)  # type: ignore

    skin_datas = extract_skin_infos(codes)
    to_database("multi-crawler", "skin_info", skin_datas)  # type: ignore
