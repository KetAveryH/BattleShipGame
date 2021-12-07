import random

"""
To begin we will want to start with the creation of an 8x8 grid
"""
white = '\u2B1C'    #defining our colored squares for use throughout
blue = '\U0001f7e6'
red = '\U0001F7E5'
weird = '\U0001F533'
black = '\U00002B1B'


# Create a converter, so we can take in A4 or C2, then actually use 04 or 32
letcol = {'a':0,
        'b':1,
        'c':2,
        'd':3,
        'e':4,
        'f':5,
        'g':6,
        'h':7,
        'i':8,
        'j':9,
        'k':10,
        'l':11,
        'm':12,
        'n':13,
        'o':14,
        'p':15,
        'q':16,
        'r':17,
        's':18,
        't':19,
        'u':20,
        'v':21,
        'w':22,
        'x':23,
        'y':24,
        'z':25,}
def convertCord(col):
    """Create a converter, so we can take in A4 or C2, then actually use 04 or 32"""
    col = col.lower()
    if col in letcol:
        return letcol.get(col)
    
    return False

class Board:

    def __init__(self, width, height):
        """Construct objects of type Board, with the given width and height."""
        self.width = width
        self.height = height
        self.dataPS = [[blue]*width for row in range(height)] #Player Ship
        self.dataPT = [[weird]*width for row in range(height)] #Player Target
        self.dataAS = [[blue]*width for row in range(height)] #AI Ship
        self.dataAT = [[weird]*width for row in range(height)] #AI target
        self.dataPSL = [[[],[],[],[],[],'good'],[[],[],[],[],'good'],[[],[],[],'good'],[[],[],[],'good'],[[],[],'good']]
        self.dataASL = [[[],[],[],[],[],'good'],[[],[],[],[],'good'],[[],[],[],'good'],[[],[],[],'good'],[[],[],'good']]

    def __repr__(self):
        """This method returns a string representation for an object of type Board."""
        alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        s = ''                          # Define the string to return
        s += "   "                         #Code that labels each column
        for col in range(0, self.width):
            s += " "
            s += alphabet[col]
        s += "       "
        for col in range(0, self.width):
            s += " "
            s += alphabet[col]
        s += '\n'  + ' ' 
        s += '\u2B1C'*(self.width + 2) + "   " + '\u2B1C'*(self.width + 2) + "\n"
        
        for row in range(0, self.height):
            s += str(row)
            s += '\u2B1C'
            for col in range(0, self.width):
                s += self.dataPS[row][col] + ''
            s += "\u2B1C"
            s += "  "
            s += str(row)
            s += '\u2B1C'
            for col in range(0, self.width):
                s += self.dataPT[row][col] + ''
            s += "\u2B1C"
            s += '\n'
        s += ' '
        s += (self.width +2) * '\u2B1C' +  "   " + (self.width +2) * '\u2B1C' # Bottom of the board
        #Below, table for whether things are sunk or not
        s += '\n\n' + '        YOUR SHIPS                 ENEMY SHIPS'
        s += '\n\n' + '           ' + self.dataPSL[0][5] + '    <   CARRIER   >     ' + self.dataASL[0][5]
        s += '\n' + '           ' + self.dataPSL[1][4] + '    <  BATTLESHIP >     ' + self.dataASL[1][4]
        s += '\n' + '           ' + self.dataPSL[1][4] + '    <   CRUISER   >     ' + self.dataASL[1][4]
        s += '\n' + '           ' + self.dataPSL[1][4] + '    <  SUBMARINE  >     ' + self.dataASL[1][4]
        s += '\n' + '           ' + self.dataPSL[1][4] + '    <  DESTROYER  >     ' + self.dataASL[1][4]

        return s       # Return the Board

    def aiBoard(self):
        """Allows the ai's board to be displayed at will. Is typically hidden, as in a typical game of battleship"""
        alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        s = ''                          # Define the string to return
        s += "   "                         #Code that labels each column
        for col in range(0, self.width):
            s += " "
            s += alphabet[col]
        s += "       "
        for col in range(0, self.width):
            s += " "
            s += alphabet[col]
        s += '\n'  + ' ' 
        s += black*(self.width + 2) + "   " + black*(self.width + 2) + "\n"
        
        for row in range(0, self.height):
            s += str(row)
            s += black
            for col in range(0, self.width):
                s += self.dataAS[row][col] + ''
            s += black
            s += "  "
            s += str(row)
            s += black
            for col in range(0, self.width):
                s += self.dataAT[row][col] + ''
            s += black
            s += '\n'
        s += ' '
        s += (self.width +2) * black +  "   " + (self.width +2) * black # Bottom of the board
        
        print(s)       # Return the Board

    def clearBoard(self, p):
            if p == 'player':
                self.dataPS = [[blue]*self.width for row in range(self.height)]
                self.dataPT = [[weird]*self.width for row in range(self.height)]
            if p == 'ai':
                self.dataAS = [[blue]*self.width for row in range(self.height)]
                self.dataAT = [[weird]*self.width for row in range(self.height)]

    def allowsMove(self, col, row, ship, ori, p):
        """Checks whether a ship placement will be allowed. Accepts:
        Col, a number representing a letter where ship starts
        Row, a number representing how far down to start
        l, the length of the ship in question (>=1)
        ori, either 'up' 'down' 'left' 'right'
        p, the player whose turn it is"""
        if not( 0 <= row and row <= self.height) or not( 0 <= col and col <= self.width):   #check to make sure that the row and col are in the given range of self board
            print('something went wrong, coords not in range')
            return False
        if ship == 'carrier':
            l = 5
        elif ship == 'battleship':
            l = 4
        elif ship == 'cruiser':
            l = 3
        elif ship == 'submarine':
            l = 3
        elif ship == 'destroyer':
            l = 2
        else:
            print('Ship error!')
            False
        if p == 'player':
            if ori == 'up':      #Start for each orientation... 'up' 'down' 'left' 'right'
                if (row+1)-l < 0:    #check to make sure that the L for each ori isn't too long for the board
                    print('you did something wrong, if up')
                    return False #Here we will reprompt the player in a later function
                for x in range(l):   #check to make sure that the places we will place the ship are empty
                    if self.dataPS[row-x][col] !=  blue:
                        print("you did something wrong, for loop up")
                        return False
                return True      #all good! let the magic happen
            if ori == 'down':
                if (row)+l > self.height: 
                    print('you did something wrong, if down')
                    return False #Here we will reprompt the player in a later function
                for x in range(l):
                    if self.dataPS[row+x][col] !=  blue:
                        print("you did something wrong, for loop down")
                        return False
                return True
            if ori == 'left':
                if (col+1)-l < 0:
                    print('you did something wrong, if left')
                    return False
                for x in range(l):
                    if self.dataPS[row][col-x] !=  blue:
                        print("you did something wrong, for loop left")
                        return False
                return True
            if ori == 'right':
                if col+l > self.width:
                    print('you did something wrong, if right')
                    return False
                for x in range(l):
                    if self.dataPS[row][col+x] != blue:
                        print("you did something wrong, for loop right")
                        return False
                return True
            print("you did something wrong, no ori assigned")
            return False
        if p == 'ai':
            if ori == 'up':      #Start for each orientation... 'up' 'down' 'left' 'right'
                if (row+1)-l < 0:    #check to make sure that the L for each ori isn't too long for the board
                    print('you did something wrong, if up')
                    return False #Here we will reprompt the player in a later function
                for x in range(l):   #check to make sure that the places we will place the ship are empty
                    if self.dataAS[row-x][col] !=  blue:
                        print("you did something wrong, for loop up")
                        return False
                return True      #all good! let the magic happen
            if ori == 'down':
                if (row)+l > self.height: 
                    print('you did something wrong, if down')
                    return False #Here we will reprompt the player in a later function
                for x in range(l):
                    if self.dataAS[row+x][col] !=  blue:
                        print("you did something wrong, for loop down")
                        return False
                return True
            if ori == 'left':
                if (col+1)-l < 0:
                    print('you did something wrong, if left')
                    return False
                for x in range(l):
                    if self.dataAS[row][col-x] !=  blue:
                        print("you did something wrong, for loop left")
                        return False
                return True
            if ori == 'right':
                if col+l > self.width:
                    print('you did something wrong, if right')
                    return False
                for x in range(l):
                    if self.dataAS[row][col+x] != blue:
                        print("you did something wrong, for loop right")
                        return False
                return True
            print("you did something wrong, no ori assigned")
            return False

    def placeShip(self, col, row, ship, ori, p):
        """Taking in a valid col, row, length and orientation, will actually place the described ship on p's board"""
        if ship == 'carrier':
            l = 5
            r = 0
        elif ship == 'battleship':
            l = 4
            r= 1
        elif ship == 'cruiser':
            l = 3
            r = 2
        elif ship == 'submarine':
            l = 3
            r = 3
        elif ship == 'destroyer':
            l = 2
            r = 4
        if p == 'player':
            if ori == 'up':#   For placing a players ship
                for x in range(l):
                    self.dataPS[row-x][col] = black
                    self.dataPSL[r][x] = [row-x, col]
            if ori == 'down':
                for x in range(l):
                    self.dataPS[row+x][col] = black
                    self.dataPSL[r][x] = [row+x, col]
            if ori == 'left':
                for x in range(l):
                    self.dataPS[row][col-x] = black
                    self.dataPSL[r][x] = [row, col-x]
            if ori == 'right':
                for x in range(l):
                    self.dataPS[row][col+x] = black
                    self.dataPSL[r][x] = [row, col+x]
        if p == 'ai':#    For placing the AI's ships
            if ori == 'up':
                for x in range(l):
                    self.dataAS[row-x][col] = black
                    self.dataASL[r][x] = [row-x, col]
            if ori == 'down':
                for x in range(l):
                    self.dataAS[row+x][col] = black
                    self.dataASL[r][x] = [row+x, col]
            if ori == 'left':
                for x in range(l):
                    self.dataAS[row][col-x] = black
                    self.dataASL[r][x] = [row, col-x]
            if ori == 'right':
                for x in range(l):
                    self.dataAS[row][col+x] = black
                    self.dataASL[r][x] = [row, col+x]

    def isVertical(self, ship, p):
        """Checks whether a given ship for a given p player is orientated vertically or horizontally. True if vertical, false if otherwise."""
        horScore = 0
        verScore = 0 
        carrierLoc = self.dataPSL[0][0:5]
        battleshipLoc = self.dataPSL[1][0:4]
        cruiserLoc = self.dataPSL[2][0:3]
        submarineLoc = self.dataPSL[3][0:3]
        destroyerLoc = self.dataPSL[4][0:2]
        if ship == 'carrier':
            for x in range(4):
                if carrierLoc[x][0] == carrierLoc[x+1][0]:
                    verScore += 1
                if carrierLoc[x][1] == carrierLoc[x+1][0]:
                    horScore += 1
                if verScore >= 4:
                    return True
                if horScore >= 4:
                    return False
        if ship == 'battleship':
            for x in range(3):
                if carrierLoc[x][0] == carrierLoc[x+1][0]:
                    verScore += 1
                if carrierLoc[x][1] == carrierLoc[x+1][0]:
                    horScore += 1
                if verScore >= 3:
                    return True
                if horScore >= 3:
                    return False
        if ship == 'cruiser':
            for x in range(2):
                if carrierLoc[x][0] == carrierLoc[x+1][0]:
                    verScore += 1
                if carrierLoc[x][1] == carrierLoc[x+1][0]:
                    horScore += 1
                if verScore >= 2:
                    return True
                if horScore >= 2:
                    return False
        if ship == 'submarine':
            for x in range(2):
                if carrierLoc[x][0] == carrierLoc[x+1][0]:
                    verScore += 1
                if carrierLoc[x][1] == carrierLoc[x+1][0]:
                    horScore += 1
                if verScore >= 2:
                    return True
                if horScore >= 2:
                    return False
        if ship == 'destroyer':
            for x in range(1):
                if carrierLoc[x][0] == carrierLoc[x+1][0]:
                    verScore += 1
                if carrierLoc[x][1] == carrierLoc[x+1][0]:
                    horScore += 1
                if verScore >= 1:
                    return True
                if horScore >= 1:
                    return False

    def shipPerimeter(self, ship, p):
        """
        For this function we will input the ship and player, and it will return a list of points around the ship
        The way we do this is we just add 1 and subtract 1 from each column value if vertical, or we add 1 and 
        subtract 1 from each row if horizontal. 
        """
        carrierLoc = self.dataPSL[0][0:5]
        battleshipLoc = self.dataPSL[1][0:4]
        cruiserLoc = self.dataPSL[2][0:3]
        submarineLoc = self.dataPSL[3][0:3]
        destroyerLoc = self.dataPSL[4][0:2]

        #THIS STILL HAS TO BE CREATED

        if self.isVertical(ship, p) == True:
            #code that draws perimeter of a vertical ship
            for x in range():
                print()
        else:
            print()
            # code that draws perimeter of a horizontal ship
        
    def randomPlacement(self, p):
        """
        This function will continuosly generate new coordinates and orientations until all ships are placed
        """
        x=0
        shipList = ['carrier', 'battleship', 'cruiser', 'submarine', 'destroyer']
        oriList = ['right', 'left', 'up', 'down']
        while x < 5:
            randCol = random.randint(0,9)
            randRow = random.randint(0,9)
            randShip = random.choice(shipList)
            randOri = random.choice(oriList)

            if self.allowsMove(randCol, randRow, randShip, randOri, p) == True:
                self.placeShip(randCol, randRow, randShip, randOri, p)
                x += 1
                shipList.remove(randShip)
        return d

    def stratRandomPlacement(self, p): #in order to make this function, it would be way easier to make another function that defines the area around each ship.
        """
        This function will add on to the previous function by adding constraints, boats may never be touching
        """
        x=0
        shipList = ['carrier', 'battleship', 'cruiser', 'submarine', 'cruiser']
        oriList = ['right', 'left', 'up', 'down']
        while x < 5:
            randCol = random.randint(0,9)
            randRow = random.randint(0,9)
            randShip = random.choice(shipList)
            randOri = random.choice(oriList)

            if self.allowsMove(randCol, randRow, randShip, randOri, p) == True:
                self.placeShip(randCol, randRow, randShip, randOri, p)
                x += 1
                shipList.remove(randShip)
        return d

    def validTarget(self, col, row, p):
        """Determines whether a selected target is valid, given a converted col, row, and p's turn"""
        if not( 0 <= row and row <= self.height) or not( 0 <= col and col <= self.width):   #check to make sure that the row and col are in the given range of self board
            print('something went wrong, coords not in range')
            return False
        if p == 'ai':#   if ai's turn, check ai target board
            if self.dataAT[row][col] != weird:
                return False
        if p == 'player':#    If players turn, check players targer board
            if self.dataPT[row][col] != weird:
                return False
        return True

    def shot(self, col, row, p):
        """
        This function will check whether the given point is a 'hit', 
        'miss', or 'False' (meaning the position is not valid). A
        position is not valid if it is out of bounds, or has been already hit.
        """
        if p == 'ai':#   If Ai's turn
            if self.dataPS[row][col] == black:# check to see what the ai is hitting on the players board
                print("AI's Hit!")
                self.dataPS[row][col] = red
                self.dataAT[row][col] = red
            if self.dataPS[row][col] == blue:
                print("AI's Miss!")
                self.dataAT[row][col] = blue
        if p == 'player':#   If Players turn
            if self.dataAS[row][col] == black:# check to see what the player is hitting on the AI's board
                print("Player's Hit!")
                self.dataPT[row][col] = red
                self.dataAS[row][col] = red
            if self.dataAS[row][col] == blue:
                print("Player's Miss!")
                self.dataPT[row][col] = blue
    
    def randomShot(self, p):
        row = random.randint(0,9)
        col = random.randint(0,9)
        if p == 'ai':#   If Ai's turn
            if self.dataPS[row][col] == black:# check to see what the ai is hitting on the players board
                print("AI's Hit!")
                self.dataPS[row][col] = red
                self.dataAT[row][col] = red
            if self.dataPS[row][col] == blue:
                print("AI's Miss!")
                self.dataAT[row][col] = blue
        if p == 'player':#   If Players turn
            if self.dataAS[row][col] == black:# check to see what the player is hitting on the AI's board
                print("Player's Hit!")
                self.dataPT[row][col] = red
                self.dataAS[row][col] = red
            if self.dataAS[row][col] == blue:
                print("Player's Miss!")
                self.dataPT[row][col] = blue

    def isClear(self):
        """checks whether a gameboard is clear"""
        for col in range(self.width):
            for row in range(self.height):
                if self.dataPS[row][col] != blue:
                    return False
                if self.dataPT[row][col] != weird:
                    return False
                if self.dataAS[row][col] != blue:
                    return False
                if self.dataAT[row][col] != weird:
                    return False
        return True

    #The Below functions return True if the type of ship is sunk and False if they have not sunk

    def carrierSunk(self, p):  # Example FN, can be used to write the next four. Then afterwards, we can write a winsFor which checks all the ai or player ships depending on input p. This will be the win condition that ends the game.
        """Checks the locations of the carrier in p player's board, and sticks sunk into the location list if sunk."""
        count = 0
        if p == 'player':                          
            if self.dataPSL[0][5] == 'sunk':
                True
            
            for x in range(5):
                if self.dataPS[self.dataPSL[0][x][0]][self.dataPSL[0][x][1]] == red:
                    count += 1
                if count == 5:
                    self.dataPSL[0][5] = 'sunk'
                    print ("YOUR CARRIER HAS SUNK")
                    return True
            else:
                return False
        if p == 'ai':
            if self.dataASL[0][5] == 'sunk':
                return True
            
            for x in range(5):
                if self.dataAS[self.dataASL[0][x][0]][self.dataASL[0][x][1]] == red:
                    count += 1
                if count == 5:
                    self.dataASL[0][5] = 'sunk'
                    print("THE ENEMY CARRIER HAS SUNK")
                    return True
            else:
                return False
    def battleshipSunk(self, p):
        count = 0
        if p == 'player':
            if self.dataPSL[1][4] == 'sunk':
                return True
            
            for x in range(4):
                if self.dataPS[self.dataPSL[1][x][0]][self.dataPSL[1][x][1]] == red:
                    count += 1
                if count == 4:
                    self.dataPSL[1][4] = 'sunk'
                    print('YOUR BATTLESHIP HAS SUNK')
                    return True
            else:
                return False
        if p == 'ai':
            if self.dataASL[1][4] == 'sunk':
                return True
            
            for x in range(4):
                if self.dataAS[self.dataASL[1][x][0]][self.dataASL[1][x][1]] == red:
                    count += 1
                if count == 4:
                    self.dataASL[1][4] = 'sunk'
                    print('THE ENEMY BATTLSHIP HAS SUNK')
                    return True
            else:
                return False
    def cruiserSunk(self, p):
        count = 0
        if p == 'player':
            if self.dataPSL[2][3] == 'sunk':
                return True
            
            for x in range(3):
                if self.dataPS[(self.dataPSL[2][x][0])][self.dataPSL[2][x][1]] == red:
                    count += 1
                if count == 3:
                    self.dataPSL[2][3] = 'sunk'
                    print('YOUR CRUISER HAS SUNK')
                    return True
            else:
                return False
        if p == 'ai':
            if self.dataASL[2][3] == 'sunk':
                return True
            
            for x in range(3):
                if self.dataAS[self.dataASL[2][x][0]][self.dataASL[2][x][1]] == red:
                    count += 1
                if count == 3:
                    self.dataASL[2][3] = 'sunk'
                    print('THE ENEMY CRUISER HAS SUNK')
                    return True
            else:
                return False
    def submarineSunk(self, p):
        count = 0
        if p == 'player':
            if self.dataPSL[3][3] == 'sunk':
                return True
            
            for x in range(3):
                if self.dataPS[self.dataPSL[3][x][0]][self.dataPSL[3][x][1]] == red:
                    count += 1
                if count == 3:
                    self.dataPSL[3][3] = 'sunk'
                    print('YOUR SUBMARINE HAS SUNK')
                    return True
            
            else:
                return False

        if p == 'ai':
            if self.dataASL[3][3] == 'sunk':
                return True
            
            for x in range(3):
                if self.dataAS[self.dataASL[3][x][0]][self.dataASL[3][x][1]] == red:
                    count += 1
                if count == 3:
                    self.dataASL[3][3] = 'sunk'
                    print('THE ENEMY SUBMARINE HAS SUNK')
                    return True
            else:
                return False
    def destroyerSunk(self, p):
        count = 0
        if p == 'player':
            if self.dataPSL[4][2] == 'sunk':
                return True

            for x in range(2):
                if self.dataPS[self.dataPSL[4][x][0]][self.dataPSL[4][x][1]] == red:
                    count += 1
            if count == 2:
                self.dataPSL[4][2] = 'sunk'
                print('YOUR DESTROYER HAS SUNK')
                return True
            else:
                return False

        if p == 'ai':
            if self.dataASL[4][2] == 'sunk':
                return True
            
            for x in range(2):
                if self.dataAS[self.dataASL[4][x][0]][self.dataASL[4][x][1]] == red:
                        count += 1
                if count == 2:
                    self.dataASL[4][2] = 'sunk'
                    print('THE ENEMY DESTROYER HAS SUNK') 
                    return True
            else:
                return False           
    def allSunk(self, p):
        """
        This runs all of the above functions, and if they are all true it returns true and prints the end of the game.
        """
        if p == 'player':
            if self.carrierSunk('player') == True and self.battleshipSunk('player') == True and self.cruiserSunk('player') == True and self.submarineSunk('player') == True and self.destroyerSunk('player') == True:
                print("GAME OVER, " + p + "Lost")
                return True
            else:
                return False
        
        if p == 'ai':
            if self.carrierSunk('ai') == True and self.battleshipSunk('ai') == True and self.cruiserSunk('ai') == True and self.submarineSunk('ai') == True and self.destroyerSunk('ai') == True:
                print("GAME OVER, " + p + "Lost")
                return True
            else:
                return False
            
    def hostGame(self):
        """Function which builds the game, playing it until one player has sunk all of their opponents ships. Player vs. AI"""
        if self.isClear() == False:
            return print("Your Board is not clear! Clear it, then you can start a new game.")
        print("Welcome to Battleship!")
        print(self)
        print("\nWe will begin by placing your ships...")
        while True:#     Carrier
            colrow = str(input("Which grid tile would you like to start your aircraft carrier on (length 5)?  Use form A6, G4, etc.  -  "))
            col = int(convertCord(colrow[0]))
            row = int(colrow[1])
            ori = input("How would you like to place it? Up, Down, Left or Right?  -  ")
            ori.lower()
            if self.allowsMove(col, row, 'carrier', ori, 'player'):
                self.placeShip(col, row, 'carrier', ori, 'player')
                print(self)
                break
            else:
                print("Oh no! Something went wrong... Let's try that again")
        while True:#     Battleship
            colrow = str(input("Which grid tile would you like to start your battleship on (length 4)?  Use form A6, G4, etc.  -  "))
            col = int(convertCord(colrow[0]))
            row = int(colrow[1])
            ori = input("How would you like to place it? Up, Down, Left or Right?  -  ")
            ori.lower()
            if self.allowsMove(col, row, 'battleship', ori, 'player'):
                self.placeShip(col, row, 'battleship', ori, 'player')
                print(self)
                break
            else:
                print("Oh no! Something went wrong... Let's try that again")
        while True: #Submarine
            colrow = str(input("Which grid tile would you like to start your submarine on (length 3)?  Use form A6, G4, etc.  -  "))
            col = int(convertCord(colrow[0]))
            row = int(colrow[1])
            ori = input("How would you like to place it? Up, Down, Left or Right?  -  ")
            ori.lower()
            if self.allowsMove(col, row, 'submarine', ori, 'player'):
                self.placeShip(col, row, 'submarine', ori, 'player')
                print(self)
                break
            else:
                print("Oh no! Something went wrong... Let's try that again")
        while True:#Cruiser
            colrow = str(input("Which grid tile would you like to start your cruiser on (length 3)?  Use form A6, G4, etc.  -  "))
            col = int(convertCord(colrow[0]))
            row = int(colrow[1])
            ori = input("How would you like to place it? Up, Down, Left or Right?  -  ")
            ori.lower()
            if self.allowsMove(col, row, 'cruiser', ori, 'player'):
                self.placeShip(col, row, 'cruiser', ori, 'player')
                print(self)
                break
            else:
                print("Oh no! Something went wrong... Let's try that again")
        while True:#Destroyer
            colrow = str(input("Which grid tile would you like to start your destroyer on (length 2)?  Use form A6, G4, etc.  -  "))
            col = int(convertCord(colrow[0]))
            row = int(colrow[1])
            ori = input("How would you like to place it? Up, Down, Left or Right?  -  ")
            ori.lower()
            if self.allowsMove(col, row, 'destroyer', ori, 'player'):
                self.placeShip(col, row, 'destroyer', ori, 'player')
                print(self)
                break
            else:
                print("Oh no! Something went wrong... Let's try that again")
        
        #   END OF PLAYER SHIP PLACING, START OF AI SHIP PLCEMENT

        #   temporary
        self.placeShip(0,0,'carrier','down','ai')
        self.placeShip(4,2,'battleship','right','ai')
        self.placeShip(1,6,'submarine','down','ai')
        self.placeShip(9,8,'cruiser','left','ai')
        self.placeShip(4,6,'destroyer','right','ai')
        #   temporary

        #   END OF AI SHIP PLACEMENT, START OF PLAYER ROUND 1!

        #   Start of a round

        while True:
            print("Player, it's your turn! Where would you like to target your opponent's board?")
            while True:
                colrow = str(input("Remember to input in the form A7, D4, I3, etc.  -  "))
                col = int(convertCord(colrow[0]))
                row = int(colrow[1])
                if self.validTarget(col, row, 'player'):
                    self.shot(col, row, 'player')
                    print(self)
                    break
                else:
                    print("Oh no! Something went wrong... lets try that again...")
            print("Now, It's AI's turn...")
            cc = 0
            rr = 0
            self.shot(cc,rr,'ai')
            cc +=1
            rr +=1


