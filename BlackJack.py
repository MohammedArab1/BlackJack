import random
import pdb

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':1}


#Specific card class

class Card():

    #Initiates a card
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    
    #allows to print the card suit and rank
    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)


class Deck():

    #Initiate a deck
    def __init__(self):
        self.cardsInDeck = []
        for suit in suits:
            for rank in ranks:
                self.cardsInDeck.append(Card(suit,rank))
    #Shuffle the deck
    def shuffle(self):
        random.shuffle(self.cardsInDeck)
    
    #Take a card from the deck and deal it to a player
    def dealOne(self):
        return self.cardsInDeck.pop()

    #Reset the Deck
    def Deckreset(self):
        self.cardsInDeck = []
        for suit in suits:
            for rank in ranks:
                self.cardsInDeck.append(Card(suit,rank))        


#Initiate a player
class Player():

    #create a player with a name, cards in hand and money.
    def __init__(self,name):
        self.name = name
        self.cardsInHand = []
        self.totalMoney = 50


    #Asks the player if they want to get another card or if they want to stand.
    def hitOrStand(self,deck):
        input1 = input("input 1 if you would like a hit, input 2 if you would like to stand. ")

        while input1 != '1' and input1 != '2':
            input1 = input ("Please input a valid value. input 1 if you would like a hit, input 2 if you would like to stand. ")
        
        if int(input1) == 1:
            print("Hit!\n")
            self.cardsInHand.append(deck.dealOne())
        else:
            print("Stand! you will no longer be dealt cards this round\n")
            return False
    
    #adds a card to the player's hand 
    def addCard(self,deck):
        self.cardsInHand.append(deck.dealOne())

    #Asks the player to place his bet
    def placeBet(self):
        bet = input("Place your bet for the current round: $")
        while not bet.isdigit() or int(bet) > self.totalMoney:
            bet = input("Please only input valid integers. Place your bet for the current round (cannot exceed {}): $".format(player1.totalMoney))
        self.totalMoney -= int(bet)
        return int(bet)
    
    #Allows the player to see what cards they have
    def showCards(self):
        print("Cards currently in the hands of {}: \n".format(self.name))
        for card in self.cardsInHand:
            print(card)

    #In case player gets an ace, asks which value he'd like it to be
    def ifAce(self):                                   
        for card in self.cardsInHand:
            if card.rank == 'Ace':
                aceValue = input("Input 1 if you'd like your Ace to be of value 1, 2 if you'd like your ace to be of value 11 ")
                while not aceValue.isdigit() or (int(aceValue) != 1 or int(aceValue) != 2):
                    aceValue = input("Please only input valid integers. Input 1 if you'd like your Ace to be of value 1, 2 if you'd like your ace to be of value 11 ")
            
                if int(aceValue) == 1:
                    card.value = 1
                elif int(aceValue) == 2:
                    card.value = 11

    #Counts the total value of all the cards in the player's hand
    def countTotal(self):
        total = 0
        for card in self.cardsInHand:
            total += card.value
        return total
    
    #Allows to compate the cards in player's hands to dealer
    def compareWithDealer(self,dealer):
        if self.countTotal() > dealer.countTotal():
            return 'win'
        
        elif self.countTotal() < dealer.countTotal():
            return 'lose'
        
        else:
            return 'tie'
    
    #Resets player's hands
    def resetHand(self):
        self.cardsInHand = []


     


#Dealer class which inherits from player class

class Dealer(Player):

    #Initiating a Dealer object through the constructor for Player
    def __init__(self, name):
        Player.__init__(self, name)
        self.numberOfAces = 1
    
    #If dealer has ace, works out whether the ace is of value 1 or 11
    def dealerIfAce(self, card):
            if card.rank == 'Ace' and self.numberOfAces == 1 and self.countTotal() + 10 <= 21:
                card.value = 11
                self.numberOfAces += 1 
    

    




##Game Logic

#Starting the Game and creating a deck
gameOn = True
gameDeck = Deck()

