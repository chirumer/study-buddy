import tkinter
from PIL import ImageTk, Image
import random


def crop_center_align(img, width, height):

    img_w, img_h = img.size

    img = img.crop((img_w/2 - width/2,
                    img_h/2 - height/2,
                    img_w/2 + width/2,
                    img_h/2 + height/2))
    return img


def resize_to_fit(img, width, height):

    img_w, img_h = img.size
    img_aspct = img_w / img_h

    needed_width_w = width - img_w
    needed_width_h = int((height - img_h) * img_aspct)

    new_width = (needed_width_w if needed_width_w < needed_width_h else
                 needed_width_h) + img_w
    new_height = int(new_width//img_aspct)

    img = img.resize((new_width, new_height), Image.ANTIALIAS)

    return img


def resize_to_spill(img, width, height):

    img_w, img_h = img.size
    img_aspct = img_w / img_h

    needed_width_w = width - img_w
    needed_width_h = int((height - img_h) * img_aspct)

    new_width = (needed_width_w if needed_width_w > needed_width_h else
                 needed_width_h) + img_w
    new_height = int(new_width//img_aspct)

    img = img.resize((new_width, new_height), Image.ANTIALIAS)

    return img


def popup_message(title, msg):
    popup = tkinter.Tk()
    popup.title(title)
    label = tkinter.Label(popup, text=msg, wraplength=400, justify='center')
    label.pack(side="top", fill="x", pady=10)
    B1 = tkinter.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def fun_fact(event):

    facts_file_name = 'assets/facts.txt'
    n_lines = 3080

    random_line = random.randrange(0, n_lines)

    facts_file = open(facts_file_name)

    for i in range(random_line):
        facts_file.readline()

    popup_message('Fun Fact', facts_file.readline())
