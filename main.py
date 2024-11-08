import pygame
import random
import cairo
import math

# Variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 10
GRAVITY = 1
PIPE_WIDTH = 80
PIPE_GAP = 150
BIRD_RADIUS = 20
LIVES = 3

# Difficulty settings
DIFFICULTY_SETTINGS = {
    "Easy": 3,
    "Medium": 5,
    "Hard": 8
}

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
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 2 * BIRD_RADIUS, 2 * BIRD_RADIUS)
        cr = cairo.Context(surface)
        
        gradient = cairo.RadialGradient(BIRD_RADIUS, BIRD_RADIUS, 5, BIRD_RADIUS, BIRD_RADIUS, BIRD_RADIUS)
        gradient.add_color_stop_rgba(0, 0.2, 0.2, 1, 1)  # Center color
        gradient.add_color_stop_rgba(1, 0, 0, 0.6, 1)  # Edge color
        
        cr.set_source(gradient)
        cr.arc(BIRD_RADIUS, BIRD_RADIUS, BIRD_RADIUS, 0, 2 * math.pi)
        cr.fill()

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
        self.x -= game_speed

    def draw(self, screen):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, PIPE_WIDTH, SCREEN_HEIGHT)
        cr = cairo.Context(surface)
        
        cr.rectangle(0, 0, PIPE_WIDTH, SCREEN_HEIGHT)
        gradient = cairo.LinearGradient(0, 0, PIPE_WIDTH, 0)
        gradient.add_color_stop_rgba(0, 0.55, 0.55, 0.55, 1)
        gradient.add_color_stop_rgba(1, 1, 1, 0.8, 1)
        cr.set_source(gradient)
        cr.fill()

        pipe_surface = pygame.image.frombuffer(surface.get_data(), (PIPE_WIDTH, SCREEN_HEIGHT), "ARGB")
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

# Functions
def create_pipes():
    height = random.randint(100, 400)
    top_pipe = Pipe(SCREEN_WIDTH, height, True)
    bottom_pipe = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT - height - PIPE_GAP, False)
    return top_pipe, bottom_pipe

def display_lives(lives):
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))

def game_intro():
    global game_speed
    intro = True
    while intro:
        screen.fill((0, 0, 0))
        title_text = font.render("3D Flappy Sphere", True, (255, 255, 255))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))

        easy_text = font.render("Press E for Easy", True, (0, 255, 0))
        medium_text = font.render("Press M for Medium", True, (255, 255, 0))
        hard_text = font.render("Press H for Hard", True, (255, 0, 0))
        
        screen.blit(easy_text, (SCREEN_WIDTH // 2 - easy_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(medium_text, (SCREEN_WIDTH // 2 - medium_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
        screen.blit(hard_text, (SCREEN_WIDTH // 2 - hard_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    game_speed = DIFFICULTY_SETTINGS["Easy"]
                    intro = False
                elif event.key == pygame.K_m:
                    game_speed = DIFFICULTY_SETTINGS["Medium"]
                    intro = False
                elif event.key == pygame.K_h:
                    game_speed = DIFFICULTY_SETTINGS["Hard"]
                    intro = False

def end_screen():
    end = True
    while end:
        screen.fill((0, 0, 0))
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        retry_text = font.render("Press R to Retry", True, (0, 255, 0))
        quit_text = font.render("Press Q to Quit", True, (255, 0, 0))
        
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Retry
                elif event.key == pygame.K_q:
                    return False  # Quit

# Main Game Loop
game_intro()

while True:
    bird = Bird()
    pipes = list(create_pipes())
    lives = LIVES
    running = True

    while running:
        screen.fill((0, 0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.bump()

        # Update game state
        bird.update()
        for pipe in pipes:
            pipe.update()

        # Check for collisions
        if any(pipe.collide(bird) for pipe in pipes) or bird.y >= SCREEN_HEIGHT - BIRD_RADIUS:
            lives -= 1
            if lives <= 0:
                running = False  # End game loop

        # Generate new pipes when previous ones go off-screen
        if pipes[0].x < -PIPE_WIDTH:
            pipes = pipes[2:] + list(create_pipes())

        # Draw everything
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)
        display_lives(lives)

        pygame.display.flip()
        clock.tick(30)

    if not end_screen():  # Show end screen and decide whether to retry or quit
        break  # Exit the game loop if the player chooses to quit
