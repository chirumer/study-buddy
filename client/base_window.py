from helpers import resize_to_fit, resize_to_spill, popup_message, fun_fact, crop_center_align
import tkinter
from PIL import ImageTk, Image
from PIL import ImageFilter


class Base_window():


    def __init__(self, parameters):

        self.parameters = parameters

        self.root = tkinter.Tk()
        self.root.geometry(f"{parameters['window_width']}x{parameters['window_height']}")
        self.root.resizable(False, False)
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


    def _resize_background(self, background_img):

        width = self.parameters['window_width']
        height = self.parameters['window_height']

        background_img = resize_to_spill(background_img, width, height)
        background_img = crop_center_align(background_img, width, height)

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
