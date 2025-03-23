import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

if getattr(sys, "frozen", False):
    os.environ["ENV"] = "production"
    dotenv_path = os.path.join(sys._MEIPASS, ".env.prod")  # type: ignore
    load_dotenv(dotenv_path)
    log_file = f"{os.path.dirname(sys.executable)}/{os.getenv('LOG_FILE')}"

else:
    load_dotenv(".env.local")
    log_file = os.getenv("LOG_FILE")


# 환경 변수 사용
DEBUG = os.getenv("DEBUG") == "True"
LOG_LEVEL = os.getenv("LOG_LEVEL")

# 로그 파일 디렉토리 생성
os.makedirs(name=os.path.dirname(log_file), exist_ok=True)

# 로그 포맷 설정
formatter = logging.Formatter(
    # %(module)s
    fmt="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d %(funcName)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# 파일 핸들러 (로그 로테이션)
file_handler = RotatingFileHandler(
    log_file,
    maxBytes=1024 * 1024 * 10,
    backupCount=5,
)

file_handler.setFormatter(formatter)

handlers: list[logging.Handler] = [file_handler]


if DEBUG:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    handlers.append(console_handler)


# 루트 로거 설정
logging.basicConfig(
    level=LOG_LEVEL,
    handlers=handlers,
)

logger = logging.getLogger()
