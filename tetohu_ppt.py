import os
import sys
import webbrowser
from tkinter import ttk, Tk, PhotoImage, filedialog
from PyQt5 import QtWidgets, QtCore, QtGui
from PIL import Image, ImageDraw, ImageTk, ImageGrab
import tempfile
import cv2
import numpy as np

# テト譜の仕様→https://docs.google.com/presentation/d/1V4PNyt41to81phK9u0iXnIkAfp-nV3g3xcl7c5qW-FI/edit


def imagetotetohu(orgimg):
    img = Image.open(orgimg)
    img = img.convert("RGB")
    width, height = img.size
    draw = ImageDraw.Draw(img)
    square_width = width/10
    square_height = height/20
    URL = 'http://fumen.zui.jp/?v115@'
    tetohuconvert = [['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'], ['K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T'], ['U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd'], [
        'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n'], ['o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x'], ['y', 'z', '0', '1', '2', '3', '4', '5', '6', '7'], ['8', '9', '+', '/']]
    tetohu = [8, 29]

    def colorjudge(colorlist):  # そのマスにミノがあるかどうか判定
        colorlist.sort()
        if (colorlist[2]-70 > colorlist[1] or colorlist[1]-70 > colorlist[0]):
            return True
        elif(sum(colorlist) > 600 and sum(colorlist)-colorlist[1]*3 < 10):
            return True
        else:
            return False
    # テト譜を生成する時にループ内で使用する関数

    def maketetohu(r, g, b):
        tetohulen = len(tetohu)
        colorlist = [r, g, b]
        if colorjudge(colorlist) == True:
            # ミノがあると判定したとき
            if tetohu[tetohulen-2] == 16:
                tetohu[tetohulen-1] += 1
            else:
                tetohu.append(16)
                tetohu.append(0)
        else:
            # ミノがないと判定したとき
            if tetohu[tetohulen-2] == 8:
                tetohu[tetohulen-1] += 1
            else:
                tetohu.append(8)
                tetohu.append(0)

    for i in range(20):
        for j in range(10):
            r, g, b = img.getpixel(
                (j*square_width+int(square_height/2), i*square_height+int(square_height/2)))
            maketetohu(r, g, b)
            # 色を取得した地点に点を打つ(デバッグ用)
            draw.point([round(j * square_width + square_height / 2),
                        round(i * square_height + square_height / 2)], fill=(255, 0, 0))
    # 点を打った画像を保存(デバッグ用)
    imgname = 'grided.png'
    img.save(imgname, 'PNG')
    while len(tetohu) > 1:
        a = tetohu.pop(0)
        b = tetohu.pop(0)  # フィールドの構成#1の一番下の形を作る
        c = a*240+b  # ここから上の形を作るために逆算していく
        a = c % 64
        b = int(c/64)  # (a,b)の形が#1の一番上と同じ形式になっているはず
        URL += tetohuconvert[int(a/10)][a % 10] + \
            tetohuconvert[int(b/10)][b % 10]
    webbrowser.open(URL)


root = Tk()
root.title('テト譜生成')


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle("")
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

        print("Capture the screen...")
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor("black"), 1))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.end = event.pos()
        self.close()

        global x1, y1, x2, y2
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())
        updatelabel1()


frame1 = ttk.Frame(root, height=800, width=500)
frame1.grid(row=0, column=0)

label1 = ttk.Label(frame1)
label1.grid(row=1, column=0, columnspan=5)


def updatelabel1():
    # 画面更新処理
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    imgname = tempdir.name+"/capture.png"
    img.save(imgname)
    photoim = PhotoImage(file=imgname)
    label1.configure(image=photoim)
    label1.image = photoim
    label1.imagename = imgname


def button1():
    # 画面キャプチャ処理
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    app.exec_()
    button4["state"] = "active"
    button3["state"] = "active"


button1 = ttk.Button(frame1, text="画面キャプチャ", command=button1)
button1.grid(row=0, column=0)


def button4():
    # 画像更新処理
    updatelabel1()


button4 = ttk.Button(frame1, text="画面更新", command=button4, state="disable")
button4.grid(row=0, column=1)


def button2():
    # ファイルから画像を開く処理
    fTyp = [("Image Files", ('.jpg', '.png'))]
    iDir = os.path.abspath(os.path.dirname(__file__))
    filepath = filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
    if filepath[-4:] == '.jpg' or filepath[-4:] == '.png':
        # 画面更新ボタンを無効化してテト譜生成ボタンを有効化
        button4["state"] = "disable"
        button3["state"] = "active"
        # label1の画像を開いた画像で更新
        img = Image.open(filepath)
        imgname = tempdir.name+"/image.png"
        img.save(imgname, "PNG")
        photoim = PhotoImage(file=imgname)
        label1.configure(image=photoim)
        label1.image = photoim
        label1.imagename = imgname


button2 = ttk.Button(frame1, text="ファイルから開く", command=button2)
button2.grid(row=0, column=2)


def button3():
    imagetotetohu(label1.imagename)


button3 = ttk.Button(frame1, text="テト譜生成", command=button3, state="disable")
button3.grid(row=0, column=3)
tempdir = tempfile.TemporaryDirectory()
root.mainloop()
