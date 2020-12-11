import pygame
import math
import random

# setup display

pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HANGMAN GAME")

# button variables

RADIUS = 20
GAP = 5
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + (RADIUS * 2 + GAP) * (i % 13)
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# fonts

LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# load images

images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)
win1=pygame.image.load("wind.png")
win1=pygame.transform.scale(win1, (800,500))
lose1=pygame.image.load("lose.png")
lose1=pygame.transform.scale(lose1,(800,500))

# game variable

hangman_status = 0
words=[]
with open("resource.txt", "r") as resource:
	lines= resource.readlines()
for l in lines:
    words.append(l.replace("\n",""))
words = [x.upper() for x in words]
word = random.choice(words)
print(word)
guessed = []

# colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (150, 38, 171)
def color():
    a = random.randint(0, 250)
    b = random.randint(0, 250)
    c = random.randint(0, 250)
    return (a, b, c)

def draw():
    win.fill(BACKGROUND)

    # draw title

    text = TITLE_FONT.render("HANGMAN", 1, (88, 0, 0))
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # draw word

    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, (23, 90, 65), (x, y), RADIUS, 3)

            text = LETTER_FONT.render(ltr, 1, color())
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()

# function to draw the winning and losing screen
def display_message(message):
    pygame.time.delay(1000)
    if message=="YOU WON!":
      win.blit(win1, (0, 0))
      pygame.display.update()
    else:
      win.blit(lose1, (0, 0))
      pygame.display.update()
    pygame.time.delay(3000)
def dis_word(mess):
    text = WORD_FONT.render(mess, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height()))
    pygame.display.update()
# setup game loop

FPS = 5
clock = pygame.time.Clock()
run = True

while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()  # get the position of the mouse
            for letter in letters:
                x, y, ltr, visible = letter
                dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                if dis < RADIUS:
                    letter[3] = False
                    guessed.append(ltr)
                    if ltr not in word:
                        hangman_status += 1
    draw()
    won = True
    for letter in word:
        if letter not in guessed:
            won = False
            break
    if won:
        display_message("YOU WON!")
        win.fill((255, 0, 0))
        dis_word("THANK YOU FOR PLAYING")
        pygame.time.delay(1000)
        break
    if hangman_status == 6:
        display_message("YOU LOST!")
        win.fill((255, 0, 0))
        dis_word("YOUR WORD WAS:")
        pygame.time.delay(1000)
        win.fill((255, 0, 0))
        dis_word(word)
        pygame.time.delay(2000)
        win.fill((255, 0, 0))
        dis_word("THANK YOU FOR PLAYING")
        pygame.time.delay(1000)
        break

pygame.quit()
