import tkinter
from PIL import ImageTk, Image
from PIL import ImageFilter
import random


MILLISEC_PER_FRAME = 50

root = None 
canvas = None
mascot_images = None
mascots = None
background_img = None


def popup_message(title, msg):
    popup = tkinter.Tk()
    popup.title(title)
    label = tkinter.Label(popup, text=msg, wraplength=400, justify='center')
    label.pack(side="top", fill="x", pady=10)
    B1 = tkinter.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


def fun_fact(event):

    facts_file_name = 'facts.txt'
    n_lines = 3080

    random_line = random.randrange(0, n_lines)

    facts_file = open(facts_file_name)

    for i in range(random_line):
        facts_file.readline()

    popup_message('Fun Fact', facts_file.readline())


def init_window():

    global root, canvas, mascot_images, mascots, background_img

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

    # load mascot animation frames
    mascot_images, mascots = load_mascots(canvas, window_width, window_height)

    # display mascot
    current_frame = 0
    canvas.itemconfigure(mascots[current_frame], state='normal')

    def update_mascot():
        nonlocal current_frame
        canvas.itemconfigure(mascots[current_frame], state='hidden')
        current_frame += 1
        if current_frame >= len(mascots):
            current_frame = 0
        canvas.itemconfigure(mascots[current_frame], state='normal')
        root.after(MILLISEC_PER_FRAME, update_mascot)

    root.after(MILLISEC_PER_FRAME, update_mascot)


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


def load_mascots(canvas, window_width, window_height):

    mascot_images = []
    mascots = []

    # load mascot image
    mascot_frames = Image.open('mascot.gif')

    for frame in range(mascot_frames.n_frames):

        mascot_frames.seek(frame)

        mascot_img = resize_to_fit(mascot_frames, int(window_width//2), window_height)
        mascot_img = mascot_img.convert('RGBA')
        #mascot_img = mascot_img.filter(ImageFilter.BLUR)

        mascot_img = ImageTk.PhotoImage(mascot_img)
        mascot_images.append(mascot_img)
        mascot = canvas.create_image(window_width/2, 0, image=mascot_img, anchor=tkinter.NW)
        mascots.append(mascot)

        canvas.itemconfigure(mascot, state='hidden')

        canvas.tag_bind(mascot, '<Button-1>', fun_fact)
            # later: identify whether mascot was clicked or transparent background

    return mascot_images, mascots

def get_username():

    username = ''

    # define submit action
    def submit(event):
        nonlocal username
        username = entry.get()
        entry.destroy()
        canvas.delete(go_button)
        canvas.delete(username_text)


    # username text
    username_img = tkinter.PhotoImage(file='username.png')
    username_text = canvas.create_image(130, 180, image=username_img, anchor=tkinter.NW)

    # entry
    entry = tkinter.Entry(canvas, width=17, font=("default", 15))
    entry.place(x=145, y=240)

    # go button
    go_img = tkinter.PhotoImage(file='lets_go.png')
    go_button = canvas.create_image(140, 285, image=go_img, anchor=tkinter.NW)
    canvas.tag_bind(go_button, '<Button-1>', submit)


    root.mainloop()
    return username
