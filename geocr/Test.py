import ttkbootstrap as tkb
import helpers.ImageHelper as ImageHelper
import cv2
from PIL import Image, ImageTk
import pytesseract
from win32api import GetSystemMetrics
import numpy as np

def get_resized_for_display_img(img):
    screen_w, screen_h = GetSystemMetrics(0), GetSystemMetrics(1)
    print("screen size", screen_w, screen_h)
    h, w, channel_nbr = img.shape
    # img get w of screen and adapt h
    h = h * (screen_w / w)
    w = screen_w
    if h > screen_h:  # if img h still too big
        # img get h of screen and adapt w
        w = w * (screen_h / h)
        h = screen_h
    w, h = w * 0.9, h * 0.9  # because you don't want it to be that big, right ?
    w, h = int(w), int(h)  # you need int for the cv2.resize
    return cv2.resize(img, (w, h))

class Test(tkb.Toplevel):
    def __init__(self, parent, db, item):
        super().__init__(parent)
        self.title("Archives")
        self.geometry("1200x800")
        self.transient(parent)
        self.update_idletasks()
        self.grab_set()
        self.DB = db
        self.item = self.DB.search_in_db_by_id(item)[0]
        self.image = cv2.imread(self.item[0])
        self.image = get_resized_for_display_img(self.image)

        self.btn_open = tkb.Button(self, text="Ouvrir", command=self.open_img)
        self.btn_open.pack()

        self.btn_invert = tkb.Button(self, text="Invert", command=self.invert_img)
        self.btn_invert.pack()

        self.btn_binarisation = tkb.Button(self, text="Binarisation", command=self.binarisation_img)
        self.btn_binarisation.pack()
        self.btn_noise = tkb.Button(self, text="noise", command=self.noise_img)
        self.btn_noise.pack()

    def open_img(self):
        cv2.imshow("1921", self.image)

    def grayscale(self):
        return cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def binarisation_img(self):
        self.image = self.grayscale()
        thresh, self.image = cv2.threshold(self.image, 127, 255, cv2.THRESH_BINARY)
        self.noise_img()
        self.open_img()

    def invert_img(self):
        self.image = cv2.bitwise_not(self.image)
        self.open_img()

    def noise_img(self):
        kernel = np.ones((1, 1), np.uint8)
        self.image = cv2.dilate(self.image, kernel, iterations=6)
        kernel = np.ones((1, 1), np.uint8)
        self.image = cv2.erode(self.image, kernel, iterations=1)
        self.image = cv2.morphologyEx(self.image, cv2.MORPH_CLOSE, kernel)
        self.image = cv2.medianBlur(self.image, 1)



