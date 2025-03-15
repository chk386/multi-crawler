import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="multi_crawler.log",
)

logger = logging.getLogger(__name__)

# 회전 핸들러 생성 (최대 1MB, 최대 3개 파일 보관)
handler = RotatingFileHandler("multi_crawler.log", maxBytes=1024 * 1024, backupCount=3)
logger.addHandler(handler)

# 로그 메시지 출력
logging.debug("이 메시지는 출력되지 않습니다.")  # DEBUG 레벨은 출력되지 않음
logging.info("정보 메시지입니다.")
logging.warning("경고 메시지입니다.")
logging.error("오류 메시지입니다.")
logging.critical("심각한 오류 메시지입니다.")
