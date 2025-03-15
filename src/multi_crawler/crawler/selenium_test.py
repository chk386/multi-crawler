from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--headless")  # 헤드리스 모드 실행

# WebDriver 설정 (시스템에 설치된 ChromeDriver 사용)
driver = webdriver.Chrome(options=chrome_options)

try:
    # 웹페이지 열기
    driver.get("https://www.python.org")

    # 페이지 제목 출력
    print(driver.title)

    # 검색 입력란 찾기
    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )

    # 검색어 입력 및 제출
    search_bar.send_keys("pycon")
    search_bar.submit()

    # 검색 결과 확인
    results = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "list-recent-events"))
    )
    print("검색 결과:", results.text)

finally:
    # 브라우저 종료
    driver.quit()
