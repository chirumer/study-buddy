from base_window import Base_window
from helpers import resize_to_fit, resize_to_spill, popup_message, crop_center_align
import server_interface
import tkinter
from PIL import ImageTk, Image, ImageFont, ImageDraw

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

    def cleanup():
        pass

    def create_text_image(canvas, text, index, txt_imgs, txt_ids):

        img = Image.new('RGBA', (400, 80), (0, 255, 0, 0))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('montserrat.otf', 25)

        if draw.textsize(text, font=font)[0] > 300:
            while draw.textsize(text + '..', font=font)[0] > 300:
                text = text[:-1]
            text += '..'

        w, h = draw.textsize(text, font=font)
        draw.text((400/2-w/2, 0), text, (255, 255, 255), font=font)

        img = ImageTk.PhotoImage(img)
        txt_imgs.append(img)

        if index == 0:
            txt_ids.append(canvas.create_image(100, 60, image=img, anchor=tkinter.NW))
        elif index == 1:
            txt_ids.append(canvas.create_image(100, 160, image=img, anchor=tkinter.NW))
        elif index == 2:
            txt_ids.append(canvas.create_image(100, 260, image=img, anchor=tkinter.NW))
        elif index == 3:
            txt_ids.append(canvas.create_image(100, 360, image=img, anchor=tkinter.NW))

        return img

    tile_img = Image.open('tile.jpeg')
    tile_img = resize_to_spill(tile_img, 400, 80)
    tile_img = crop_center_align(tile_img, 400, 80)
    tile_img = ImageTk.PhotoImage(tile_img)
    temp_assets.append(tile_img)

    join_img = tkinter.PhotoImage(file='join_group.png')
    temp_assets.append(join_img)

    details_img = tkinter.PhotoImage(file='details.png')
    temp_assets.append(details_img)

    join_img = tkinter.PhotoImage(file='join_group.png')
    temp_assets.append(join_img)

    already_img = tkinter.PhotoImage(file='already_joined.png')
    temp_assets.append(already_img)

    empty_img = tkinter.PhotoImage(file='empty.png')
    temp_assets.append(empty_img)

    
    tiles = []
    tiles.append(base.canvas.create_image(100, 60, image=tile_img, anchor=tkinter.NW))
    tiles.append(base.canvas.create_image(100, 160, image=tile_img, anchor=tkinter.NW))
    tiles.append(base.canvas.create_image(100, 260, image=tile_img, anchor=tkinter.NW))
    tiles.append(base.canvas.create_image(100, 360, image=tile_img, anchor=tkinter.NW))

    detail_btns = []
    detail_btns.append(base.canvas.create_image(100+20, 60+42, image=details_img, anchor=tkinter.NW))
    detail_btns.append(base.canvas.create_image(100+20, 160+42, image=details_img, anchor=tkinter.NW))
    detail_btns.append(base.canvas.create_image(100+20, 260+42, image=details_img, anchor=tkinter.NW))
    detail_btns.append(base.canvas.create_image(100+20, 360+42, image=details_img, anchor=tkinter.NW))

    join_btns = []
    join_btns.append(base.canvas.create_image(100+270, 60+42, image=join_img, anchor=tkinter.NW))
    join_btns.append(base.canvas.create_image(100+270, 160+42, image=join_img, anchor=tkinter.NW))
    join_btns.append(base.canvas.create_image(100+270, 260+42, image=join_img, anchor=tkinter.NW))
    join_btns.append(base.canvas.create_image(100+270, 360+42, image=join_img, anchor=tkinter.NW))

    joined_txts = []
    joined_txts.append(base.canvas.create_image(100+190, 60+42, image=already_img, anchor=tkinter.NW))
    joined_txts.append(base.canvas.create_image(100+190, 160+42, image=already_img, anchor=tkinter.NW))
    joined_txts.append(base.canvas.create_image(100+190, 260+42, image=already_img, anchor=tkinter.NW))
    joined_txts.append(base.canvas.create_image(100+190, 360+42, image=already_img, anchor=tkinter.NW))

    empty_txts = []
    empty_txts.append(base.canvas.create_image(100+110, 60+10, image=empty_img, anchor=tkinter.NW))
    empty_txts.append(base.canvas.create_image(100+110, 160+10, image=empty_img, anchor=tkinter.NW))
    empty_txts.append(base.canvas.create_image(100+110, 260+10, image=empty_img, anchor=tkinter.NW))
    empty_txts.append(base.canvas.create_image(100+110, 360+10, image=empty_img, anchor=tkinter.NW))

    txt_imgs = []
    temp_assets.append(txt_imgs)
    txt_ids = []

    text = 'monkey adventures and donkey dancing'
    create_text_image(base.canvas, text, 0, txt_imgs, txt_ids)
    create_text_image(base.canvas, text, 1, txt_imgs, txt_ids)
    create_text_image(base.canvas, text, 2, txt_imgs, txt_ids)
    create_text_image(base.canvas, text, 3, txt_imgs, txt_ids)

    right_img = tkinter.PhotoImage(file='right.png')
    temp_assets.append(right_img)
    right_btn = base.canvas.create_image(510, 250, image=right_img, anchor=tkinter.NW)

    left_img = tkinter.PhotoImage(file='left.png')
    temp_assets.append(left_img)
    left_btn = base.canvas.create_image(30, 250, image=left_img, anchor=tkinter.NW)

    back_img = tkinter.PhotoImage(file='back.png')
    temp_assets.append(back_img)
    back_btn = base.canvas.create_image(900, 20, image=back_img, anchor=tkinter.NW)

    def clicked_back(event):
        cleanup()
        category_selection_page(base, temp_assets)

    base.canvas.tag_bind(back_btn, '<Button-1>', clicked_back)


if __name__ == '__main__':

    temp_assets = []

    base = Base_window(parameters)
    base.root.after(0, username_page, base, temp_assets)
    base.root.mainloop()
