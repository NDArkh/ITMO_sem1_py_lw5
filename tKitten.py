import tkinter as tk
from PIL import ImageTk
from urllib.request import urlopen
from json import loads


def get_cat_url() -> str:
    return loads(urlopen('https://aws.random.cat/meow').read())['file']


def another_one():
    global bg_label

    try:
        data = urlopen(get_cat_url())
        image = ImageTk.PhotoImage(data=data.read())
        bg_label.image = image
        bg_label['image'] = bg_label.image
    except:
        pass


if __name__ == '__main__':
    wdw = tk.Tk()
    wdw.title("tKitten")
    wdw.geometry(f'800x800')
    bg_label = tk.Label()
    bg_label.place(x=0, y=50)
    tk.Button(wdw, text='NEXT', font=('Consolas', 14), command=another_one, width=50)\
        .pack(side='top')

    wdw.mainloop()
