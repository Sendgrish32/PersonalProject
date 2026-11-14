import pygame
balls = {"ball0":{"pos": pygame.Vector2(400, 300),
        "vel": pygame.Vector2(0, 0),
        "radius": 50,
        "mass": 20,
        "color": (50, 50, 50),
        "is_clicked": False}}
for x in balls.values():
    cl = x
#balls[cl]["is_clicked"] = True
print(cl, "\n" )
for key, value in list(balls.items()):
    if value is cl:
        balls.pop(key, None)
        break
print(balls)
