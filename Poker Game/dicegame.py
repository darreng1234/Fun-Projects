import dice
import random

max_dice = 5
def deal_hand(max_dice):
    hand = []
    for i in range(0,max_dice,1):
        die_value = roll_die() #generate the random num
        hand.append(die_value) #append to list
    return hand  

def roll_die():
    return random.randint(1,6)


def rank_hand(hand):
    rank = 0
    one = 0
    two = 0 
    three = 0
    four = 0
    five = 0
    
    die_count = [0,0,0,0,0,0,0] 
    for y in hand:
        die_count[y] = die_count[y] + 1
    
    
    for x in die_count:
        if x == 5:
            five+=1
        elif x == 4:
            four+=1
        elif x == 3:
            three+=1
        elif x == 2:
            two+=1
        elif x == 1:
            one+=1
        else:
            'no hits'
    
    if five == 1:
        rank = 6
    elif four == 1:
        rank = 5
    elif three == 1 and two == 1:
        rank = 4
    elif three == 1 and one == 2:
        rank = 3
    elif two == 2 and one == 1:
        rank = 2
    elif two == 1 and one == 3:
        rank = 1
    elif one == 5:
        rank =  0
    
    return rank

def display_rank(rank):
    if rank == 0:
        print('Nothing special')
    elif rank == 1:
        print('One pair')
    elif rank == 2:
        print('Two pairs')
    elif rank == 3:
        print('Three of a kind')
    elif rank == 4:
        print('Full house')
    elif rank == 5:
        print('Four of a kind')
    elif rank == 6:
        print('Five of a kind')

def guessWinner(rank_player,rank_dealer):
    if(rank_player == rank_dealer):
        print("** Draw! **")
    elif(rank_player > rank_dealer):
        print("** Player Wins! **")
    else:
        print("** Dealer Wins! **") 
    
    
 
def gameSummary(rank_player,rank_dealer):
    global draw 
    global player 
    global dealer 
    
    if(rank_player == rank_dealer):
        draw+=1
    elif(rank_player > rank_dealer):
        player+=1
    else:
        dealer+=1 
    
       
    
def display_details():
        print("File:test.py \nAuthor: Batman\nStud ID:0123456X \nEmailID: test@gmail.com\nThis is my own work")
        
def playGame():
    print("Player's Hand:\n")
    hand_player = deal_hand(5)
    dice.display_hand(hand_player, 5)
    rank_player = rank_hand(hand_player)   
       
    
    print("Dealer's Hand:\n")
    hand_dealer = deal_hand(5)
    dice.display_hand(hand_dealer, 5)
    rank_dealer = rank_hand(hand_dealer)
    
    print("Player has... ")
    display_rank(rank_player) 
    print("Dealer has... ")
    display_rank(rank_dealer)
    
    guessWinner(rank_player,rank_dealer)
    gameSummary(rank_player,rank_dealer)
    
      
draw = 0  
player = 0
dealer = 0     
display_details()  
while(True):
    user_choice = input("Would you like to play dice poker [y|n]? \nPlease enter either 'y' or 'n'\n")
    if user_choice == 'y':
        playGame()
    elif user_choice == 'n':
        print(draw, " Games have been drawn\n",player,"Games have been won by the Player \n",dealer,"Games have been won by the Dealer\n")
        print("No worries... another time perhaps...:")
        print("End Of Game")
        break
    else:
        print("Please enter either 'y' or 'n'")

    
    

