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

def show_instructions():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 150 <= x <= 650 and 450 <= y <= 550:
                    running = False

        screen.blit(bg_img, (0, 0))
        font = pygame.font.SysFont(None, 32)
        lines = [
            "Привіт я Губка Боб я загубив десь свої ключі від дому",
            "допоможеш мені їх знайти, також мені потрібно зібрати всі",
            "Крабові Петті (бургери) для пана Крабса, доречі я чув що тут є",
            "cекретний левел, кажуть те що там неймовірно багато крабових Петті,",
            "досліди це мій друже)"
        ]
        y_offset = 120
        for line in lines:
            text_surface = font.render(line, True, (255, 255, 0))
            screen.blit(text_surface, (400 - text_surface.get_width() // 2, y_offset))
            y_offset += 45
        draw_button(screen, "Повернутись до меню", (0, 150, 0), 150, 450, 500, 100)
        pygame.display.flip()

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
                if 150 <= x <= 650 and 500 <= y <= 600:
                    show_instructions()

        screen.blit(bg_img, (0, 0))
        draw_button(screen, "Start Game", (0, 150, 0), 150, 200, 500, 100)
        draw_button(screen, "Exit", (200, 0, 0), 150, 350, 500, 100)
        draw_button(screen, "Інструкція", (0, 0, 200), 150, 500, 500, 100)
        pygame.display.flip()

def show_score_table(score):
    table = True
    while table:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                table = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 150 <= x <= 650 and 350 <= y <= 450:
                    table = False
                    exit()
                if 150 <= x <= 650 and 200 <= y <= 300:
                    table = False

        screen.blit(bg_img, (0, 0))
        font = pygame.font.SysFont(None, 48)
        score_text = font.render(f'Ви зібрали бонусів: {score}', True, (255, 255, 0))
        screen.blit(score_text, (400 - score_text.get_width() // 2, 120))
        draw_button(screen, "Головне меню", (0, 150, 0), 150, 200, 500, 100)
        draw_button(screen, "Exit", (200, 0, 0), 150, 350, 500, 100)
        pygame.display.flip()

def show_time_over():
    over = True
    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                over = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                over = False
        screen.blit(bg_img, (0, 0))
        font = pygame.font.SysFont(None, 48)
        text = font.render('Ви нажаль не встигли!', True, (255, 0, 0))
        screen.blit(text, (400 - text.get_width() // 2, 250))
        pygame.display.flip()

def show_secret_win_message(score):
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                show = False
        screen.blit(bg_img, (0, 0))
        font = pygame.font.SysFont(None, 40)
        text1 = font.render("Щірі вітання ти молодець!", True, (0, 255, 0))
        text2 = font.render("Постарайся наступного разу зібрати ще більше Крабовиз Петті", True, (255, 255, 0))
        score_text = font.render(f'Твій результат: {score}', True, (255, 255, 255))
        screen.blit(text1, (400 - text1.get_width() // 2, 180))
        screen.blit(text2, (400 - text2.get_width() // 2, 240))
        screen.blit(score_text, (400 - score_text.get_width() // 2, 320))
        pygame.display.flip()

def win():
    finish_sound = pygame.mixer.Sound('Finish.mp3')
    finish_sound.set_volume(0.8)
    finish_sound.play()
    win_menu = True
    secret_button_rect = pygame.Rect(150, 500, 500, 70)
    secret_level = False
    while win_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:    
                win_menu = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 150 <= x <= 650 and 200 <= y <= 300:
                    win_menu = False
                if 150 <= x <= 650 and 350 <= y <= 450:
                    win_menu = False
                    exit()
                if secret_button_rect.collidepoint(x, y):
                    win_menu = False
                    secret_level = True

        screen.blit(bg_img, (0, 0))
        draw_button(screen, "Вітаємо! Ви втекли з лабіринту!", (0, 0, 120), 150, 200, 500, 100)
        draw_button(screen, "Exit", (200, 0, 0), 150, 350, 500, 100)
        draw_button(screen, "Secret levl", (120, 0, 120), 150, 500, 500, 70)
        pygame.display.flip()
    if secret_level:
        secret_level_loop()

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

def secret_level_loop():
    # Всі вільні клітинки стають бонусами Burger.png
    secret_player_x, secret_player_y = 1, 1
    secret_score = 0
    secret_bonus_positions = [cell[:] for cell in free_cells if cell != [secret_player_x, secret_player_y]]
    secret_door_position = free_cells[-1]
    running = True
    direction = 0

    # Stop background music and play secret level music
    pygame.mixer.music.stop()
    secret_music = pygame.mixer.Sound('Secret_level.mp3')
    secret_music.set_volume(0.7)
    secret_music.play(-1)

    # Таймер 35 секунд
    start_ticks = pygame.time.get_ticks()
    time_limit = 35  # seconds

    time_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                secret_music.stop()
                exit()
            if event.type == pygame.KEYDOWN:
                moved = False
                if event.key == pygame.K_LEFT and secret_player_x > 0 and maze[secret_player_y][secret_player_x - 1] == 0:
                    secret_player_x -= 1
                    direction = 2
                    moved = True
                elif event.key == pygame.K_RIGHT and secret_player_x < len(maze[0])-1 and maze[secret_player_y][secret_player_x + 1] == 0:
                    secret_player_x += 1
                    direction = 1
                    moved = True
                elif event.key == pygame.K_UP and secret_player_y > 0 and maze[secret_player_y - 1][secret_player_x] == 0:
                    secret_player_y -= 1
                    direction = 3
                    moved = True
                elif event.key == pygame.K_DOWN and secret_player_y < len(maze) - 1 and maze[secret_player_y + 1][secret_player_x] == 0:
                    secret_player_y += 1
                    direction = 4
                    moved = True
                else:
                    direction = 0
                if moved:
                    walk_sound.play()
            if event.type == pygame.KEYUP:
                direction = 0

        # Таймер
        seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
        time_left = max(0, int(time_limit - seconds_passed))

        background_img = pygame.image.load('background.png')
        background_img = pygame.transform.scale(background_img, (800, 600))
        screen.blit(background_img, (0, 0))
        for y in range(len(maze)): 
            for x in range(len(maze[0])):
                if maze[y][x] == 1:
                    screen.blit(wall_img, (x * cell_size, y * cell_size))
        
        # Малюємо всі бонуси
        for pos in secret_bonus_positions:
            screen.blit(bonus_img, (pos[0] * cell_size, pos[1] * cell_size))
        # Перевіряємо чи гравець зібрав бонус
        for pos in secret_bonus_positions[:]:
            if [secret_player_x, secret_player_y] == pos:
                secret_bonus_positions.remove(pos)
                secret_score += 1
                burger_sound.play()

        screen.blit(door_img, (secret_door_position[0] * cell_size, secret_door_position[1] * cell_size))

        if direction == 0:
            screen.blit(player_img[0], (secret_player_x * cell_size, secret_player_y * cell_size))
        elif direction == 1:
            screen.blit(player_img[1], (secret_player_x * cell_size, secret_player_y * cell_size))
        elif direction == 2:
            screen.blit(player_img[2], (secret_player_x * cell_size, secret_player_y * cell_size))
        elif direction == 3:
            screen.blit(player_img[3], (secret_player_x * cell_size, secret_player_y * cell_size))
        elif direction == 4:
            screen.blit(player_img[3], (secret_player_x * cell_size, secret_player_y * cell_size))

        # Відображаємо рахунок бонусів
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Бонуси: {secret_score}', True, (255, 255, 0))
        screen.blit(score_text, (10, 10))

        # Відображаємо таймер
        timer_text = font.render(f'Час: {time_left}', True, (255, 0, 0) if time_left <= 5 else (255, 255, 255))
        screen.blit(timer_text, (650, 10))

        # Гравець може вийти коли завгодно через двері
        if [secret_player_x, secret_player_y] == secret_door_position:
            running = False

        # Якщо час вийшов
        if time_left == 0:
            time_over = True
            running = False

        pygame.display.flip()
        clock.tick(fps)

    secret_music.stop()
    if time_over:
        show_time_over()
    else:
        show_secret_win_message(secret_score)

main_menu()
game_loop()
pygame.quit()
