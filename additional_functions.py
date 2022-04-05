import pygame

def display_text(surface, text, location, size):
    font = pygame.font.Font('pixel_font.ttf', size)

    text = font.render(text, True, 'white')
    text_rect = text.get_rect()
    surface.blit(text, location)

    return text_rect
