import random
import time
import keyboard
import numpy as np
import pygame

flag = True

pygame.init()
size = (400, 400)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("2048 Game")
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
font_small = pygame.font.SysFont('Arial', 20)
font_large = pygame.font.SysFont('Arial', 50)



tahta = np.zeros((4, 4), dtype=int)
tahta[random.randint(0, 3)][random.randint(0, 3)] = 2


def draw_board():
    global score

    cell_size = 90
    cell_margin = 10
    for i in range(4):
        for j in range(4):
            cell_value = tahta[i][j]
            x = j * (cell_size + cell_margin) + cell_margin
            y = i * (cell_size + cell_margin) + cell_margin
            pygame.draw.rect(screen, white, [x, y, cell_size, cell_size])
            if cell_value != 0:
                font_color = black
                font = font_large
                text = font.render(str(cell_value), True, font_color)
                text_rect = text.get_rect()
                text_rect.centerx = x + cell_size/2
                text_rect.centery = y + cell_size/2
                screen.blit(text, text_rect)

            if flag:
                score = np.sum(tahta)

            score_text = pygame.font.SysFont('Arial', 30).render('Puan: ' + str(score), True, black)
            score_rect = score_text.get_rect()
            score_rect.centerx = size[0] / 2
            score_rect.centery = 30
            screen.blit(score_text, score_rect)


def temizle(yon, tahta_fonksiyon):
    if yon == "sag":
        for a in range(4):
            for m in range(4):
                for p in range(3):
                    if tahta_fonksiyon[m][p] != 0 and tahta_fonksiyon[m][p + 1] == 0:
                        tahta_fonksiyon[m][p + 1] = tahta_fonksiyon[m][p]
                        tahta_fonksiyon[m][p] = 0

    elif yon == "sol":
        for a in range(4):
            for m in range(4):
                for p in range(3, 0, -1):
                    if tahta_fonksiyon[m][p] != 0 and tahta_fonksiyon[m][p - 1] == 0:
                        tahta_fonksiyon[m][p - 1] = tahta_fonksiyon[m][p]
                        tahta_fonksiyon[m][p] = 0

    elif yon == "yukari":
        for a in range(4):
            for m in range(3, 0, -1):
                for p in range(4):
                    if tahta_fonksiyon[m][p] != 0 and tahta_fonksiyon[m - 1][p] == 0:
                        tahta_fonksiyon[m - 1][p] = tahta_fonksiyon[m][p]
                        tahta_fonksiyon[m][p] = 0

    elif yon == "asagi":
        for a in range(4):
            for m in range(3):
                for p in range(4):
                    if tahta_fonksiyon[m][p] != 0 and tahta_fonksiyon[m + 1][p] == 0:
                        tahta_fonksiyon[m + 1][p] = tahta_fonksiyon[m][p]
                        tahta_fonksiyon[m][p] = 0
    return tahta_fonksiyon


def random_yerde_olustur():
    global tahta

    iki_mi_dort = random.choice([2, 4])
    olabilir = []
    for i in range(4):
        for a in range(4):
            if tahta[i][a] == 0:
                olabilir.append((i, a))
    tahta[random.choice(olabilir)] = iki_mi_dort


def sag():
    global tahta

    tahta = temizle("sag", tahta)

    for a in range(4):
        for i in range(3, -1, -1):
            if tahta[a][i] == tahta[a][i - 1]:
                tahta[a][i] = tahta[a][i] * 2
                tahta[a][i - 1] = 0

    tahta = temizle("sag", tahta)



def sol():
    global tahta

    tahta = temizle("sol", tahta)

    for a in range(4):
        for i in range(3):
            if tahta[a][i] == tahta[a][i + 1]:
                tahta[a][i] = tahta[a][i] * 2
                tahta[a][i + 1] = 0

    tahta = temizle("sol", tahta)



def yukari():
    global tahta


    tahta = temizle("yukari", tahta)

    for p in range(4):
        for i in range(2, -1, -1):
            if tahta[i][p] == tahta[i + 1][p]:
                tahta[i + 1][p] = tahta[i][p] * 2
                tahta[i][p] = 0

    tahta = temizle("yukari", tahta)



def asagi():
    global tahta

    tahta = temizle("asagi", tahta)

    for p in range(4):
        for i in range(3):
            if tahta[i][p] == tahta[i + 1][p]:
                tahta[i][p] = tahta[i][p] * 2
                tahta[i + 1][p] = 0

    tahta = temizle("asagi", tahta)


def kayip():
    global tahta
    temp = tahta.copy()
    yukari()
    if str(temp) != str(tahta):
        tahta = temp.copy()
        return False
    asagi()
    if str(temp) != str(tahta):
        tahta = temp.copy()
        return False
    sag()
    if str(temp) != str(tahta):
        tahta = temp.copy()
        return False
    sol()
    if str(temp) != str(tahta):
        tahta = temp.copy()
        return False
    return True



while True:
    eski = str(tahta.copy())

    if keyboard.is_pressed("w"):
        (yukari())
    elif keyboard.is_pressed("s"):
        (asagi())
    elif keyboard.is_pressed("a"):
        (sol())
    elif keyboard.is_pressed("d"):
        (sag())

    if str(tahta) != eski:
        random_yerde_olustur()
        print(tahta)
        time.sleep(0.08)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if np.sum(tahta) >= 2048:
        score = "Kazandınız"
        flag = False
    elif kayip():
        score = "Kaybettiniz"
        flag = False

    screen.fill(gray)
    draw_board()
    pygame.display.update()
