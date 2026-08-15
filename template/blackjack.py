import pygame
import sys
import random
import os

pygame.init()
pygame.mixer.init()

# =========================
# WINDOW
# =========================
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")
clock = pygame.time.Clock()

# =========================
# PATHS
# =========================
BASE_DIR = r"C:\Users\jtam2\OneDrive\Desktop\pygametest\template"

CARD_DIR = os.path.join(
    BASE_DIR,
    "boardgamePack_v2",
    "PNG",
    "Cards"
)

# =========================
# GAME STATES
# =========================
MAIN_MENU = "main_menu"
GAMEPLAY = "gameplay"

# =========================
# CARDS
# =========================
SUITS = ['S', 'H', 'D', 'C']
RANKS = ['A'] + [str(n) for n in range(2, 11)] + ['J', 'Q', 'K']

CARD_VALUES = {
    **{str(n): n for n in range(2, 11)},
    'J': 10,
    'Q': 10,
    'K': 10,
    'A': 11
}

SUIT_NAMES = {
    'S': 'Spades',
    'H': 'Hearts',
    'D': 'Diamonds',
    'C': 'Clubs'
}

# =========================
# BUTTONS
# =========================
BUTTON_W = 120
BUTTON_H = 50

# =========================
# LOAD CARD IMAGES
# =========================
CARD_IMAGES = {}

def load_card_images():

    for suit in SUITS:
        for rank in RANKS:

            filename = f"card{SUIT_NAMES[suit]}{rank}.png"

            path = os.path.join(CARD_DIR, filename)

            try:
                image = pygame.image.load(path).convert_alpha()
                image = pygame.transform.scale(image, (90, 130))

                CARD_IMAGES[(rank, suit)] = image

            except Exception as e:
                print(f"Missing image: {path}")
                print(e)

    # Back card
    back_path = os.path.join(CARD_DIR, "cardBack_red2.png")

    try:
        back = pygame.image.load(back_path).convert_alpha()
        back = pygame.transform.scale(back, (90, 130))
        CARD_IMAGES["BACK"] = back

    except:
        CARD_IMAGES["BACK"] = None

# =========================
# SOUNDS
# =========================
CARD_PLACE_SOUND = pygame.mixer.Sound(
    os.path.join(
        BASE_DIR,
        "boardgamePack_v2",
        "BonusAudio",
        "cardPlace1.ogg"
    )
)

CARD_PLACE_SOUND.set_volume(0.4)

# =========================
# TEXT
# =========================
def draw_text(surface, text, size, color, x, y, center=True):

    font = pygame.font.SysFont(None, size)

    txt = font.render(text, True, color)

    rect = txt.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    surface.blit(txt, rect)


def draw_multiline_text(surface, text, size, color, x, y):

    lines = text.splitlines()

    for i, line in enumerate(lines):

        draw_text(
            surface,
            line,
            size,
            color,
            x,
            y + i * (size + 10)
        )


# =========================
# DECK
# =========================
def create_deck():

    return [
        (rank, suit)
        for suit in SUITS
        for rank in RANKS
    ]


def create_shoe(num_decks=6):

    shoe = []

    for _ in range(num_decks):
        shoe.extend(create_deck())

    random.shuffle(shoe)

    return shoe


# =========================
# HAND VALUE
# =========================
def hand_value(hand):

    value = 0
    aces = 0

    for rank, _ in hand:

        value += CARD_VALUES[rank]

        if rank == 'A':
            aces += 1

    while value > 21 and aces:

        value -= 10
        aces -= 1

    return value


# =========================
# DRAW HAND
# =========================
def draw_hand(surface, hand, x, y, hide_first=False):

    for i, card in enumerate(hand):

        card_x = x + i * 100

        if i == 0 and hide_first:

            back = CARD_IMAGES["BACK"]

            if back:
                surface.blit(back, (card_x, y))

        else:

            image = CARD_IMAGES.get(card)

            if image:
                surface.blit(image, (card_x, y))
# =========================
# PLAY SOUND
# =========================

def play_card_sound():
    pygame.mixer.find_channel(True).play(CARD_PLACE_SOUND)

# =========================
# DEAL
# =========================
def deal_initial(state):

    if len(state['shoe']) < 52:
        state['shoe'] = create_shoe(6)

    state['player_hands'] = [[]]
    state['bets'] = [state['bet']]
    state['active_hand'] = 0

    state['money'] -= state['bet']

    player = state['player_hands'][0]

    player.append(state['shoe'].pop())
    play_card_sound()
    state['dealer'].append(state['shoe'].pop())
    play_card_sound()

    player.append(state['shoe'].pop())
    play_card_sound()
    state['dealer'].append(state['shoe'].pop())
    play_card_sound()

    state['player_stand'] = False
    state['game_over'] = False
    state['result'] = ""

    check_blackjack(state)


