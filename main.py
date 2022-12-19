import tkinter
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont
import os

# ---------------------------- CONSTANTS ------------------------------- #
WATERMARK_TEXT = "Watermark"
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
LIGHT_GREEN = "#E8F3D6"
DARK_BLUE = "#1C658C"
YELLOW = "#f7f5dd"
GREY = "#CFD2CF"
FONT_NAME = "Courier"

# ----------------------------Global Variables---------------------------
file_path = ""
file_name = ""
marked_image = None
save_directory = ""


# ------------------------------Functionalities--------------------------#
def load_image():
    global file_path
    file_path = filedialog.askopenfilename()
    global file_name
    file_name = os.path.basename(file_path)
    file_label.config(text=f"File Path: {file_path}")


def show_image():
    if file_path == "":
        file_label.config(text=f"Load a picture first.")
    else:
        image = Image.open(file_path)
        image.show()


def add_watermark():
    if file_path == "":
        file_label.config(text=f"Load a picture first.")
    else:
        image = Image.open(file_path)
        width, height = image.size
        draw = ImageDraw.Draw(image)

        # create watermark
        text = mark_entry.get()
        font = ImageFont.truetype('arial.ttf', 20)
        # text_width, text_height = draw.textsize(text, font)
        (left, bottom, text_width, text_height) = draw.textbbox(xy=(0, 0), text=text, font=font)

        # calculate the x,y coordinates of the text
        margin = 10
        x = width - text_width - margin
        y = height - text_height - margin

        # draw watermark in the bottom right corner
        draw.text((x, y), text=text, font=font)
        image.show()
        global marked_image
        marked_image = image
        mark_entry.delete(0, "end")


# Save watermarked image
def save():
    if file_name == "":
        file_label.config(text=f"Watermark a picture first.")
    else:
        global save_directory
        save_directory = filedialog.askdirectory()
        prefix = file_name.rsplit('.')[0]
        suffix = file_name.rsplit('.')[1]
        save_path = save_directory + "/" + prefix + "_watermarked" + "." + suffix
        marked_image.save(save_path)


def open_directory():
    if save_directory == "":
        file_label.config(
            text=f"Now this only opens the default directory, you should first watermark and save an image."
        )
    os.startfile(save_directory)


# ---------------------------- UI SETUP ------------------------------- #
window = tkinter.Tk()
window.title("Watermarking")
window.config(pady=50, padx=100, bg=GREY)

heading_label = tkinter.Label(
    text="Watermark An Image of Your Choice",
    bg=GREY, fg=DARK_BLUE, font=(FONT_NAME, 20, "bold")
)
heading_label.grid(column=0, row=0, columnspan=5)

canvas = tkinter.Canvas(width=64, height=64, bg=GREY, highlightthickness=0)
coffee_img = tkinter.PhotoImage(file="images/small_coffee.png")
canvas.create_image(32, 32, image=coffee_img)
canvas.grid(column=0, row=1, columnspan=5, pady=(40, 0))

file_label = tkinter.Label(text="", bg=GREY)
file_label.config(pady=20)
file_label.grid(column=0, row=2, columnspan=5)

mark_label = tkinter.Label(text="Watermark Text:", bg=GREY)
mark_label.config(pady=15)
mark_label.grid(column=0, row=3)

mark_entry = tkinter.Entry(width=32)
mark_entry.grid(column=1, row=3, columnspan=2, pady=(15, 15))
mark_entry.focus()

load_button = tkinter.Button(text="Load Image", command=load_image, width=13)
load_button.grid(column=0, row=4)

show_button = tkinter.Button(text="Show Image", command=show_image, width=11)
show_button.grid(column=1, row=4)

watermark_button = tkinter.Button(text="Add Watermark", command=add_watermark, width=14)
watermark_button.grid(column=3, row=3)

save_button = tkinter.Button(text="Save Watermarked", command=save)
save_button.grid(column=2, row=4)

directory_button = tkinter.Button(text="Open Directory", command=open_directory, width=14)
directory_button.grid(column=3, row=4)

window.mainloop()
