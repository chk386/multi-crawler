from multi_crawler.crawler.agencies import do_agencies_info_crawling, to_database

if __name__ == "__main__":
    print("크롤러 GUI 시작")

    datas = do_agencies_info_crawling()
    to_database("multi-crawler", "agency_info", datas)
