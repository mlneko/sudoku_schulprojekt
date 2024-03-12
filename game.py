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

def draw_numbers(numbers):
    font = pygame.font.Font(None, 40)
    for row in range(9):
        for number in range(9):
            text = font.render(str(numbers[row][number]), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=((number+1)*50, (row+1)*50)))
            

    
def generate_numbers():
    numbers = [[i]*9 for i in range(1, 10)]
    return numbers

value, solution = generate_board()

while run:
    screen.fill((255, 255, 255))
    draw_grid()
    draw_numbers(value)
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update() 

pygame.quit()	 