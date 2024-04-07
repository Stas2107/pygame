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
GREY = (100, 100, 100)

show_ai_cards = False  # Показывать ли карты ИИ

# Класс для карты--------------------------------------------------------------
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
        self.image.blit(text_value, (5, 40))

    def draw(self, screen, show_value=True):
        screen.blit(self.image, self.pos)
        if not show_value:
            pygame.draw.rect(screen, GREY, self.rect)  # Закрываем карту серым прямоугольником

    def move(self, pos):
        self.pos = pos
        self.rect.topleft = self.pos

# Класс для кнопки-------------------------------------------------------------
class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
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


class Label:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont(None, 24)

    def draw(self, screen):
        text = self.font.render(self.text, True, BLACK)
        screen.blit(text, (self.x, self.y))


total_player_wins = 0
total_ai_wins = 0




# Создаем и перемешиваем набор карт---------------------------------------------
cards = [
    Card((100, 500), 'Туз', 11),
    Card((200, 500), 'Король', 4),
    Card((300, 500), 'Дама', 3),
    Card((400, 500), 'Валет', 2),
    Card((500, 500), '10', 10),
    Card((600, 500), '9', 9),
    Card((700, 500), '8', 8),
    Card((800, 500), '7', 7),
    Card((900, 500), '6', 6)
]
random.shuffle(cards)  # Перемешиваем карты

# Раздача карт игрокам
player_cards = cards[:2]  # Первые две карты для игрока
ai_cards = cards[2:4]     # Следующие две карты для ИИ/второго игрока
deck_cards = cards[4:]          # Оставшиеся карты в колоде

start_pos_x = 20 # позиция колоды по x
start_pos_y = 250 # позиция колоды по y


player_score = 0 # счет игрока
ai_score = sum(card.value for card in ai_cards)     # счет ИИ



# Адаптируем положение карт игрока-------------------------------------------
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


# Кнопка "Взять"---------------------------------------------------------------
take_button = Button(GREY, start_pos_x, start_pos_y, 70, 100, 'Взять')
open_button = Button(GREY, 600, 200, 130, 50, 'Открыть карты')
reboot_button = Button(GREY, 600, 100, 130, 50, 'Начать заново')

label_player = Label(f'Ваши очки:{player_cards[0].value + player_cards[1].value}',    600, 300)
label_ai = Label(f'Очки ИИ:{ai_cards[0].value + ai_cards[1].value}', 600, 330)
label_total_wins = Label(f'Счет игрока: {total_player_wins} Счет ИИ: {total_ai_wins}', 300, 10)


# Переменные для контроля состояний
dragging = False
selected_card = None

# Основной игровой цикл---------------------------------------------------------
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
# Кнопка "Взять карту"--------------------------------------------------------
            if take_button.is_over(event.pos): # Если нажали на кнопку "Взять карту"
                if len(deck_cards) > 0:
                    card = deck_cards.pop()
                    player_cards.append(card)
                    card.pos = (start_pos_x + len(player_cards)*100, start_pos_y + 200)
                    card.rect = card.image.get_rect(topleft=card.pos)
                    player_score = sum(card.value for card in player_cards)  # Обновляем счет игрока
                    label_player.text = f'Ваши очки:{player_score}'
                elif len(deck_cards) == 0:
                    take_button.text = 'Колода пуста'

# Кнопка "Открыть карты"--------------------------------------------------------
            if open_button.is_over(event.pos): # Если нажали на кнопку "Открыть карты"
                player_score = sum(card.value for card in player_cards)  # Обновляем счет игрока
                ai_score = sum(card.value for card in ai_cards)  # Обновляем счет ИИ
                label_ai.text = f'Очки ИИ:{ai_score}'
                show_ai_cards = True
                if player_score > ai_score and player_score <= 21:
                    total_player_wins += 1
                    label_total_wins.text = f'Игрок:{total_player_wins} AI: {total_ai_wins}'
                elif player_score < ai_score and ai_score <= 21:
                    total_ai_wins += 1
                    label_total_wins.text = f'Игрок:{total_player_wins} AI: {total_ai_wins}'
                elif player_score == ai_score and player_score <= 21:
                    label_total_wins.text = f'Игрок:{total_player_wins} AI: {total_ai_wins}'
                elif ai_score > 21:
                    total_player_wins += 1
                    label_total_wins.text = f'Игрок:{total_player_wins} AI: {total_ai_wins}'
                else:
                    label_total_wins.text = f'Игрок:{total_player_wins} AI: {total_ai_wins}'

# Кнопка "Перемешать карты"--------------------------------------------------------
            if reboot_button.is_over(event.pos): # Если нажали на кнопку "Перемешать карты"
                random.shuffle(cards) # Перемешивание карт
                player_cards = cards[:2] # Первые две карты для игрока
                ai_cards = cards[2:4] # Первые две карты для ИИ
                deck_cards = cards[4:]
                for i, card in enumerate(player_cards): # Адаптируем положение карт игрока
                    card.pos = (start_pos_x + 100 + i * 100, start_pos_y + 200)
                    card.rect = card.image.get_rect(topleft=card.pos)
                for i, card in enumerate(ai_cards): # Адаптируем положение карт ИИ
                    card.pos = (start_pos_x + 100 + i * 100, start_pos_y - 200)
                    card.rect = card.image.get_rect(topleft=card.pos)
                show_ai_cards = False  # Скрываем карты ИИ
                player_score = sum(card.value for card in player_cards)  # Обновляем счет игрока
                ai_score = sum(card.value for card in ai_cards)  # Обновляем счет ИИ
                label_player.text = f'Ваши очки:{player_score}'
                label_ai.text = f'Очки ИИ:{ai_score}'





        # Логика для AI - берет еще одну карту если его счет меньше 10
        if ai_score < 15 and len(deck_cards) > 0:  # Добавляем условие наличия карт в колоде
            card = deck_cards.pop()
            ai_cards.append(card)
            card.pos = (start_pos_x + len(ai_cards)*100, start_pos_y - 200)
            card.rect = card.image.get_rect(topleft=card.pos)
            ai_score = sum(card.value for card in ai_cards)  # Пересчитываем счет AI
            label_ai.text = f'Очки ИИ:{ai_score}'  # Обновляем текст очков AI




        if event.type == pygame.MOUSEMOTION and dragging:
            if selected_card is not None:
                mouse_x, mouse_y = event.pos
                selected_card.move((mouse_x-35, mouse_y-50))

    screen.fill((0, 128, 0))  # Зеленый цвет фона



    for card in ai_cards:
        card.draw(screen, show_value=show_ai_cards)
    for card in player_cards:
        card.draw(screen)



    take_button.draw(screen) # Отрисовываем кнопку "Взять карту"
    open_button.draw(screen) # Отрисовываем кнопку "Открыть карты"
    reboot_button.draw(screen)

    label_player.draw(screen)
#    label_ai.draw(screen)
    label_total_wins.draw(screen)

# Обновляем экран--------------------------------------------------------------
    pygame.display.flip()

pygame.quit()