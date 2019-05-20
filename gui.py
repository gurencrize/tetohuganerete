from tkinter import *
from tkinter import ttk
from PIL import ImageGrab

def foo():
    print('Hello')
if __name__ == "__main__":
    root = Tk()
    root.title('テト譜生成')
    frame1 = ttk.Frame(root,height=200,width=300)
    img = PhotoImage(file="dummy.png")
    label2 = ttk.Label(frame1,image=img)
    button1 = ttk.Button(frame1, text='画面取得', command=foo)
    #button2 = ttk.Button(frame1, text='', command=foo)
    button3 = ttk.Button(frame1, text='URLを開く', command=foo)

    frame1.grid(row=0,column=0,sticky=(N,E,S,W))
    label2.grid(row=1,column=1,columnspan=3,sticky=N)
    button1.grid(row=2,column=1,sticky=W)
    #button2.grid(row=2,column=2)
    button3.grid(row=2,column=3,sticky=E)

    for child in frame1.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()