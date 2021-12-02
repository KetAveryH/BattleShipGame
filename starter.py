"""
To begin we will want to start with the creation of an 8x8 grid
"""
blue = '\u2B1C'
class Board:
    

    def __init__(self, width, height):
        """Construct objects of type Board, with the given width and height."""
        self.width = width
        self.height = height
        self.data = [['\U0001f7e6']*width for row in range(height)]

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
        s += '\n'  + ' ' 
        s += blue*(self.width + 2) + '\n'                        
        
        for row in range(1, self.height+1):
            s += str(row-1)
            s += blue
            for col in range(0, self.width):
                s += self.data[row-1][col] + ''
            s += "\u2B1C"
            s += '\n'
        s += ' '
        s += (self.width +1) * blue   # Bottom of the board
        s += blue

        return s       # Return the Board

    def allowsMove(self, col, row, l, ori):
        #Up Orientation
        if not( 0 <= row and row <= self.height) or not( 0 <= col and col <= self.width):
            return False
            return False
        if ori == 'up':
            if (row+1)-l < 0: 
                return False #Here we will reprompt the player in a later function
            for x in range(l):
                if self.data[row-x][col] !=  blue:
                    return False
            else:
                return True
        if ori == 'down':
            if (row)+l <= self.height: 
                return False #Here we will reprompt the player in a later function
            for x in range(l):
                if self.data[row+x][col] !=  blue:
                    return False
            else:
                return True
        if ori == 'left':
            if (col+1)-l < 0:
                return False
            for x in range(l):
                if self.data[row][col-x] !=  blue:
                    return False
            




d = Board(10,10)