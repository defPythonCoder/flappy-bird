import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Text Box Example")

# Set up font
font = pygame.font.Font(None, 36)

# Function to display text on screen
def display_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to draw the text box
def draw_text_box(x, y, width, height, text, active):
    color = (255, 255, 255) if active else (200, 200, 200)
    pygame.draw.rect(screen, color, (x, y, width, height), 2)
    display_text(text, x + 5, y + 5, (0, 0, 0))

# Main game loop
def main():
    text = ""
    active = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if text_box_rect.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print("Entered text:", text)
                        text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((255, 255, 255))
        text_box_rect = pygame.Rect(100, 100, 200, 50)
        draw_text_box(*text_box_rect, text, active)
        pygame.display.flip()

if __name__ == "__main__":
    main()
