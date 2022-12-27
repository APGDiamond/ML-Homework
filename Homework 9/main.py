import pygame as pg
from PIL import Image, ImageEnhance
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

pg.init()
sc = pg.display.set_mode((1000, 700))
sc.fill('white')
pg.display.update()

while True:
    for i in pg.event.get():
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 3:
                pg.image.save(sc, 'picture.jpg')
                image = Image.open('picture.jpg')
                enhancer = ImageEnhance.Contrast(image)
                img = enhancer.enhance(2)
                thresh = 200
                fn = lambda x: 255 if x > thresh else 0
                res = img.convert('L').point(fn, mode='1')
                text = pytesseract.image_to_string(res, lang='eng',
                                                   config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
                print(text)
            if i.button == 2:
                sc.fill('white')
                pg.display.update()
    if True:
        cursor = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if click[0]:
            pg.draw.circle(sc, 'black', (cursor[0], cursor[1]), 10)
        pg.display.update()
