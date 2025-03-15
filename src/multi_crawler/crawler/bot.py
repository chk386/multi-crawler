import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3


# 비동기 HTTP 요청 함수
async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()


# HTML 파싱 및 데이터 추출 함수
def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    # 예시: 테이블 데이터를 추출한다고 가정
    table = soup.find("table")  # HTML에서 테이블 태그를 찾음
    if not table:
        return None

    # 테이블의 헤더와 데이터를 추출
    headers = [th.text.strip() for th in table.find_all("th")]
    rows = []
    for tr in table.find_all("tr")[1:]:  # 헤더 제외
        row = [td.text.strip() for td in tr.find_all("td")]
        if row:
            rows.append(row)

    # pandas DataFrame 생성
    df = pd.DataFrame(rows, columns=headers)
    return df


# SQLite에 저장하는 함수
def save_to_sqlite(df, db_name="data.db", table_name="parsed_data"):
    conn = sqlite3.connect(db_name)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    print(f"Data saved to {db_name} in table {table_name}")


# 메인 비동기 함수
async def main(urls):
    async with aiohttp.ClientSession() as session:
        # 모든 URL에 대해 비동기 요청
        tasks = [fetch_url(session, url) for url in urls]
        html_responses = await asyncio.gather(*tasks)

        # HTML 파싱 및 DataFrame 생성
        all_dfs = []
        for html in html_responses:
            df = parse_html(html)
            if df is not None:
                all_dfs.append(df)

        # 모든 DataFrame을 하나로 합침 (필요 시)
        if all_dfs:
            final_df = pd.concat(all_dfs, ignore_index=True)
            # SQLite에 저장
            save_to_sqlite(final_df)
        else:
            print("No data to save.")


# 비동기 HTTP 요청 함수
async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()


async def fetch(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


# 실행 예시
if __name__ == "__main__":
    url = "https://d.cafe24.com/designer/designer_main?safety=Y&order=REG_ASC&pageNo=1&isActive=T"
    # 위 url에서 pageNo를 1씩 증가하여 없을떄까지 지속적으로 조회
    #

    html = asyncio.run(fetch(url))
    print(html)

    # # 파싱할 URL 리스트 (예시)
    # urls = [
    #     "https://d.cafe24.com/designer/designer_main?keyword=&searchBrand=&companyType=&productCntMin=0&productCntMax=2686&termType=all&startDate=&endDate=&safety=Y&order=REG_ASC&pageNo=5&isActive=T",
    #     "https://example.com/page2",
    # ]

    # # 비동기 실행
    # asyncio.run(main(urls))
