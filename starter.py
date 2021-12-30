import random
import copy
import time
"""
To begin we will want to start with the creation of an 8x8 grid
"""
white = '\u2B1C'    #defining our colored squares for use throughout
blue = '\U0001f7e6'
red = '\U0001F7E5'
weird = '\U0001F533'
black = '\U00002B1B'

playerWinCount = 0
aiWinCount = 0

# Create a converter, so we can take in A4 or C2, then actually use 04 or 22 (index starts at 0)
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

collet = {
        0 : "a",
        1 : "b",
        2 : "c",
        3 : "d",
        4 : "e",
        5 : "f",
        6 : "g",
        7 : "h",
        8 : "i",
        9 : "j",
        10: "k",
        11: "l",
        12: "m",
        13: "n",
        14: "o",
        15: "p",
        16: "q",
        17: "r",
        18: "s",
        19: "t",
        20: "u",
        21: "v",
        22: "w",
        23: "x",
        24: "y",
        25: "z",
        }
def convertCord(col):
    """Create a converter, so we can take in A4 or C2, then actually use 04 or 32"""
    col = col.lower()
    if col in letcol:
        return letcol.get(col)
    
    return False

def revertCord(col):
    """create a reverter, inverse of convertCord, so that we can take in 02 or 32, the actually print A2 or C2"""
    if col in collet:
        return collet.get(col).upper()
    
    return False

