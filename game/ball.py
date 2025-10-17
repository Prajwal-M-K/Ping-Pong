import pygame
import random

# Initialize sound system once here
pygame.mixer.init()

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

        # --- Load sounds ---
        try:
            self.sound_paddle = pygame.mixer.Sound("assets/paddle_hit.wav")
            self.sound_wall = pygame.mixer.Sound("assets/wall_bounce.wav")
            self.sound_score = pygame.mixer.Sound("assets/score.wav")
        except pygame.error:
            # Handle missing files gracefully
            print("Warning: One or more sound files not found in 'assets/'")

    def move(self, player, ai):
        # Move the ball
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top/bottom walls
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            if hasattr(self, "sound_wall"):
                self.sound_wall.play()

        # Check paddle collisions
        self.check_collision(player, ai)

    def check_collision(self, player, ai):
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()

        if ball_rect.colliderect(player_rect):
            self.velocity_x = abs(self.velocity_x)
            self.x = player_rect.right
            if hasattr(self, "sound_paddle"):
                self.sound_paddle.play()

        elif ball_rect.colliderect(ai_rect):
            self.velocity_x = -abs(self.velocity_x)
            self.x = ai_rect.left - self.width
            if hasattr(self, "sound_paddle"):
                self.sound_paddle.play()

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])
        if hasattr(self, "sound_score"):
            self.sound_score.play()

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
