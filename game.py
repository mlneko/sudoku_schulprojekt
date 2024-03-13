import pygame, copy, random
import requests

pygame.init()

screen = pygame.display.set_mode((500, 600))

run = True

def wait_on_user_key():
    k = False
    while True:
        for event in pygame.event.get():
            if event.type in [pygame.KEYUP, pygame.MOUSEBUTTONUP]:
                k = True
            break
        if k:
            break

def draw_false_numbers(value, solution):
    screen.fill((255, 255, 255))
    draw_grid()
    draw_numbers(value, [-1, 0])
    for row in range(9):
        for number in range(9):
            if value[row][number] != 0 and solution[row][number] != value[row][number]:
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((number+1)*50-25, (row+1)*50-25, 50, 50), 3, 0)
    pygame.display.update()
                

def generate_board():
    res = requests.get(("https://sudoku-api.vercel.app/api/dosuku?query={newboard(limit:1){grids{value,solution}}}")).json()['newboard']['grids'][0]
    return res['value'], res['solution']

def draw_grid():
    cord = 25
    for i in range(10):
        width = 3 if i % 3 == 0 else 1
        pygame.draw.line(screen, (0, 0, 0), (25, cord), (475, cord), width)
        pygame.draw.line(screen, (0, 0, 0), (cord, 25), (cord, 475), width)
        cord+=50

def draw_numbers(numbers, selected_value):
    font = pygame.font.Font(None, 40)
    for row in range(9):
        for number in range(9):
            text = font.render(str(numbers[row][number]) if numbers[row][number] != 0 else "", True, (0, 0, 0))
            rect = text.get_rect(center=((number+1)*50, (row+1)*50))
            screen.blit(text, rect)
            if [number, row] == selected_value:
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((number+1)*50-24, (row+1)*50-24, 49, 49), 2, 2)
            
def draw_buttons():
    font = pygame.font.Font(None, 50)
    text1 = font.render("Reset", True, (0,0,0))
    text2 = font.render("Check Entries", True, (0,0,0))
    rect1 = text1.get_rect(center=(125, 525))
    rect2 = text2.get_rect(center=(325, 525))
    screen.blit(text1, rect1)
    screen.blit(text2, rect2)
    pygame.draw.rect(screen, (125, 125, 125), rect1,2, 1)
    pygame.draw.rect(screen, (125, 125, 125), rect2,2, 1)
    return rect1, rect2
            
value, solution = generate_board()
selected_number = [0, 0]

while run:
    screen.fill((255, 255, 255))
    draw_grid()
    draw_numbers(value, selected_number)
    reset_button, check_entries_button = draw_buttons()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if reset_button.collidepoint(event.pos):
                value, solution = generate_board()
                selected_number = [0, 0]
            elif check_entries_button.collidepoint(event.pos):
                draw_false_numbers(value, solution)
                wait_on_user_key()
                draw_numbers(value, selected_number)
            elif 475 >= event.pos[0] >= 25 and 475 >= event.pos[1] >= 25:
                selected_number = [int((event.pos[0]-25)/50),int((event.pos[1]-25)/50)]
            else:
                selected_number = [-1, 0]
        elif event.type == pygame.KEYUP and event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
            if event.key == pygame.K_UP and selected_number[1] > 0:
                selected_number[1] -= 1
            elif event.key == pygame.K_DOWN and selected_number[1] < 8:
                selected_number[1] += 1
            elif event.key == pygame.K_LEFT and selected_number[0] > 0:
                selected_number[0] -= 1
            elif event.key == pygame.K_RIGHT and selected_number[0] < 9:
                selected_number[0] += 1
        elif (event.type == pygame.TEXTINPUT and event.text in [str(i) for i in range(10)] + ["-"]) or (event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE):
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE) or event.text == "-":
                event.text = "0"
            value[selected_number[1]][selected_number[0]] = int(event.text)
    pygame.display.update() 

pygame.quit()