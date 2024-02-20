import random
import time

# Define the ranks, suits, and values for a standard deck of cards
ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

# Creates 3 decks of cards
decks = 3
deck = [{'rank': rank, 'suit': suit} for i in range(decks) for rank in ranks for suit in suits]
# Shuffle the deck
random.shuffle(deck)

#Player inventory/money set-up
player_money = {0}

# Player's hand dictionary
hand = {'cards': []}
dealer_hand = {'cards': []}

#replay number initialization 
replay_number = 0

#player win, lose, or tie variable to end game
player_win = False
player_tie = False
#blackjack check for payout
blackjack = False

# Sum player and dealer hand function. Also, handle aces worth 1 or 11.
def sum_of_ranks(hand):
    total = sum(ranks[card['rank']] for card in hand['cards'])
    num_aces = sum(1 for card in hand['cards'] if card['rank'] == 'Ace')
    # Handle aces dynamically
    while total > 21 and num_aces:
        total -= 10
        num_aces -= 1
    return total
hand_sum = sum_of_ranks(hand)

def sum_of_dealer(dealer_hand):
    total = sum(ranks[card['rank']] for card in dealer_hand['cards'])
    num_aces = sum(1 for card in dealer_hand['cards'] if card['rank'] == 'Ace')
    # Handle aces dynamically
    while total > 21 and num_aces:
        total -= 10
        num_aces -= 1
    return total

dealer_sum = sum_of_dealer(dealer_hand)

# Draw card functions
def draw_and_append(hand, deck):
    drawn_card = deck.pop()
    hand['cards'].append(drawn_card)
    global hand_sum
    hand_sum = sum_of_ranks(hand)

def dealer_dap(hand, deck):
    drawn_card = deck.pop()
    dealer_hand['cards'].append(drawn_card)
    global dealer_sum
    dealer_sum = sum_of_dealer(dealer_hand)
    dealer_sum

# hit function, draws 1 and tells player card 
def draw_on_hit(hand, deck):
    drawn_card = deck.pop()
    hand['cards'].append(drawn_card)
    print(f"You draw a {hand['cards'][-1]['rank']} of {hand['cards'][-1]['suit']}")
    print()
    global hand_sum
    hand_sum = sum_of_ranks(hand)

#game start function, draws 2 and tells player card

def game_start(hand, deck):
    draw_and_append(hand, deck)
    print(f"You draw a {hand['cards'][-1]['rank']} of {hand['cards'][-1]['suit']}")
    print()
    time.sleep(1.5)
    dealer_dap(hand, deck)
    print(f"The dealer draws a {dealer_hand['cards'][-1]['rank']} of {dealer_hand['cards'][-1]['suit']}")
    print()
    time.sleep(1.5)
    draw_and_append(hand, deck)
    print(f"You draw a {hand['cards'][-1]['rank']} of {hand['cards'][-1]['suit']}")
    print()
    #this card is not shown, but stored in dealer_hand
    dealer_dap(hand, deck)
    time.sleep(1.5)
    print('The dealer draws a card and keeps it face down')
    print()
    time.sleep(1.5)
    if hand_sum == 21:
        global blackjack
        blackjack = True
#Set player inventory
print('How much money are you bringing to the table?')
print()
while True:
    player_money = input('>')
    if not player_money.isdigit() or int(player_money) < 1:
        print('Invalid input. Please enter a number')
        print()
    else:
        print(f'You receive {player_money} chips.')
        print()
        break
