# Ashley Naratadam

class Node:
    def __init__(self, board = None, parent = None, score = 0, aiScore = 0):
        self.board = board # will contain game board in form of 2D list
        self.parent = parent
        self.score = score # player's score
        self.aiScore = aiScore # AI's score

    def __str__(self):
        return str(self.board)


    def printBoard(self): # prints out game board and both scores
        maxlen = max((len(str(item)) for l in self.board for item in l))
        for row in self.board:
            print(" ".join(["{:<{maxlen}}".format(item, maxlen=maxlen) for item in row]))
        print "Your score: " + str(self.score) + "  Computer score: " + str(self.aiScore)

    def gameOver(self):
        for i in range(0,9):
            if self.board[0][i] == []: # check if first row has any empty spaces left
                return False
        return True

    def tileScore(self, row, col, player): # computes number of points resulting from a given move
        points = 0
        # points are determined based on relative position to "player's" other pieces
        # 1 point for diagonals. 2 points for pieces that are right next to or above or below each other
        if col < 8:
            if row < 8:
                if self.board[row + 1][col + 1] == player:
                    points += 1
            if row > 0:
                if self.board[row - 1][col + 1] == player:
                    points += 1
            if self.board[row][col + 1] == player:
                points += 2  # directly to right
        if col > 0:
            if row < 8:
                if self.board[row + 1][col - 1] == player:
                    points += 1  # diag bot left
            if row > 0:
                if self.board[row - 1][col - 1] == player:
                    points += 1  # diag top left
            if self.board[row][col - 1] == player:
                points += 2  # to left
        if row < 8:
            if self.board[row + 1][col] == player:
                points += 2  # down
        if row > 0:
            if self.board[row - 1][col] == player:
                points += 2  # up
        return points

    def move(self, col, player): # returns new node with board that has newly inserted tile & updated scores
        if (col < 0) or (col > 8):
            return None
        temp = [x[:] for x in self.board]
        for i in reversed(xrange(9)):
            if temp [i][col] == []:
                temp[i][col] = player
                s = self.tileScore(i, col, player)
                if player == 'O':
                    return Node(temp, self, self.score+s, self.aiScore)
                if player == 'X':
                    return Node(temp, self, self.score, self.aiScore+s)
        return None

    def expand(self): # returns list with a node's successors
        successors = []
        for i in range(0,9):
            x = self.move(i, 'X')
            successors.append(x)
        return successors


    def getCol(self): # gets col number for newly placed tile (compares board with parent board)
        for i in range(0,9):
            for j in range(0,9):
                if self.board[i][j] == 'X' and self.parent.board[i][j] != 'X': # used for AI
                    return j
        return None



def minimax(node, ply, isMaxPlayer): # main algorithm; boolean set to True for AI

    if ply == 0 or node.gameOver(): # if it's a leaf node, return score difference and column that a piece was dropped into to get this board
        return node.aiScore-node.score, node.getCol() # utility value that AI tries to maximize and col number

    elif isMaxPlayer: # AI is maximizing player
        best = 0
        c = 0
        for state in node.expand():
            if state is not None:
                val = (minimax(state, ply-1, False))[0] # recursively call minimax on successors
                if val > best:
                    c = state.getCol() # holds on to col number for maximizing move
                    best = val # holds max value
        return best, c
    else: # simulates minimizing player
        best = float("inf")
        c = 0
        for state in node.expand():
            if state is not None:
                val = (minimax(state, ply-1, True))[0] # recursive minimax call
                if val < best:
                    c = state.getCol()
                    best = val # holds on to minimum utility  value

        return best, c # best returns utility value for best move; c returns the column for best move


def minimaxDec(node, ply, isMaxPlayer): # returns the column the AI should drop it's piece into
    x = minimax(node, ply, isMaxPlayer)
    # isMaxPlayer is True for AI
    return x[1]



def main():



    print("Hello! Ready to play Simacogo? You will be player O.")
    plys = int(raw_input("First, select the number of plys for your opponent: "))
    gameBoard = Node([[[] for i in range(0,9)]for j in range(0,9)])
    while not gameBoard.gameOver():
        choice = int(raw_input("Your move? (pick from columns 1-9):  "))
        choice = choice -1
        while (gameBoard.board[0][choice] != []):  # make sure col isn't full
            choice = int(raw_input("This column is full. Please pick another: "))
            choice = choice -1

        gameBoard = gameBoard.move(choice, 'O')
        if not gameBoard.gameOver():
            gameBoard.printBoard()
            print "Your opponent is thinking..."
            x = minimaxDec(gameBoard, plys, True )
            gameBoard = gameBoard.move(x, 'X')
            gameBoard.printBoard()
        else:
            print "Game over!"
            gameBoard.printBoard()
            return





if __name__ == "__main__":
    main()

