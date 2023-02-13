class tttgame:
    ''' We will make the board using dictionary 
    in which keys will be the location(i.e : top-left,mid-right,etc.)
    and initialliy it's values will be empty space and then after every move 
    we will change the value according to player's choice of move. '''


    ''' We will have to print the updated board after every move in the game and 
        thus we will make a function in which we'll define the printBoard function
        so that we can easily print the board everytime by calling this function. '''
        
    #class constructor
    def __init__(self, turn, playBoard, win, tie):
        self.playBoard = playBoard
        self.turn = turn
        self.win = win
        self.tie = tie

    #define setters and getters
    def setTurn(self, updateTurn):
        self.turn = updateTurn

    def getTurn(self):
        return self.turn

    def setBoard(self, board):
        self.playBoard = board

    def getBoard(self):
        return self.playBoard

    def setWin(self, win):
        self.win = win

    def getWin(self):
        return self.win

    def setTie(self, tie):
        self.tie = tie
    
    def getTie(self):
        return self.tie

    #print the board
    def printBoard(self, board):
        print('' , board['7'] , '|' , board['8'] , '|' , board['9'])
        print('---+---+---')
        print('' , board['4'] , '|' , board['5'] , '|' , board['6'])
        print('---+---+---')
        print('' , board['1'] , '|' , board['2'] , '|' , board['3'])

    #print the game result
    def printWinner(self, tie):
        print("\nGame Over.\n")  
        if tie:               
            print("It's a Tie!!")
        else:           
            print(" **** " + str(self.getTurn())  + " won. ****")

    #play the game
    def play(self, t):
        '''this method is designed to play one turn at a time. 
        Every time a player wants to play, this method has to be called'''

        self.setTurn(t)
        count = 0

        #count the taken moves
        for j in self.getBoard():
            if self.getBoard()[j] == 'X' or self.getBoard()[j] == 'O':
                count += 1

        print("\nIt's your turn," , str(self.turn) + ". Move to which place?")

        # select a location to play at
        move = input()        
        while self.getBoard()[move] != ' ':
            print("That place is already filled.\nMove to which place?")
            move = input()
        self.getBoard()[move] = self.getTurn()
        count += 1
        self.setBoard(self.getBoard())  #update the board before sending it to the other player
        self.printBoard(self.getBoard())#print the board to the current player
        
        # Now we will check if player X or O has won,for every move after 5 moves. 
        if count >= 5:
            if self.getBoard()['7'] == self.getBoard()['8'] == self.getBoard()['9'] != ' ': # across the top
                self.printWinner(0)
                self.setWin(1)               
            elif self.getBoard()['4'] == self.getBoard()['5'] == self.getBoard()['6'] != ' ': # across the middle
                self.printWinner(0)
                self.setWin(1)
            elif self.getBoard()['1'] == self.getBoard()['2'] == self.getBoard()['3'] != ' ': # across the bottom
                self.printWinner(0)
                self.setWin(1)
            elif self.getBoard()['1'] == self.getBoard()['4'] == self.getBoard()['7'] != ' ': # down the left side
                self.printWinner(0)
                self.setWin(1)
            elif self.getBoard()['2'] == self.getBoard()['5'] == self.getBoard()['8'] != ' ': # down the middle
                self.printWinner(0)
                self.setWin(1)
            elif self.getBoard()['3'] == self.getBoard()['6'] == self.getBoard()['9'] != ' ': # down the right side
                self.printWinner(0)
                self.setWin(1)
            elif self.getBoard()['7'] == self.getBoard()['5'] == self.getBoard()['3'] != ' ': # diagonal
                self.printWinner(0)
                self.setWin(1)
            elif self.getBoard()['1'] == self.getBoard()['5'] == self.getBoard()['9'] != ' ': # diagonal
                self.printWinner(0)
                self.setWin(1)

        # If neither X nor O wins and the board is full, we'll declare the result as 'tie'.
        if count == 9 and self.getWin() != 1:
            self.setTie(1)
            self.printWinner(self.getTie())

        # change turn after each play        
        if self.getTurn() == 'X':
            self.setTurn('O')
        else:
            self.setTurn('X')