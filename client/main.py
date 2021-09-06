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

    def cleanup():
        temp_assets.clear()
        base.canvas.delete(username_txt)
        base.canvas.delete(go_btn)
        entry.destroy()

    def is_valid(username):
        if not username:
            return "Empty username"
        return True

    username_img = tkinter.PhotoImage(file='username.png')
    temp_assets.append(username_img)
    username_txt = base.canvas.create_image(130, 180, image=username_img, anchor=tkinter.NW)

    entry = tkinter.Entry(base.canvas, width=17, font=('default', 15))
    entry.place(x=145, y=240)

    go_img = tkinter.PhotoImage(file='lets_go.png')
    temp_assets.append(go_img)
    go_btn = base.canvas.create_image(140, 285, image=go_img, anchor=tkinter.NW)

    def submit(event):
        username = entry.get().strip()

        if is_valid(username) != True:
            popup_message('Alert!', 
                          f'Invalid username.\nReason: {is_valid(username)}')
            return
        cleanup()
        user_login(base, username, temp_assets)

    base.canvas.tag_bind(go_btn, '<Button-1>', submit)


def user_login(base, username, temp_assets):

    is_success = server_interface.login(username)

    if not is_success:
            # later: implement error handling
        poppup_message('Alert!', 'socket error')
        return

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

    def cleanup():
        temp_assets.clear()
        title_entry.destroy()
        tags_entry.destroy()
        goals_entry.destroy()
        base.canvas.delete(book_title_txt)
        base.canvas.delete(tags_entry_txt)
        base.canvas.delete(goals_txt)
        base.canvas.delete(create_btn)
        base.canvas.delete(back_btn)

    def is_valid(title, tags, goals):
        if not title:
            return "Empty title field!"
        elif not tags:
            return "Empty tags field!"
        elif not goals:
            return "Empty goals field!"
        return True

    book_title_img = tkinter.PhotoImage(file='book_title.png')
    temp_assets.append(book_title_img)
    book_title_txt = base.canvas.create_image(80, 30, image=book_title_img, anchor=tkinter.NW)

    title_entry = tkinter.Entry(base.canvas, width=17, font=('default', 15))
    title_entry.place(x=90, y=90)

    tags_entry_img = tkinter.PhotoImage(file='tags.png')
    temp_assets.append(tags_entry_img)
    tags_entry_txt= base.canvas.create_image(80, 150, image=tags_entry_img, anchor=tkinter.NW)

    tags_entry = tkinter.Text(base.canvas, width=17, height=2, font=('default', 15))
    tags_entry.place(x=90, y=205)

    goals_img = tkinter.PhotoImage(file='group_goals.png')
    temp_assets.append(goals_img)
    goals_txt = base.canvas.create_image(80, 280, image=goals_img, anchor=tkinter.NW)

    goals_entry = tkinter.Text(base.canvas, width=20, height=5, font=('default', 15))
    goals_entry.place(x=90, y=340)

    create_img = tkinter.PhotoImage(file='study_create.png')
    temp_assets.append(create_img)
    create_btn = base.canvas.create_image(400, 190, image=create_img, anchor=tkinter.NW)

    def clicked_create(event):
        title = title_entry.get().strip()
        tags = tags_entry.get('1.0', tkinter.END).strip()
        goals = goals_entry.get('1.0', tkinter.END).strip()

        if is_valid(title, tags, goals) != True:
            popup_message('Alert!',
                          f'Error parsing fields.\nReason: {is_valid(title, tags, goals)}')
            return

        cleanup()
            # later: mascot notifies success

        is_success = server_interface.create_page(title, tags, goals)
        if not is_success:
                # later: error handling
            poppup_message('Alert!', 'socket error')
            return

        category_selection_page(base, temp_assets)

    base.canvas.tag_bind(create_btn, '<Button-1>', clicked_create)

    back_img = tkinter.PhotoImage(file='back.png')
    temp_assets.append(back_img)
    back_btn = base.canvas.create_image(900, 20, image=back_img, anchor=tkinter.NW)

    def clicked_back(event):
        cleanup()
        category_selection_page(base, temp_assets)

    base.canvas.tag_bind(back_btn, '<Button-1>', clicked_back)



def join_page(base, temp_assets):
    print('join page')



if __name__ == '__main__':

    temp_assets = []

    base = Base_window(parameters)
    base.root.after(0, username_page, base, temp_assets)
    base.root.mainloop()
