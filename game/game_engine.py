import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.target_score = 5  # Default winning score
        self.font = pygame.font.SysFont("Arial", 30)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # Move ball and handle collisions internally
        self.ball.move(self.player, self.ai)

        # Score updates
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x + self.ball.width >= self.width:
            self.player_score += 1
            self.ball.reset()

        # AI movement
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))
    
    def check_game_over(self, screen):
        if self.player_score >= self.target_score or self.ai_score >= self.target_score:
            winner = "Player Wins!" if self.player_score >= self.target_score else "AI Wins!"
            text = self.font.render(winner, True, WHITE)
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2 - 40))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(1000)

            return self.show_replay_menu(screen)  # returns False to exit, True to replay
        return True
    
    def show_replay_menu(self, screen):
        """Display replay options and wait for keypress"""
        options = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit"
        ]
        y = self.height // 2 + 20
        for opt in options:
            txt = self.font.render(opt, True, WHITE)
            rect = txt.get_rect(center=(self.width // 2, y))
            screen.blit(txt, rect)
            y += 40

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    elif event.key == pygame.K_3:
                        self.target_score = 2  # Best of 3 → first to 2
                        waiting = False
                    elif event.key == pygame.K_5:
                        self.target_score = 3  # Best of 5 → first to 3
                        waiting = False
                    elif event.key == pygame.K_7:
                        self.target_score = 4  # Best of 7 → first to 4
                        waiting = False

        self.reset_game()
        return True
    
    def reset_game(self):
        """Reset scores, positions, and ball for a new round"""
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.player.y = self.height // 2 - self.paddle_height // 2
        self.ai.y = self.height // 2 - self.paddle_height // 2

