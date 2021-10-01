import pygame
import math
import random

win_x, win_y = 640, 480 
win = pygame.display.set_mode((win_x, win_y))
clock = pygame.time.Clock()

balls = []
ball_count = 30
fps = 30
colors = [ (0,0,188), (0,188,0), (188,0,0) ]

# Very simple way of determining if two circles collide
def circle_collided(x1, y1, r1, x2, y2, r2):
    # First get the distance between two circles from their centers
    # And then subtract it by the radius of second circle
    # If the distance if smaller than the first circle's radius
    # then it the second circle should be inside the first one
    dx = x2 - x1
    dy = y2 - y1 
    dist = math.sqrt(dx ** 2 + dy ** 2) - r2
    
    return dist <= r1

# Get new velocity after the two objects collide
def new_velocity(u1, m1, u2, m2):
    if m1 == m2:    return u1, u2
    # for reference, wikipedia.org/wiki/Elastic_collision
    v1 = (((m1 - m2) / (m1 + m2)) * u1) + ((2*m2 / (m1 + m2)) * u2)
    v2 = ((2*m1 / (m1 + m2)) * u1) + (((m2 - m1) / (m1 + m2)) * u2)
    return v1, v2

# Every 'ball' contains a list like this format
# [ x, y, x_velocity, y_velocity, mass, radius, color, already_hit? ]

# For the sake of readability, i added these constants to use as list indexes for that ^
X = 0
Y = 1
X_VELOCITY = 2
Y_VELOCITY = 3
MASS = 4
RADIUS = 5
COLOR = 6
ALREADY_HIT = 7

for i in range(ball_count):
    mass = random.randint(5, 25)
    radius = 10
    x = random.randint(radius, win_x - radius)
    y = random.randint(radius, win_y - radius)
    x_velocity = random.randint(-8, 8)
    y_velocity = random.randint(-8, 8)
    color = random.choice(colors)
    balls.append( [x, y, x_velocity, y_velocity, mass, radius, color, False] )

def update():
    global balls
    for ball in balls:
        if ball[ALREADY_HIT]:
            ball[ALREADY_HIT] = False
        pygame.draw.circle(win, ball[COLOR], [ball[X], ball[Y]], ball[RADIUS])
        
        ball[X] += ball[X_VELOCITY]
        ball[Y] += ball[Y_VELOCITY]
        
        # Wall collision
        if ball[X] <= ball[RADIUS]:
            ball[X_VELOCITY] = abs(ball[X_VELOCITY])
        elif ball[X] >= win_x - ball[RADIUS]:
            ball[X_VELOCITY] = -1 * abs(ball[X_VELOCITY])
        if ball[Y] <= ball[RADIUS]:
            ball[Y_VELOCITY] = abs(ball[Y_VELOCITY])
        elif ball[Y] >= win_y - ball[RADIUS]:
            ball[Y_VELOCITY] = -1 * abs(ball[Y_VELOCITY])

        # Now check if this ball has collided with the other balls
        # Make a list containing other balls except the current ball, since we dont want to compare with itself
        tmp = balls.copy()
        tmp.pop(balls.index(ball))
        for target_ball in tmp:
            if not target_ball[ALREADY_HIT]:
                if circle_collided(ball[X], ball[Y], ball[RADIUS], target_ball[X], target_ball[Y], target_ball[RADIUS]):
                    ball[X_VELOCITY], target_ball[X_VELOCITY] = new_velocity(ball[X_VELOCITY], ball[MASS], target_ball[X_VELOCITY], target_ball[MASS])
                    ball[Y_VELOCITY], target_ball[Y_VELOCITY] = new_velocity(ball[Y_VELOCITY], ball[MASS], target_ball[Y_VELOCITY], target_ball[MASS])
                    ball[ALREADY_HIT] = True    

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit()

    win.fill((0,0,0))
    update()
    clock.tick(fps)
    pygame.display.update()