while gameOn:
    print("Welcome to BlackJack!\n")

    #Creating a dealer and a player
    dealer = Dealer("Dealer")
    player1 = Player(input("Please input the name for Player 1: "))

    #Showing the player how much money he'll be starting with
    print("All players, including the dealer, will start with a total of ${}.\n".format(dealer.totalMoney))

    roundStart = True
    roundCount = 0

    #Starting a round
    while roundStart:
        #Reseting and reshuffling the deck and reseting the hands of both the dealer and the player at the start of each round
        roundCount += 1
        print("Beginning of round {}\n". format(roundCount))
        gameDeck.Deckreset()
        gameDeck.shuffle()
        player1.resetHand()
        dealer.resetHand()

        #Showing the player how much money he has
        print("You currently have ${}".format(player1.totalMoney))

        #Asking for a bet from the player
        player1Bet = player1.placeBet()


        #Start the round by dealing two cards to the player and dealing two cards to the dealer
        print("\nDealing two cards to {} and the dealer\n".format(player1.name))

        dealer.addCard(gameDeck)
        dealer.addCard(gameDeck)

        player1.addCard(gameDeck)
        player1.addCard(gameDeck)

        #Show the player one of the dealer's cards, not both (as per the rules)
        print("One of the dealer's cards is: {}\n".format(dealer.cardsInHand[0]))

        
        #Player specific actions
        while True:

            #Show the cards that are currently in your hand
            player1.showCards()              

            #Have to check if your two cards are equal to 21.
            if player1.countTotal() == 21:
                print("\nCongratulations! your 2 cards are equal to 21. You win 1.5x your bet. You now have: ${}".format(player1.totalMoney + player1Bet*1.5))
                player1.totalMoney += player1Bet*1.5
                dealer.totalMoney -= player1Bet/2       #Dealer only gives the remainder after the player takes back what he bet.

            #While your cards add up to less than 21, you can decide whether you want a hit or you want to stand
            while player1.countTotal() < 21:                
                if player1.hitOrStand(gameDeck) == False:
                    player1.ifAce()
                    break
                else:
                    player1.showCards()

            #if your total is greater than 21, you lose
            if player1.countTotal() > 21:
                print("\nUnfortunately, your cards total to {}, you lose this round.".format(player1.countTotal()))
                print("You lose your initial bet of ${}. You now have ${}.\n".format(player1Bet, player1.totalMoney))
                break           
                                    

            #after all your hits, see if your total is equal to 21
            if player1.countTotal() == 21:
                print("\nCongratulations! your {} cards are equal to 21. you win 2x your bet. You now have : ${}".format(len(player1.cardsInHand), player1.totalMoney + player1Bet*2))
                player1.totalMoney += player1Bet*2
                dealer.totalMoney -= player1Bet
                break

            #After you finished adding more cards, it's time for the player to continue with his actions (which are automatic). 
            #Start by showing all the dealer's cards
            dealer.showCards()

            #Working out what the values of the aces in the dealer's hands will be
            dealer.dealerIfAce(dealer.cardsInHand[0])
            dealer.dealerIfAce(dealer.cardsInHand[1])   

            #Dealer picks up a card if his two cards add up to 16 or less.            
            if dealer.countTotal() <= 16:
                print("\nThe dealer's cards total to {}, therefore he will pick up another card".format(dealer.countTotal()))
                dealer.addCard(gameDeck)
                dealer.dealerIfAce(dealer.cardsInHand[2])  
                dealer.showCards()
            

            #If dealer busts, player wins
            if dealer.countTotal() > 21:
                print("\nThe dealer has busted. You win 2x your bet. You now have {}".format(player1.totalMoney+player1Bet*2))
                player1.totalMoney += player1Bet*2
                dealer.totalMoney -= player1Bet


            #If neither player nor dealer busts, start comparing the dealer's hands with the player's hands

            #If player has greater hand than dealer, win
            if player1.compareWithDealer(dealer) == 'win':
                print("\nCongratulations! your card total is {} while the dealer's total is {}. You win this round".format(player1.countTotal(), dealer.countTotal()))
                print("You win 2x your bet. You now have : ${}\n".format(player1.totalMoney + player1Bet*2))
                player1.totalMoney += player1Bet*2
                dealer.totalMoney -= player1Bet
            
            #If dealer has greater hand than player, lose
            elif player1.compareWithDealer(dealer) == 'lose':
                print("\nUnfortunately, your card total is {} while the dealer's total is {}. You lose this round".format(player1.countTotal(), dealer.countTotal()))
                print("You lose your initial bet of ${}. You now have ${}.\n".format(player1Bet, player1.totalMoney))
            
            #Otherwise it's a tie
            else:
                print("You and the dealer tie, you do not lose nor gain anything this round.")
                player1.totalMoney += player1Bet
            
            print("\nEnd of round.")


            break

        #Check to see if either player or Dealer has run out of money, if so they can't play again.
        if player1.totalMoney == 0:
            print("You lost all your money! You unfortunately cannot play another round.")
            break
        elif dealer.totalMoney == 0:
            print("The dealer no longer has any money! You win the whole game!")
            break

        #Ask player if they want to play again.
        playAgain = input("Would you like to play another round? (Y/N)")


        while playAgain.upper() != 'Y' and playAgain.upper() != 'N':
            playAgain = input("Please input a valid character. Either Y or N")
        if playAgain.upper() == 'N':
            print("You end the game with ${}.\n".format(player1.totalMoney))
            break


    print("Thank you for playing BlackJack!")
    break




#If adding more players, going to have to replace every 'player1.' instance in the player specific round loop with an index or something that increases at the end of the loop, indicating a change in player




        
