# imports
import time
import winsound

# Consts
GAME_NAME = 'Text BlackJack'
GAME_VER = '0.05'
GAME_INIT_COINS = 100

# classes


class Card:
    def __init__(self, card_val='ace'):
        self.card_val = card_val

    def value(self, is_ace_one=True):
        if self.card_val == 'ace':
            if is_ace_one:
                return 1
            else:
                return 11
        elif self.card_val == 'two':
            return 2
        elif self.card_val == 'three':
            return 3
        elif self.card_val == 'four':
            return 4
        elif self.card_val == 'five':
            return 5
        elif self.card_val == 'six':
            return 6
        elif self.card_val == 'seven':
            return 7
        elif self.card_val == 'eight':
            return 8
        elif self.card_val == 'eight':
            return 8
        elif self.card_val == 'nine':
            return 9
        elif self.card_val == 'jack' or self.card_val == 'queen' \
                or self.card_val == 'king':
            return 10
        else:
            return 1


class Deck:
    def __init__(self):
        self.deck = [Card('ace'), Card('two'), Card('three'),
                     Card('six'), Card('seven'), Card('eight'),
                     Card('nine'), Card('jack'), Card('queen'),
                     Card('king')] * 4

    def refill(self):
        self.deck = [Card('ace'), Card('two'), Card('three'),
                     Card('six'), Card('seven'), Card('eight'),
                     Card('nine'), Card('jack'), Card('queen'),
                     Card('king')] * 4

    def take_card(self):
        return self.deck.pop()

    def shuffle_deck(self):
        import random
        random.shuffle(self.deck)

    def __len__(self):
        return len(self.deck)


class AbstractPlayer:
    def __init__(self, *args):
        self.hand = list(args)

    def hit(self, deck):
        card = deck.take_card()
        self.hand.append(card)

    def best_hand_value(self):
        value_ace_one = 0
        value_ace_ele = 0
        for card in self.hand:
            value_ace_one += card.value()
            value_ace_ele += card.value(False)
        if value_ace_ele > 21:
            return value_ace_one
        else:
            return value_ace_ele

    def low_hand_value(self):
        value = 0
        for card in self.hand:
            value += card.value()
        return value

    def is_bust(self):
        return self.low_hand_value() > 21

    def empty_hand(self):
        self.hand = []


class Dealer(AbstractPlayer):
    def __init__(self, *args):
        AbstractPlayer.__init__(self, args)

    def display_hand(self):
        print('The dealer currently hold: ', end='')
        for index, card in enumerate(self.hand):
            if index == 0:
                print(str(card.card_val), end='')
            else:
                print(', ' + str(card.card_val), end='')


class Player(AbstractPlayer):
    def __init__(self, *args, coins=GAME_INIT_COINS, bet=0):
        AbstractPlayer.__init__(self, args)
        self.coins = coins
        self.bet = bet

    def display_hand(self):
        print('You currently hold: ', end='')
        for index, card in enumerate(self.hand):
            if index == 0:
                print(str(card.card_val), end='')
            else:
                print(', ' + str(card.card_val), end='')

# functions


def game_menu():
    clear_screen()
    print('Welcome to ' + GAME_NAME + '!')
    print('     version-' + GAME_VER)
    print('-------Menu----------')
    print('     1.Start         ')
    print('     2.Instructions  ')
    print('     3.About         ')
    print('     4.Exit          ')
    print('-------Menu----------')
    choice = user_input([1, 2, 3, 4])
    if choice == 1:
        game_start_screen()
    elif choice == 2:
        game_ins()
    elif choice == 3:
        game_about()
    else:
        game_exit_screen()


def game_end():
    clear_screen()
    choice = input('Would you like to play again? (y/n)')
    if choice.lower() == 'y' or choice.lower() == 'yes':
        game_menu()
    else:
        game_exit_screen()


def game_exit_screen():
    clear_screen()
    print('Thank you for playing ' + GAME_NAME)


def game_start_screen():
    clear_screen()
    print('Hello there player, nice to see you :)')
    print(f'You initial currency is {GAME_INIT_COINS} coins')
    input('')
    deck = Deck()
    deck.shuffle_deck()
    player = Player()
    dealer = Dealer()
    game_data = {'player': player, 'dealer': dealer, 'deck': deck}
    game_main_start(game_data)


def game_main_start(game_data):
    # extract game data
    player = game_data['player']
    dealer = game_data['dealer']
    deck = game_data['deck']
    player.empty_hand()
    dealer.empty_hand()
    deck.refill()
    deck.shuffle_deck()
    clear_screen()
    game_player_bet(game_data)
    clear_screen()
    dealer.hit(deck)
    player.hit(deck)
    game_prepare()
    game_main_turn(game_data)


def game_player_bet(game_data):
    player = game_data['player']
    while True:
        try:
            clear_screen()
            print('Your currently hold ' + str(player.coins) + ' coins\n')
            bet_amo = int(input('Please enter bet amount: '))
            if bet_amo in range(0, player.coins + 1):
                player.bet = bet_amo
                break
            else:
                print('bet amount not possible')
                print('remember you have ' + str(player.coins) + ' coins')
                input('')
                continue
        except:
            print('Input not a number, please enter a correct input')
            input('')
            continue


def game_prepare():
    winsound.PlaySound('slot_machine_sound.wav', winsound.SND_ASYNC)
    clear_screen()
    print('Preparing a new game please wait..')
    time.sleep(1)
    print('Shuffling deck...')
    time.sleep(1)
    print('Ready!')
    time.sleep(1)
    game_music_on()


