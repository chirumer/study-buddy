from base_window import Base_window
import server_interface
import tkinter

parameters = {
    'MILLISEC_PER_FRAME': 50,
    'mascot_path': 'mascot.gif',
    'background_path': 'background.jpg',
    'window_width': 1000,
    'window_height': 500,
    'window_title': 'Study Buddy'
}
parameters['aspect_ratio'] = (parameters['window_width'] /
                              parameters['window_height'])


def username_page(base, temp_assets):

    username_img = tkinter.PhotoImage(file='username.png')
    temp_assets.append(username_img)
    username_txt = base.canvas.create_image(130, 180, image=username_img, anchor=tkinter.NW)

    entry = tkinter.Entry(base.canvas, width=17, font=('default', 15))
    entry.place(x=145, y=240)

    go_img = tkinter.PhotoImage(file='lets_go.png')
    temp_assets.append(go_img)
    go_btn = base.canvas.create_image(140, 285, image=go_img, anchor=tkinter.NW)

    def submit(event):
        username = entry.get()
        temp_assets = []
        base.canvas.delete(username_txt)
        base.canvas.delete(go_btn)
        entry.destroy()

        base.root.after(0, room_selection, username)

    base.canvas.tag_bind(go_btn, '<Button-1>', submit)


def room_selection(username):
    print(username)



if __name__ == '__main__':

    temp_assets = []

    base = Base_window(parameters)
    base.root.after(0, username_page, base, temp_assets)
    base.root.mainloop()
