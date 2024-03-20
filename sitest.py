# -*- coding: utf-8 -*-
"""
Created on Sun May 28 01:56:04 2023

@author: Asus
"""
import pygame
import random
import sys


# Initialize Pygame
pygame.init()

# Window dimensions
WIDTH = 800
HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0) 
GREEN = (0, 255, 0)

# Game states
MENU = 0
GAME = 1
GAME_OVER = 2
GAME_WON = 4

# Button states
PLAY = 0
PAUSE = 1

# Options in the start menu
OPTIONS = ["New Game", "Exit Game"]

# Set up the window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Impact")

# Load images
player_ship_img = pygame.image.load("player_ship.png").convert_alpha()
enemy_images = [
    pygame.image.load("enemy_1.png").convert_alpha(),
    pygame.image.load("enemy_2.png").convert_alpha(),
    pygame.image.load("enemy_3.png").convert_alpha(),
]
boss_img = pygame.image.load("boss1.png").convert_alpha()

# Player ship variables
player_ship_x = WIDTH // 2 - player_ship_img.get_width() // 2
player_ship_speed = 0

# Bullets
bullets = []
enemy_bullets = []
boss_bullets = []

# Enemies
enemies = []

# Boss variables
boss_x = WIDTH // 2 - boss_img.get_width() // 2
boss_speed = 3
boss_alive = False
boss_health = 10

# Game variables
state = MENU
selected_option = 0
button_state = PLAY
score = 0
life = 100

# AI behavior variables
enemy_fire_delay = 1000  # Delay between enemy shots (in milliseconds)
enemy_fire_timer = pygame.time.get_ticks()  # Timer for enemy shots
boss_fire_delay = 500  # Delay between boss shots (in milliseconds)
boss_fire_timer = pygame.time.get_ticks()  # Timer for boss shots

# Fonts
title_font = pygame.font.Font(None, 72)
text_font = pygame.font.Font(None, 36)

