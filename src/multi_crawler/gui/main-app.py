from customtkinter import (
    CTk,
    CTkButton,
    CTkComboBox,
    CTkImage,
    CTkLabel,
    StringVar,
    set_appearance_mode,
    set_default_color_theme,
    CTkEntry,
)
from PIL import Image


def combobox_callback(choice: str):
    print("combobox dropdown clicked:", choice)


if __name__ == "__main__":
    app = CTk()

    set_appearance_mode("dark")
    set_default_color_theme("green")

    app.geometry("1024x768")
    app.title("크롤러")

    img = Image.open("comments.png")

    btn = CTkButton(
        master=app,
        text="에이전시 목록 수집",
        corner_radius=32,
        fg_color="transparent",
        hover_color="#4158D0",
        border_color="#FFCC70",
        border_width=2,
        image=CTkImage(dark_image=img, light_image=img),
    )
    btn.place(relx=0.5, rely=0.5, anchor="center")

    label = CTkLabel(
        master=app, text="Input 텍스트인가?", font=("", 20), text_color="#FFCC70"
    )
    label.place(relx=0.3, rely=0.3, anchor="center")

    # 콤보박스
    combobox_var = StringVar(value="option 2")
    combobox = CTkComboBox(
        app,
        values=["option 1", "option 2"],
        command=combobox_callback,
        variable=combobox_var,
    )
    combobox_var.set("option 2")

    combobox.place(relx=0.1, rely=0.1, anchor="center")

    entry = CTkEntry(app, placeholder_text="인풋박스네?")
    entry.place(relx=0.1, rely=0.2, anchor="center")

    app.mainloop()
