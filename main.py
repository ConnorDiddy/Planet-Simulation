import pygame
import math
from Assets.constants import WIDTH, HEIGHT, WHITE, YELLOW, BLUE,\
     RED, DARK_GRAY, GREEN, BLACK, FPS, LIGHT_BLUE

PLAY_BTN = pygame.transform.scale(pygame.image.load('Assets/play.jpg'), (80,70))
PAUSE_BTN = pygame.transform.scale(pygame.image.load('Assets/pause.jpg'), (80,70))

pygame.init()

FONT = pygame.font.SysFont("comicsans", 16)
FONT2 = pygame.font.SysFont("comicsans", 25)

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

    def draw(self, win, time_elapsed, play):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        pygame.draw.circle(win, self.color, (x,y), self.radius)

        days_elapsed_text = FONT.render("Days passed: " + str(time_elapsed / (3600*24)), 1, WHITE)
        play_text = FONT2.render("Play", 1, WHITE)
        pause_text = FONT2.render("Pause", 1, WHITE)
        win.blit(days_elapsed_text, (10, 10))

        years_elapsed_text = FONT.render("Years passed: " + str(time_elapsed / (3600*24) / 365.25), 1, WHITE)
        win.blit(years_elapsed_text, (10,30))

        if play:
            win.blit(PAUSE_BTN, (WIDTH - PAUSE_BTN.get_width() - 20, 20))
            win.blit(pause_text, (WIDTH - play_text.get_width() - 35, 85))

        else:
            win.blit(PLAY_BTN, (WIDTH - PAUSE_BTN.get_width() - 20, 20))
            win.blit(play_text, (WIDTH - play_text.get_width() - 35, 85))
        
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
    earth = Planet(1.4959826e8 * 1000, 0, 12, BLUE, 5.9742 * 10**24, "Earth")
    earth.y_vel = -2.9783e4
    mars = Planet(-1.524 * Planet.AU, 0, 11, RED, 6.3 * 10**23, "Mars")
    mars.y_vel = 24.077 * 1000
    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GRAY, 3.30 * 10**23, "Mercury")
    mercury.y_vel = -47.4 * 1000
    venus = Planet(0.723 * Planet.AU, 0, 11, WHITE, 4.8685 * 10**24, "Venus")
    venus.y_vel = -35.02 * 1000

    play = False
    sun.sun = True

    planets = [sun,mercury, venus, earth, mars]

    while run:

        clock.tick(FPS)

        time_elapsed += Planet.TIMESTEP
        WIN.fill(BLACK)

        if play:
            Planet.TIMESTEP = 3600 * 24
        else:
            Planet.TIMESTEP = 0

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    pass

            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = pos
                if 1300 < x < 1372 and 22 < y < 98:
                    play = not play

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN, time_elapsed, play)
        pygame.display.update()

    pygame.quit()

main()