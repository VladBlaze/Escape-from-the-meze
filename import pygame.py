import pygame
import random
pygame.init()
pygame.mixer.init()

collect_sound = pygame.mixer.Sound('spongebob-production.mp3')
background_sound = 'spongebob-production.mp3'

pygame.mixer.music.load(background_sound)
pygame.mixer.music.set_volume(0.5)

collect_sound.set_volume(0.7)
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Втеча з лабіринту')

# Load background image for menus
bg_img = pygame.image.load('background.png')
bg_img = pygame.transform.scale(bg_img, (800, 600))


background_color = (0,0,0)
cell_size = 40


player_img = [pygame.image.load(f'{i}.png') for i in range(1, 5) ]
player_img = [pygame.transform.scale(player, (cell_size, cell_size)) for player in player_img]
player_id = 0


wall_img = pygame.image.load('wall.png')
wall_img = pygame.transform.scale(wall_img, (cell_size, cell_size))


key_img = pygame.image.load('key.png')
key_img = pygame.transform.scale(key_img, (cell_size, cell_size))


door_img = pygame.image.load('door.png')
door_img = pygame.transform.scale(door_img, (cell_size, cell_size))


maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
free_cells = []
for y in range(len(maze)):
    for x in range(len(maze[y])):
        if maze[y][x] == 0:
            free_cells.append([x, y])

key_position = random.choice(free_cells[:-1])
door_position = free_cells[-1]
clock = pygame.time.Clock()
fps = 15
player_x, player_y = 1, 1
key_exists = False 

def draw_button(screen, text, color, x, y, w, h):
    pygame.draw.rect(screen, color, (x, y, w, h))
    font = pygame.font.SysFont(None, 36)
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x + (w - text_surface.get_width()) / 2, y + (h - text_surface.get_height()) / 2))

def main_menu():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:    
                menu = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 150 <= x <= 650 and 200 <= y <= 300:
                    menu = False
                if 150 <= x <= 650 and 350 <= y <= 450:
                    menu = False
                    exit()

        screen.blit(bg_img, (0, 0))
        draw_button(screen, "Start Game", (0, 150, 0), 150, 200, 500, 100)
        draw_button(screen, "Exit", (200, 0, 0), 150, 350, 500, 100)
        pygame.display.flip()

def win():
    finish_sound = pygame.mixer.Sound('Finish.mp3')
    finish_sound.set_volume(0.8)
    finish_sound.play()
    win = True
    while win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:    
                win = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 150 <= x <= 650 and 200 <= y <= 300:
                    win = False
                if 150 <= x <= 650 and 350 <= y <= 450:
                    win = False
                    exit()

        screen.blit(bg_img, (0, 0))
        draw_button(screen, "Вітаємо! Ви втекли з лабіринту!", (0, 0, 120), 150, 200, 500, 100)
        draw_button(screen, "Exit", (200, 0, 0), 150, 350, 500, 100)
        pygame.display.flip()

player_direction = 0

# Додаємо бонуси
bonus_img = pygame.image.load('Crabypetty.png')
bonus_img = pygame.transform.scale(bonus_img, (cell_size, cell_size))
num_bonuses = 5
bonus_positions = []
while len(bonus_positions) < num_bonuses:
    pos = random.choice(free_cells)
    if pos != key_position and pos != door_position and pos not in bonus_positions and [player_x, player_y] != pos:
        bonus_positions.append(pos)
score = 0

# Додаємо звук ходьби
walk_sound = pygame.mixer.Sound('walk.mp3')
walk_sound.set_volume(1.0)  # Збільшено гучність до максимуму

# Додаємо звук для бонусу
burger_sound = pygame.mixer.Sound('Burger.mp3')
burger_sound.set_volume(0.7)

# Додаємо звук для ключа
collect_key_sound = pygame.mixer.Sound('collect.mp3')
collect_key_sound.set_volume(0.7)

def game_loop():
    global player_x, player_y, player_direction, key_exists, bonus_positions, score
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                moved = False
                if event.key == pygame.K_LEFT and player_x > 0 and maze[player_y][player_x - 1] == 0:
                    player_x -= 1
                    player_direction = 2
                    moved = True
                elif event.key == pygame.K_RIGHT and player_x < len(maze[0])-1 and maze[player_y][player_x + 1] == 0:
                    player_x += 1
                    player_direction = 1
                    moved = True
                elif event.key == pygame.K_UP and player_y > 0 and maze[player_y - 1][player_x] == 0:
                    player_y -= 1
                    player_direction = 3
                    moved = True
                elif event.key == pygame.K_DOWN and player_y < len(maze) - 1 and maze[player_y + 1][player_x] == 0:
                    player_y += 1
                    player_direction = 4
                    moved = True
                else:
                    player_direction = 0
                if moved:
                    walk_sound.play()
            if event.type == pygame.KEYUP:
                player_direction = 0

        background_img = pygame.image.load('background.png')
        background_img = pygame.transform.scale(background_img, (800, 600))
        screen.blit(background_img, (0, 0))
        for y in range(len(maze)): 
            for x in range(len(maze[0])):
                if maze[y][x] == 1:
                    screen.blit(wall_img, (x * cell_size, y * cell_size))
        
        # Малюємо бонуси
        for pos in bonus_positions:
            screen.blit(bonus_img, (pos[0] * cell_size, pos[1] * cell_size))
        # Перевіряємо чи гравець зібрав бонус
        for pos in bonus_positions[:]:
            if [player_x, player_y] == pos:
                bonus_positions.remove(pos)
                score += 1
                burger_sound.play()  # Відтворюємо звук при підборі бонусу

        if not key_exists:
            if [player_x, player_y] == key_position:
                key_exists = True
                collect_key_sound.play()  # Відтворюємо звук при підборі ключа
            else:
                screen.blit(key_img, (key_position[0] * cell_size, key_position[1] * cell_size))

        screen.blit(door_img, (door_position[0] * cell_size, door_position[1] * cell_size))

        if player_direction == 0:
            screen.blit(player_img[0], (player_x * cell_size, player_y * cell_size))
        elif player_direction == 1:
            screen.blit(player_img[1], (player_x * cell_size, player_y * cell_size))
        elif player_direction == 2:
            screen.blit(player_img[2], (player_x * cell_size, player_y * cell_size))
        elif player_direction == 3:
            screen.blit(player_img[3], (player_x * cell_size, player_y * cell_size))
        elif player_direction == 4:
            screen.blit(player_img[3], (player_x * cell_size, player_y * cell_size))

        # Відображаємо рахунок бонусів
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Бонуси: {score}', True, (255, 255, 0))
        screen.blit(score_text, (10, 10))

        if key_exists and [player_x, player_y] == door_position:
            running = False

        pygame.display.flip()
        clock.tick(fps)

    if key_exists and [player_x, player_y] == door_position:
        win()

main_menu()
game_loop()
pygame.quit()
