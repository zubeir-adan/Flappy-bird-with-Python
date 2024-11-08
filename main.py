import pygame
import random
import cairo
import math



# Variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 10
GRAVITY = 1
GAME_SPEED = 5
PIPE_WIDTH = 80 
PIPE_GAP = 150
BIRD_RADIUS = 20
LIVES = 3


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('3D Flappy Sphere')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)


# Bird (Sphere) Class with 3D gradient effect
class Bird:
    def __init__(self):
        self.x = SCREEN_WIDTH // 6
        self.y = SCREEN_HEIGHT // 2
        self.speed = 0

    def update(self):
        self.speed += GRAVITY
        self.y += self.speed

    def bump(self):
        self.speed = -SPEED

    def draw(self, screen):
        # Using Cairo to create a radial gradient to simulate 3D sphere effect
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 2 * BIRD_RADIUS, 2 * BIRD_RADIUS)
        cr = cairo.Context(surface)
        
        # Radial gradient for the 3D effect on the sphere
        gradient = cairo.RadialGradient(BIRD_RADIUS, BIRD_RADIUS, 5, BIRD_RADIUS, BIRD_RADIUS, BIRD_RADIUS)
        gradient.add_color_stop_rgba(0, 0.2, 0.2, 1, 1)  # Center color
        gradient.add_color_stop_rgba(1, 0, 0, 0.6, 1)  # Edge color
        
        cr.set_source(gradient)
        cr.arc(BIRD_RADIUS, BIRD_RADIUS, BIRD_RADIUS, 0, 2 * math.pi)
        cr.fill()

        # Convert Cairo surface to Pygame surface and blit
        ball_surface = pygame.image.frombuffer(surface.get_data(), (2 * BIRD_RADIUS, 2 * BIRD_RADIUS), "ARGB")
        screen.blit(ball_surface, (self.x - BIRD_RADIUS, int(self.y) - BIRD_RADIUS))

# Pipe Class with shading for 3D effect
class Pipe:
    def __init__(self, x, height, inverted):
        self.x = x 
        self.width = PIPE_WIDTH
        self.height = height
        self.inverted = inverted

    def update(self):
        self.x -= GAME_SPEED

    def draw(self, screen):
        # Use Cairo for shading effect on the pipes
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, PIPE_WIDTH, SCREEN_HEIGHT)
        cr = cairo.Context(surface)
        
        # Draw pipe with shading for 3D effect
        cr.rectangle(0, 0, PIPE_WIDTH, SCREEN_HEIGHT)
        gradient = cairo.LinearGradient(0, 0, PIPE_WIDTH, 0)
        gradient.add_color_stop_rgba(0, 140.2, 140.8, 140.2, 1)  # Left side
        gradient.add_color_stop_rgba(1, 255, 255, 0.8, 1)      # Right side
        cr.set_source(gradient)
        cr.fill()

        # Convert Cairo surface to Pygame surface
        pipe_surface = pygame.image.frombuffer(surface.get_data(), (PIPE_WIDTH, SCREEN_HEIGHT), "ARGB")

        # Draw pipe in the correct position
        if self.inverted:
            screen.blit(pipe_surface, (self.x, 0), (0, SCREEN_HEIGHT - self.height, PIPE_WIDTH, self.height))
        else:
            screen.blit(pipe_surface, (self.x, SCREEN_HEIGHT - self.height))

    def collide(self, bird):
        if bird.x + BIRD_RADIUS > self.x and bird.x - BIRD_RADIUS < self.x + self.width:
            if self.inverted and bird.y - BIRD_RADIUS < self.height:
                return True
            if not self.inverted and bird.y + BIRD_RADIUS > SCREEN_HEIGHT - self.height:
                return True
        return False


