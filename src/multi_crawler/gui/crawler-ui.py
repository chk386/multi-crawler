import math
import tkinter
import tkinter.messagebox
from enum import Enum
from tkinter import filedialog

from customtkinter import *
from icecream import ic

from multi_crawler.crawler.utils import get_count_table, to_excel
from multi_crawler.gui.gui_utils import throttle  # type: ignore
from multi_crawler.crawler.agencies import (
    do_agencies_info_crawling,
    to_database,  # type: ignore
)
from multi_crawler.crawler.skins import extract_skin_infos, get_all_skin_codes


class ButtonType(Enum):
    SKIN = (1, "스킨 목록", "skin_info")
    AGENCY = (2, "에이전시 목록", "agency_info")
    APP = (3, "앱 목록", "app_info")

    def __init__(self, id: int, filename: str, tablename: str):
        self.id = id
        self.filename = filename
        self.tablename = tablename


class App(CTk):
    entry_text = " : %s 건"

    def __init__(self) -> None:
        super().__init__()

        # 앱 설정 & 레이아웃 구성
        self._init_app()

        # 왼쪽 상단 프레임 셋팅
        self._init_left_top_frame()

        # 왼쪽-중단 Frame
        self._init_left_middle_frame()

        # 랜더링
        self._render_entry_data()

    def _init_app(self):
        set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
        set_default_color_theme(
            "blue"
        )  # Themes: "blue" (standard), "green", "dark-blue"

        # configure window
        self.title("만능 크롤러")
        self.geometry(f"{1200}x{800}")

        # configure grid layout (2x2)
        self.grid_columnconfigure((0), minsize=340, weight=0)
        self.grid_columnconfigure((1), weight=1)
        self.grid_rowconfigure((0, 1), weight=0)

    def _init_left_middle_frame(self):
        self.left_middle_frame = CTkFrame(self, corner_radius=0)
        self.left_middle_frame.grid(
            row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="ew"
        )

        self.left_middle_frame.grid_columnconfigure(0, weight=1)
        self.left_middle_frame.grid_columnconfigure((1, 2), minsize=50, weight=1)

        self.result_label = CTkLabel(
            self.left_middle_frame,
            text="추출 결과",
            font=CTkFont(size=20, weight="bold"),
        )

        self.result_label.grid(row=0, column=0, columnspan=3, padx=0, pady=(20, 0))

        self.skin_entry_stringvar = tkinter.StringVar(value="")

        self.skin_entry = CTkEntry(
            master=self.left_middle_frame,
            textvariable=self.skin_entry_stringvar,
            justify="right",
            state="readonly",
        )
        self.skin_entry.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="ew")

        self.skin_excel_button = CTkButton(
            master=self.left_middle_frame,
            command=lambda id=ButtonType.SKIN: self._extract_data(id),
            width=50,
            text="추출",
        )
        self.skin_excel_button.grid(row=1, column=1, padx=(5, 0), pady=(20, 0))

        self.skin_extract_button = CTkButton(
            master=self.left_middle_frame,
            command=lambda id=ButtonType.SKIN: self._save_file(id),
            width=50,
            text="엑셀",
        )
        self.skin_extract_button.grid(row=1, column=2, padx=(0, 20), pady=(20, 0))

        self.agency_entry_stringvar = tkinter.StringVar(value="")

        self.agency_entry = CTkEntry(
            self.left_middle_frame,
            textvariable=self.agency_entry_stringvar,
            justify="right",
            state="readonly",
        )
        self.agency_entry.grid(row=2, column=0, padx=(20, 0), pady=(20, 0), sticky="ew")

        self.agency_extract_button = CTkButton(
            master=self.left_middle_frame,
            command=lambda id=ButtonType.AGENCY: self._extract_data(id),
            width=50,
            text="추출",
        )
        self.agency_extract_button.grid(row=2, column=1, padx=(5, 0), pady=(20, 0))

        self.agency_excel_button = CTkButton(
            master=self.left_middle_frame,
            command=lambda id=ButtonType.AGENCY: self._save_file(id),
            width=50,
            text="엑셀",
        )
        self.agency_excel_button.grid(row=2, column=2, padx=(0, 20), pady=(20, 0))

        self.app_entry_stringvar = tkinter.StringVar(value="")

        self.app_entry = CTkEntry(
            self.left_middle_frame,
            textvariable=self.app_entry_stringvar,
            justify="right",
            state="readonly",
        )
        self.app_entry.grid(row=3, column=0, padx=(20, 0), pady=(20, 20), sticky="ew")

        self.app_extract_button = CTkButton(
            master=self.left_middle_frame,
            command=lambda id=ButtonType.APP: self._extract_data(id),
            width=50,
            text="추출",
        )
        self.app_extract_button.grid(row=3, column=1, padx=(5, 0), pady=(20, 20))

        self.app_excel_button = CTkButton(
            master=self.left_middle_frame,
            command=lambda id=ButtonType.APP: self._save_file(id),
            width=50,
            text="엑셀",
        )
        self.app_excel_button.grid(row=3, column=2, padx=(0, 20), pady=(20, 20))

    def _init_left_top_frame(self):
        # 왼쪽-상단 Frame
        self.left_top_frame = CTkFrame(self, corner_radius=1)
        self.left_top_frame.grid(
            row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nswe"
        )

        self.left_top_frame.grid_columnconfigure((0, 1), weight=1)
        self.left_top_frame.grid_rowconfigure((1, 2), weight=1)

        self.config_label = CTkLabel(
            self.left_top_frame,
            text="설정",
            font=CTkFont(size=20, weight="bold"),
        )

        self.config_label.grid(row=0, column=0, columnspan=2, padx=0, pady=(20, 0))

        switch = CTkSwitch(master=self.left_top_frame, text="브라우저 실행모드")
        switch.grid(
            row=1, column=0, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="w"
        )

        self.slider = CTkSlider(
            self.left_top_frame,
            from_=0,
            to=1,
            number_of_steps=5,
            width=100,
            command=self._slider_change_event,
        )
        self.slider.grid(row=2, column=0, padx=(20, 0), pady=(20, 20), sticky="w")
        self.slider.set(0)

        self.slider_label = CTkLabel(
            master=self.left_top_frame,
            text="0초 지연 추출",
            font=CTkFont(size=14, weight="normal"),
        )

        self.slider_label.grid(row=2, column=1, padx=0, pady=(20, 20))

    def _render_entry_data(self):
        db = "multi-crawler"

        type_to_stringvar = {
            ButtonType.SKIN: self.skin_entry_stringvar,
            ButtonType.AGENCY: self.agency_entry_stringvar,
            ButtonType.APP: self.app_entry_stringvar,
        }

        for type in ButtonType:
            cnt = get_count_table(db, type.tablename)
            text = f"{type.filename} {self.entry_text}"
            stringvar = type_to_stringvar.get(type, self.app_entry_stringvar)
            stringvar.set(self._get_entry_text(text, cnt))

    def _save_file(self, type: ButtonType):
        """파일 저장 대화상자를 열고 파일을 저장하는 함수"""
        # 파일 저장 대화상자 열기
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            initialfile=f"{type.filename}.xlsx",
            filetypes=[
                ("excel", "*.xlsx"),
            ],
            title="엑셀 저장",
        )

        # 파일 경로가 선택되었는지 확인
        if file_path:
            try:
                ic("저장될 파일 경로 : " + file_path)
                to_excel(f"SELECT * FROM {type.tablename}", file_path)

                tkinter.messagebox.showinfo(
                    "다운로드 완료", f"{file_path}로 저장이 완료 되었습니다."
                )
            except Exception as e:
                ic(e)
                tkinter.messagebox.showerror("다운로드 실패", f"{e} 에러 발생")
        else:
            ic("asd")
            tkinter.messagebox.showwarning("다운로드 취소", "취소 완료")

    def _get_entry_text(self, text: str, cnt: int):
        return text % (str(cnt)).rjust(5)

    def _extract_data(self, type: ButtonType):
        # 에이전시 크롤링 고고
        datas = do_agencies_info_crawling(False)
        to_database("multi-crawler", "agency_info", datas)

    @throttle(delay=500)
    def _slider_change_event(self, value: float):
        sec: int = math.ceil(value * 5)

        self.slider_label.configure(text=str(sec) + "초 지연 추출")
        self.slider_label_text = sec
        ic(self.slider_label_text)


if __name__ == "__main__":
    app = App()
    app.mainloop()
