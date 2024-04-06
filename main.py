import pygame
import sys

pygame.font.init()

class Card:
    def __init__(self, pos, value):
        self.value = value
        self.pos = pos
        self.image = pygame.Surface((70,100))
        self.rect = self.image.get_rect(topleft = self.pos)
        self.font = pygame.font.SysFont(None, 24)
        self.text = self.font.render(str(self.value), True, (0, 0, 0))

    def draw(self, screen):
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, 70, 100), 2)  # Draw border
        pygame.draw.rect(self.image, (255, 255, 255), (1, 1, 68, 98))  # Fill card
        self.image.blit(self.text, (20, 40))  # Draw value
        screen.blit(self.image, self.pos)

    def is_over(self, pos):
        return self.rect.collidepoint(pos)

pygame.init()
screen = pygame.display.set_mode((800, 600))

cards = [Card((100, 100), 'Ace'), Card((200, 200), '2')]

dragged_card = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for card in cards:
                if card.is_over(pygame.mouse.get_pos()):
                    dragged_card = card
                    # moving the dragged card to the top of the list
                    cards.remove(card)
                    cards.append(card)

        elif event.type == pygame.MOUSEBUTTONUP:
            dragged_card = None

        elif event.type == pygame.MOUSEMOTION:
            if dragged_card is not None :
                dragged_card.pos = pygame.mouse.get_pos()
                dragged_card.rect.topleft = dragged_card.pos

    screen.fill((255, 255, 255))
    for card in cards:
        card.draw(screen)
    pygame.display.update()