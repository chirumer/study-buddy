import tkinter

def get_username():

    window_width = 1000
    window_height = 500
    aspect_ratio = window_width/window_height
        # later: handle user resizes

    root = tkinter.Tk()
    root.geometry(f'{window_width}x{window_height}')

    root.mainloop()

username = get_username()
    # later: change to user authentication page
