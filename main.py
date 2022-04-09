import pygame
import math
from Assets.constants import WIDTH, HEIGHT, WHITE, YELLOW, BLUE,\
     RED, DARK_GRAY, GREEN, BLACK, FPS, LIGHT_BLUE

pygame.init()

FONT = pygame.font.SysFont("comicsans", 16)

FONT = pygame.font.SysFont("comicsans", 16)

FPS = 60
WIDTH, HEIGHT = 1400,1000
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("Planet Simulation")

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU # 1 AU = 100 pixels
    TIMESTEP = 3600 * 24 # 1 day

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.starting_distance = math.sqrt(x*x + y*y)
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win, time_elapsed, name):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        pygame.draw.circle(win, self.color, (x,y), self.radius)

        days_elapsed_text = FONT.render("Days passed: " + str(time_elapsed / (3600*24)), 1, WHITE)
        win.blit(days_elapsed_text, (10, 10))

        years_elapsed_text = FONT.render("Years passed: " + str(time_elapsed / (3600*24) / 365.25), 1, WHITE)
        win.blit(years_elapsed_text, (10,30))

        
        if len(self.orbit) > 2:
            updated_points = []

            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2

                updated_points.append((x, y))
                
            pygame.draw.lines(win, self.color, False, updated_points, 2)

            if not self.sun:
                distance_text = FONT.render(self.name, 1, WHITE)
                win.blit(distance_text, (x - distance_text.get_width() / 2, y + 10))
        
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
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():

    clock = pygame.time.Clock()
    run = True
    time_elapsed = 0

    name = ""
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30, "Sun")
    earth = Planet(1.4959826e8 * 1000, 0, 10, BLUE, 5.9742 * 10**24, "Earth")
    earth.y_vel = -2.9783e4
    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.3 * 10**23, "Mars")
    mars.y_vel = 24.077 * 1000
    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GRAY, 3.30 * 10**23, "Mercury")
    mercury.y_vel = -47.4 * 1000
    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24, "Venus")
    venus.y_vel = -35.02 * 1000
    jupiter = Planet(5.2 * Planet.AU, 0, 30, BLUE, 1.9 * 10**27, "Jupiter")
    jupiter.y_vel = 13.06 * 1000
    saturn =Planet(9.5 * Planet.AU, 0, 25, YELLOW, 5.683 * 10**26, "Saturn")
    saturn.y_vel = 9.68 * 1000
    uranus = Planet(19.8 * Planet.AU, 0, 20, LIGHT_BLUE, 8.681 * 10**25, "Uranus")
    uranus.y_vel = 6.8 * 1000
    neptune = Planet(30 * Planet.AU, 0, 20, BLUE, 1.024 * 10**26, "Neptune")
    neptune.y_vel = 5.43 * 1000
    sun.sun = True

    planets = [sun,mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    while run:

        clock.tick(FPS)

        time_elapsed += Planet.TIMESTEP
        WIN.fill(BLACK)

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                pass

            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN, time_elapsed, name)
        pygame.display.update()

        

    pygame.quit()

main()