from PIL import Image,ImageDraw
#テト譜の仕様→https://docs.google.com/presentation/d/1V4PNyt41to81phK9u0iXnIkAfp-nV3g3xcl7c5qW-FI/edit
img = Image.open('original.png')
img = img.convert("RGB")
width, height = img.size
draw = ImageDraw.Draw(img)
square_width = int(width/10)
square_height = int(height/20)
URL = 'http://fumen.zui.jp/?v115@'
tetohuconvert = [['A','B','C','D','E','F','G','H','I','J'],['K','L','M','N','O','P','Q','R','S','T'],['U','V','W','X','Y','Z','a','b','c','d'],['e','f','g','h','i','j','k','l','m','n'],['o','p','q','r','s','t','u','v','w','x'],['y','z','0','1','2','3','4','5','6','7'],['8','9','+','/']]
tetohu = [8,29]
def maketetohu(r,g,b):
    tetohulen = len(tetohu)
    colorlist = [r,g,b]
    colorlist.sort()
    if colorlist[2]-30<colorlist[1] and colorlist[1]-30<colorlist[0]:
        if tetohu[tetohulen-2] == 8:
            tetohu[tetohulen-1] += 1
        else:
            tetohu.append(8)
            tetohu.append(0)
    else:
        if tetohu[tetohulen-2] == 16:
            tetohu[tetohulen-1] += 1
        else:
            tetohu.append(16)
            tetohu.append(0)

for i in range(20):
    for j in range(10):
        r,g,b = img.getpixel((j*square_width+int(square_height/2),i*square_height+int(square_height/2)))
        maketetohu(r,g,b)
        draw.point([j*square_width+int(square_height/2),i*square_height+int(square_height/2)],fill=(255,0,0))
img.save('original_grided.png','PNG')
while len(tetohu)>1:
    a = tetohu.pop(0)
    b = tetohu.pop(0)#フィールドの構成#1の一番下の形を作る
    c = a*240+b#ここから上の形を作るために逆算していく
    a = c%64
    b = int(c/64)#(a,b)の形が#1の一番上と同じ形式になっているはず
    URL += tetohuconvert[int(a/10)][a%10]+tetohuconvert[int(b/10)][b%10]
print(URL)