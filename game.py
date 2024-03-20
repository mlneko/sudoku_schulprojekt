import pygame, copy, random
import requests



def wait_on_user_key():
    k = False
    
    font = pygame.font.Font(None, 30)
    
    text = font.render("Drück einen beliebigen Knopf um Fortzufahren", True, (0, 0, 0))
    screen.blit(text, text.get_rect(center=(245, 550)))
    
    pygame.display.update()
    
    while True:
        
        for event in pygame.event.get():
            
            if event.type in [pygame.KEYUP, pygame.MOUSEBUTTONUP]:
                k = True
                
            elif event.type == pygame.QUIT:
                run = False
                
            break
        
        if k:
            break


def check_win(value, solution, lives, diff):
    
    if value == solution:
        screen.fill((255,255,255))
        draw_grid()
        draw_numbers(value, [-1,0], lives, diff)
        
        for row in range(9):
          for number in range(9):
              
                pygame.draw.rect(screen, (0, 255, 0), pygame.Rect((number+1)*50-25, (row+1)*50, 50, 50), 3, 0)
                
        pygame.display.update()
        pygame.time.wait(2500)
        screen.fill((255,255,255,))
        
        font = pygame.font.Font(None, 50)
        text = font.render("GEWONNEN", True, (0,0,0))
        screen.blit(text, text.get_rect(center=(250,250)))
        
        pygame.display.update()
        pygame.time.wait(2500)
        
        return True


def check_lose(lives):
    
    if lives == 0:
        
        src_img = pygame.image.load("heart.png")
        src_img.convert()
        
        font = pygame.font.Font(None, 40)
        
        for i in range(1, 6):
            
            screen.fill((255,255,255))
            img = pygame.transform.scale(src_img, (25*i, 25*i))
            
            screen.blit(img, img.get_rect(center=(i*50, i*50)))
            
            pygame.display.update()
            pygame.time.wait(750)
            
        text = font.render("VERLOREN", True, (0,0,0))
        screen.blit(text, text.get_rect(center=(250,340)))
        
        pygame.display.update()
        wait_on_user_key()
        
        return True


def draw_false_numbers(value, solution, lives, diff):
    mistake = False
    
    if not check_win(value, solution, lives, diff):
        
        screen.fill((255, 255, 255))
        draw_grid()
        
        for row in range(9):
            for number in range(9):
                
                if value[row][number] != 0 and solution[row][number] != value[row][number]:
                    
                    mistake = True
                    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((number+1)*50-25, (row+1)*50, 50, 50), 3, 0)
                    
        draw_numbers(value, [-1, 0], lives-1 if mistake else lives, diff)
        
        pygame.display.update()
        wait_on_user_key()
        
        return False, mistake
    
    else: return True, mistake


def generate_board():
    try: 
        
        res = requests.get(("https://sudoku-api.vercel.app/api/dosuku?query={newboard(limit:1){grids{value,solution,difficulty}}}")).json()['newboard']['grids'][0]
        return 3, res['value'], res['solution'], res['difficulty']
    
    except requests.exceptions.JSONDecodeError:
        return generate_board()


def draw_grid():
    cord = 25
    
    for i in range(10):
        
        width = 3 if i % 3 == 0 else 1
        
        pygame.draw.line(screen, (0, 0, 0), (25, cord+25), (475, cord+25), width)
        pygame.draw.line(screen, (0, 0, 0), (cord, 50), (cord, 500), width)
        
        cord+=50
        
    img = pygame.image.load("heart.png")
    img = pygame.transform.scale(img, (25, 25))
    img.convert()
    
    screen.blit(img, img.get_rect(center=(50, 25)))


def draw_numbers(numbers, selected_value, lives, diff):
    font = pygame.font.Font(None, 40)
    
    for row in range(9):
        for number in range(9):
            
            text = font.render(str(numbers[row][number]) if numbers[row][number] != 0 else "", True, (0, 0, 0))
            rect = text.get_rect(center=((number+1)*50, (row+1)*50+25))
            
            screen.blit(text, rect)
            
            if [number, row] == selected_value:
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((number+1)*50-24, (row+1)*50+1, 49, 49), 2, 2)

    text = font.render(f"{int((pygame.time.get_ticks()-ticks)/1000/60):02}:{int((pygame.time.get_ticks()-ticks)/1000%60):02}", True, (0, 0, 0))
    screen.blit(text, text.get_rect(midleft=(405, 25)))
    
    text = font.render(str(diff), True, (0, 0, 0))
    screen.blit(text, text.get_rect(center=(245, 25)))
    
    text = font.render(str(lives), True, (0, 0, 0))
    screen.blit(text, text.get_rect(center=(75, 25)))
            
                
def draw_buttons():
    font = pygame.font.Font(None, 45)
    
    text1 = font.render("Zurücksetzen", True, (255,255,255))
    text2 = font.render("Einträge prüfen", True, (255,255,255))
    
    rect1 = text1.get_rect(midleft=(25, 550))
    rect2 = text2.get_rect(midright=(475, 550))
    
    pygame.draw.rect(screen, (0, 0, 0), rect1, 0, 5)
    pygame.draw.rect(screen, (0, 0, 0), rect2, 0, 5)
    
    screen.blit(text1, rect1)
    screen.blit(text2, rect2)
    
    return rect1, rect2
            
            

lives, value, solution, diff = generate_board()


global ticks
ticks = .0

selected_number = [0, 0]

pygame.init()

screen = pygame.display.set_mode((500, 600))

run = True


while run:
    
    screen.fill((255, 255, 255))
    draw_grid()
    draw_numbers(value, selected_number, lives, diff)
    reset_button, check_entries_button = draw_buttons()
    
    value = copy.deepcopy(solution)
    
    for event in pygame.event.get():
        print(event)
        
        if event.type == pygame.QUIT:
            run = False
            
            
        elif event.type == pygame.MOUSEBUTTONUP:
            
            if reset_button.collidepoint(event.pos):
                lives, value, solution, diff = generate_board()
                ticks = pygame.time.get_ticks()
                
            elif check_entries_button.collidepoint(event.pos):
                
                selected_number = [0, 0]
                check = draw_false_numbers(value, solution, lives, diff)
                
                if check[0]: # if check_win is true
                    lives, value, solution, diff  = generate_board()
                    ticks = pygame.time.get_ticks()
                    
                elif check[1]:
                    lives -= 1
                    
            elif 475 >= event.pos[0] >= 25 and 500 >= event.pos[1] >= 50:
                selected_number = [int((event.pos[0]-25)/50),int((event.pos[1]-50)/50)]
              
                
        elif event.type == pygame.KEYUP and event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
            
            if event.key == pygame.K_UP and selected_number[1] > 0:
                selected_number[1] -= 1
                
            elif event.key == pygame.K_DOWN and selected_number[1] < 8:
                selected_number[1] += 1
                
            elif event.key == pygame.K_LEFT and selected_number[0] > 0:
                selected_number[0] -= 1
                
            elif event.key == pygame.K_RIGHT and selected_number[0] < 8:
                selected_number[0] += 1
                
                
        elif (event.type == pygame.TEXTINPUT and event.text in [str(i) for i in range(10)] + ["-"]) or (event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE):
            
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE) or event.text == "-":
                event.text = "0"
                
            value[selected_number[1]][selected_number[0]] = int(event.text)
            
            
    if check_lose(lives):
        
        lives, value, solution, diff = generate_board()
        ticks = pygame.time.get_ticks()
        selected_number = [0, 0]
        
        
    pygame.display.update() 

pygame.quit()