def game_main_turn(game_data):
    # extract game data
    player = game_data['player']
    dealer = game_data['dealer']
    deck = game_data['deck']
    # determent if player turn or dealer turn
    is_player_turn = True
    while True:
        game_main_display(game_data, is_disp_action=is_player_turn)
        # Player is still playing
        if is_player_turn:
            action = user_input([1, 2])
            # player hit
            if action == 1:
                player.hit(deck)
                # player hit 21
                if player.best_hand_value() == 21:
                    winsound.PlaySound('oh_baby_sound', winsound.SND_FILENAME)
                    game_music_on()
                    game_main_display(game_data, False)
                    print('You hit 21 baby!')
                    game_player_won(game_data)
                    break
                # player is bust
                elif player.is_bust():
                    game_main_display(game_data, False)
                    print('Dude you just bust :(')
                    game_player_lost(game_data)
                    break
                # player continue play another turn
                else:
                    continue
            # player choose stand
            else:
                is_player_turn = False
                continue
        # Player stand
        else:
            # Dealer is bust:
            if dealer.is_bust():
                game_main_display(game_data, False)
                print('The dealer is bust!')
                game_player_won(game_data)
                break
            # Dealer won
            elif dealer.best_hand_value() > player.best_hand_value():
                game_main_display(game_data, False)
                print('The dealer got the better hand :(')
                game_player_lost(game_data)
                break
            # Dealer is still playing
            else:
                print('Dealer is playing..')
                dealer.hit(deck)
                time.sleep(1)
                continue


def game_main_display(game_data, is_disp_action=True):
    clear_screen()
    print('-----You VS the computer-------\n')
    game_data['player'].display_hand()
    print('\n')
    game_data['dealer'].display_hand()
    print('\n\n------------------------------\n')
    if is_disp_action:
        print('Action menu:')
        print('1.hit')
        print('2.stand')


def game_player_won(game_data):
    winsound.PlaySound('win_sound.wav', winsound.SND_FILENAME)
    game_music_on()
    clear_screen()
    print('You won the game! good job!')
    print(f'You just won yourself {game_data["player"].coins} coins!')
    game_data['player'].coins += game_data['player'].bet
    print(f'You currently have {game_data["player"].coins} coins total')
    game_data['player'].bet = 0
    input('')
    game_play_again(game_data)


def game_player_lost(game_data):
    winsound.PlaySound('fail_sound.wav', winsound.SND_FILENAME)
    game_music_on()
    # extract game data
    player = game_data['player']
    dealer = game_data['dealer']
    deck = game_data['deck']
    clear_screen()
    print('Sorry you lost the bet of ' + str(player.bet) + ' coins')
    player.coins -= player.bet
    print('You currently have ' + str(player.coins) + ' coins total')
    player.bet = 0
    if player.coins == 0:
        print('Because you have 0 coins, here 30 on the house ;)')
        player.coins = 30
    input('')
    game_play_again(game_data)


def game_play_again(game_data):
    player = game_data['player']
    clear_screen()
    print(f'You can play again with your {player.coins} coins')
    print('or quit the game and loss all coins and progress.')
    answer = input('\nWould you like to play again (y/n)? : ')
    if answer.lower() == 'y' or answer.lower() == 'yes':
        game_main_start(game_data)
    else:
        game_return_menu()


def game_ins():
    clear_screen()
    print('---Game Instructions---')
    print(
        " Blackjack is played with 1 to 9 decks of 52 cards each. \n"
        " The values of the cards correspond to their numerical value from 2-10. \n"
        " All face cards (Jack, Queen, King) count 10 and the Ace either 1 or 11, \n"
        " as the holders desires. A score with an ace valued as 11 is named soft-hand. \n"
        " A soft-hand score of 17 is denoted as 7/17. \n"
        " The color of the cards does not have any effect \n"
        " The goal of the game is to reach a score (=sum of the cards) as high as possible but not more than 21.\n"
        " A Blackjack (Ace and a card whose value is 10) beats all other combination of cards.\n"
        " If the final sum is higher than the sum of the dealer, \n"
        " the player gets a play-off of 1:1 of his initial stake.\n"
        " If the players combination is Blackjack, the play-off is 3:2 of the initial stake.\n"
        " If the sum of the dealer is higher, the player loses his bet. If the sum is equal, then nobody wins.\n"
        " If the player holds a score of 22 or more, he busted and thus he loses his bet immediately.\n"
        " If the dealer busts, the players wins independently of his final score.\n")
    game_return_menu()


def game_about():
    clear_screen()
    print('---Game About---')
    print(' This is a text based blackjack game')
    print(' Current version is ' + GAME_VER)
    print(' This game was create by Omri Gal Shenhav ')
    print(' from Israel, as part of a learning experience')
    print(' in python')
    game_return_menu()


def game_return_menu():
    print('Input anything to return to menu')
    input()
    game_menu()


def user_input(choices):
    while True:
        try:
            choice = int(input('Please enter action: '))
            if choice in choices:
                return choice
            else:
                print('input action is not available')
                continue
        except:
            print('Input not a number, please enter a correct input')
            continue


def clear_screen():
    from os import system
    system('cls')


def game_music_on():
    winsound.PlaySound('background_music.wav', winsound.SND_ASYNC)


if __name__ == '__main__':
    print('loading please wait..')
    game_music_on()
    game_menu()
