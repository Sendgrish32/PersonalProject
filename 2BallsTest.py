import sys, pygame
from itertools import combinations

def new_ball(pos, radius, mass):
    global ball_counter

    ball_counter += 1
    name = f"ball{ball_counter}"

    balls[name] = {
        "pos": pygame.Vector2(pos),
        "vel": pygame.Vector2(0, 0),
        "radius": int(radius),
        "mass": int(mass),
        "color": (100, 150, 255),
        "is_dragged": False
    }

    return name

def collide_balls(ball1, ball2, bounce):
  pos1 = ball1["pos"]
  pos2 = ball2["pos"]
  delta = pos2 - pos1
  dist = delta.length()
  min_dist = ball1["radius"] + ball2["radius"]

  if dist >= min_dist:
    return

  if dist < 1e-8:
    normal = pygame.Vector2(1, 0)
    dist = 0
  else:
    normal = delta / dist

  m1 = ball1["mass"]
  m2 = ball2["mass"]

  overlap = min_dist - dist
  inv1 = 1 / m1
  inv2 = 1 / m2
  inv_sum = inv1 + inv2

  ball1["pos"] -= normal * overlap * (inv1 / inv_sum)
  ball2["pos"] -= normal * overlap * (inv2 / inv_sum)

  relative_vel = ball2["vel"] - ball1["vel"]
  vel_normal = relative_vel.dot(normal)

  if vel_normal >= 0:
    return

  impulse = -(1+bounce) * vel_normal / inv_sum

  ball1["vel"] -= normal * (impulse / m1)
  ball2["vel"] -= normal * (impulse / m2)

pygame.init()

#---INIT---
width = 1000
height = 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Physical Engine")
clock = pygame.time.Clock()
FPS = 60

#---counts---
font = pygame.font.SysFont("arial", 18, bold=True)
g = 980  # Ускорение свободного падения
bounce = 0.75  # Коэффициент упругости
gravity = False
ball_counter = 1
# --- ИНТЕРФЕЙС И СОСТОЯНИЯ ---
prev_mouse_pos = pygame.Vector2(0, 0)
GBut = pygame.Rect(795, 5, 200, 30)
CBBut = pygame.Rect(795, 40, 200, 30)
ButCol = (100, 100, 100)
CBButCol = (100, 100, 100)

#---Balls---
balls = {"ball0":{"pos": pygame.Vector2(400, 300),
        "vel": pygame.Vector2(0, 0),
        "radius": 50,
        "mass": 10,
        "color": (50, 50, 50),
        "is_dragged": False}}

#Main cycle
running = True
while running:
  dt = clock.tick(FPS) / 1000.0 / 20

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN: #нажатие ЛКМ
      if event.button == 1:
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) #Записываем координаты мыши

        for ball in balls.values(): #Для каждого шара проверяем касание с мышью
          if mouse_pos.distance_to(ball["pos"]) <= ball["radius"]:
            ball["color"] = (70, 70, 70)
            ball["is_dragged"] = True
            ball["vel"] = pygame.Vector2(0, 0)
            prev_mouse_pos = mouse_pos.copy()

        if GBut.collidepoint(mouse_pos): #нажатие кнопки гравитации
          gravity = not gravity
          ButCol = (0, 150, 0) if gravity else (100, 100, 100)

        if CBBut.collidepoint(mouse_pos): #Нажатие кнопки создания шара
          new_ball((500, 300), 50, 10)

    elif event.type == pygame.MOUSEBUTTONUP: #
      if event.button == 1:

        for ball in balls.values(): #Для каждого шара проверяем касание с мышью
            if ball["is_dragged"]:
                ball["is_dragged"] = False
                mouse_pos = pygame.Vector2(event.pos)
                if dt > 0:
                    ball["vel"] = (mouse_pos - prev_mouse_pos) / dt

    elif event.type == pygame.MOUSEMOTION: #Если мышь перемещена 
      for ball in balls.values():
        if ball["is_dragged"]:
          prev_mouse_pos = ball["pos"].copy()
          ball["pos"] = pygame.Vector2(event.pos)

  # Физика шаров
  for ball in balls.values(): # Для каждого шара
    if not ball["is_dragged"]:
      if gravity:
        ball["vel"].y += g * dt
      ball["pos"] += ball["vel"] * dt

      # --- ОТСКОК ОТ ПОЛА (Y = 700) ---
      if ball["pos"].y + ball["radius"] >= 700:
        ball["pos"].y = 700 - ball["radius"]
        ball["vel"].y = -ball["vel"].y * bounce
        if abs(ball["vel"].y) < 15:
          ball["vel"].y = 0

      # --- ОТСКОК ОТ ПОТОЛКА (Y = 0) ---
      if ball["pos"].y - ball["radius"] <= 0:
        ball["pos"].y = ball["radius"]
        ball["vel"].y = -ball["vel"].y * bounce

      # --- ОТСКОК ОТ ЛЕВОЙ СТЕНЫ (X = 0) ---
      if ball["pos"].x - ball["radius"] <= 0:
        ball["pos"].x = ball["radius"]
        ball["vel"].x = -ball["vel"].x * bounce

      # --- ОТСКОК ОТ ПРАВОЙ СТЕНЫ (X = width) ---
      elif ball["pos"].x + ball["radius"] >= width:
        ball["pos"].x = width - ball["radius"]
        ball["vel"].x = -ball["vel"].x * bounce
      # --- СКОРОСТЬ ШАРА ---
      '''circle_speed_sqrt = ball["vel"].x**2 + ball["vel"].y**2
      circle_speed = circle_speed_sqrt ** 0.5'''

  for ball1, ball2 in  combinations(balls.values(), 2):
    collide_balls(ball1, ball2, bounce)

  # --- ОТРИСОВКА ---
  screen.fill((30, 30, 30))

  # Кнопка гравитации
  pygame.draw.rect(screen, ButCol, GBut, 0, 15)
  text_str = "GRAVITY: ON" if gravity else "GRAVITY: OFF"
  text_surface = font.render(text_str, True, (255, 255, 255))
  text_rect = text_surface.get_rect(center=GBut.center)
  screen.blit(text_surface, text_rect)

  # Кнопка создания шара
  pygame.draw.rect(screen, CBButCol, CBBut, 0, 15)
  CBBut_str = "CREATE BALL"
  text_surface_CBBut = font.render(CBBut_str, True, (255, 255, 255))
  text_rect_CBBut = text_surface_CBBut.get_rect(center=CBBut.center)
  screen.blit(text_surface_CBBut, text_rect_CBBut)

  # Шары
  for ball in balls.values():
    if ball["is_dragged"]:
        ball["color"] = (70, 70, 70)
    else:
        ball["color"] = (50, 50, 50)
    pygame.draw.circle(screen, ball["color"], ball["pos"], ball["radius"])

  pygame.draw.rect(screen, (10, 10, 10), (0, 700, 1000, 50)) # Пол
  pygame.display.flip()

pygame.quit()
sys.exit()