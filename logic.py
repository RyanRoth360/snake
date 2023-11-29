import random

class Logic():

    def __init__(self):
        self.board = self.clear_board()

    def clear_board(self):
        board = []
        row = []
        for r in range(15):
            row = []
            for c in range(15):
                row.append(' ')
            board.append(row)
        return board

    def generate_starting_pos(self):
        row = random.randrange(3,12)
        col = random.randrange(3,12)
        self.board[row][col]='S'
        self.board[row-1][col]=1
        self.board[row-2][col]=2

    def generate_piece(self,piece):
        row = random.randrange(0,15)
        col = random.randrange(0,15)
        while self.board[row][col]!=' ':
            row = random.randrange(0,15)
            col = random.randrange(0,15)

        self.board[row][col]=piece

    def find_piece(self,piece):
        for r in range(15):
            for c in range(15):
                if self.board[r][c]==piece:
                    return True
        return False 

    def erase_piece(self,piece):
        for r in range(15):
            for c in range(15):
                if self.board[r][c]==piece:
                    self.board[r][c]=' '

    def _get_head_index(self):
        for r in range(15):
            for c in range(15):
                if self.board[r][c]=='S':
                    return r,c 
        
    def move(self,direction,power_up):#Add bounds to this eventually

        row,col = self._get_head_index()
        og = (row,col)
        #Checks left,upper bounds
        if not power_up:
            if og[0]==0 and direction == 'left':
                return 'OOB'
            elif og[1]==0 and direction == 'up':
                return 'OOB'
            elif og[1]==14 and direction =='down':
                return 'OOB'
            elif og[0]==14 and direction=='right':
                return 'OOB'


        #accounts for directions
        if direction=='up':
            col = col-1
        elif direction=='down':
            col = col+1
            if og[1]==14: col = 0
        elif direction=='right':
            row = row+1
            if og[0]==14: row = 0
        elif direction=='left':
            row = row-1


        found = False
        for r in range(15):
            for c in range(15):
                if not found and self.board[r][c]=='S':

                    if self.board[row][col]==1:
                        self.board[r][c]='S'
                        return 'Delete'
                    elif type(self.board[row][col])==int:
                        if self.board[row][col]>1:
                            self.board[row][col]='S'
                            self.board[r][c]=99
                        return 'Crossed'
                            
                    else:
                        self.board[row][col]='S'
                        self.board[r][c]=' '
                        found = True
                        self._shift_snake(direction,og)
                              
    def _shift_snake(self,direction,og:tuple):
        
        new_x, new_y, = og
        
        number = 1
        for i in range(self._find_max()[0]):
            for r in range(15):
                for c in range(15):
                    if self.board[r][c]==number:
                        self.board[new_x][new_y]=number
                        self.board[r][c]=' '
                        new_x = r
                        new_y = c
                        number+=1
                                       
    def _find_max(self):
        max = 0 
        x_cord = -1
        y_cord = -1
        for r in range(15):
            for c in range(15):
                if type(self.board[r][c])==int:
                    if self.board[r][c]>max:
                        max = self.board[r][c]
                        x_cord = r
                        y_cord = c

        return int(max),x_cord,y_cord
    
    def add_tail(self,gold_power): 
        try:
            
            loops = 1
            if gold_power: loops = 3

            for i in range(loops):
                maximum, x_cord, y_cord = self._find_max()
                for r in range(x_cord-1,x_cord+2):#account for out of bounds
                    for c in range(y_cord-1,y_cord+2):
                        if type(self.board[r][c])==int:
                            if self.board[r][c]+1==self.board[x_cord][y_cord]:
                                x_dif = 2*(x_cord-r)
                                y_dif = 2*(y_cord-c)
                                self.board[r+x_dif][c+y_dif]=maximum+1
                                maximum+=1
        except IndexError:
            pass
                                 
    def get_board(self):
        return self.board

   