# Clock
clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if state == MENU:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(OPTIONS)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(OPTIONS)
                elif event.key == pygame.K_RETURN:
                    if OPTIONS[selected_option] == "New Game":
                        state = GAME
                        button_state = PLAY
                        player_ship_x = WIDTH // 2 - player_ship_img.get_width() // 2
                        player_ship_speed = 0
                        bullets.clear()
                        enemies.clear()
                        boss_bullets.clear()
                        score = 0
                        life = 100
                    elif OPTIONS[selected_option] == "Exit Game":
                        pygame.quit()
                        sys.exit()

            elif state == GAME:
                if button_state == PLAY:
                    if event.key == pygame.K_LEFT:
                        player_ship_speed = -5
                    elif event.key == pygame.K_RIGHT:
                        player_ship_speed = 5
                    elif event.key == pygame.K_SPACE:
                        bullet_x = player_ship_x + player_ship_img.get_width() // 2
                        bullet_y = HEIGHT - player_ship_img.get_height() - 50
                        bullet = pygame.Rect(bullet_x, bullet_y, 2, 5)
                        bullets.append(bullet)

        if event.type == pygame.KEYUP:
            if state == GAME:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_ship_speed = 0

    window.fill(BLACK)

    if state == MENU:
        # Draw title
        title_text = title_font.render("Space Impact", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        window.blit(title_text, title_rect)

        # Draw menu options
        for i, option in enumerate(OPTIONS):
            text = text_font.render(option, True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
            if i == selected_option:
                pygame.draw.rect(window, GRAY, text_rect.inflate(10, 10))
            window.blit(text, text_rect)

    elif state == GAME:
        # Move and draw player ship
        player_ship_x += player_ship_speed
        if player_ship_x < 0:
            player_ship_x = 0
        elif player_ship_x > WIDTH - player_ship_img.get_width():
            player_ship_x = WIDTH - player_ship_img.get_width()

        player_ship_rect = player_ship_img.get_rect(topleft=(player_ship_x, HEIGHT - player_ship_img.get_height() - 50))
        window.blit(player_ship_img, player_ship_rect)

        # Move and draw bullets
        for bullet in bullets:
            pygame.draw.rect(window, WHITE, bullet)  # Draw a rectangle for bullets
            bullet.y -= 5  # Adjust bullet speed as needed

            # Check collision with enemies
            for enemy in enemies:
                enemy_rect = enemy["image"].get_rect(topleft=enemy["position"])
                if bullet.colliderect(enemy_rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1

            # Remove bullets that go off the screen
            if bullet.y < 0:
                bullets.remove(bullet)

        # Spawn enemies
        if len(enemies) == 0 and not boss_alive:
           enemy_x = random.randint(0, WIDTH - enemy_images[0].get_width())
           enemy_y = -enemy_images[0].get_height()
           enemy_img = random.choice(enemy_images)
           enemy = {"image": enemy_img, "position": (enemy_x, enemy_y), "speed": 1, "fire_timer": 0}
           enemies.append(enemy)

        if len(enemies) < random.randint(1, 10) and not boss_alive:
           if random.random() < 1 or len(enemies) == 0:  # Adjust the probability to control enemy spawn rate
              enemy_x = random.randint(0, WIDTH - enemy_images[0].get_width())
              enemy_y = -enemy_images[0].get_height()
              enemy_img = random.choice(enemy_images)
              enemy = {"image": enemy_img, "position": (enemy_x, enemy_y), "speed": 1, "fire_timer": 0}
              enemies.append(enemy)
        # Remove enemies that go beyond the window boundaries
        enemies_to_remove = []
        for enemy in enemies:
            enemy_x, enemy_y = enemy["position"]
            if enemy_y > HEIGHT:
               enemies_to_remove.append(enemy)

        for enemy in enemies_to_remove:
            enemies.remove(enemy)



        # Move and draw enemies
        for enemy in enemies:
            enemy_rect = enemy["image"].get_rect(topleft=enemy["position"])
            window.blit(enemy["image"], enemy_rect)
            enemy["position"] = (enemy["position"][0], enemy["position"][1] + enemy["speed"])

            # Check collision with player ship
            if enemy_rect.colliderect(player_ship_rect):
                life -= 10
                if life <= 0:
                    state = GAME_OVER  # Game over, go to the game over state

            # Check collision with player bullets
            for bullet in bullets:
                if enemy_rect.colliderect(bullet):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1

            # Enemy AI behavior: Fire bullets
            for enemy in enemies:
                   if pygame.time.get_ticks() - enemy["fire_timer"] >= enemy_fire_delay:
                      enemy_bullet_x = enemy["position"][0] + enemy["image"].get_width() // 2
                      enemy_bullet_y = enemy["position"][1] + enemy["image"].get_height()
                      enemy_bullet = pygame.Rect(enemy_bullet_x, enemy_bullet_y, 2, 5)
                      enemy_bullets.append(enemy_bullet)
                      enemy["fire_timer"] = pygame.time.get_ticks()


        # Move and draw enemy bullets
        for bullet in enemy_bullets:
            pygame.draw.rect(window, RED, bullet)  # Draw a rectangle for enemy bullets
            bullet.y += 2  # Adjust bullet speed as needed

            # Check collision with player ship
            if bullet.colliderect(player_ship_rect):
                life -= 20
                enemy_bullets.remove(bullet)
                if life <= 0:
                    state = GAME_OVER  # Game over, go to the game over state

            # Remove bullets that go off the screen
            if bullet.y > HEIGHT:
                enemy_bullets.remove(bullet)

        # Spawn boss
        if score >= 25 and not boss_alive:
            boss_alive = True
            boss_health = 100
            boss_x = WIDTH // 2 - boss_img.get_width() // 2

        # Boss behavior
        if boss_alive:
            boss_rect = boss_img.get_rect(topleft=(boss_x, 100))
            window.blit(boss_img, boss_rect)
        

            # Boss AI behavior: Move towards the player ship
            if player_ship_x + player_ship_img.get_width() // 2 < boss_x + boss_img.get_width() // 2:
                boss_x -= boss_speed
            elif player_ship_x + player_ship_img.get_width() // 2 > boss_x + boss_img.get_width() // 2:
                boss_x += boss_speed

            # Boss AI behavior: Fire bullets
            if pygame.time.get_ticks() - boss_fire_timer >= boss_fire_delay:
                boss_bullet_x = boss_rect.x + boss_rect.width // 2
                boss_bullet_y = boss_rect.y + boss_rect.height
                boss_bullet = pygame.Rect(boss_bullet_x, boss_bullet_y, 2, 5)
                boss_bullets.append(boss_bullet)
                boss_fire_timer = pygame.time.get_ticks()

            # Draw boss health
            boss_health_text = text_font.render(f"Boss Health: {boss_health}", True, WHITE)
            window.blit(boss_health_text, (WIDTH - boss_health_text.get_width() - 10, 50))

            # Boss AI behavior: Check collision with player bullets
            for bullet in bullets:
                if boss_rect.colliderect(bullet):
                    bullets.remove(bullet)
                    boss_health -= 1
                    if boss_health <= 0:
                        state = GAME_WON  # Game over, go to the game over state
                        boss_alive = False
                        score += 10
                        break

            # Move and draw boss bullets
            for bullet in boss_bullets:
                pygame.draw.rect(window, RED, bullet)  # Draw a rectangle for boss bullets
                bullet.y += 2  # Adjust bullet speed as needed
            

                # Check collision with player ship
                if bullet.colliderect(player_ship_rect):
                    life -= 20
                    boss_bullets.remove(bullet)
                    if life <= 0:
                        state = GAME_OVER  # Game over, go to the game over state

                # Remove bullets that go off the screen
                if bullet.y > HEIGHT:
                    boss_bullets.remove(bullet)

        # Update score display
        score_text = text_font.render(f"Score: {score}", True, WHITE)
        window.blit(score_text, (10, 10))

        # Update life display
        life_text = text_font.render(f"Life: {life}", True, WHITE)
        window.blit(life_text, (WIDTH - life_text.get_width() - 10, 10))
    

    elif state == GAME_OVER:
        # Draw game over message
        game_over_text = title_font.render("Game Over", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        window.blit(game_over_text, game_over_rect)

        # Draw final score
        final_score_text = text_font.render(f"Final Score: {score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        window.blit(final_score_text, final_score_rect)
        
        pygame.display.flip()
        
        # Wait for 2 seconds (2000 milliseconds)
        pygame.time.wait(2000)

        state = MENU
        # Reset game variables and states
    elif state == GAME_WON:
        # Draw "You've Won" message
        won_text = title_font.render("You've Won!", True, WHITE)
        won_rect = won_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        window.blit(won_text, won_rect)

        # Draw final score
        final_score_text = text_font.render(f"Final Score: {score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        window.blit(final_score_text, final_score_rect)
    
        pygame.display.flip()
     
    # Wait for 2 seconds (2000 milliseconds)
        pygame.time.wait(2000)

        state = MENU
    # Reset game variables and states
        
    pygame.display.flip()
    
    clock.tick(60)
