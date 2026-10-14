import sys, pygame

pygame.init()

width = 1000
height = 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Physical Engine")
clock = pygame.time.Clock()
FPS = 60
font = pygame.font.SysFont("arial", 18, bold=True)


circle_pos = pygame.Vector2(400, 300)
circle_vel = pygame.Vector2(0, 0)  # Вектор скорости
circle_rad = 50
color = (50, 50, 50)

g = 980  # Ускорение свободного падения
bounce = 0.75  # Коэффициент упругости
gravity = False

# --- ИНТЕРФЕЙС И СОСТОЯНИЯ ---
is_dragged = False
prev_mouse_pos = pygame.Vector2(0, 0)

rect = pygame.Rect(795, 5, 200, 30)
ButCol = (100, 100, 100)

# Main
running = True
while running:
  dt = clock.tick(FPS) / 1000.0

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    elif event.type == pygame.MOUSEBUTTONDOWN: #нажатие ЛКМ
      if event.button == 1:
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

        if mouse_pos.distance_to(circle_pos) <= circle_rad: #взаимодействие с шаром
          color = (70, 70, 70)
          is_dragged = True
          circle_vel = pygame.Vector2(0, 0)
          prev_mouse_pos = mouse_pos.copy()

        if rect.collidepoint(mouse_pos): #нажатие кнопки гравитации
          gravity = not gravity
          ButCol = (0, 150, 0) if gravity else (100, 100, 100)

    elif event.type == pygame.MOUSEBUTTONUP:
      if event.button == 1:
        color = (50, 50, 50)
        if is_dragged:
          is_dragged = False
          mouse_pos = pygame.Vector2(event.pos)
          # Расчет начальной скорости при броске (v = ds / dt)
          if dt > 0:
            circle_vel = (mouse_pos - prev_mouse_pos) / dt

    elif event.type == pygame.MOUSEMOTION:
      if is_dragged:
        prev_mouse_pos = circle_pos.copy()
        circle_pos = pygame.Vector2(event.pos)

  # 2. ФИЗИКА И ЛОГИКА (Работает, пока шар не перетаскивают мышью)
  if not is_dragged:
    # Применение гравитации
    if gravity:
      circle_vel.y += g * dt

    # Движение
    circle_pos += circle_vel * dt

    # --- ОТСКОК ОТ ПОЛА (Y = 700) ---
    if circle_pos.y + circle_rad >= 700:
      circle_pos.y = 700 - circle_rad
      circle_vel.y = -circle_vel.y * bounce
      if abs(circle_vel.y) < 15:
        circle_vel.y = 0

    # --- ОТСКОК ОТ ПОТОЛКА (Y = 0) ---
    if circle_pos.y - circle_rad <= 0:
      circle_pos.y = circle_rad
      circle_vel.y = -circle_vel.y * bounce

    # --- ОТСКОК ОТ ЛЕВОЙ СТЕНЫ (X = 0) ---
    if circle_pos.x - circle_rad <= 0:
      circle_pos.x = circle_rad
      circle_vel.x = -circle_vel.x * bounce

    # --- ОТСКОК ОТ ПРАВОЙ СТЕНЫ (X = width) ---
    elif circle_pos.x + circle_rad >= width:
      circle_pos.x = width - circle_rad
      circle_vel.x = -circle_vel.x * bounce
    # --- СКОРОСТЬ ШАРА ---
    circle_speed_sqrt = circle_vel.x**2 + circle_vel.y**2
    circle_speed = circle_speed_sqrt ** 0.5

  # 3. ОТРИСОВКА
  screen.fill((30, 30, 30))

  # Кнопка
  pygame.draw.rect(screen, ButCol, rect, 0, 15)
  text_str = "GRAVITY: ON" if gravity else "GRAVITY: OFF"
  text_surface = font.render(text_str, True, (255, 255, 255))
  text_rect = text_surface.get_rect(center=rect.center)
  screen.blit(text_surface, text_rect)

  # Шар
  pygame.draw.circle(screen, color, circle_pos, circle_rad)

  
  pygame.draw.rect(screen, (10, 10, 10), (0, 700, 1000, 50))
  print(circle_vel, f" --- speed: {circle_speed}", " "*20, end = "\r", flush=True)
  

  pygame.display.flip()

pygame.quit()
sys.exit()