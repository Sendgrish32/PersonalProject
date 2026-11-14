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
        "is_clicked": False
    }

    return name

def collide_balls(ball1, ball2, bounce):
  position1 = ball1["pos"]
  position2 = ball2["pos"]
  vector12 = position2 - position1 #Вектор, который соединяет центры оскружностей
  distance = vector12.length() #Расстояние между центрми
  min_distance = ball1["radius"] + ball2["radius"] #Минимальное расстояние между центрами

  if distance >= min_distance:
    return

  if distance < 1e-8: #Совпадение центров, нормаль неопределена
    normal = pygame.Vector2(1, 0) #Задаем произвольную нормаль
    distance = 0
  else:
    normal = vector12 / distance #Единичный вектор-нормаль

  m1 = ball1["mass"]
  m2 = ball2["mass"]

  overlap = min_distance - distance #Длина отрезка, на который коружности зашли друг в друга
  inv1 = 1 / m1 #Оптимизация кода (обратные массы)
  inv2 = 1 / m2
  inv_sum = inv1 + inv2

  ball1["pos"] -= normal * overlap * (inv1 / inv_sum) #Сдвигаем окружности пропорционально их массам: Чем больше масса, тем меньше сдвиг
  ball2["pos"] += normal * overlap * (inv2 / inv_sum)

  relative_vel = ball2["vel"] - ball1["vel"] #Скорость второго шара относительно первого
  vel_normal = relative_vel.dot(normal) #Проекция эток скорсти на нормаль

  if vel_normal >= 0: #Шары разлетаются друг от друга
    return

  impulse = -(1+bounce) * vel_normal / inv_sum #Импульс

  ball1["vel"] -= normal * (impulse * inv1)
  ball2["vel"] += normal * (impulse * inv2)

pygame.init()

#---INIT---
width = 1000
height = 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Physical Engine")
clock = pygame.time.Clock()
FPS = 120

#---counts---
font = pygame.font.SysFont("arial", 18, bold=True)
g = 980  # Ускорение свободного падения
bounce = 0.75  # Коэффициент упругости
gravity = False
ball_counter = 1
clicked_ball = None
# --- ИНТЕРФЕЙС И СОСТОЯНИЯ ---
prev_mouse_pos = pygame.Vector2(0, 0)
GBut = pygame.Rect(795, 5, 200, 30)
CBBut = pygame.Rect(795, 40, 200, 30)
MBut = pygame.Rect(795, 75, 200, 110)
GButCol = (100, 100, 100)
CBButCol = (100, 100, 100)
MButCol = (100, 100, 100)
ColBut = pygame.Rect(800, 80, 190, 30)
ColButCol = (120, 120, 120)
VelBut = pygame.Rect(800, 115, 190, 30)
VelButCol = (120, 120, 120)
DelBut = pygame.Rect(800, 150, 190, 30)
DelButCol = (120, 120, 120)

#---Balls---
balls = {"ball0":{"pos": pygame.Vector2(400, 300),
        "vel": pygame.Vector2(0, 0),
        "radius": 50,
        "mass": 20,
        "color": (50, 50, 50),
        "is_clicked": False}}

