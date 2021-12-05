"""
To begin we will want to start with the creation of an 8x8 grid
"""
white = '\u2B1C'
blue = '\U0001f7e6'
red = '\U0001F7E5'
weird = '\U0001F533'

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
        col = col.lower()
        if col in letcol:
            return letcol.get(col)
        
        return False


class Board:
    

    def __init__(self, width, height):
        """Construct objects of type Board, with the given width and height."""
        self.width = width
        self.height = height
        self.data = [[blue]*width for row in range(height)]
        self.data2 = [[weird]*width for row in range(height)]
        self.data3 = [[red]*width for row in range(height)]
        self.data4 = [[red]*width for row in range(height)]


    def __repr__(self):
        """This method returns a string representation
            for an object of type Board.
        """
        alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        
        s = ''                          # The string to return
        
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
                s += self.data[row][col] + ''
            s += "\u2B1C"
            s += "  "
            s += str(row)
            s += '\u2B1C'
            for col in range(0, self.width):
                s += self.data2[row][col] + ''
            s += "\u2B1C"



            s += '\n'
        s += ' '
        s += (self.width +2) * '\u2B1C' +  "   " + (self.width +2) * '\u2B1C' # Bottom of the board
        

        return s       # Return the Board

    def allowsMove(self, col, row, l, ori):
        """Checks whether a ship placement will be allowed. Accepts:
        Col, a number representing a letter where ship starts
        Row, a number representing how far down to start
        l, the length of the ship in question (>=1)
        ori, either 'up' 'down' 'left' 'right'"""
        if not( 0 <= row and row <= self.height) or not( 0 <= col and col <= self.width):   #check to make sure that the row and col are in the given range of self board
            print('something went wrong, coords not in range')
            return False
        if ori == 'up':      #Start for each orientation... 'up' 'down' 'left' 'right'
            if (row+1)-l < 0:    #check to make sure that the L for each ori isn't too long for the board
                print('you did something wrong, if up')
                return False #Here we will reprompt the player in a later function
            for x in range(l):   #check to make sure that the places we will place the ship are empty
                if self.data[row-x][col] !=  blue:
                    print("you did something wrong, for loop up")
                    return False
            return True      #all good! let the magic happen
        if ori == 'down':
            if (row)+l > self.height: 
                print('you did something wrong, if down')
                return False #Here we will reprompt the player in a later function
            for x in range(l):
                if self.data[row+x][col] !=  blue:
                    print("you did something wrong, for loop down")
                    return False
            return True
        if ori == 'left':
            if (col+1)-l < 0:
                print('you did something wrong, if left')
                return False
            for x in range(l):
                if self.data[row][col-x] !=  blue:
                    print("you did something wrong, for loop left")
                    return False
            return True
        if ori == 'right':
            if row+l > self.width:
                print('you did something wrong, if right')
                return False
            for x in range(l):
                if self.data[row][col+x] != blue:
                    print("you did something wrong, for loop right")
                    return False
            return True
        print("you did something wrong, no ori assigned")
        return False

    def placeShip(self, col, row, l, ori):
        """"""
        if ori == 'up':
            for x in range(l):
                self.data[row-x][col] = white
        if ori == 'down':
            for x in range(l):
                self.data[row+x][col] = white
        if ori == 'left':
            for x in range(l):
                self.data[row][col-x] = white
        if ori == 'right':
            for x in range(l):
                self.data[row][col+x] = white
    
    def shot(self, col, row, player):
        """
        This function will check whether the given point is a 'hit', 
        'miss', or 'False' (meaning the position is not valid). A
        position is not valid if it is out of bounds, or has been already hit.
        """
        if player == "player":
            
        if not( 0 <= row and row <= self.height) or not( 0 <= col and col <= self.width):   #check to make sure that the row and col are in the given range of self board
            print('something went wrong, coords not in range')
            return False
        if self.data[col][row] == white:
            return 'hit'
        if self.data[col][row] == blue:
            return 'miss'
    

    
        
d = Board(10,10)
f = Board(10,10)