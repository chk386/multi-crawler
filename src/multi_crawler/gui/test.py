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
        self.grid_columnconfigure((1), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # 왼쪽-상단 Frame
        self.left_top_frame = CTkFrame(self, corner_radius=0)
        self.left_top_frame.grid(
            row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nwe"
        )

        self.left_top_frame.grid_columnconfigure((0, 1), weight=1)
        self.left_top_frame.grid_rowconfigure((1, 2), weight=1)
        self.config_label = CTkLabel(
            self.left_top_frame,
            text="Configuration",
            font=CTkFont(size=20, weight="bold"),
        )

        self.config_label.grid(row=0, column=0, columnspan=2, padx=0, pady=10)

        switch = CTkSwitch(master=self.left_top_frame, text="headless")
        switch.grid(row=1, column=0, padx=(50, 0), pady=(20, 0), sticky="w")

        self.slider_1 = CTkSlider(self.left_top_frame, from_=0, to=1, number_of_steps=5)
        self.slider_1.grid(row=2, column=0, padx=(40, 40), pady=(20, 20), sticky="w")

        # # 왼쪽-중단 Frame
        self.left_middle_frame = CTkFrame(self, corner_radius=0)
        self.left_middle_frame.grid(
            row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="ew"
        )
        self.left_middle_frame.grid_rowconfigure((0, 1, 2, 4), weight=1)

        self.saved_label = CTkLabel(
            self.left_middle_frame,
            text="Saved list",
            font=CTkFont(size=20, weight="bold"),
        )

        self.saved_label.grid(row=0, column=0, padx=0, pady=0)

        self.skin_entry = CTkEntry(
            self.left_middle_frame,
            textvariable=tkinter.StringVar(value="skin list - 3 count"),
            state="readonly",
        )
        self.skin_entry.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="ew")

        self.agency_entry = CTkEntry(
            self.left_middle_frame,
            textvariable=tkinter.StringVar(value="agency list - 360 count"),
            state="readonly",
        )
        self.agency_entry.grid(row=2, column=0, padx=(20, 0), pady=(20, 0), sticky="ew")

        self.agency_entry = CTkEntry(
            self.left_middle_frame,
            textvariable=tkinter.StringVar(value="apps list - 360 count"),
            state="readonly",
        )
        self.agency_entry.grid(row=3, column=0, padx=(20, 0), pady=(20, 0), sticky="ew")

        # 왼쪽-하단 Frame
        self.left_bottom_frame = CTkFrame(self, width=140, corner_radius=0)
        self.left_bottom_frame.grid(
            row=2, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew"
        )
        self.left_middle_frame.grid_rowconfigure(2, weight=1)

        self.download_label = CTkLabel(
            self.left_bottom_frame,
            text="Saved list",
            font=CTkFont(size=20, weight="bold"),
        )

        self.download_label.grid(row=0, column=0, padx=0, pady=0)

        # 오른쪽 Textbox
        self.textbox = CTkTextbox(master=self, width=250)
        self.textbox.grid(
            row=0, column=1, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew"
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()
