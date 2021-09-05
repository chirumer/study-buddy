import tkinter
from PIL import ImageTk, Image
from PIL import ImageFilter #


def resize_background(background_img, window_width, window_height):
    background_img = resize_to_spill(background_img, window_width, window_height)
    img_w, img_h = background_img.size
    background_img = background_img.crop((img_w/2 - window_width/2,
                                          img_h/2 - window_height/2,
                                          img_w/2 + window_width/2,
                                          img_h/2 + window_height/2))
    return background_img


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


def get_username():

    # constants
    window_width = 1000
    window_height = 500
    aspect_ratio = window_width/window_height
        # later: handle user resizes

    # create window
    root = tkinter.Tk()
    root.geometry(f'{window_width}x{window_height}')
    root.title('Study Buddy')

    # create canvas
    canvas = tkinter.Canvas(root, width=window_width, height=window_height, highlightthickness=0)
    canvas.place(x=0, y=0, relheight=1, relwidth=1)

    # load background image for window
    background_img = Image.open('background.jpg')
    background_img = background_img.filter(ImageFilter.BLUR)

    # resize and crop image to fit window
    background_img = resize_background(background_img, window_width, window_height)

    # insert background image to window
    background_img = ImageTk.PhotoImage(background_img)
    canvas.create_image(0, 0, image=background_img, anchor=tkinter.NW)

    # load mascot image
    mascot_img = Image.open('mascot.gif')
    mascot_img = mascot_img.convert('RGBA')
    mascot_img = mascot_img.filter(ImageFilter.BLUR)

    # resize image
    mascot_img = resize_to_fit(mascot_img, int(window_width//2), window_height)

    # insert mascot image to window
    mascot_img = ImageTk.PhotoImage(mascot_img)
    mascot = canvas.create_image(window_width/2, 0, image=mascot_img, anchor=tkinter.NW)

    canvas.tag_bind(mascot, '<Button-1>', lambda e: print(e.x, e.y))
        # later: identify whether mascot was clicked

    root.mainloop()


username = get_username()
    # later: change to user authentication page