# =========================
# BLACKJACK CHECK
# =========================
def check_blackjack(state):

    player_val = hand_value(state['player_hands'][0])
    dealer_val = hand_value(state['dealer'])

    if player_val == 21 or dealer_val == 21:

        state['game_over'] = True

        if player_val == 21 and dealer_val == 21:

            state['result'] = "Push!"
            state['money'] += state['bets'][0]

        elif player_val == 21:

            state['result'] = "BLACKJACK!"
            payout = int(state['bets'][0] * 2.5)
            state['money'] += payout

        else:

            state['result'] = "Dealer Blackjack!"


# =========================
# DEALER PLAY
# =========================
def dealer_play(state):

    while hand_value(state['dealer']) < 17:
        state['dealer'].append(state['shoe'].pop())
        play_card_sound()

# =========================
# GAME RESULT
# =========================
def resolve_hands(state):

    dealer_val = hand_value(state['dealer'])

    results = []

    for i, hand in enumerate(state['player_hands']):

        player_val = hand_value(hand)

        bet = state['bets'][i]

        if player_val > 21:

            results.append(f"Hand {i+1}: Bust")

        elif dealer_val > 21:

            results.append(f"Hand {i+1}: Win")
            state['money'] += bet * 2

        elif player_val > dealer_val:

            results.append(f"Hand {i+1}: Win")
            state['money'] += bet * 2

        elif player_val < dealer_val:

            results.append(f"Hand {i+1}: Lose")

        else:

            results.append(f"Hand {i+1}: Push")
            state['money'] += bet

    state['result'] = "\n".join(results)

    state['game_over'] = True


