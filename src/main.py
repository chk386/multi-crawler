from multi_crawler.config.logging import logger
from multi_crawler.gui.crawler_ui import App

if __name__ == "__main__":
    logger.info("크롤러 GUI 시작")

    app = App()
    app.mainloop()
