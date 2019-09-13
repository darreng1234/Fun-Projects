import dice
import random

max_dice = 5
def deal_hand(max_dice):
    hand = []
    for i in range(0,max_dice,1):
        die_value = roll_die() #generate the random num
        hand.append(die_value) #append to list
    dice.display_hand(hand, 5)  
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

def guessWinner(rank_player,dealer_rank):
    status = [0,0,0]
    
    if(rank_player == dealer_rank):
        print("** Draw! **") 
        status[0] = status[0]+1
    elif(rank_player > dealer_rank):
        print("** Player Wins! **")
        status[1] = status[1]+1
    else:
        print("** Dealer Wins! **") 
        status[2] = status[2]+1
    return status
    
    
def display_details():
        print("File:test.py \nAuthor: Batman\nStud ID:0123456X \nEmailID: test@gmail.com\nThis is my own work")
    


def playGame():
    print("Player's Hand:\n")
    hand_player = deal_hand(5)
    rank_player = rank_hand(hand_player)   
       
    
    print("Dealer's Hand:\n")
    hand_dealer = deal_hand(5)
    rank_dealer = rank_hand(hand_dealer)
    
    print("Player has... ")
    display_rank(rank_player) 
    print("Dealer has... ")
    display_rank(rank_dealer)
    
    guessWinner(rank_player,rank_dealer)
    
    
def endGame():
    print("End Of Game")    
    
while():
user_choice = input("Would you like to play dice poker [y|n]? /nPlease enter either 'y' or 'n'")
if user_choice == 'y':
    playGame()
elif user_choice == 'n':
    print("No worries... another time perhaps...:")
else:
    print("Please enter either 'y' or 'n'")






    
    

