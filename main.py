import pygame
import math

pygame.init()

WHITE = (255,255,255)
YELLOW = (255,255,0)
BLUE = (100,149,255)
RED = (188, 39, 50)
DARK_GRAY = (80,78,81)
GREEN = (0, 255, 0)

FPS = 60
WIDTH, HEIGHT = 1000,1000
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("Planet Simulation")

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU # 1 AU = 100 pixels
    TIMESTEP = 3600*24 # 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        pygame.draw.circle(win, self.color, (x,y), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0

        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP





def main():

    clock = pygame.time.Clock()
    run = True

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.3 * 10**23)
    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GRAY, 3.30 * 10**23)
    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)

    sun.sun = True

    planets = [sun, earth, mars, mercury, venus]

    while run:

        clock.tick(FPS)
        #WIN.fill(WHITE)
        #pygame.display.update()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.draw(WIN)
    
        pygame.display.update()
        
    
    pygame.quit()

main()