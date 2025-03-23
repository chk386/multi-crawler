from icecream import ic

from multi_crawler.crawler.utils import generate_random_float


def test_랜덤_지연시간():
    # given : 초기 조건 설정
    start, end = 0, 5
    print("hihi")

    for _ in range(0, 100):
        # when : 테스트 대상 실행
        random_number = generate_random_float(start, end)
        ic(generate_random_float(start, end))

        # then : 예상 결과 검증
        assert start <= random_number <= end, (
            f"{end}초 를 입력했을 경우 랜덤 숫자는 {start}~{end} 숫자로 나와야 한다."
        )
