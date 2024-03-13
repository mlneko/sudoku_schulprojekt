import pygame, copy, random
import requests

pygame.init()

screen = pygame.display.set_mode((500, 600))

run = True

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
            text = font.render(str(numbers[row][number]), True, (0, 0, 0))
            rect = text.get_rect(center=((number+1)*50, (row+1)*50))
            screen.blit(text, rect)
            if (number, row) == selected_value:
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
selected_number = (0, 0)

while run:
    screen.fill((255, 255, 255))
    draw_grid()
    draw_numbers(value, selected_number)
    reset_button, check_entries_button = draw_buttons()
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if reset_button.collidepoint(event.pos):
                value, solution = generate_board()
                selected_number = (-1, 0)
            elif check_entries_button.collidepoint(event.pos):
                print(1)
                selected_number = (-1, 0)
            elif 475 >= event.pos[0] >= 25 and 475 >= event.pos[1] >= 25:
                selected_number = (int((event.pos[0]-25)/50),int((event.pos[1]-25)/50))
            else:
                selected_number = (-1, 0)

                                
    pygame.display.update() 

pygame.quit()