import pygame
import random

pygame.init()

# Экран
screenwidth, screenheight = 800, 600
screen = pygame.display.set_mode((screenwidth, screenheight))

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Класс для карт
class Card:
    def init(self, pos, name, value):
        self.name = name
        self.value = value
        self.pos = pos
        self.image = pygame.Surface((70, 100))
        self.rect = self.image.get_rect(topleft=self.pos)
        self.font = pygame.font.SysFont(None, 24)
        text_name = self.font.render(str(self.name), True, BLACK)
        self.image.fill(WHITE)
        pygame.draw.rect(self.image, BLACK, (0, 0, 70, 100), 3)
        self.image.blit(text_name, (5, 10))

    def draw(self, screen):
        screen.blit(self.image, self.pos)

    def move(self, pos):
        self.pos = pos
        self.rect.topleft = self.pos

# Класс для кнопки
class Button:
    def init(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline,
                (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(screen, self.color,
                (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.SysFont(None, 24)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2),
                self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

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
player_cards = cards[:2] # Первые две карты для игрока
ai_cards = cards[2:4] # Следующие две карты для ИИ/второго игрока
deck_cards = cards[4:] # Оставшиеся карты в колоде

startposx = 20
startposy = 250

# Адаптируем положение карт игрока
for i, card in enumerate(player_cards):
    card.pos = (startposx + 100 + i*100, startposy + 200)
    card.rect = card.image.get_rect(topleft=card.pos)

# Адаптируем положение карт ИИ (в нашем случае не видно)
for i, card in enumerate(ai_cards):
    card.pos = (startposx + 100 + i*100, startposy - 200)  # Расположим их в верхней части экрана
    card.rect = card.image.get_rect(topleft=card.pos)

# Адаптируем положение карт в колоде
for i, card in enumerate(deck_cards):
    card.pos = (startposx + i*5, startposy)
    card.rect = card.image.get_rect(topleft=card.pos)

# Кнопка "Взять карту"
take_button = Button((0,255,0), 600, 50, 100, 50, 'Взять карту')

# Основной цикл игры----------------------------------------------------------
running = True
dragging = False
selected_card = None

while running:
    pygame.time.delay(100)

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

            if take_button.is_over(event.pos): # Если нажали на кнопку "Взять карту"
                if len(deck_cards) > 0:
                    card = deck_cards.pop()
                    player_cards.append(card)

        if event.type == pygame.MOUSEMOTION and dragging:
            if selected_card is not None:
                mouse_x, mouse_y = event.pos
                selected_card.move((mouse_x-35, mouse_y-50))

    screen.fill((0, 128, 0))  # Зеленый цвет фона

    for card in player_cards + ai_cards + deck_cards:  # Отрисовываем карты обоих игроков
        card.draw(screen)

    take_button.draw(screen) # Отрисовываем кнопку "Взять карту"

# Обновляем экран--------------------------------------------------------------
    pygame.display.flip()

pygame.quit()