#  Next Steps...
"""In no particular order:
    build the end functions that check for a sunk board
    building off that, the functions have to print player's Ship Sunk when a given ship sinks
    AI targeting system
    AI ship placement system
    
    Right now, the player placement is fully functional, and basically so is player targeting. Just need AI time."""



d = Board(10,10)

# d.placeShip(4,4,'destroyer','right','player')
# d.shot(4,4,'ai')
# d.shot(5,4,'ai')
# d.placeShip(4,5,'battleship','right','player')
# d.shot(4,5,'ai')
# d.shot(5,5,'ai')
# d.shot(6,5,'ai')
# d.shot(7,5,'ai')
# d.placeShip(4,6,'cruiser','right','player')
# d.shot(4,6, 'ai')
# d.shot(5,6, 'ai')
# d.shot(6,6, 'ai')
# d.placeShip(4,7,'submarine','right','player')
# d.shot(4,7, 'ai')
# d.shot(5,7, 'ai')
# d.shot(6,7, 'ai')
# d.placeShip(4,8,'carrier','right','player')
# d.shot(4,8, 'ai')
# d.shot(5,8, 'ai')
# d.shot(6,8, 'ai')
# d.shot(7,8, 'ai')
# d.shot(8,8, 'ai')


"""we meed to build functiond that need to check weather the individual ships are sunk.
 Then a larger helper that is all ships are sunk returm true fals... run return string in hostgame... """