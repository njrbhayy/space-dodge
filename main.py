import pygame
import random
import time
import pickle

pygame.font.init()

WIDTH, HEIGHT = 1000, 700   # width and height of the window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Dodge')

BG = pygame.transform.scale(pygame.image.load('bg.jpeg'), (WIDTH, HEIGHT))
FONT = pygame.font.SysFont('Consolas', 30)

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5

PROJECTILE_WIDTH = 10
PROJECTILE_HEIGHT = 20
PROJECTILE_VEL = 3

def draw(player, elapsed_time, projectiles, high_score):
    WINDOW.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, 'white')
    high_score_text = FONT.render(f"Highest Time: {high_score}s", 1, "white")

    WINDOW.blit(time_text, (20, 20))    
    WINDOW.blit(high_score_text, (WIDTH - high_score_text.get_width() - 20, 20))

    pygame.draw.rect(WINDOW, "red", player)

    for projectile in projectiles:
        pygame.draw.rect(WINDOW, 'white', projectile)

    pygame.display.update()

def main():
    running = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0
    
    try:
        with open('high_score.dat', 'rb') as file:
            high_score = pickle.load(file)
    except:
        high_score = 0

    projectiles_add_increment = 2000
    projectiles_count = 0

    projectiles = []
    hit = False

    while running:
        projectiles_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if projectiles_count > projectiles_add_increment:
            for _ in range(3):
                projectile_x = random.randint(0, WIDTH - PROJECTILE_WIDTH)
                projectile = pygame.Rect(projectile_x, -PROJECTILE_HEIGHT, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
                projectiles.append(projectile)

            projectiles_add_increment = max(200, projectiles_add_increment - 50)
            projectiles_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL

        for projectile in projectiles[:]:
            projectile.y += PROJECTILE_VEL
            if projectile.y > HEIGHT:
                projectiles.remove(projectile)
            elif projectile.y >= player.y and projectile.colliderect(player):
                projectiles.remove(projectile)
                hit = True
                
                if high_score < round(elapsed_time):
                    high_score = round(elapsed_time)

                break

        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            

            with open('high_score.dat', 'wb') as file:
                pickle.dump(high_score, file)

            WINDOW.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))

            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, projectiles, high_score)

    pygame.quit()


if __name__ == "__main__":
    main()