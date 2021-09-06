import tkinter
from PIL import ImageTk, Image
from PIL import ImageFilter
import random


class Base_window():

    def __init__(self, parameters):

        self.parameters = parameters

        self.root = tkinter.Tk()
        self.root.geometry(f"{parameters['window_width']}x{parameters['window_height']}")
        self.root.title(parameters['window_title'])

        self.canvas = tkinter.Canvas(self.root, width=parameters['window_width'],
                                     height=parameters['window_height'], highlightthickness=0)
        self.canvas.place(x=0, y=0, relheight=1, relwidth=1)

        self.background_img = self._load_background()
        self.canvas.create_image(0, 0, image=self.background_img, anchor=tkinter.NW)

        self.mascot_images, self.mascot_ids = self._load_mascot()
        self.current_frame = 0
        self.canvas.itemconfigure(self.mascot_ids[self.current_frame], state='normal')
        self.root.after(parameters['MILLISEC_PER_FRAME'], self._update_mascot)

        self.root.mainloop()


    def _resize_background(self, background_img):

        width = self.parameters['window_width']
        height = self.parameters['window_height']

        background_img = resize_to_spill(background_img, width, height)
        img_w, img_h = background_img.size
        background_img = background_img.crop((img_w/2 - width/2,
                                              img_h/2 - height/2,
                                              img_w/2 + width/2,
                                              img_h/2 + height/2))
        return background_img


    def _load_background(self):

        background_img = Image.open(self.parameters['background_path'])
        background_img = background_img.filter(ImageFilter.BLUR)
        background_img = self._resize_background(background_img)
        background_img = ImageTk.PhotoImage(background_img)

        return background_img


    def _load_mascot(self):

        mascot_images = []
        mascot_ids = []

        window_width = self.parameters['window_width']
        window_height = self.parameters['window_height']

        mascot_frames = Image.open(self.parameters['mascot_path'])

        for frame in range(mascot_frames.n_frames):

            mascot_frames.seek(frame)

            mascot_img = resize_to_fit(mascot_frames, int(window_width//2), window_height)
            mascot_img = mascot_img.convert('RGBA')

            mascot_img = ImageTk.PhotoImage(mascot_img)
            mascot_images.append(mascot_img)
            
            mascot_id = self.canvas.create_image(window_width/2, 0, image=mascot_img, anchor=tkinter.NW)
            mascot_ids.append(mascot_id)

            self.canvas.itemconfigure(mascot_id, state='hidden')
            self.canvas.tag_bind(mascot_id, '<Button-1>', fun_fact)

        return mascot_images, mascot_ids


    def _update_mascot(self):
        
        self.canvas.itemconfigure(self.mascot_ids[self.current_frame], state='hidden')
        self.current_frame += 1
        if self.current_frame >= len(self.mascot_ids):
            self.current_frame = 0
        self.canvas.itemconfigure(self.mascot_ids[self.current_frame], state='normal')
        self.root.after(self.parameters['MILLISEC_PER_FRAME'], self._update_mascot)



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

    facts_file_name = 'facts.txt'
    n_lines = 3080

    random_line = random.randrange(0, n_lines)

    facts_file = open(facts_file_name)

    for i in range(random_line):
        facts_file.readline()

    popup_message('Fun Fact', facts_file.readline())
