# @Author  : ShiRui
from PIL import Image
import hashlib
import os
import math


# Python 类实现向量空间
class ConversionVector:
    def magnitude(self, concordance):
        total = 0
        for word, count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    # 上面这个函数是构造向量空间，concordance是一个字典，sqrt是开平方。

    def relation(self, concordance1, concordance2):
        relevance = 0
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))

    # relation是计算矢量之间的值，意思就是word在concordance1中又在concordance2中，word是它们两个的交集。

    def buildVector(self, img):
        d1 = {}
        count = 0
        for i in img.getdata():  # 说明一下'getdata'方法是返回一个图像内容的像素值序列
            d1[count] = i
            count += 1
        return d1  # d1中每个键值对就是一个对应的像素序列

    # 将图像转换为矢量值。

    def run(self):

        iconset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                   'j', 'k',
                   'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        imageset = []

        for letter in iconset:
            for img in os.listdir('./iconset/iconset/%s/' % (letter)):  # 这一步是打开文件夹
                temp = []
                if img != "Thumbs.db" and img != ".DS_Store":  # 排除不是训练集的文件
                    temp.append(conversionvector.buildVector(
                        Image.open("./iconset/iconset/%s/%s" % (letter, img))))  # 这一步是打开了图片
                imageset.append({letter: temp})  # 将'iconset'中的每个元素对应训练集中的照片

        img1 = Image.open("./examples/examples/0q3tje.gif")  # 打开图片
        img2 = Image.new("P", img1.size, 255)  # 创建一个和img1一样的画布，背景色是白色
        img1.convert("P")  # 把图片转换成8位像素的模式
        temp = {}

        for x in range(img1.size[1]):
            for y in range(img1.size[0]):  # size[1]或则size[0]表示对应的颜色的像素数量
                pix = img1.getpixel((y, x))  # 获取像素值，ps：'getpixel'中只能传值或则元祖
                temp[pix] = pix  # 将键值对存储起来
                if pix == 220 or pix == 227:  # 找到红色或则灰色，因为红色对应的像素值是220，灰色是227.
                    img2.putpixel((y, x), 0)  # 'putpixel'是设置像素值，背景色是黑色

        inletter = False
        foundletter = False
        start = 0
        end = 0

        letters = []

        for y in range(img2.size[0]):
            for x in range(img2.size[1]):
                pix = img2.getpixel((y, x))
                if pix != 255:
                    inletter = True  # 我们知道255是白色，img2是黑白的，如果不是255，表示我们已经进去了字符。

            if foundletter == False and inletter == True:  # 表示已经进入图片，但是没有找到字符
                foundletter = True
                start = y

            if foundletter == True and inletter == False:  # 找到字符，但没进入图片，表示字符查找完成。
                foundletter = False
                end = y
                letters.append((start, end))

            inletter = False  # 清空，一次循环之后还原。

        count = 0
        for letter in letters:
            m = hashlib.md5()
            img3 = img2.crop((letter[0], 0, letter[1], img2.size[1]))

            guess = []

            for image in imageset:
                for x, y in image.items():
                    if len(y) != 0:
                        guess.append((conversionvector.relation(y[0], conversionvector.buildVector(img3)), x))

            guess.sort(reverse=True)
            print("", guess[0])
            count += 1

            # 将解析出来的字母打印出来。


if __name__ == "__main__":

    conversionvector = ConversionVector()  # 实例化对象
    conversionvector.run()  # 调用实例中的方法


# 训练库链接：https://pan.baidu.com/s/1Oc3vbJYzaldt_8RF-t3tFQ 密码：61ys
# 验证码图片：https://pan.baidu.com/s/13aYAjXUzAGMMyF7D-mmamA 密码：eh10
#GitHub：https://github.com/ruibababa/Verifying-code-cracking
