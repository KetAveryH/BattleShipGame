"""
To begin we will want to start with the creation of an 8x8 grid
"""

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
        s += '\u2B1C'*(self.width + 2) + '\n'                        
        
        for row in range(1, self.height+1):
            s += str(row-1)
            s += '\u2B1C'
            for col in range(0, self.width):
                s += self.data[row-1][col] + ''
            s += "\u2B1C"
            s += '\n'
        s += ' '
        s += (self.width +1) * '\u2B1C'   # Bottom of the board
        s += '\u2B1C'

        return s       # Return the Board



d = Board(10,10)