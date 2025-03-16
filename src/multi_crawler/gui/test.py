import tkinter
import tkinter.messagebox

from customtkinter import (
    CTk,
    CTkButton,
    CTkCheckBox,
    CTkComboBox,
    CTkEntry,
    CTkFont,
    CTkFrame,
    CTkInputDialog,
    CTkLabel,
    CTkOptionMenu,
    CTkProgressBar,
    CTkRadioButton,
    CTkScrollableFrame,
    CTkSegmentedButton,
    CTkSlider,
    CTkSwitch,
    CTkTabview,
    CTkTextbox,
    set_appearance_mode,
    set_default_color_theme,
    set_widget_scaling,
)

set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(CTk):
    def __init__(self) -> None:
        super().__init__()

        # configure window
        self.title("처음 만들어보는 크롤러")
        self.geometry(f"{1200}x{800}")

        # configure grid layout (2x3)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # 설정 영역 frame
        self.config_frame = CTkFrame(self)
        self.config_frame.grid_columnconfigure((0, 1), weight=1)
        self.config_frame.grid(row=0, column=0, padx=0, pady=0, sticky="w")

        self.label_config_group = CTkLabel(
            master=self.config_frame, text="*Configuration*"
        )
        self.label_config_group.grid(row=0, column=0, columnspan=1, padx=10, pady=10)

        # 추출 버튼 frame
        self.extract_frame = CTkFrame(self)
        self.extract_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

        self.extract_agency = CTkButton(
            self.extract_frame, text="에이전시 정보 크롤링 시작", width=300
        )
        self.extract_agency.grid(row=0, column=0, padx=0, pady=0, sticky="")

        self.extract_skin = CTkButton(
            self.extract_frame, text="스킨 정보 크롤링 시작", width=300
        )
        self.extract_skin.grid(row=1, column=0, padx=0, pady=0, sticky="")

        # 엑셀 버튼 frame
        self.excel_frame = CTkFrame(self)
        self.excel_frame.grid(row=2, column=0, padx=0, pady=0, sticky="nsew")

        self.excel_agency = CTkButton(
            self.excel_frame, text="에이전시 정보 크롤링 시작", width=300
        )
        self.excel_agency.grid(row=0, column=0, padx=0, pady=0, sticky="")

        self.excel_skin = CTkButton(
            self.excel_frame, text="스킨 정보 크롤링 시작", width=300
        )
        self.excel_skin.grid(row=1, column=0, padx=0, pady=0, sticky="")

        # 오른쪽 로그
        # create textbox
        self.textbox = CTkTextbox(self, width=600)
        self.textbox.grid(
            row=0, column=1, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew"
        )

        # self.radio_var = tkinter.IntVar(value=0)
        # self.label_radio_group = CTkLabel(
        #     master=self.radiobutton_frame, text="CTkRadioButton Group:"
        # )
        # self.label_radio_group.grid(
        #     row=0, column=2, columnspan=1, padx=10, pady=10, sticky=""
        # )
        # self.radio_button_1 = CTkRadioButton(
        #     master=self.radiobutton_frame, variable=self.radio_var, value=0
        # )
        # self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        # self.radio_button_2 = CTkRadioButton(
        #     master=self.radiobutton_frame, variable=self.radio_var, value=1
        # )
        # self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        # self.radio_button_3 = CTkRadioButton(
        #     master=self.radiobutton_frame, variable=self.radio_var, value=2
        # )
        # self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        self.textbox.insert(
            "0.0",
            "크롤링을 시작합니다.\n\n"
            + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n"
            * 20,
        )

        self.textbox.insert(index=10.0, text="야 서강준\n서장준")


if __name__ == "__main__":
    app = App()
    app.mainloop()
