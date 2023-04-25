import numpy as np
import matplotlib.pyplot as plt
import random

MAX_LINES= 3
MAX_BET= 500
MIN_BET= 25
WIN_AMT= 0
u=0

ROWS = 3
COLS = 3

def slot_spin(rows,cols,symbols):
    all_symbols = [symbol for symbol, count in symbols.items() for _ in range (count)]
    columns=  []
    for _ in range (cols):
        columns.append(random.sample(all_symbols, rows))
    k=np.flipud(np.array(columns).transpose())
    return k

'''
def print_slot(columns):
    for rows in range(len(columns)):
        for i,j in enumerate(columns):
            if i<=(len(j)-1):
                print(j[rows], end= " | " )
            else:
                print(j[rows], end= "")
        print()
'''
def triple_row(tot_bet, slots, dict, WIN_AMT):
        d=0
        for i in range(ROWS):
                if slots[i,d]== slots[i,d+1] == slots[i,d+2]:
                    z=dict[slots[i,d]]
                    WIN_AMT+=(z*tot_bet)/3
        return WIN_AMT 

def winnings(f, tot_bet,lines, slots, dict, WIN_AMT):

    if lines == 1:
        if slots[1,0]== slots[1,1] and slots[1,1] == slots[1,2]:
            z=dict[slots[1,1]]
            WIN_AMT+=(z*tot_bet)
        return WIN_AMT
        
    if lines == 2:
        return (f)

    if lines == 3:
        WIN_AMT+=(f*3)/5
        j=0
        for i in range (ROWS):
            if i==0:
                j+=1
                def count(i):
                    return slots[i,i]
            
            if i>0 and count(i)==count(i-1):
                j+=1
                if j==3:
                    z=dict[count(i)]
                    WIN_AMT+=(z*tot_bet)/5
        if slots[0,2]== slots[1,1]== slots[2,0]:
            WIN_AMT+=(dict[slots[1,1]]*tot_bet)/5
        return WIN_AMT

def plot(k,color_dict):

    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor('#F5DEB3')
    ax.set_title('SLOT MACHINE', fontsize=24, fontweight='bold', color='black', y=1.05)
    ax.axis('off')

# Create a 3x3 array of rectangles with character-unique background colors and character labels
    for i in range(ROWS):
        for j in range(COLS):
            rect = plt.Rectangle((j/3, i/3), 1/3, 1/3, color=color_dict[k[i][j]], ec='black', lw=2, zorder=0)
            ax.add_artist(rect)
            ax.text((j+0.5)/3, (i+0.5)/3, k[i][j], ha='center', va='center', fontsize=64, fontweight='bold', color='white')

    plt.show()

def deposit(h):
    if h==0:
        while True:
            amount= input("how much would you like to deposit?: ")
            if amount.isdigit():
                amount= int(amount)
                if amount> 0:
                    return amount
                else:
                        print("The amount has to be greater than 0.")
            else:
                print("Please enter a number.")
            break

    else:
        return 0
        

def get_number_of_lines():
        print(f'''BETTING LINES!!!
            1 - Place Bet on the Middle Horizontal line
            2 - Place Bets on all {str(MAX_LINES)} Horizontal lines
            3 - Place Bets on 2 Diagonals and all {str(MAX_LINES)} Horizontal lines ''')
        
        while True:
            lines= input("Enter the number of lines you would like to bet on (1-"+ str(MAX_LINES)+"): ")
            if lines.isdigit():
                lines= int(lines)
                if 1<= lines<=MAX_LINES:
                    break
                else:
                    print("The amount has to be within the range: (1-3)")
            else:
                print("Please enter a number.")
        return lines 
def get_bet():
        print(f"Betting Range : [${MIN_BET} - ${MAX_BET}]")
        while True:
            amount= input("how much would you like to bet?: ")
            if amount.isdigit():
                amount= int(amount)
                if MIN_BET<=amount<= MAX_BET:
                    break
                else:
                    print(f"Please place your bets within ${MIN_BET} - ${MAX_BET} per line")
            else:
                print("Please enter a number.")
        return amount
def confirmation(bet, lines, balance, u=0):
    confirm= input(f"Are you sure that you want to bet ${bet} on {lines} ? (yes/no): ")
    if confirm.capitalize()== "Yes":
        print(f"You have bet ${bet} on {lines} lines")
    else:
        print("Please enter the details of your bet again")
        main(balance, u)

def repeat(balance, h):
        g=input("Would you like to continue playing? (yes/no): ")
        if g.capitalize() == "Yes":
            return main(balance, h)
        else:
            print("Thank You For Playing! Please lose more of your money to us!")

balance=0
def main(balance, u=0):
    symbol_count = {
     "7":100,
     "$":200,
     "@":400,
     "0":1000
    }
    color_dict = {
    "7": "#FFC107",   
    "$": "#4CAF50",   
    "@": "#2196F3",   
    "0": "#F44336"    
    }
    combination_value = {
     "7":16,
     "$":8,
     "@":4,
     "0":2
    }
    if u ==0:
        print("WELCOME! To play the game, please make a deposit")
    else:
        None
    balance= balance + deposit(u)
    o=input("Do you want to check your balance? (yes/no): ")
    if o.capitalize()=="Yes":
        print(f"You have a balance of {balance} ")
    else:
        print("Alright! Lets get started!")
    lines= get_number_of_lines()
    bet= get_bet()
    total_bet= bet*lines
    if total_bet > balance:
        print(f"Your current balance of ${balance} is not sufficient for the bet")
        print(f"You are still short by ${total_bet-balance}")
        s= input("Would you you like to deposit more? (yes/no): ")
        if s.capitalize()=="No":
            print("Thank you for playing")
            exit()
            

        elif s.capitalize()=="Yes":
            while total_bet >= balance:
                balance= balance + deposit(0)
                if total_bet > balance:   
                    print(f"You still need to deposit an amount of {total_bet-balance}")
                    continue

                elif total_bet <= balance:
                    confirm= confirmation(bet, lines, balance, u) 
                    break
                return total_bet    
        
    #confirm= confirmation(bet, lines, balance, u) 
    balance-=total_bet
    slots= slot_spin(ROWS, COLS, symbol_count)
    #print_slot(slots)
    x=np.array(slots)
    f=triple_row(total_bet, x, combination_value, WIN_AMT)
    win=winnings(f, total_bet,lines, x, combination_value, WIN_AMT)
    balance+= win
    print("Spinning the Slots.........")
    plot(slots, color_dict)
    
    if win < total_bet:
        print("Your luck is shitty af, try again loser")
        print(f"You have lost ${total_bet-win}")
        repeat(balance, 1)

    elif total_bet <= win:
        print(f"Congratulations! You have won ${win-total_bet}")
        repeat(balance, 1)    
        
main(balance)