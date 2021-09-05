import tkinter
from PIL import ImageTk, Image


def resize_background(background_img, window_width, window_height):
    img_w, img_h = background_img.size
    img_aspct = img_w/img_h
    needed_width_w = window_width - img_w
    needed_width_h = (window_height - img_h) * img_aspct
    new_width = (needed_width_w if needed_width_w > needed_width_h else
                 needed_width_h) + img_w
    new_height = int(new_width//img_aspct)
    background_img = background_img.resize((new_width, new_height), Image.ANTIALIAS)
    img_w, img_h = background_img.size
    background_img = background_img.crop((img_w/2 - window_width/2,
                                          img_h/2 - window_height/2,
                                          img_w/2 + window_width/2,
                                          img_h/2 + window_height/2))
    return background_img


def get_username():

    # constants
    window_width = 1000
    window_height = 500
    aspect_ratio = window_width/window_height
        # later: handle user resizes

    # set dimensions of window
    root = tkinter.Tk()
    root.geometry(f'{window_width}x{window_height}')

    # load background image for window
    background_img = Image.open('background.jpg')

    # resize and crop image to fit window
    background_img = resize_background(background_img, window_width, window_height)

    # insert background image to window
    background_img = ImageTk.PhotoImage(background_img)
    background_label = tkinter.Label(root, image=background_img)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    root.mainloop()


username = get_username()
    # later: change to user authentication page
