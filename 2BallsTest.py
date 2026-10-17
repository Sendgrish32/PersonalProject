import sys, pygame

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
is_dragged = False
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
  dt = clock.tick(FPS) / 1000.0

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    elif event.type == pygame.MOUSEBUTTONDOWN: #нажатие ЛКМ
      if event.button == 1:
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) #Записываем координаты мыши

        for ball in balls.values():
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

        for ball in balls.values():
            if ball["is_dragged"]:
                ball["is_dragged"] = False
                mouse_pos = pygame.Vector2(event.pos)
                if dt > 0:
                    ball["vel"] = (mouse_pos - prev_mouse_pos) / dt

    elif event.type == pygame.MOUSEMOTION:
      for ball in balls.values():
        if ball["is_dragged"]:
          prev_mouse_pos = ball["pos"].copy()
          ball["pos"] = pygame.Vector2(event.pos)

  # 2. ФИЗИКА И ЛОГИКА (Работает, пока шар не перетаскивают мышью)
  for ball in balls.values():
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

  # 3. ОТРИСОВКА
  screen.fill((30, 30, 30))

  # Кнопка гравитации
  pygame.draw.rect(screen, ButCol, GBut, 0, 15)
  text_str = "GRAVITY: ON" if gravity else "GRAVITY: OFF"
  text_surface = font.render(text_str, True, (255, 255, 255))
  text_rect = text_surface.get_rect(center=GBut.center)
  screen.blit(text_surface, text_rect)

  #Кнопка создания шара
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

  #pygame.draw.circle(screen, color, ball["pos"], ball["radius"])

  
  pygame.draw.rect(screen, (10, 10, 10), (0, 700, 1000, 50))
  #print(ball["vel"], f" --- speed: {circle_speed}", " "*20, end = "\r", flush=True)
  

  pygame.display.flip()

pygame.quit()
sys.exit()