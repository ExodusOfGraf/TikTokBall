import pygame
import random
import time
import math

# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# размеры окна
WIDTH = 1200
HEIGHT = 800

# скорость работы
FPS = 30

# Основная координата расположения круга (центр)
CENTER = (600, 400)
main_circl_radius = 300

# Параметры отверстия
hole_radius = 120
hole_distance_from_center = 370
hole_angle = 0  # Угол относительно горизонтали (в радианах)

speed_of_rotation = 0.03
gravity = 0.2


class BallSimulation:
    def __init__(self, x, y, radius, color = (0, 0, 255)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = random.randint(-7, 5)
        self.speed_y = random.randint(-5, -5)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_y += gravity + random.uniform(0, 0.2)

        # определение расстояния между центром основного круга и мяча
        distance = math.sqrt((self.x - CENTER[0])**2 + (self.y - CENTER[1])**2)
        # определение расстояния между центром "отверстия" и мяча
        distance_between_centers_hole = math.sqrt((ball.x - hl_center_x_global) ** 2 + (ball.y - hl_center_y_global) ** 2)
        # определения расстояния между
        if ((distance >= (main_circl_radius - self.radius) - 5) and (distance_between_centers_hole > hole_radius - ball.radius)):
            elasticity = random.uniform(0.5, 0.7)  # Случайная "упругость"
            impulse_x = random.uniform(-0.2, 0) # случайный импульс по x
            impulse_y = random.uniform(-0.2, 0.3)  # случайный импульс по y
            if self.x < 600 and self.speed_x < 0:
                #self.speed_x *= -elasticity
                self.speed_x *= random.uniform(-1.08, -0.7) + impulse_x
            elif self.x > 600 and self.speed_x > 0:
                #self.speed_x *= -elasticity
                self.speed_x *= random.uniform(-1.06, -0.7) + impulse_x
            if self.y < 400 and self.speed_y < 0:
                self.speed_y *= random.uniform(-1.1, -0.8)
            elif self.y > 400 and self.speed_y > 0:
                self.speed_y *= random.uniform(-1.1, -0.8)


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius, width = 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BollSimulation")
clock = pygame.time.Clock()

ball_radius = 15
ball_color = BLUE
ball_start_x = CENTER[0]
ball_start_y = CENTER[1]
ball = BallSimulation(ball_start_x, ball_start_y, ball_radius, ball_color)

global hl_center_x_global
global hl_center_y_global

hl_center_x_global = 0
hl_center_y_global = 0

game_state = "running"
game_over = False
start_time = pygame.time.get_ticks()
font = pygame.font.Font(None, 36) # Инициализация шрифта

running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Обработка событий
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        elif game_state == "game_over" and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if button_rect.collidepoint(mouse_pos):
                # Перезапуск симуляции
                game_state = "running"
                game_over = False
                ball = BallSimulation(CENTER[0], CENTER[1], ball_radius, ball_color)
                start_time = pygame.time.get_ticks()

    if game_state == "running":
        # Обновление угла отверстия (соответвсвено и анимация "вращения" красного круга)
        hole_angle += speed_of_rotation

        # Рендеринг
        screen.fill(BLACK)
        #Рисует круг
        pygame.draw.circle(screen, RED, CENTER, radius=main_circl_radius, width=3)

        hole_center_x = CENTER[0] + hole_distance_from_center * math.cos(hole_angle)
        hole_center_y = CENTER[1] + hole_distance_from_center * math.sin(hole_angle)

        hl_center_x_global = hole_center_x
        hl_center_y_global = hole_center_y
        #print(hl_center_x_global, hl_center_y_global)

        pygame.draw.circle(screen, BLACK, (int(hole_center_x), int(hole_center_y)), hole_radius, width=0)

        ball.draw(screen)
        ball.move()

        # триггер на остановку игры при вылете мячика из круга
        if ((math.sqrt((ball.x - CENTER[0])**2 + (ball.y - CENTER[1])**2)) > (main_circl_radius + ball.radius)):
            game_over = True
            game_state = "game_over"
            end_time = pygame.time.get_ticks()
            elapsed_time = (end_time - start_time) / 1000
            ball.speed_x = 0
            ball.speed_y = 0


    elif game_state == "game_over":
        screen.fill(BLACK)  # Закрашиваем экран

        # Отрисовка текста "Игра окончена!"
        text_surface = font.render("Симуляция окончена!", True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(text_surface, text_rect)

        # Отрисовка текста с прошедшим временем
        time_surface = font.render(f"Время: {elapsed_time:.2f} сек", True, WHITE)
        time_rect = time_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(time_surface, time_rect)

        # Отрисовка кнопки "OK"
        button_width = 150
        button_height = 50
        button_x = WIDTH // 2 - button_width // 2
        button_y = HEIGHT * 2 // 3
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, GREEN, button_rect)

        # Отрисовка текста "OK" на кнопке
        button_text_surface = font.render("OK", True, BLACK)
        button_text_rect = button_text_surface.get_rect(center=button_rect.center)
        screen.blit(button_text_surface, button_text_rect)

    # после отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()


