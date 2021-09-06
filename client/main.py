from base_window import Base_window, popup_message
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
        temp_assets.clear()
        base.canvas.delete(username_txt)
        base.canvas.delete(go_btn)
        entry.destroy()

        user_login(base, username, temp_assets)

    base.canvas.tag_bind(go_btn, '<Button-1>', submit)


def user_login(base, username, temp_assets):

    is_success = server_interface.login(username)

    if not is_success:
            # later: implement error handling
        pass

    category_selection_page(base, temp_assets)


def category_selection_page(base, temp_assets):

    def cleanup():
        temp_assets.clear()
        base.canvas.delete(existing_btn)
        base.canvas.delete(create_btn)
        base.canvas.delete(join_btn)

    existing_img = tkinter.PhotoImage(file='study_existing.png')
    temp_assets.append(existing_img)
    existing_btn = base.canvas.create_image(130, 90, image=existing_img, anchor=tkinter.NW)

    def clicked_existing(event):
        cleanup()
        existing_page(base, temp_assets)

    base.canvas.tag_bind(existing_btn, '<Button-1>', clicked_existing)

    create_img = tkinter.PhotoImage(file='study_create.png')
    temp_assets.append(create_img)
    create_btn = base.canvas.create_image(147, 220, image=create_img, anchor=tkinter.NW)

    def clicked_create(event):
        cleanup()
        create_page(base, temp_assets)

    base.canvas.tag_bind(create_btn, '<Button-1>', clicked_create)

    join_img = tkinter.PhotoImage(file='study_join.png')
    temp_assets.append(join_img)
    join_btn = base.canvas.create_image(150, 370, image=join_img, anchor=tkinter.NW)

    def clicked_join(event):
        cleanup()
        join_page(base, temp_assets)

    base.canvas.tag_bind(join_btn, '<Button-1>', clicked_join)


def existing_page(base, temp_assets):
    print('existing page')

def create_page(base, temp_assets):
    print('create page')

def join_page(base, temp_assets):
    print('join page')



if __name__ == '__main__':

    temp_assets = []

    base = Base_window(parameters)
    base.root.after(0, username_page, base, temp_assets)
    base.root.mainloop()
