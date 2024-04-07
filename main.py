import pygame
import sys
import random  # Добавляем для перемешивания карт

pygame.init()

# Настройки экрана
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Класс для карты
class Card:
    def __init__(self, pos, name, value):  # Исправленная строка
        self.name = name
        self.value = value
        self.pos = pos
        self.image = pygame.Surface((70, 100))
        self.rect = self.image.get_rect(topleft=self.pos)
        self.font = pygame.font.SysFont(None, 24)
        text_name = self.font.render(str(self.name), True, BLACK)
        text_value = self.font.render(str(self.value), True, BLACK)
        self.image.fill(WHITE)
        pygame.draw.rect(self.image, BLACK, (0, 0, 70, 100), 3)
        self.image.blit(text_name, (5, 10))
#        self.image.blit(text_value, (5, 40))

    def draw(self, screen):
        screen.blit(self.image, self.pos)

    def move(self, pos):
        self.pos = pos
        self.rect.topleft = self.pos

# Создаем и перемешиваем набор карт
cards = [
    Card((100, 500), 'Туз', 11),
    Card((200, 500), 'Король', 10),
    Card((300, 500), 'Дама', 9),
    Card((400, 500), 'Валет', 8),
    Card((500, 500), '10', 7),
    Card((600, 500), '9', 6),
    Card((700, 500), '8', 5),
    Card((800, 500), '7', 4),
    Card((900, 500), '6', 3)
]
random.shuffle(cards)  # Перемешиваем карты

# Раздача карт игрокам
player_cards = cards[:2]  # Первые две карты для игрока
ai_cards = cards[2:4]     # Следующие две карты для ИИ/второго игрока
deck_cards = cards[4:]          # Оставшиеся карты в колоде

start_pos_x = 20 # позиция колоды по x
start_pos_y = 250 # позиция колоды по y


# Адаптируем положение карт игрока
for i, card in enumerate(player_cards):
    card.pos = (start_pos_x + 100 + i*100, start_pos_y + 200)
    card.rect = card.image.get_rect(topleft=card.pos)

# Адаптируем положение карт ИИ (в нашем случае не видно)
for i, card in enumerate(ai_cards):
    card.pos = (start_pos_x + 100 + i*100, start_pos_y - 200)  # Расположим их в верхней части экрана
    card.rect = card.image.get_rect(topleft=card.pos)

# Адаптируем положение карт в колоде
for i, card in enumerate(deck_cards):
    card.pos = (start_pos_x + i*5, start_pos_y)  # Расположим их в верхней части экрана
    card.rect = card.image.get_rect(topleft=card.pos)


# Переменные для контроля состояний
dragging = False
selected_card = None

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for card in player_cards:  # Разрешаем перемещать только карты игрока
                if card.rect.collidepoint(event.pos):
                    dragging = True
                    selected_card = card
                    break

        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            selected_card = None

        if event.type == pygame.MOUSEMOTION and dragging:
            if selected_card is not None:
                mouse_x, mouse_y = event.pos
                selected_card.move((mouse_x-35, mouse_y-50))

    screen.fill((0, 128, 0))  # Зеленый цвет фона

    for card in player_cards + ai_cards + deck_cards:  # Отрисовываем карты обоих игроков
        card.draw(screen)

    pygame.display.flip()

pygame.quit()