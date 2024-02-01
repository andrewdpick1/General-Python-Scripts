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

# Player's hand dictionary
hand = {'cards': []}
dealer_hand = {'cards': []}

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

# hit function, draws 1 and tells player card 
def draw_on_hit(hand, deck):
    drawn_card = deck.pop()
    hand['cards'].append(drawn_card)
    print(f"You drew a {hand['cards'][-1]['rank']} of {hand['cards'][-1]['suit']}")
    global hand_sum
    hand_sum = sum_of_ranks(hand)

#game start function, draws 2 and tells player card

def game_start(hand, deck):
    draw_and_append(hand, deck)
    print(f"You draw a {hand['cards'][-1]['rank']} of {hand['cards'][-1]['suit']}")
    time.sleep(1)
    dealer_dap(hand, deck)
    print(f"The dealer draws a {dealer_hand['cards'][-1]['rank']} of {dealer_hand['cards'][-1]['suit']}")
    time.sleep(1)
    draw_and_append(hand, deck)
    print(f"You draw a {hand['cards'][-1]['rank']} of {hand['cards'][-1]['suit']}")
    #this card is not shown, but stored in dealer_hand
    dealer_dap(hand, deck)
    time.sleep(1)
    print('The dealer draws a card and keeps it face down')
    time.sleep(1)
    if hand_sum == 21:
        global blackjack
        blackjack = True

#game start, place bets
print('How much would you like to wager?')
while True:
    wager = input('>')
    if not wager.isdigit():
        print("Invalid input. Please enter a number.")
    else:
        int(wager)
        print(f'You bet {wager} chips')
        time.sleep(1)
        break
game_start(hand, deck)

while True:
    #dealer draws to try to get 21 to match blackjack
    if blackjack:
        print(f"The dealer turns over a {dealer_hand['cards'][-1]['rank']} of {hand['cards'][-1]['suit']}")
        while dealer_sum < 17:
            dealer_dap(hand, deck)
            print(f"The dealer draws a {dealer_hand['cards'][-1]['rank']} of {dealer_hand['cards'][-1]['suit']}")
            time.sleep(1.5)
            if dealer_sum >= 17:
                break
        break

    if not blackjack:
        print('Hit or stand?')
        hit_or_stand = input('>')
    #player hits, drawing until stands
        if hit_or_stand in ['hit', 'Hit', '1', '1.']:
            print('You hit.')
            draw_on_hit(hand, deck)
            if hand_sum > 21:
                time.sleep(0.75)
                print('Bust! You lose.')
                print(f"The dealer turns over a {dealer_hand['cards'][-1]['rank']} of {hand['cards'][-1]['suit']}")
                time.sleep(1)
                while dealer_sum < 17:
                    dealer_dap(hand, deck)
                    print(f"The dealer draws a {dealer_hand['cards'][-1]['rank']} of {dealer_hand['cards'][-1]['suit']}")
                    time.sleep(1.5)
                    if dealer_sum >= 17:
                        break
                break
            elif hand_sum == 21:
                print(f"The dealer turns over a {dealer_hand['cards'][-1]['rank']} of {hand['cards'][-1]['suit']}")
            time.sleep(1)
            while dealer_sum < 17:
                dealer_dap(hand, deck)
                print(f"The dealer draws a {dealer_hand['cards'][-1]['rank']} of {dealer_hand['cards'][-1]['suit']}")
                time.sleep(1.5)
                if dealer_sum >= 17:
                    break
                break
            else:
                print('')

        elif hit_or_stand in ['stand', 'Stand', '2', '2.']:
            print(f"The dealer turns over a {dealer_hand['cards'][-1]['rank']} of {hand['cards'][-1]['suit']}")
            time.sleep(1)
            while dealer_sum < 17:
                dealer_dap(hand, deck)
                print(f"The dealer draws a {dealer_hand['cards'][-1]['rank']} of {dealer_hand['cards'][-1]['suit']}")
                time.sleep(1.5)
                if dealer_sum >= 17:
                    break
            break
        else:
            print('Please enter "hit" or "stand"')

    #check hand counts after hits and/or stands            
if blackjack:
    print(f'Blackjack! You win ___ chips')
elif dealer_sum > 21 and hand_sum <= 21:
    print(f'The dealer busts, you win ___ chips!') 
    player_win = True 
elif dealer_sum < hand_sum and hand_sum <= 21:
    player_win = True
elif dealer_sum == hand_sum and hand_sum <= 21:
    player_tie = True
   
    

#payout
if blackjack:
    print('blacjack 2.5x payout')
elif player_win == True:
    print('payout code goes here')
elif player_tie == True:
    print('Standoff. You keep your bet')
elif player_win == False:
    print('Try again?')