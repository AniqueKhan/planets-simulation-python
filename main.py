# Imports
import pygame
import math

# Initialization
pygame.init()

# Constants
WIDTH , HEIGHT = 700 , 700
WHITE = (255,255,255)
YELLOW = (255,255,0)
BLUE = (100,149,237)
RED = (189,39,50)
DARK_GRAY = (80,78,81)
BLACK = (0,0,0)
FONT = pygame.font.SysFont("comicsans",16)
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

# Caption
pygame.display.set_caption("Planets Simulation By Anique.")

# Planet Class
class Planet:
    # AU is astronomical units 
    # AU is approximately equal to the distance between the earth and the sun
    AU = 149.6e6 * 1000     # Meters

    # Gravitational Constant
    G = 6.67428e-11

    SCALE = 210 / AU        # 1 AU = 100 pixels
    TIMESTEP = 3600*24      # 1 day  

    def __init__(self,x,y,radius,color,mass):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.mass=mass

        # In order to move in a circle , we must have a velocity in multiple directions
        self.x_velocity = 0
        self.y_velocity = 0

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

    def draw(self,win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points =[]
            for point in self.orbit:
                x,y=point
                x = x*self.SCALE + WIDTH/2
                y = y*self.SCALE + HEIGHT/2
                updated_points.append((x,y))
            pygame.draw.lines(win,self.color,False,updated_points,2)

        
        pygame.draw.circle(win,self.color,(x,y),self.radius)

        if not self.sun:
            distance_text=FONT.render(f'{round(self.distance_to_sun/1000,2)}km',1,WHITE)
            win.blit(distance_text,(x-distance_text.get_width()/2,y-distance_text.get_height()/2))
    
    # This method is going to give the force of attraction between the current and other object   
    def force_of_attraction(self,other):
        other_x,other_y=other.x,other.y
        distance_x=other_x - self.x
        distance_y=other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        # F = (G)(M)(m)/(r^2) # Straight Line Force
        force = self.G * self.mass * other.mass / distance ** 2

        # Angle
        theta = math.atan2(distance_y,distance_x)

        # FX and FY
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x,force_y

    def update_position(self,planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx , fy = self.force_of_attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_velocity += total_fx / self.mass * self.TIMESTEP
        self.y_velocity += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_velocity * self.TIMESTEP
        self.y += self.y_velocity * self.TIMESTEP

        self.orbit.append((self.x,self.y))


# Main event loop
def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0 ,0 ,30 ,YELLOW ,1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU ,0 ,16 ,BLUE ,5.9742 * 10**24)
    mars = Planet(-1.524 * Planet.AU ,0 ,12 ,RED ,6.39 * 10**23)
    mercury = Planet(0.387 * Planet.AU ,0 ,8 ,DARK_GRAY ,3.30 * 10**23)
    venus = Planet(0.723 * Planet.AU ,0 ,14 ,WHITE ,4.8685 * 10**24)

    # The planets are horizontally aligned to the sun 
    # So we need a starting y-velocity for all the planets

    earth.y_velocity = 29.783 * 1000 # Meters
    mars.y_velocity = 24.077 * 1000
    mercury.y_velocity = -47.4 * 1000
    venus.y_velocity = -35.02 * 1000

    planets = [sun,earth,mars,mercury,venus]

    while run:
        clock.tick(60)
        WIN.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run=False
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
        pygame.display.update()
    pygame.quit()
main()