#Main cycle
running = True
while running:
  dt = clock.tick(FPS) / 1000.0
  #print(1 / dt)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN: #нажатие ЛКМ
      if event.button == 1:
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) #Записываем координаты мыши

        for ball in balls.values(): #Для каждого шара проверяем касание с мышью
          if mouse_pos.distance_to(ball["pos"]) <= ball["radius"]:
            ball["color"] = (70, 70, 70)
            ball["is_clicked"] = not ball["is_clicked"]
            if clicked_ball != None:
              clicked_ball["is_clicked"] = False
            clicked_ball = ball
            if not ball["is_clicked"]:
              clicked_ball = None
            ball["vel"] = pygame.Vector2(0, 0)
            prev_mouse_pos = mouse_pos.copy()

        if GBut.collidepoint(mouse_pos): #нажатие кнопки гравитации
          gravity = not gravity

        if CBBut.collidepoint(mouse_pos): #Нажатие кнопки создания шара
          new_ball((500, 300), 50, 10)

        #if ColBut.collidepoint(mouse_pos) and menu:
          # Здесь будет изменение цвета

        #if VelBut.collidepoint(mouse_pos) and menu:
          # Здесь будет изменение вектора
        
        if DelBut.collidepoint(mouse_pos) and menu:
          for key, value in list(balls.items()):
            if value is clicked_ball:
                balls.pop(key, None)
                clicked_ball = None
                break
        

    elif event.type == pygame.MOUSEBUTTONUP: #
      '''if event.button == 1:
        for ball in balls.values(): #Для каждого шара проверяем касание с мышью
            if ball["is_clicked"]:
                ball["is_clicked"] = False
                mouse_pos = pygame.Vector2(event.pos)
                if dt > 0:
                    ball["vel"] = (mouse_pos - prev_mouse_pos) / dt

    elif event.type == pygame.MOUSEMOTION: #Если мышь перемещена 
      for ball in balls.values():
        if ball["is_clicked"]:
          prev_mouse_pos = ball["pos"].copy()
          ball["pos"] = pygame.Vector2(event.pos)'''
    elif event.type == pygame.MOUSEMOTION:
      mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
      if CBBut.collidepoint(mouse_pos):
        CBButCol = (120, 120, 120)
      else:
        CBButCol = (100, 100, 100)
      if GBut.collidepoint(mouse_pos) and not gravity:
        GButCol = (120, 120, 120)
      else:
        GButCol = (100, 100, 100)
      
  # Физика шаров
  for ball in balls.values(): # Для каждого шара
    if not ball["is_clicked"]:
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
      elif ball["pos"].x + ball["radius"] >= width - 210:
        ball["pos"].x = width - 210 - ball["radius"]
        ball["vel"].x = -ball["vel"].x * bounce
      # --- СКОРОСТЬ ШАРА ---
      '''circle_speed_sqrt = ball["vel"].x**2 + ball["vel"].y**2
      circle_speed = circle_speed_sqrt ** 0.5'''

  if clicked_ball == None:
    menu = False
  else:
    menu = True

  for ball1, ball2 in  combinations(balls.values(), 2):
    collide_balls(ball1, ball2, bounce)

  # --- ОТРИСОВКА ---
  screen.fill((30, 30, 30))

  # Шары
  for ball in balls.values():
    if ball["is_clicked"]:
        ball["color"] = (70, 70, 70)
    else:
        ball["color"] = (50, 50, 50)
    pygame.draw.circle(screen, ball["color"], ball["pos"], ball["radius"])

  # Состояние меню.
  if not menu:
    ColButCol = (70, 70, 70)
    VelButCol = (70, 70, 70)
    DelButCol = (70, 70, 70)
    MButCol = (50, 50, 50)
  else:
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    MButCol = (100, 100, 100)
    if DelBut.collidepoint(mouse_pos):
      DelButCol = (140, 140, 140)
    else:
      DelButCol = (120, 120, 120)
    if VelBut.collidepoint(mouse_pos):
      VelButCol = (140, 140, 140)
    else:
      VelButCol = (120, 120, 120)
    if ColBut.collidepoint(mouse_pos):
      ColButCol = (140, 140, 140)
    else:
      ColButCol = (120, 120, 120)

  # Кнопки меню
  pygame.draw.rect(screen, MButCol, MBut, 0, 15)
  pygame.draw.rect(screen, ColButCol, ColBut, 0, 15)
  But_str = "COLOR"
  text_surface_But = font.render(But_str, True, (255, 255, 255))
  text_rect_But = text_surface_But.get_rect(center=ColBut.center)
  screen.blit(text_surface_But, text_rect_But)
  pygame.draw.rect(screen, VelButCol, VelBut, 0, 15)
  But_str = "VELOCITY"
  text_surface_But = font.render(But_str, True, (255, 255, 255))
  text_rect_But = text_surface_But.get_rect(center=VelBut.center)
  screen.blit(text_surface_But, text_rect_But)
  pygame.draw.rect(screen, DelButCol, DelBut, 0, 15)
  But_str = "DELETE"
  text_surface_But = font.render(But_str, True, (255, 255, 255))
  text_rect_But = text_surface_But.get_rect(center=DelBut.center)
  screen.blit(text_surface_But, text_rect_But)


  # Кнопка гравитации
  if gravity: GButCol = (0, 150, 0) 
  pygame.draw.rect(screen, GButCol, GBut, 0, 15)
  GBut_str = "GRAVITY: ON" if gravity else "GRAVITY: OFF"
  text_surface = font.render(GBut_str, True, (255, 255, 255))
  text_rect = text_surface.get_rect(center=GBut.center)
  screen.blit(text_surface, text_rect)

  # Кнопка создания шара
  pygame.draw.rect(screen, CBButCol, CBBut, 0, 15)
  CBBut_str = "CREATE BALL"
  text_surface_CBBut = font.render(CBBut_str, True, (255, 255, 255))
  text_rect_CBBut = text_surface_CBBut.get_rect(center=CBBut.center)
  screen.blit(text_surface_CBBut, text_rect_CBBut)

  pygame.draw.rect(screen, (10, 10, 10), (0, 700, 1000, 50)) # Пол
  pygame.display.flip()
  #print(clicked_ball, balls)

pygame.quit()
sys.exit()