# =========================
# MAIN MENU
# =========================
def draw_main_menu(surface, mouse_pos, clicked):

    surface.fill((30, 30, 60))

    draw_text(
        surface,
        "BLACKJACK",
        70,
        (255, 255, 255),
        WIDTH // 2,
        150
    )

    play_rect = pygame.Rect(WIDTH // 2 - 100, 300, 200, 60)

    pygame.draw.rect(surface, (70, 130, 180), play_rect)

    draw_text(
        surface,
        "PLAY",
        40,
        (255, 255, 255),
        play_rect.centerx,
        play_rect.centery
    )

    if clicked and play_rect.collidepoint(mouse_pos):
        return "play"

    return None


# =========================
# GAMEPLAY
# =========================
def draw_gameplay(surface, mouse_pos, clicked, state):

    surface.fill((0, 100, 0))

    # MONEY
    draw_text(
        surface,
        f"Money: ${state['money']}",
        36,
        (255, 255, 0),
        30,
        30,
        center=False
    )

    draw_text(
        surface,
        f"Bet: ${state['bet']}",
        36,
        (255, 255, 255),
        30,
        70,
        center=False
    )

    # DEALER
    draw_text(
        surface,
        "Dealer",
        36,
        (255, 255, 255),
        WIDTH // 2,
        50
    )

    hide = not state['player_stand'] and not state['game_over']

    draw_hand(
        surface,
        state['dealer'],
        WIDTH // 2 - 100,
        90,
        hide_first=hide
    )

    # PLAYER HANDS
    start_y = 400

    for idx, hand in enumerate(state['player_hands']):

        x = WIDTH // 2 - 150

        if len(state['player_hands']) > 1:
            x = 250 + idx * 400

        label = f"Hand {idx+1}"

        if idx == state['active_hand'] and not state['game_over']:
            label += " (ACTIVE)"

        draw_text(
            surface,
            label,
            30,
            (255, 255, 255),
            x + 100,
            start_y - 40
        )

        draw_hand(surface, hand, x, start_y)

        draw_text(
            surface,
            f"Value: {hand_value(hand)}",
            28,
            (255, 255, 255),
            x + 100,
            start_y + 160
        )

    # BUTTONS
    hit_rect = pygame.Rect(400, 620, BUTTON_W, BUTTON_H)
    stand_rect = pygame.Rect(550, 620, BUTTON_W, BUTTON_H)
    double_rect = pygame.Rect(700, 620, BUTTON_W, BUTTON_H)
    split_rect = pygame.Rect(850, 620, BUTTON_W, BUTTON_H)
    deal_rect = pygame.Rect(50, 620, BUTTON_W, BUTTON_H)

    action = None

    if not state['in_round']:

        pygame.draw.rect(surface, (70, 130, 180), deal_rect)

        draw_text(
            surface,
            "DEAL",
            30,
            (255, 255, 255),
            deal_rect.centerx,
            deal_rect.centery
        )

        if clicked and deal_rect.collidepoint(mouse_pos):
            action = "deal"

    else:

        pygame.draw.rect(surface, (70, 180, 100), hit_rect)
        pygame.draw.rect(surface, (180, 180, 70), stand_rect)
        pygame.draw.rect(surface, (70, 70, 180), double_rect)
        pygame.draw.rect(surface, (180, 70, 180), split_rect)

        draw_text(surface, "HIT", 30, (255,255,255), hit_rect.centerx, hit_rect.centery)
        draw_text(surface, "STAND", 30, (255,255,255), stand_rect.centerx, stand_rect.centery)
        draw_text(surface, "DOUBLE", 26, (255,255,255), double_rect.centerx, double_rect.centery)
        draw_text(surface, "SPLIT", 30, (255,255,255), split_rect.centerx, split_rect.centery)

        if clicked:

            if hit_rect.collidepoint(mouse_pos):
                action = "hit"

            elif stand_rect.collidepoint(mouse_pos):
                action = "stand"

            elif double_rect.collidepoint(mouse_pos):
                action = "double"

            elif split_rect.collidepoint(mouse_pos):
                action = "split"

    # RESULT
    if state['game_over']:

        draw_multiline_text(
            surface,
            state['result'],
            40,
            (255,255,0),
            WIDTH // 2,
            300
        )

        draw_text(
            surface,
            "Click anywhere to continue",
            28,
            (255,255,255),
            WIDTH // 2,
            370
        )

        if clicked:
            action = "restart"

    return action


# =========================
# MAIN
# =========================
def main():

    load_card_images()

    current_screen = MAIN_MENU

    state = {

        'shoe': create_shoe(6),

        'dealer': [],

        'player_hands': [[]],

        'bets': [],

        'active_hand': 0,

        'player_stand': False,

        'game_over': False,

        'result': "",

        'money': 1000,

        'bet': 50,

        'in_round': False
    }

    while True:

        mouse_clicked = False

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    mouse_clicked = True

        # =========================
        # MAIN MENU
        # =========================
        if current_screen == MAIN_MENU:

            action = draw_main_menu(
                screen,
                mouse_pos,
                mouse_clicked
            )

            if action == "play":
                current_screen = GAMEPLAY

        # =========================
        # GAMEPLAY
        # =========================
        elif current_screen == GAMEPLAY:

            action = draw_gameplay(
                screen,
                mouse_pos,
                mouse_clicked,
                state
            )

            if action == "deal":

                state['dealer'] = []

                deal_initial(state)

                state['in_round'] = True

            elif action == "hit":

                hand = state['player_hands'][state['active_hand']]

                hand.append(state['shoe'].pop())
                play_card_sound()

                if hand_value(hand) > 21:

                    if state['active_hand'] < len(state['player_hands']) - 1:
                        state['active_hand'] += 1

                    else:
                        state['player_stand'] = True
                        dealer_play(state)
                        resolve_hands(state)

            elif action == "stand":

                if state['active_hand'] < len(state['player_hands']) - 1:

                    state['active_hand'] += 1

                else:

                    state['player_stand'] = True

                    dealer_play(state)

                    resolve_hands(state)

            elif action == "double":

                active = state['active_hand']

                bet = state['bets'][active]

                if state['money'] >= bet:

                    state['money'] -= bet

                    state['bets'][active] *= 2

                    hand = state['player_hands'][active]

                    hand.append(state['shoe'].pop())
                    play_card_sound()
                    if state['active_hand'] < len(state['player_hands']) - 1:

                        state['active_hand'] += 1

                    else:

                        state['player_stand'] = True

                        dealer_play(state)

                        resolve_hands(state)

            elif action == "split":

                hand = state['player_hands'][0]

                if (
                    len(hand) == 2 and
                    hand[0][0] == hand[1][0] and
                    state['money'] >= state['bet']
                ):

                    state['money'] -= state['bet']

                    card1 = hand[0]
                    card2 = hand[1]

                    new_hand1 = [card1, state['shoe'].pop()]
                    play_card_sound()
                    new_hand2 = [card2, state['shoe'].pop()]
                    play_card_sound()

                    state['player_hands'] = [new_hand1, new_hand2]

                    state['bets'] = [
                        state['bet'],
                        state['bet']
                    ]

                    state['active_hand'] = 0

            elif action == "restart":

                state['dealer'] = []

                state['player_hands'] = [[]]

                state['bets'] = []

                state['active_hand'] = 0

                state['player_stand'] = False

                state['game_over'] = False

                state['result'] = ""

                state['in_round'] = False

        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    main()