#The rest of the code is actual gameplay:
while True:
    #game start, place bets
    replay_number += 1
    print('How much would you like to wager?')
    print()
    while True:
        wager = input('>')
        if not wager.isdigit():
            print("Invalid input. Please enter a number.")
        elif int(player_money) < int(wager):
            print("Insufficient funds.")
            print()
        else:
            print(f'You bet {wager} chips')
            print()
            player_money = int(player_money) - int(wager)
            time.sleep(1)
            break
    
    game_start(hand, deck)
    while True:
        #dealer draws until 17, gives illusion of other players in game
        if blackjack:
            print(f"The dealer turns over a {dealer_hand['cards'][-1]['rank']} of {hand['cards'][-1]['suit']}")
            print()
            if dealer_sum == 21:
                player_tie = True
            else:
                player_win = True
            while dealer_sum < 17:
                dealer_dap(hand, deck)
                print(f"The dealer draws a {dealer_hand['cards'][-1]['rank']} of {dealer_hand['cards'][-1]['suit']}")
                print()
                time.sleep(1.5)
                if dealer_sum >= 17:
                    break
            break

        if not blackjack:
            print('Hit or stand?')
            print()
            hit_or_stand = input('>')
        #player hits, drawing until stands
            if hit_or_stand in ['hit', 'Hit', '1', '1.']:
                print('You hit.')
                print()
                time.sleep(1)
                draw_on_hit(hand, deck)
                if hand_sum > 21:
                    time.sleep(0.75)
                    print('Bust! You lose.')
                    time.sleep(1)
                    print()
                    print(f"The dealer turns over a {dealer_hand['cards'][-1]['rank']} of {hand['cards'][-1]['suit']}")
                    print()
                    time.sleep(1)
                    while dealer_sum < 17:
                        dealer_dap(hand, deck)
                        print(f"The dealer draws a {dealer_hand['cards'][-1]['rank']} of {dealer_hand['cards'][-1]['suit']}")
                        print()
                        time.sleep(1)
                        if dealer_sum >= 17:
                            break
                    break
                elif hand_sum == 21:
                    print(f"The dealer turns over a {dealer_hand['cards'][-1]['rank']} of {hand['cards'][-1]['suit']}")
                    print()
                    time.sleep(1)
                    while dealer_sum < 17:
                        dealer_dap(hand, deck)
                        print(f"The dealer draws a {dealer_hand['cards'][-1]['rank']} of {dealer_hand['cards'][-1]['suit']}")
                        print()
                        time.sleep(1.5)
                        if dealer_sum >= 17:
                            break
                    break
                else:
                    print()

            elif hit_or_stand in ['stand', 'Stand', '2', '2.']:
                print(f"The dealer turns over a {dealer_hand['cards'][-1]['rank']} of {hand['cards'][-1]['suit']}")
                print()
                time.sleep(1)
                while dealer_sum < 17:
                    dealer_dap(hand, deck)
                    print(f"The dealer draws a {dealer_hand['cards'][-1]['rank']} of {dealer_hand['cards'][-1]['suit']}")
                    print()
                    time.sleep(1.5)
                    if dealer_sum >= 17:
                        break
                break
            else:
                print('Please enter "hit" or "stand"')
                print()

        #check hand counts after hits and/or stands            
    if blackjack and player_win:
        print(f'Blackjack!')
        print()
        time.sleep(0.75)
        #payout code 2.5x payout
        player_blackjack_reward = int(wager) * 2.5
        blackjack_winnings_for_print = int(player_blackjack_reward) - int(wager)
        player_money = int(player_money) + int(player_blackjack_reward)
        print(f'You win {blackjack_winnings_for_print} chips.')
        print()
        time.sleep(1)

    elif dealer_sum > 21 and hand_sum <= 21:
        player_win = True
        #payout code
        player_reward = int(wager) * 2
        player_money = int(player_money) + int(player_reward)
        print(f'The dealer busts, you win {wager} chips!')
        print() 
        time.sleep(1)

    elif dealer_sum < hand_sum and hand_sum <= 21:
        player_win = True
        player_reward = int(wager) * 2
        player_money = int(player_money) + int(player_reward)
        print(f'The dealer busts, you win {wager} chips!') 
        print()
        time.sleep(1)

        #payout code
    elif dealer_sum == hand_sum and hand_sum <= 21:
        player_tie = True
        #return bet to hand
        player_money = int(player_money) + int(wager)
        print(f'Standoff. Your wager of {wager} chips is returned to your hand.')
        print()
        time.sleep(1)
    else:
        #chips have already been taken out when the bet was placed.
        print(f'You lose {wager} chips.')
        print()
        time.sleep(1)
    print(f'You have {player_money} chips.')
    time.sleep(.75)
    print()
    
    if player_money == 0:
        print('You are out of money! Would you like to get more chips?')
        print()
        while True:
            add_money = input('>')
            if add_money in ['yes', 'Yes', '1']:
                print('How much would you like to add?')
                print()
                player_money = input('>')
                if not player_money.isdigit():
                    print('Invalid input. Please enter a number')
                    print('')
                
                else:
                    print(f'You receive {player_money} chips.')
                    print('')
                    print('Are you ready for the next hand?')
                    print()
                    break

                
            elif add_money in ['no', 'No', '2']:
                break
            else:
                print('Please enter "yes" or "no".')


        if add_money in ['no', 'No', '2']:
            print('Thanks for playing!')
            break
    else: 
        print('Do you want to play again?')
        print()

    # Replay
    while True:
        #initializes add_money so the code can run properly
        if player_money != 0:
            add_money = ''
        if add_money in ['yes', 'Yes', '1']:
            break
    
        else:
            while True:
                replay = input('>')
                if replay in ['yes', 'Yes', '1']:
                    break
                elif replay in ['no', 'No', '2']:
                    break
                else:
                    print('Please enter "yes" or "no".')
                    print()
                #shuffles deck every 10 hands 
            if replay_number % 10 == 0:
                print('Shuffling the deck...')
                print()
                time.sleep(5)
                # Reshuffle the cards and "add" popped cards back into the deck... I'm not tracking popped cards so this is easiest.
                ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
                suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
                decks = 3
                deck = [{'rank': rank, 'suit': suit} for i in range(decks) for rank in ranks for suit in suits]
                random.shuffle(deck)
            # Reset player and dealer hand
            hand = {'cards': []}
            dealer_hand = {'cards': []}
            dealer_sum
            hand_sum
            break
    if add_money in ['yes', 'Yes', '1'] or replay in ['yes', 'Yes', '1']:
            continue
    elif replay in ['no', 'No', '2']:
            break
    else:
        break
