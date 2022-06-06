import time
import pygame
from tkinter import *
from tkinter import messagebox

Tk().wm_withdraw()

icon = pygame.image.load('icon.jpg')

pygame.init()
screen = pygame.display.set_mode((850, 150))
pygame.display.set_caption("WARNING!")
font = pygame.font.SysFont("Lucida Console", 20)
label = font.render("YOU DOWNLOADED VIRUS", 1, (12, 140, 0, 1))

pygame.display.set_icon(icon)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            time.sleep(0.10)
            screen = pygame.display.set_mode((850, 150))
            pygame.display.set_caption("IMPORTANT MESSAGE")
            pygame.display.set_icon(icon)
            messagebox.showerror("LOL", "WE ARE ENCRYPTING YOUR FILES")

    screen.fill((0, 0, 0))
    screen.blit(label, (50, 50))
    pygame.display.update()