def getcolrow(self):
    """Smart function which prompts for a board input. This input must be within range of the board, and a valid combo of letter + number, before getcolrow accepts the input"""
    while True:
        colrow = input("Remember to input in the form A7, D4, I3, etc.  -  ")
        if len(colrow) > 2 or len(colrow) < 2:
            print("Not understood! Target Length...")
            continue

        try:                   #Checks whether the first value of the string is a letter, if it is and returns an error it passes, if valid tells to re-enter
            let = colrow[0]
            let = let.upper()
            if let not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                print("Not understood! Not a letter...")
                continue
            if convertCord(let) not in [*range(self.width)]:
                print("Letter out of range!")
                continue
            dig = int(colrow[1])
            if dig not in [*range(self.height)]:
                print("Number out of range!")
                continue

            return let, dig
        except:
            print("Not understood!")
            continue




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
        self.dataATC = []
        self.dataPrevShot = [0,[],[],[],0,[],True, []] #7 is for perimeter targets
        self.scoreboard = [0,0]#  Player1/Player wins, vs AI/Player 2 wins

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
        s += '\n\n' + '       PLAYER SHIPS                   AI SHIPS'
        s += '\n\n' + '           ' + self.dataPSL[0][5] + '    <   CARRIER   >     ' + self.dataASL[0][5]
        s += '\n' + '           ' + self.dataPSL[1][4] + '    <  BATTLESHIP >     ' + self.dataASL[1][4]
        s += '\n' + '           ' + self.dataPSL[2][3] + '    <   CRUISER   >     ' + self.dataASL[2][3]
        s += '\n' + '           ' + self.dataPSL[3][3] + '    <  SUBMARINE  >     ' + self.dataASL[3][3]
        s += '\n' + '           ' + self.dataPSL[4][2] + '    <  DESTROYER  >     ' + self.dataASL[4][2]

        return s       # Return the Board

    def aiBoard(self):
        """Allows the ai's board to be displayed at will. Is typically hidden, as in a typical game of battleship. Adapted to display for AI games and PVP games."""
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

        s += '\n\n' + '       PLAYER SHIPS                   AI SHIPS'
        s += '\n\n' + '           ' + self.dataPSL[0][5] + '    <   CARRIER   >     ' + self.dataASL[0][5]
        s += '\n' + '           ' + self.dataPSL[1][4] + '    <  BATTLESHIP >     ' + self.dataASL[1][4]
        s += '\n' + '           ' + self.dataPSL[1][4] + '    <   CRUISER   >     ' + self.dataASL[2][3]
        s += '\n' + '           ' + self.dataPSL[1][4] + '    <  SUBMARINE  >     ' + self.dataASL[3][3]
        s += '\n' + '           ' + self.dataPSL[1][4] + '    <  DESTROYER  >     ' + self.dataASL[4][2]
        
        print(s)

    def clearBoard(self, p):
        """Clears the given boards, although is no longer in use. Will not properly clear boards!!!"""
        if p == 'player':
            self.dataPS = [[blue]*self.width for row in range(self.height)]
            self.dataPT = [[weird]*self.width for row in range(self.height)]
        if p == 'ai':                                                              #  RETIRED FUNCTION
            self.dataAS = [[blue]*self.width for row in range(self.height)]
            self.dataAT = [[weird]*self.width for row in range(self.height)]

    def allowsMove(self, col, row, ship, ori, p):
        """Checks whether a ship placement will be allowed. Accepts:
        Col, a number representing a letter where ship starts
        Row, a number representing how the starting row
        ship, the ship in question to be placed
        ori, either 'up' 'down' 'left' 'right', the orientation to place the ship starting at col,row
        p, the player upon whose board to place the ship"""
        if not( 0 <= row <= (self.height-1)) or not( 0 <= col <= (self.width-1)):   #check to make sure that the row and col are in the given range of self board
            #print('something went wrong, coords not in range')
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
                    #print('you did something wrong, if up')
                    return False #Here we will reprompt the player in a later function
                for x in range(l):   #check to make sure that the places we will place the ship are empty
                    if self.dataPS[row-x][col] !=  blue:
                        #print("you did something wrong, for loop up")
                        return False
                return True      #all good! let the magic happen
            if ori == 'down':
                if (row)+l > self.height: 
                    #print('you did something wrong, if down')
                    return False #Here we will reprompt the player in a later function
                for x in range(l):
                    if self.dataPS[row+x][col] !=  blue:
                        #print("you did something wrong, for loop down")
                        return False
                return True
            if ori == 'left':
                if (col+1)-l < 0:
                    #print('you did something wrong, if left')
                    return False
                for x in range(l):
                    if self.dataPS[row][col-x] !=  blue:
                        #print("you did something wrong, for loop left")
                        return False
                return True
            if ori == 'right':
                if col+l > self.width:
                    #print('you did something wrong, if right')
                    return False
                for x in range(l):
                    if self.dataPS[row][col+x] != blue:
                        #print("you did something wrong, for loop right")
                        return False
                return True
            #print("you did something wrong, no ori assigned")
            return False
        if p == 'ai':
            if ori == 'up':      #Start for each orientation... 'up' 'down' 'left' 'right'
                if (row+1)-l < 0:    #check to make sure that the L for each ori isn't too long for the board
                    #print('you did something wrong, if up')
                    return False #Here we will reprompt the player in a later function
                for x in range(l):   #check to make sure that the places we will place the ship are empty
                    if self.dataAS[row-x][col] !=  blue:
                        #print("you did something wrong, for loop up")
                        return False
                return True      #all good! let the magic happen
            if ori == 'down':
                if (row)+l > self.height: 
                    #print('you did something wrong, if down')
                    return False #Here we will reprompt the player in a later function
                for x in range(l):
                    if self.dataAS[row+x][col] !=  blue:
                        #print("you did something wrong, for loop down")
                        return False
                return True
            if ori == 'left':
                if (col+1)-l < 0:
                   #print('you did something wrong, if left')
                    return False
                for x in range(l):
                    if self.dataAS[row][col-x] !=  blue:
                        #print("you did something wrong, for loop left")
                        return False
                return True
            if ori == 'right':
                if col+l > self.width:
                    #print('you did something wrong, if right')
                    return False
                for x in range(l):
                    if self.dataAS[row][col+x] != blue:
                        #print("you did something wrong, for loop right")
                        return False
                return True
            #print("you did something wrong, no ori assigned")
            return False

    def validTarget(self, col, row, p):
        """KEY FUNCTION:  Determines whether a selected target is valid, given a converted col, row, and p's turn"""
        if not( 0 <= row <= (self.height-1)) or not( 0 <= col <= (self.width-1)):   #check to make sure that the row and col are in the given range of self board
            return False
        if p == 'ai':#   if ai's turn, check ai target board
            if self.dataAT[row][col] != weird:
                return False
        if p == 'player':#    If players turn, check players targer board
            if self.dataPT[row][col] != weird:
                return False
        return True

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
        """RETIRED FUNCTION:   Checks whether a given ship for a given p player is orientated vertically or horizontally. True if vertical, false if otherwise."""
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

    def possibilityPerimeter(self, coords):
        """
        THIS IS AN AI FUNCTION
        This function will take in a list of coordinates and output a list of valid coordinates
        that surround this list. It will not return it but make changes to data that is stored.
        It will simply return points that are above below and to the right of the given coordinates, and
        only return the coordinate if it is data point "weird". 
        The plan is to sum all of the individual possible perimeters of these individual points,
        then to subtract the points themselves from this list of possible perimeter coordinates
        input: [[5,5],[5,6],[5,7]]
        output: []
        """
        #self.dataAt[row, col]
        perimeter = []
        for i in range(len(coords)):
            if self.validTarget(coords[i][0]+1, coords[i][1], 'ai') == True: #checks if the given value DOWN 1 row is within range to avoid errors
                if self.dataAT[coords[i][0]+1][coords[i][1]] == weird:   #checks whether the value 1 row BELOW is valid
                    self.dataPrevShot[7] += [[coords[i][0]+1, coords[i][1]]] #adds to perimeter targets
            if self.validTarget(coords[i][0]-1, coords[i][1], 'ai') == True: #checks if the given value UP 1 row is within range to avoid errors
                if self.dataAT[coords[i][0]-1][coords[i][1]] == weird:   #checks whether the value 1 row BELOW is valid
                    self.dataPrevShot[7] += [[coords[i][0]-1, coords[i][1]]]
            if self.validTarget(coords[i][0], coords[i][1]+1, 'ai') == True: #checks if the given value 1 column RIGHT is within range to avoid errors
                if self.dataAT[coords[i][0]][coords[i][1]+1] == weird:   #checks whether the value 1 colimn RIGHT is valid
                    self.dataPrevShot[7] += [[coords[i][0], coords[i][1]+1]]
            if self.validTarget(coords[i][0], coords[i][1]-1, 'ai') == True: #checks if the given value 1 column RIGHT is within range to avoid errors
                if self.dataAT[coords[i][0]][coords[i][1]-1] == weird:   #checks whether the value 1 colimn RIGHT is valid
                    self.dataPrevShot[7] += [[coords[i][0], coords[i][1]-1]]
            
        for i in range(len(coords)):
            d.dataPrevShot[7].remove(coords[i])
        
    
        
    def randomPlacement(self, p):
        """
        This function will continuosly generate new coordinates and orientations until all ships are placed for a given p player or ai
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
        """RETIRED FUNCTION:  
        This function will add on to randomPlacement() by adding constraints, boats may never be touching
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

    def shot(self, col, row, p):
        """
        This executor preforms the necessary actions of a given shot, accepting col,row for p player's turn.
        it will print hit or miss, while changing the necessary grid tiles to red or blue.
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
    
    def shotPVP(self, col, row, p):
        """
        This function will check whether the given point is a 'hit', FOR PLAYER V PLAYER MODE
        'miss', or 'False' (meaning the position is not valid). A
        position is not valid if it is out of bounds, or has been already hit.
        Specifically for use in PVP, with adjusted messages
        """
        if p == 'ai':#   If Ai's turn
            if self.dataPS[row][col] == black:# check to see what the ai is hitting on the players board
                print("Player 2 Hit!")
                self.dataPS[row][col] = red
                self.dataAT[row][col] = red
            if self.dataPS[row][col] == blue:
                print("Player 2 Miss!")
                self.dataAT[row][col] = blue
        if p == 'player':#   If Players turn
            if self.dataAS[row][col] == black:# check to see what the player is hitting on the AI's board
                print("Player 1 Hit!")
                self.dataPT[row][col] = red
                self.dataAS[row][col] = red
            if self.dataAS[row][col] == blue:
                print("Player 1 Miss!")
                self.dataPT[row][col] = blue

    def randomShot(self, p):
        """For use by the dumb AI, shoots a random shot on p player's turn"""
        row = random.randint(0,9)
        col = random.randint(0,9)
        
        if p == 'ai':#   If Ai's turn
            self.dataPrevShot = [col, row]
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

    def randomCheckerCreation(self):
        """Helper which fills self.dataATC with the proper checkered pattern when called"""
        x = []
        for col in range(self.width):
            for row in range(self.height):
                if col%2 == row %2:
                    pass
                else:
                    x += [[col, row]]
        self.dataATC = x 

    def isClear(self):
        """checks whether a gameboard is clear, for use in starting a new game"""
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
        """Checks the locations of the carrier in p player's board, and sticks sunk into the location list if True. Also reports in print form when a ship has been sunk."""
        count = 0
        if p == 'player':                          
            if self.dataPSL[0][5] == 'sunk':
                return True
            
            for x in range(5):
                if self.dataPS[self.dataPSL[0][x][0]][self.dataPSL[0][x][1]] == red:
                    count += 1
                if count == 5:
                    self.dataPSL[0][5] = 'sunk'
                    print ("PLAYER 1 CARRIER HAS SUNK")
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
        """Checks the locations of the battleship in p player's board, and sticks sunk into the location list if True. Also reports in print form when a ship has been sunk."""

        count = 0
        if p == 'player':
            if self.dataPSL[1][4] == 'sunk':
                return True
            
            for x in range(4):
                if self.dataPS[self.dataPSL[1][x][0]][self.dataPSL[1][x][1]] == red:
                    count += 1
                if count == 4:
                    self.dataPSL[1][4] = 'sunk'
                    print('PLAYER 1 BATTLESHIP HAS SUNK')
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
        """Checks the locations of the cruiser in p player's board, and sticks sunk into the location list if True. Also reports in print form when a ship has been sunk."""

        count = 0
        if p == 'player':
            if self.dataPSL[2][3] == 'sunk':
                return True
            
            for x in range(3):
                if self.dataPS[(self.dataPSL[2][x][0])][self.dataPSL[2][x][1]] == red:
                    count += 1
                if count == 3:
                    self.dataPSL[2][3] = 'sunk'
                    print('PLAYER 1 CRUISER HAS SUNK')
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
        """Checks the locations of the submarine in p player's board, and sticks sunk into the location list if True. Also reports in print form when a ship has been sunk."""

        count = 0
        if p == 'player':
            if self.dataPSL[3][3] == 'sunk':
                return True
            
            for x in range(3):
                if self.dataPS[self.dataPSL[3][x][0]][self.dataPSL[3][x][1]] == red:
                    count += 1
                if count == 3:
                    self.dataPSL[3][3] = 'sunk'
                    print('PLAYER 1 SUBMARINE HAS SUNK')
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
        """Checks the locations of the destroyer in p player's board, and sticks sunk into the location list if True. Also reports in print form when a ship has been sunk."""

        count = 0
        if p == 'player':
            if self.dataPSL[4][2] == 'sunk':
                return True

            for x in range(2):
                if self.dataPS[self.dataPSL[4][x][0]][self.dataPSL[4][x][1]] == red:
                    count += 1
            if count == 2:
                self.dataPSL[4][2] = 'sunk'
                print('PLAYER 1 DESTROYER HAS SUNK')
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
    
    #def shipsSunk(self, p): #This function will basically run through all of the functions above and declare whenever a new ship has been destroyed
    
    def allSunk(self, p):
        """
        This runs all of the Sunk functions, and if they are all true it returns true to signal game end. Primarily used for AI v AI interaction.
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
            
    def oriValid(self, col, row):
        """Helper function to keep Ket's sanity. Allowed the AI to assign corresponding remaining orientatins to check for a hit location"""
        self.dataPrevShot[2] += [[]]
        if self.validTarget(col, row-1, 'ai'):  # This series of code checks whether a certain direction if valid and places it within correspondingOri
            self.dataPrevShot[2][-1] += 'U'
        if self.validTarget(col+1, row, 'ai'):
            self.dataPrevShot[2][-1] += 'R'
        if self.validTarget(col, row+1, 'ai'):
            self.dataPrevShot[2][-1] += 'D'
        if self.validTarget(col-1, row, 'ai'):
            self.dataPrevShot[2][-1] += 'L'

    def randomCheckerShot(self):
        """Function which lets ai execute a random shot out of a checkerboard. REPRESENTS STATE 0 OF OUR AI"""
        if not(self.dataATC):#  if list is empty, create it using above helper fn
            self.randomCheckerCreation()
        shot = random.choice(self.dataATC)#  Main point, return a random choice not done yet
        col = shot[0]
        row = shot[1]
        if self.dataPS[row][col] == black:# Check for shot being hit
            print("AI Targeted", revertCord(col), row, " and Hit!")
            self.dataPS[row][col] = red # changes players board
            self.dataAT[row][col] = red # changes ai target board
            self.dataATC.remove(shot) # removes target from checkered possible shots  ||||IMPLEMENT THIS IN OTHER STATE FUNCTIONS||||
            self.dataPrevShot[0] = 1 # Changes state to 1
            self.dataPrevShot[1] = [[col,row]]#  adds a new hit coord to groupHit      groupHit and correspondingOri are created at the same time, so the index of both lists correspond with one another. Acts like dictionary with index of list being the key 
            self.oriValid(col, row)
        if self.dataPS[row][col] == blue:       #if miss it simply removes a coordinate form the list of possible checkered shots
            print("AI Targeted", revertCord(col), row, " and Missed!")
            self.dataAT[row][col] = blue
            self.dataATC.remove(shot)

    def stateOne(self):   #Function is used once the first shot has been identified
        """State 1 of the AI brain, executes upon first contact"""
        state = self.dataPrevShot[0]
        groupHits = self.dataPrevShot[1]
        correspondingOri = self.dataPrevShot[2]
        direction = self.dataPrevShot[3]
        sunkLength = self.dataPrevShot[4]
        orStateDestroyer = copy.deepcopy(self.destroyerSunk('player'))

        ori = random.choice(correspondingOri[-1])   #Picks a random valid direction from the most recent correspondingOrientation
        col = groupHits[-1][0]
        row = groupHits[-1][1]  #sets coords of correspondingOrientation Shot
        
        
        if ori == "U":
            if 'U' in correspondingOri[-1]:
                correspondingOri[-1].remove('U') #
            #Performing the shot
            if self.dataPS[row-1][col] == black:# checks one above if it hits 
                print("AI Targeted", revertCord(col), row-1, " and Hit!")
                self.dataPS[row-1][col] = red
                self.dataAT[row-1][col] = red #changes data state on both boards to 'hit'
                direction = 'U'               #locks direction to 'U' aka Up
                self.dataPrevShot[3] = 'U'
                groupHits += [[col,row-1]]               # Adds a new coordinate to groupHit of type list, which allows it to add a new list of coords within the list
                self.oriValid(col, row-1)
                if orStateDestroyer == False and self.destroyerSunk('player') == True: #if the original state of the destroyer was false, and after the move the destroyer sunk, we want to add this to the summation of sunk ships, our 5th data variable, AKA sunk length
                    sunkLength += 2
                if sunkLength == len(groupHits):
                    state = 0
                    self.dataPrevShot[0] = 0
                if len(groupHits)-sunkLength > 0:
                    state = 2
                    self.dataPrevShot[0] = 2
            if self.dataPS[row-1][col] == blue:    
                print("AI Targeted", revertCord(col), row-1, " and Missed!")
                self.dataAT[row-1][col] = blue
            if [row-1,col] in self.dataATC:
                self.dataATC.remove([row-1,col])


        if ori == "D":
            if 'D' in correspondingOri[-1]:
                correspondingOri[-1].remove('D') #
            #Performing the shot
            if self.dataPS[row+1][col] == black:# checks one above if it hits 
                print("AI Targeted", revertCord(col), row+1, " and Hit!")
                self.dataPS[row+1][col] = red
                self.dataAT[row+1][col] = red #changes data state on both boards to 'hit'
                direction = 'D'               #locks direction to 'D' aka Down
                self.dataPrevShot[3] = 'D'
                groupHits += [[col,row+1]]               # Adds a new coordinate to groupHit of type list, which allows it to add a new list of coords within the list
                self.oriValid(col, row+1)       #Adds the valid ori's corresponding to the grouphit
                if orStateDestroyer == False and self.destroyerSunk('player') == True: #if the original state of the destroyer was false, and after the move the destroyer sunk, we want to add this to the summation of sunk ships, our 5th data variable, AKA sunk length
                    sunkLength += 2
                if sunkLength == len(groupHits):
                    state = 0
                    self.dataPrevShot[0] = 0
                if len(groupHits)-sunkLength > 0:
                    state = 2
                    self.dataPrevShot[0] = 2
            if self.dataPS[row+1][col] == blue:    
                print("AI Targeted", revertCord(col), row+1, " and Missed!")
                self.dataAT[row+1][col] = blue
            if [row+1,col] in self.dataATC:
                self.dataATC.remove([row+1,col])


        if ori == "L":
            if 'L' in correspondingOri[-1]:
                correspondingOri[-1].remove('L') #
            #Performing the shot
            if self.dataPS[row][col-1] == black:# checks one above if it hits 
                print("AI Targeted", revertCord(col-1), row, " and Hit!")
                self.dataPS[row][col-1] = red
                self.dataAT[row][col-1] = red #changes data state on both boards to 'hit'
                direction = 'L'               #locks direction to 'L' aka Left
                self.dataPrevShot[3] = 'L'
                groupHits += [[col-1,row]]               # Adds a new coordinate to groupHit of type list, which allows it to add a new list of coords within the list
                self.oriValid(col-1, row)
                if orStateDestroyer == False and self.destroyerSunk('player') == True: #if the original state of the destroyer was false, and after the move the destroyer sunk, we want to add this to the summation of sunk ships, our 5th data variable, AKA sunk length
                    sunkLength += 2
                if sunkLength == len(groupHits):
                    state = 0
                    self.dataPrevShot[0] = 0
                if len(groupHits)-sunkLength > 0:
                    state = 2
                    self.dataPrevShot[0] = 2
            if self.dataPS[row][col-1] == blue:    
                print("AI Targeted", revertCord(col-1), row, " and Missed!")
                self.dataAT[row][col-1] = blue
            if [row,col-1] in self.dataATC:
                self.dataATC.remove([row,col-1])


        if ori == "R":
            if 'R' in correspondingOri[-1]:
                correspondingOri[-1].remove('R') #
            #Performing the shot
            if self.dataPS[row][col+1] == black:# checks one above if it hits 
                print("AI Targeted", revertCord(col+1), row, " and Hit!")
                self.dataPS[row][col+1] = red
                self.dataAT[row][col+1] = red #changes data state on both boards to 'hit'
                direction = 'R'               #locks direction to 'R' aka Right
                self.dataPrevShot[3] = 'R'
                groupHits += [[col+1,row]]               # Adds a new coordinate to groupHit of type list, which allows it to add a new list of coords within the list
                self.oriValid(col+1, row)
                if orStateDestroyer == False and self.destroyerSunk('player') == True: #if the original state of the destroyer was false, and after the move the destroyer sunk, we want to add this to the summation of sunk ships, our 5th data variable, AKA sunk length
                    sunkLength += 2
                if sunkLength == len(groupHits):
                    state = 0
                    self.dataPrevShot[0] = 0
                if len(groupHits)-sunkLength > 0:
                    state = 2
                    self.dataPrevShot[0] = 2
            if self.dataPS[row][col+1] == blue:    
                print("AI Targeted", revertCord(col+1), row, " and Missed!")
                self.dataAT[row][col+1] = blue
            if [row,col+1] in self.dataATC:
                self.dataATC.remove([row,col+1])

    def stateTwo(self):
        """STATE TWO of ai brain function, executes shots once a ship orientation is proposed"""
        state = self.dataPrevShot[0]
        groupHits = self.dataPrevShot[1]
        correspondingOri = self.dataPrevShot[2]
        direction = self.dataPrevShot[3]
        sunkLength = self.dataPrevShot[4]
        orStateDestroyer = copy.deepcopy(self.destroyerSunk('player'))   #Here we are writing the original states of each ship in order to see whether our move has destroyed a ship or not
        orStateCruiser = copy.deepcopy(self.cruiserSunk('player'))       # This will keep track of whether we are truly "done" once a ship has been destroyed.
        orStateSubmarine = copy.deepcopy(self.submarineSunk('player'))
        orStateBattleship = copy.deepcopy(self.battleshipSunk('player'))
        orStateCarrier = copy.deepcopy(self.carrierSunk('player'))

        col = groupHits[-1][0]
        row = groupHits[-1][1]
        
        if direction not in correspondingOri[-1]:
            state = 3
            self.dataPrevShot[0] = 3
            self.stateThree()
            return
        
        if direction == "U":
            if 'U' in correspondingOri[-1]:
                correspondingOri[-1].remove('U') #
            #Performing the shot
            if self.dataPS[row-1][col] == black:# checks one above if it hits 
                print("AI Targeted", revertCord(col), row-1, " and Hit!")
                self.dataPS[row-1][col] = red
                self.dataAT[row-1][col] = red #changes data state on both boards to 'hit'
                direction = 'U'               #locks direction to 'U' aka Up
                self.dataPrevShot[3] = 'U'
                
                groupHits += [[col,row-1]]               # Adds a new coordinate to groupHit of type list, which allows it to add a new list of coords within the list
                self.oriValid(col, row-1)
                if orStateDestroyer == False and self.destroyerSunk('player') == True: #if the original state of the destroyer was false, and after the move the destroyer sunk, we want to add this to the summation of sunk ships, our 5th data variable, AKA sunk length
                    sunkLength += 2 
                if orStateCruiser == False and self.cruiserSunk('player') == True: 
                    sunkLength += 3
                if orStateSubmarine == False and self.submarineSunk('player') == True: 
                    sunkLength += 3
                if orStateBattleship == False and self.battleshipSunk('player') == True: 
                    sunkLength += 4
                if orStateCarrier == False and self.carrierSunk('player') == True: 
                    sunkLength += 5
                
            #Just a note, in step 3 we are going to have to remember targets
            if self.dataPS[row-1][col] == blue and len(groupHits)-sunkLength != 0:    #This basically checks, if you get a miss AND there are still ships left, go to state 3
                print("AI Targeted", revertCord(col), row-1, " and Missed!")
                self.dataAT[row-1][col] = blue
                state = 3
                self.dataPrevShot[0] = 2
            if sunkLength == len(groupHits):   #MAKE SURE THAT LEN(GROUP HITS) GIVES THE NUMBER OF COORDS[]
                state = 0
                self.dataPrevShot[0] = 0

            if [row-1,col] in self.dataATC:
                self.dataATC.remove([row-1,col])

        if direction == "D":
            if 'D' in correspondingOri[-1]:
                correspondingOri[-1].remove('D') #
            #Performing the shot
            if self.dataPS[row+1][col] == black:# checks one above if it hits 
                print("AI Targeted", revertCord(col), row+1, " and Hit!")
                self.dataPS[row+1][col] = red
                self.dataAT[row+1][col] = red #changes data state on both boards to 'hit'
                direction = 'D'               #locks direction to 'U' aka Up
                self.dataPrevShot[3] = 'D'
                groupHits += [[col,row+1]]               # Adds a new coordinate to groupHit of type list, which allows it to add a new list of coords within the list
                self.oriValid(col, row+1)
                if orStateDestroyer == False and self.destroyerSunk('player') == True: #if the original state of the destroyer was false, and after the move the destroyer sunk, we want to add this to the summation of sunk ships, our 5th data variable, AKA sunk length
                    sunkLength += 2 
                if orStateCruiser == False and self.cruiserSunk('player') == True: 
                    sunkLength += 3
                if orStateSubmarine == False and self.submarineSunk('player') == True: 
                    sunkLength += 3
                if orStateBattleship == False and self.battleshipSunk('player') == True: 
                    sunkLength += 4
                if orStateCarrier == False and self.carrierSunk('player') == True: 
                    sunkLength += 5
                
            #Just a note, in step 3 we are going to have to remember targets
            if self.dataPS[row+1][col] == blue and len(groupHits)-sunkLength != 0:    #This basically checks, if you get a miss AND there are still ships left, go to state 3
                print("AI Targeted", revertCord(col), row+1, " and Missed!")
                self.dataAT[row+1][col] = blue
                state = 3
                self.dataPrevShot[0] = 2
            if sunkLength == len(groupHits):   #MAKE SURE THAT LEN(GROUP HITS) GIVES THE NUMBER OF COORDS[]
                state = 0
                self.dataPrevShot[0] = 0
            if [row+1,col] in self.dataATC:
                self.dataATC.remove([row+1,col])

        if direction == "L":
            if 'L' in correspondingOri[-1]:
                correspondingOri[-1].remove('L') #
            #Performing the shot
            if self.dataPS[row][col-1] == black:# checks one above if it hits 
                print("AI Targeted", revertCord(col-1), row, " and Hit!")
                self.dataPS[row][col-1] = red
                self.dataAT[row][col-1] = red #changes data state on both boards to 'hit'
                direction = 'L'               #locks direction to 'U' aka Up
                self.dataPrevShot[3] = 'L'
                groupHits += [[col-1,row]]               # Adds a new coordinate to groupHit of type list, which allows it to add a new list of coords within the list
                self.oriValid(col-1,row)
                if orStateDestroyer == False and self.destroyerSunk('player') == True: #if the original state of the destroyer was false, and after the move the destroyer sunk, we want to add this to the summation of sunk ships, our 5th data variable, AKA sunk length
                    sunkLength += 2 
                if orStateCruiser == False and self.cruiserSunk('player') == True: 
                    sunkLength += 3
                if orStateSubmarine == False and self.submarineSunk('player') == True: 
                    sunkLength += 3
                if orStateBattleship == False and self.battleshipSunk('player') == True: 
                    sunkLength += 4
                if orStateCarrier == False and self.carrierSunk('player') == True: 
                    sunkLength += 5
                
            #Just a note, in step 3 we are going to have to remember targets
            if self.dataPS[row][col-1] == blue and len(groupHits)-sunkLength != 0:    #This basically checks, if you get a miss AND there are still ships left, go to state 3
                print("AI Targeted", revertCord(col-1), row, " and Missed!")
                self.dataAT[row][col-1] = blue
                state = 3
                self.dataPrevShot[0] = 2
            if sunkLength == len(groupHits):   #MAKE SURE THAT LEN(GROUP HITS) GIVES THE NUMBER OF COORDS[]
                state = 0
                self.dataPrevShot[0] = 0
            if [row,col-1] in self.dataATC:
                self.dataATC.remove([row,col-1])
            
        if direction == "R":
            if 'R' in correspondingOri[-1]:
                correspondingOri[-1].remove('R') #
            #Performing the shot
            if self.dataPS[row][col+1] == black:# checks one above if it hits 
                print("AI Targeted", revertCord(col+1), row, " and Hit!")
                self.dataPS[row][col+1] = red
                self.dataAT[row][col+1] = red #changes data state on both boards to 'hit'
                direction = 'R'               #locks direction to 'U' aka Up
                self.dataPrevShot[3] = 'R'
                groupHits += [[col-1,row]]               # Adds a new coordinate to groupHit of type list, which allows it to add a new list of coords within the list
                self.oriValid(col+1,row)
                if orStateDestroyer == False and self.destroyerSunk('player') == True: #if the original state of the destroyer was false, and after the move the destroyer sunk, we want to add this to the summation of sunk ships, our 5th data variable, AKA sunk length
                    sunkLength += 2 
                if orStateCruiser == False and self.cruiserSunk('player') == True: 
                    sunkLength += 3
                if orStateSubmarine == False and self.submarineSunk('player') == True: 
                    sunkLength += 3
                if orStateBattleship == False and self.battleshipSunk('player') == True: 
                    sunkLength += 4
                if orStateCarrier == False and self.carrierSunk('player') == True: 
                    sunkLength += 5
                
            #Just a note, in step 3 we are going to have to remember targets
            if self.dataPS[row][col+1] == blue and len(groupHits)-sunkLength != 0:    #This basically checks, if you get a miss AND there are still ships left, go to state 3
                print("AI Targeted", revertCord(col+1), row, " and Missed!")
                self.dataAT[row][col+1] = blue
                state = 3
                self.dataPrevShot[0] = 2
            if sunkLength == len(groupHits):   #MAKE SURE THAT LEN(GROUP HITS) GIVES THE NUMBER OF COORDS[]
                state = 0
                self.dataPrevShot[0] = 0
            if [row,col+1] in self.dataATC:
                self.dataATC.remove([row,col+1])

    def stateThree(self):
        """STATE THREE of ai brain, executes when state two runs out of hits forward, to run shots backwards from the origin"""
        state = self.dataPrevShot[0]
        groupHits = self.dataPrevShot[1]
        correspondingOri = self.dataPrevShot[2]
        direction = self.dataPrevShot[3]
        sunkLength = self.dataPrevShot[4]
        orStateDestroyer = copy.deepcopy(self.destroyerSunk('player'))   #Here we are writing the original states of each ship in order to see whether our move has destroyed a ship or not
        orStateCruiser = copy.deepcopy(self.cruiserSunk('player'))       # This will keep track of whether we are truly "done" once a ship has been destroyed.
        orStateSubmarine = copy.deepcopy(self.submarineSunk('player'))
        orStateBattleship = copy.deepcopy(self.battleshipSunk('player'))
        orStateCarrier = copy.deepcopy(self.carrierSunk('player'))

        if direction == 'U': 
            if self.dataPrevShot[6] == True:                   #This function basically picks opposite of the original direction from the FIRST hit in groupHits. If 
                col = groupHits[0][0]
                row = groupHits[0][1]
                if 'D' in correspondingOri[0]:
                    correspondingOri[0].remove('D') 
                self.dataPrevShot[6] = False
            else:
                col = groupHits[-1][0]
                row = groupHits[-1][1]
                if 'D' in correspondingOri[-1]:
                    correspondingOri[-1].remove('D')

            if self.dataPS[row+1][col] == black:# checks one above if it hits 
                print("AI Targeted", revertCord(col), row+1, " and Hit!")
                self.dataPS[row+1][col] = red
                self.dataAT[row+1][col] = red #changes data state on both boards to 'hit'
                groupHits += [[col,row+1]]               # Adds a new coordinate to groupHit of type list, which allows it to add a new list of coords within the list
                self.oriValid(col, row+1)  #adds all valid orientations for given groupHit coord
                if orStateDestroyer == False and self.destroyerSunk('player') == True: #if the original state of the destroyer was false, and after the move the destroyer sunk, we want to add this to the summation of sunk ships, our 5th data variable, AKA sunk length
                    sunkLength += 2 
                if orStateCruiser == False and self.cruiserSunk('player') == True: 
                    sunkLength += 3
                if orStateSubmarine == False and self.submarineSunk('player') == True: 
                    sunkLength += 3
                if orStateBattleship == False and self.battleshipSunk('player') == True: 
                    sunkLength += 4
                if orStateCarrier == False and self.carrierSunk('player') == True: 
                    sunkLength += 5
                if sunkLength == len(groupHits):
                    state = 0
                    self.dataPrevShot[0] = 0
                    self.dataPrevShot[6] = True#   Makes it a virgin again

            if self.dataPS[row+1][col] == blue:    
                print("AI Targeted", revertCord(col), row+1, " and Missed!")
                self.dataAT[row+1][col] = blue   #Moves onto next state
                if len(groupHits)-sunkLength > 0: #Moves onto the next state
                    state = 4
                    state = 0 #Temporary Shortcut Delete when state 4 Exists
                    self.dataPrevShot[0] = 0
                    self.dataPrevShot[6] = True#    Makes state 3 a virgin again (like me)



        if direction == "D":
            if self.dataPrevShot[6] == True:                   #This function basically picks opposite of the original direction from the FIRST hit in groupHits. If 
                col = groupHits[0][0]
                row = groupHits[0][1]
                if 'U' in correspondingOri[0]:
                    correspondingOri[0].remove('U') 
                self.dataPrevShot[6] = False
            else:
                col = groupHits[-1][0]
                row = groupHits[-1][1]
                if 'U' in correspondingOri[-1]:
                    correspondingOri[-1].remove('U')

            if self.dataPS[row-1][col] == black:# checks one above if it hits 
                print("AI Targeted", revertCord(col), row-1, " and Hit!")
                self.dataPS[row-1][col] = red
                self.dataAT[row-1][col] = red #changes data state on both boards to 'hit'
                groupHits += [[col,row-1]]               # Adds a new coordinate to groupHit of type list, which allows it to add a new list of coords within the list
                self.oriValid(col, row-1)  #adds all valid orientations for given groupHit coord
                if orStateDestroyer == False and self.destroyerSunk('player') == True: #if the original state of the destroyer was false, and after the move the destroyer sunk, we want to add this to the summation of sunk ships, our 5th data variable, AKA sunk length
                    sunkLength += 2 
                if orStateCruiser == False and self.cruiserSunk('player') == True: 
                    sunkLength += 3
                if orStateSubmarine == False and self.submarineSunk('player') == True: 
                    sunkLength += 3
                if orStateBattleship == False and self.battleshipSunk('player') == True: 
                    sunkLength += 4
                if orStateCarrier == False and self.carrierSunk('player') == True: 
                    sunkLength += 5
                if sunkLength == len(groupHits):
                    state = 0
                    self.dataPrevShot[0] = 0
                    self.dataPrevShot[6] = True#   Makes it a virgin again

            if self.dataPS[row-1][col] == blue:    
                print("AI Targeted", revertCord(col), row-1, " and Missed!")
                self.dataAT[row-1][col] = blue   #Moves onto next state
                if len(groupHits)-sunkLength > 0: #Moves onto the next state
                    state = 4
                    state = 0 #Temporary Shortcut Delete when state 4 Exists
                    self.dataPrevShot[0] = 0
                    self.dataPrevShot[6] = True#    Makes state 3 a virgin again (like me)



        if direction == "L":
            if self.dataPrevShot[6] == True:                   #This function basically picks opposite of the original direction from the FIRST hit in groupHits. If 
                col = groupHits[0][0]
                row = groupHits[0][1]
                if 'R' in correspondingOri[0]:
                    correspondingOri[0].remove('R') 
                self.dataPrevShot[6] = False
            else:
                col = groupHits[-1][0]
                row = groupHits[-1][1]
                if 'R' in correspondingOri[-1]:
                    correspondingOri[-1].remove('R')

            if self.dataPS[row][col+1] == black:# checks one above if it hits 
                print("AI Targeted", revertCord(col+1), row, " and Hit!")
                self.dataPS[row][col+1] = red
                self.dataAT[row][col+1] = red #changes data state on both boards to 'hit'
                groupHits += [[col+1,row]]               # Adds a new coordinate to groupHit of type list, which allows it to add a new list of coords within the list
                self.oriValid(col+1, row)  #adds all valid orientations for given groupHit coord
                if orStateDestroyer == False and self.destroyerSunk('player') == True: #if the original state of the destroyer was false, and after the move the destroyer sunk, we want to add this to the summation of sunk ships, our 5th data variable, AKA sunk length
                    sunkLength += 2 
                if orStateCruiser == False and self.cruiserSunk('player') == True: 
                    sunkLength += 3
                if orStateSubmarine == False and self.submarineSunk('player') == True: 
                    sunkLength += 3
                if orStateBattleship == False and self.battleshipSunk('player') == True: 
                    sunkLength += 4
                if orStateCarrier == False and self.carrierSunk('player') == True: 
                    sunkLength += 5
                if sunkLength == len(groupHits):
                    state = 0
                    self.dataPrevShot[0] = 0
                    self.dataPrevShot[6] = True#   Makes it a virgin again

            if self.dataPS[row][col+1] == blue:    
                print("AI Targeted", revertCord(col+1), row, " and Missed!")
                self.dataAT[row][col+1] = blue   #Moves onto next state
                if len(groupHits)-sunkLength > 0: #Moves onto the next state
                    state = 4
                    state = 0 #Temporary Shortcut Delete when state 4 Exists
                    self.dataPrevShot[0] = 0
                    self.dataPrevShot[6] = True#    Makes state 3 a virgin again (like me)


        if direction == "R":
            if self.dataPrevShot[6] == True:                   #This function basically picks opposite of the original direction from the FIRST hit in groupHits. If 
                col = groupHits[0][0]
                row = groupHits[0][1]
                if 'L' in correspondingOri[0]:
                    correspondingOri[0].remove('L') 
                self.dataPrevShot[6] = False
            else:
                col = groupHits[-1][0]
                row = groupHits[-1][1]
                if 'L' in correspondingOri[-1]:
                    correspondingOri[-1].remove('L')

            if self.dataPS[row][col-1] == black:# checks one above if it hits 
                print("AI Targeted", revertCord(col-1), row, " and Hit!")
                self.dataPS[row][col-1] = red
                self.dataAT[row][col-1] = red #changes data state on both boards to 'hit'
                groupHits += [[col-1,row]]               # Adds a new coordinate to groupHit of type list, which allows it to add a new list of coords within the list
                self.oriValid(col-1, row)  #adds all valid orientations for given groupHit coord
                if orStateDestroyer == False and self.destroyerSunk('player') == True: #if the original state of the destroyer was false, and after the move the destroyer sunk, we want to add this to the summation of sunk ships, our 5th data variable, AKA sunk length
                    sunkLength += 2 
                if orStateCruiser == False and self.cruiserSunk('player') == True: 
                    sunkLength += 3
                if orStateSubmarine == False and self.submarineSunk('player') == True: 
                    sunkLength += 3
                if orStateBattleship == False and self.battleshipSunk('player') == True: 
                    sunkLength += 4
                if orStateCarrier == False and self.carrierSunk('player') == True: 
                    sunkLength += 5
                if sunkLength == len(groupHits):
                    state = 0
                    self.dataPrevShot[0] = 0
                    self.dataPrevShot[6] = True#   Makes it a virgin again

            if self.dataPS[row][col-1] == blue:    
                print("AI Targeted", revertCord(col-1), row, " and Missed!")
                self.dataAT[row][col-1] = blue   #Moves onto next state
                if len(groupHits)-sunkLength > 0: #Moves onto the next state
                    state = 4
                    state = 0 #Temporary Shortcut Delete when state 4 Exists
                    self.dataPrevShot[0] = 0
                    self.dataPrevShot[6] = True#    Makes state 3 a virgin again (like me)      

    def stateFour(self):
        """
        State four will be triggered in the case that you hit along a line of ships, and the total amount of actual hits self.dataPrevShot[1] is not equal to the
        amount of hits that led to a ship being sunk, sunkShips, [4].0 If this is true and nothing was sunk at all it will first turn the other 
        direction, and if it hits a blue, it will then enact a guessing protocol around the perimeter of whats remaining.
        However, if you do sink a ship the program is coded to stop at that point, and remove the most recent hits from it's immediate memory, 
        which will be stored in self.dataPrevShot[5], "target hits". It will then choose the perimeter of the remaining "target hits". It would be
        useful to create a perimeter function now. It will define it's true perimeter as what is "weird".
        """

    def aiBrain(self):
                """
                Within this function we will determine the next move of the AI, it will cycle between behavorial states. (Like Picobot!)
                We will store all the data that this function uses in 'self.dataPrevShot'
                state 0: We have yet to hit something, checkerboard pattern shooting ensues.
                state 1: Our first hit, we check in a flower around it
                state 2: Direction Found, continue along this orientation
                state 3: Direction track ended, move in reverse to try and sink ship.
                state 4: State 3 established multiple ships in a grouping - currently not implemented, this is advanced.
                self.dataPrevShot = [0,[],[[coord],[coord]],[dir,dir,dir,dir]]],[],0]
                """
                state = self.dataPrevShot[0]
                groupHits = self.dataPrevShot[1]
                correspondingOri = self.dataPrevShot[2]
                direction = self.dataPrevShot[3]
                sunkLength = self.dataPrevShot[4]

                if state == 0:
                    self.randomCheckerShot()
                if state == 1:
                    self.stateOne()
                if state == 2:
                    self.stateTwo()
                if state == 3:
                    self.stateThree()

    def ai2BoardAIVAI(self):
        """Displays the AI board without bottom table of ships sunk. For use in AI v AI games."""
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
        print(s)

    #   Human V AI


    def hostGame(self):
        """Function which builds and hosts the main human v ai game, playing it until one player has sunk all of their opponents ships."""
        if self.isClear() == False:
            return print("Your Board is not clear! Clear it, then you can start a new game.")
        print("Welcome to Battleship!")
        print(self)
        print("\nWe will begin by placing your ships...")
        while True:#     Carrier
            print("Which grid tile would you like to start your aircraft carrier on (length 5)?  Use form A6, G4, etc.  -  ")
            let, dig = getcolrow(self)
            col = int(convertCord(let))
            row = dig
            print("How would you like to place it? Up, Down, Left or Right?")
            ori = input()
            ori = ori.lower()
            if self.allowsMove(col, row, 'carrier', ori, 'player'):
                self.placeShip(col, row, 'carrier', ori, 'player')
                print("\n\n\n")
                print(self)
                break
            else:
                print("Oh no! Something went wrong... Let's try that again")
        while True:#     Battleship
            print("Which grid tile would you like to start your battleship on (length 4)?  Use form A6, G4, etc.  -  ")
            let, dig = getcolrow(self)
            col = int(convertCord(let))
            row = dig
            print("How would you like to place it? Up, Down, Left or Right?")
            ori = input()
            ori = ori.lower()
            if self.allowsMove(col, row, 'battleship', ori, 'player'):
                self.placeShip(col, row, 'battleship', ori, 'player')
                print("\n\n\n")
                print(self)
                break
            else:
                print("Oh no! Something went wrong... Let's try that again")
        while True: #Submarine
            print("Which grid tile would you like to start your submarine on (length 3)?  Use form A6, G4, etc.  -  ")
            let, dig = getcolrow(self)
            col = int(convertCord(let))
            row = dig
            print("How would you like to place it? Up, Down, Left or Right?")
            ori = input()
            ori = ori.lower()
            if self.allowsMove(col, row, 'submarine', ori, 'player'):
                self.placeShip(col, row, 'submarine', ori, 'player')
                print("\n\n\n")
                print(self)
                break
            else:
                print("Oh no! Something went wrong... Let's try that again")
        while True:#Cruiser
            print("Which grid tile would you like to start your cruiser on (length 3)?  Use form A6, G4, etc.  -  ")
            let, dig = getcolrow(self)
            col = int(convertCord(let))
            row = dig
            print("How would you like to place it? Up, Down, Left or Right?")
            ori = input()
            ori = ori.lower()
            if self.allowsMove(col, row, 'cruiser', ori, 'player'):
                self.placeShip(col, row, 'cruiser', ori, 'player')
                print("\n\n\n")
                print(self)
                break
            else:
                print("Oh no! Something went wrong... Let's try that again")
        while True:#Destroyer
            print("Which grid tile would you like to start your destroyer on (length 2)?  Use form A6, G4, etc.  -  ")
            let, dig = getcolrow(self)
            col = int(convertCord(let))
            row = dig
            print("How would you like to place it? Up, Down, Left or Right?")
            ori = input()
            ori = ori.lower()
            if self.allowsMove(col, row, 'destroyer', ori, 'player'):
                self.placeShip(col, row, 'destroyer', ori, 'player')
                print("\n\n\n")
                print(self)
                break
            else:
                print("Oh no! Something went wrong... Let's try that again")
        print("\n\n\n\n\nGood Job Player! Looks like all your ships are placed! The ai will now place their ships")
        
        time.sleep(3)
        
        #   END OF PLAYER SHIP PLACING, START OF AI SHIP PLCEMENT

        #   temporary

        self.randomPlacement('ai')
        # self.placeShip(0,0,'carrier','down','ai')
        # self.placeShip(4,2,'battleship','right','ai')
        # self.placeShip(1,6,'submarine','down','ai')
        # self.placeShip(9,8,'cruiser','left','ai')
        # self.placeShip(4,6,'destroyer','right','ai')
        #   temporary

        #   END OF AI SHIP PLACEMENT, START OF PLAYER ROUND 1!

        #   Start of a COMPLETE round
        print("All done! Let's Begin!")
        time.sleep(2)
        while True:#   Player 1 Turn
            print("Player 1, it's your turn! Where would you like to target your opponent's board?")
            let, dig = getcolrow(self)
            col = int(convertCord(let))
            row = dig

            self.shot(col, row, 'player')
            
            self.carrierSunk('ai')
            self.battleshipSunk('ai')
            self.cruiserSunk('ai')
            self.submarineSunk('ai')
            self.destroyerSunk('ai')

            print(self)

            if self.carrierSunk('ai') and self.battleshipSunk('ai') and self.cruiserSunk('ai') and self.submarineSunk('ai') and self.destroyerSunk('ai'):
                print("GAME OVER, the AI Lost! Great Job Player!")
                self.scoreboard[0] += 1
                print("Scoreboard: ", self.scoreboard[0], "wins for Player, ", self.scoreboard[1], "wins for the AI!")
                break

            dhso = input("Player, press [ENTER] to end your turn! ...\n")

            #   START OF AI ROUND


            print("\n\n\n\nNow, It's AI's turn...\n\n\n")
            time.sleep(1)

            self.aiBrain()

            self.carrierSunk('player')
            self.battleshipSunk('player')
            self.cruiserSunk('player')
            self.submarineSunk('player')
            self.destroyerSunk('player')

            print(self)

            if self.carrierSunk('player') and self.battleshipSunk('player') and self.cruiserSunk('player') and self.submarineSunk('player') and self.destroyerSunk('player'):
                print("GAME OVER, the Player Lost! WooHoo go me, the AI!")
                self.scoreboard[1] += 1
                print("Scoreboard: ", self.scoreboard[0], "wins for Player, ", self.scoreboard[1], "wins for the AI!")
                break

   
    #   Player V Player


    def hostPlayerGame(self):
        """Hosts a player v. player game. More experimental, player tags may display slightly improperly at times, yet is functionally sound!"""
        if self.isClear() == False:
            return print("Your Board is not clear! Clear it, then you can start a new game.")
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nWelcome to Battleship! This is an experimental player vs. player mode, let's see what happens!")
        print("\nIt is worth noting... in this gamemode, Player 1 may be referred to as 'player' and player 2 as 'ai' (Below Board for instance).\n     Consider this an intentional goofy gag :P\n")
        print("Player 1's Board will always have a white border, while player 2 will have a black border. You will be required to turn the screen often, so get comfortable!\n\n\n\n")
        dhso = input("Press [ENTER] to continue...\n")
        print(self)
        print("\nWe will begin by placing your ships, Player 1... now would be the time to look away, Player 2!\n")
        dhso = input("Press [ENTER] to continue...\n")
        while True:#     Carrier
            print("Which grid tile would you like to start your aircraft carrier on (length 5)?  Use form A6, G4, etc.  -  ")
            let, dig = getcolrow(self)
            col = int(convertCord(let))
            row = dig
            print("How would you like to place it? Up, Down, Left or Right?")
            ori = input()
            ori = ori.lower()
            if self.allowsMove(col, row, 'carrier', ori, 'player'):
                self.placeShip(col, row, 'carrier', ori, 'player')
                print("\n\n\n")
                print(self)
                break
            else:
                print("Oh no! Something went wrong... Let's try that again")
        while True:#     Battleship
            print("Which grid tile would you like to start your battleship on (length 4)?  Use form A6, G4, etc.  -  ")
            let, dig = getcolrow(self)
            col = int(convertCord(let))
            row = dig
            print("How would you like to place it? Up, Down, Left or Right?")
            ori = input()
            ori = ori.lower()
            if self.allowsMove(col, row, 'battleship', ori, 'player'):
                self.placeShip(col, row, 'battleship', ori, 'player')
                print("\n\n\n")
                print(self)
                break
            else:
                print("Oh no! Something went wrong... Let's try that again")
        while True: #Submarine
            print("Which grid tile would you like to start your submarine on (length 3)?  Use form A6, G4, etc.  -  ")
            let, dig = getcolrow(self)
            col = int(convertCord(let))
            row = dig
            print("How would you like to place it? Up, Down, Left or Right?")
            ori = input()
            ori = ori.lower()
            if self.allowsMove(col, row, 'submarine', ori, 'player'):
                self.placeShip(col, row, 'submarine', ori, 'player')
                print("\n\n\n")
                print(self)
                break
            else:
                print("Oh no! Something went wrong... Let's try that again")
        while True:#Cruiser
            print("Which grid tile would you like to start your cruiser on (length 3)?  Use form A6, G4, etc.  -  ")
            let, dig = getcolrow(self)
            col = int(convertCord(let))
            row = dig
            print("How would you like to place it? Up, Down, Left or Right?")
            ori = input()
            ori = ori.lower()
            if self.allowsMove(col, row, 'cruiser', ori, 'player'):
                self.placeShip(col, row, 'cruiser', ori, 'player')
                print("\n\n\n")
                print(self)
                break
            else:
                print("Oh no! Something went wrong... Let's try that again")
        while True:#Destroyer
            print("Which grid tile would you like to start your destroyer on (length 2)?  Use form A6, G4, etc.  -  ")
            let, dig = getcolrow(self)
            col = int(convertCord(let))
            row = dig
            print("How would you like to place it? Up, Down, Left or Right?")
            ori = input()
            ori = ori.lower()
            if self.allowsMove(col, row, 'destroyer', ori, 'player'):
                self.placeShip(col, row, 'destroyer', ori, 'player')
                print("\n\n\n")
                print(self)
                break
            else:
                print("Oh no! Something went wrong... Let's try that again")
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nGood Job Player 1! Looks like all your ships are placed! Let's switch over to player 2\n\n")
        print("Here's where it starts to get experimental! Alright player 1, It's your turn to look away! Call player 2 back so they can place their ships...\n\n")
        dhso = input("Press [ENTER] to continue...\n")
        self.aiBoard()
        print("Here goes player 2!")

        #   PLAYER 2 SHIP PLACEMENT

        while True:#     Carrier
            print("Which grid tile would you like to start your aircraft carrier on (length 5)?  Use form A6, G4, etc.  -  ")
            let, dig = getcolrow(self)
            col = int(convertCord(let))
            row = dig
            print("How would you like to place it? Up, Down, Left or Right?")
            ori = input()
            ori = ori.lower()
            if self.allowsMove(col, row, 'carrier', ori, 'ai'):
                self.placeShip(col, row, 'carrier', ori, 'ai')
                print("\n\n\n")
                self.aiBoard()
                break
            else:
                print("Oh no! Something went wrong... Let's try that again")
        while True:#     Battleship
            print("Which grid tile would you like to start your battleship on (length 4)?  Use form A6, G4, etc.  -  ")
            let, dig = getcolrow(self)
            col = int(convertCord(let))
            row = dig
            print("How would you like to place it? Up, Down, Left or Right?")
            ori = input()
            ori = ori.lower()
            if self.allowsMove(col, row, 'battleship', ori, 'ai'):
                self.placeShip(col, row, 'battleship', ori, 'ai')
                print("\n\n\n")
                self.aiBoard()
                break
            else:
                print("Oh no! Something went wrong... Let's try that again")
        while True: #Submarine
            print("Which grid tile would you like to start your submarine on (length 3)?  Use form A6, G4, etc.  -  ")
            let, dig = getcolrow(self)
            col = int(convertCord(let))
            row = dig
            print("How would you like to place it? Up, Down, Left or Right?")
            ori = input()
            ori = ori.lower()
            if self.allowsMove(col, row, 'submarine', ori, 'ai'):
                self.placeShip(col, row, 'submarine', ori, 'ai')
                print("\n\n\n")
                self.aiBoard()
                break
            else:
                print("Oh no! Something went wrong... Let's try that again")
        while True:#Cruiser
            print("Which grid tile would you like to start your cruiser on (length 3)?  Use form A6, G4, etc.  -  ")
            let, dig = getcolrow(self)
            col = int(convertCord(let))
            row = dig
            print("How would you like to place it? Up, Down, Left or Right?")
            ori = input()
            ori = ori.lower()
            if self.allowsMove(col, row, 'cruiser', ori, 'ai'):
                self.placeShip(col, row, 'cruiser', ori, 'ai')
                print("\n\n\n")
                self.aiBoard()
                break
            else:
                print("Oh no! Something went wrong... Let's try that again")
        while True:#Destroyer
            print("Which grid tile would you like to start your destroyer on (length 2)?  Use form A6, G4, etc.  -  ")
            let, dig = getcolrow(self)
            col = int(convertCord(let))
            row = dig
            print("How would you like to place it? Up, Down, Left or Right?")
            ori = input()
            ori = ori.lower()
            if self.allowsMove(col, row, 'destroyer', ori, 'ai'):
                self.placeShip(col, row, 'destroyer', ori, 'ai')
                print("\n\n\n")
                self.aiBoard()
                break
            else:
                print("Oh no! Something went wrong... Let's try that again")
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nCongratulations Players! You have placed your boards! They both look like this:")
        time.sleep(3)
        print('\n\n\nHAHAHA just kidding. But seriously, its about to be Player 1\'s turn, so uh idk maybe look away Player 2? Lmao\n\n')
        dhso = input("Press [ENTER] to continue...\n")
        print(self)
        # START OF GAMEPLAY - PLAYER V PLAYER

        while True:#   Player 1 Turn
            print("Player 1, it's your turn! Where would you like to target your opponent's board?")
            let, dig = getcolrow(self)
            col = int(convertCord(let))
            row = dig

            self.shotPVP(col, row, 'player')
            
            self.carrierSunk('ai')
            self.battleshipSunk('ai')
            self.cruiserSunk('ai')
            self.submarineSunk('ai')
            self.destroyerSunk('ai')

            print("Note - Refer to table below boards for most accurate sunk declarations :)\n")
            print(self)

            if self.carrierSunk('ai') and self.battleshipSunk('ai') and self.cruiserSunk('ai') and self.submarineSunk('ai') and self.destroyerSunk('ai'):
                print("GAME OVER, Player 2 Lost! Great Job Player 1!")
                self.scoreboard[0] += 1
                print("Scoreboard: ", self.scoreboard[0], "wins for Player 1, ", self.scoreboard[1], "wins for Player 2!")
                break

            dhso = input("Player 1, press [ENTER] to hide your board and end your turn! ...\n")
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            dhso = input("Player 2, press [ENTER] to start your turn!")

            #   START OF PLAYER 2 ROUND

            self.aiBoard()

            print("Player 2, it's your turn! Where would you like to target your opponent's board?")
            let, dig = getcolrow(self)
            col = int(convertCord(let))
            row = dig

            self.shotPVP(col, row, 'ai')
            
            self.carrierSunk('player')
            self.battleshipSunk('player')
            self.cruiserSunk('player')
            self.submarineSunk('player')
            self.destroyerSunk('player')

            print("Note â€“ YOUR SHIPS refers to player 1, ENEMY SHIPS refers to  :)\n")
            self.aiBoard()

            if self.carrierSunk('player') and self.battleshipSunk('player') and self.cruiserSunk('player') and self.submarineSunk('player') and self.destroyerSunk('player'):
                print("GAME OVER, Player 1 Lost! Great Job Player 2!")
                self.scoreboard[0] += 1
                print("Scoreboard: ", self.scoreboard[0], "wins for Player 1, ", self.scoreboard[1], "wins for Player 2!")
                break

            dhso = input("Player 2, press [ENTER] to hide your board and end your turn! ...\n")
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            dhso = input("Player 1, press [ENTER] to start your turn!")
            print(self)


    #   AI V AI


    def hostAIGame(self):
        """should host a game of AI vs AI, which runs itself while displaying prettily for the user's experience. Pits aiBrain(), a smart Battlship AI, against a random shooter \"Dumb\" Ai"""
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        print('Welcome to the AI v AI SMASHDOWN')           #introduction
        print('\n\nwhere my computer will butt heads with itself in a thrilling game of battleship madness')
        print('\n\nNOTE: AI 1 will be referred to as "player" in this game...')
        time.sleep(6)
        print('\n\n\n\n\n\n\n\n\n\n')
        print(d)
        print('AI 1 is shown as the board surrounded in WHITE')
        time.sleep(4)
        print('\n\n\n\n\n\n\n\n\n\n')
        print(d.ai2BoardAIVAI())
        print('AI 2 is shown as the board surrounded in BLACK')
        time.sleep(4)
        print('\n\n\n\n\n\n\n\n\n\n')
        print(d)
        print('AI 1... PLACE YOUR SHIPS')           #AI 1 placing ships
        time.sleep(4)
        print('\n\n\n\n\n\n\n\n\n\n')
        print(d.randomPlacement('player'))
        print('GREAT! AI 1 ships are placed')
        time.sleep(4)
        print('\n\n\n\n\n\n\n\n\n\n')
        print(d.ai2BoardAIVAI())
        print('AI 2... PLACE YOUR SHIPS')           #AI 2 placing ships
        time.sleep(4)
        print('\n\n\n\n\n\n\n\n\n\n')
        d.randomPlacement('ai')
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        print(d.ai2BoardAIVAI())
        print('GREAT! AI 2 ships are placed')
        time.sleep(4)
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nLET THE GAMES BEGIN')    #BEGIN!
        time.sleep(4)
        while d.allSunk('player') == False and d.allSunk('ai') == False:
            print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
            print(d.ai2BoardAIVAI())
            print(d)
            print('AI 1 TURN')
            d.randomShot('player')
            time.sleep(.1)
            print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
            print(d.ai2BoardAIVAI())
            print(d)
            print('AI 2 TURN')
            d.aiBrain()
            time.sleep(.1)
        if d.allSunk('player') == True:
            print('AI 1 WINS!')
            print(d.ai2BoardAIVAI())
            print(d)
        if d.allSunk('ai') == True:
            print('AI 2 WINS!')
            print(d.ai2BoardAIVAI())
            print(d)
        return
        # while d.allSunk('player') == False and d.allSunk('ai') == False:
            

print("\nScoreboard will display when you choose a gamemode and complete your first game!  ** Run d = Board(10,10) after a match for new board! **")
print("\nGamemodes:")
print("You can use d.hostGame() for our tailored Human versus AI experience! Good Luck!\nYou can try d.hostPlayerGame() for a classic player versus player experience! Grab a friend!\nYou can try d.hostAIGame() to watch a computer v computer showdown!")
print("\n   Created by: Ket Hollingsworth, Jackson Philion, and Jason Bowman - 2021 CS5 Final Project, \"battleship.py\"")


d = Board(10,10)

#       JACKSON PROGRESS 12/11 BELOW

"""Where did I leave off? Lots of progress... Fixed a lot of errors throughout the code, so unfortunately we might have to copy it through the entire thing
or else Ket will be copying changed for quite some time. I have written this update multiple times before realizing how much easier it will be for me to
finish the bit of code I was working on now. Think I got it. **One big error is an IndexError that breaks the funciton as I try to place ships, super inconvenient.
Other than that I keep getting such silly errors, diagnosing them for like 15 mins, then realizing that we fucking boofed a hunk of code. We need to play-test WAY
more often!! Would be much easier to diagnose these errors!!
"""