from PIL import ImageGrab, ImageOps
import pyautogui
from numpy import *
import time


class DinoBot:
    def __init__(self, replaybtn, dino):
        self.replaybtn = replaybtn
        self.dino = dino

    def restartgame(self):
        pyautogui.click(self.replaybtn)

    def jump(self):
        pyautogui.keyDown('space')
        time.sleep(0.05)
        pyautogui.keyUp('space')

    def grabimage(self):
        box = (self.dino[0] + 35, self.dino[1], self.dino[0] + 75, self.dino[1] + 30)
        image = ImageGrab.grab(box)
        grayImage = ImageOps.grayscale(image)
        a = array(grayImage.getcolors())
        return a.sum()

    def start(self):
        self.restartgame()
        while True:
            if self.grabimage() != 1447:
                self.jump()


def main():
    bot = DinoBot((270, 405), (139, 410))
    bot.start()


if __name__ == '__main__':
    main()