import numpy as np

#Gameboard Class.  Handles all movement on gameboard.
class Gameboard:
    def __init__(self):
        self.status = [[0] * 8 for _ in range(8)]
        self.player = 'w'
        self.columns = {'a' : 0, 'b' : 1, 'c' : 2, 'd' : 3, 'e' : 4, 'f' : 5, 'g' : 6, 'h' : 7}
        self.wking = None
        self.bking = None

#Translates chess coordinates into list coordinates
    def translate(self, move):
        row = int(move[1]) - 1
        column = self.columns[move[0]]
        return[row, column]

#Returns a piece at a given position
    def get_piece(self, position):
        return self.status[position[0]][position[1]]

#Returns a nested list of the board state across a certain atrribut of the pieces on the board.
    def slice(self, attribute):
        return [[getattr(x, attribute) if not isinstance(x, int) else x for x in sublist] for sublist in self.status]

#Restarts/initializes the game
    def reset(self):
        for cls in Chesspiece.__subclasses__():
            dum = cls()
            i = 0
            for (x, y) in dum.startpositions:
                p = cls(id=i, player='w', position=[x,y], board=self)
                self.status[x][y] = p
                p2 = cls(id = -i, player='b', position=[7-x,7-y], board=self)
                self.status[-(x+1)][-(y+1)] = p2
                i += 1
            self.wking = self.status[0][3]
            self.bking = self.status[7][4]

#Renders the board state
    def render(self, attribute):
        row = 8

        print('   ', end='')
        print(list(self.columns.keys())[0], end='')
        for i in range(1, 8):
            print('--' + list(self.columns.keys())[i], end='')
        print('')

        for i in self.slice(attribute)[::-1]:
            print(row, end=' ')

            for j in i:
                if j == 0:
                    j = '  '
                print('|' + str(j), end = '')
            print('|', end='')
            print(' ' + str(row), end=' ')
            print()
            row -= 1

        print('   ', end='')
        print(list(self.columns.keys())[0], end='')
        for i in range(1, 8):
            print('--' + list(self.columns.keys())[i], end='')
        print('')


#Takes user input for a move, tests inputs for basic sanity then runs check_move() to see if move is valid
    def make_a_move(self):
        while 1 == 1:
            try:
                start = self.translate(input(self.player + "'s turn! Pick a piece!").split(','))
                start = list(map(int, start))
                piece = self.status[start[0]][start[1]]

                if piece == 0:
                    print('not a piece!')
                    continue

                if piece.player != self.player:
                    print('Not your piece!')
                    continue

                end = self.translate(input("to?").split(','))
                end = list(map(int, end))
            except:
                print('Out of bounds!')
                continue

            if self.check_move(start,end) == True:
                break

            print(self.check_move(start,end))

        self.status[start[0]][start[1]] = 0
        self.status[end[0]][end[1]] = piece
        piece.position = end
        piece.move_history.append(start)

#checks if move is valid
    def check_move(self, start, end):
        piece = self.status[start[0]][start[1]]
        where = list(np.array(end) - np.array(start))
        try:
            if self.status[end[0]][end[1]].player == self.player:
                return "can't eat your piece!"
        except:
            pass
        for element in piece.moves():
            if where in element:
                track = [x[element.index(where)] for x in piece.moves()]
                for i in track[1:track.index(where)]:
                    path = list(np.array(start)+np.array(i))
                    if self.status[path[0]][path[1]] != 0:
                        return 'Move blocked by other Piece!'
                return True
        print('Not a Valid Move!')
        return False

#Checks if current player is in check
    def test_check(self):
        piecelist = [x for element in self.status for x in element if (x != 0 and x.player == self.player)]
        if self.player == 'w':
            king = self.bking
        else:
            king = self.wking
        for x in piecelist:
            if self.check_move(start=x.position, end=king.position) == True:
                print("you're in check")
                if self.test_checkmate(piecelist, king) == True:
                    return True

        if self.player == 'w':
            self.player = 'b'
        else:
            self.player = 'w'

#Checks if given position is on the board
    def inboard(self, move):
        if (move[i] > 7) or (move[i] < 0) or (move[j] > 7) or (move[i] < 0):
            return False
        else:
            return True

#Tests to see if current player is in checkmate
    def test_checkmate(self, piecelist, king):
        strikes = 0
        for move in king.moves():
            end = king.position + move
            try:
                strikes += 1
                for piece in piecelist:
                    if self.check_move(start=piece.position, end=end) == True:
                        strikes -=1
            except:
                continue
            if strikes == 0:
                return False
        return True


#Chess Pieces
class Chesspiece:
    def __init__(self, id=0, player='w', position = [0,0], board=Gameboard()):
        self.base_moves = []
        self.player = player
        self.id = id
        self.name = self.__class__.__name__
        self.move_history = []
        self.position = position
        self.board = board

    def moves(self):
        return [(np.array(self.base_moves) * n).tolist() for n in range(9)]

class Pawn(Chesspiece):
    def __init__(self, id=0, position = [0,0], player='w', board=Gameboard()):
        super().__init__(id, player, position, board)
        self.startpositions = [(1, x) for x in range(8)]
        self.base_moves = []
        self.shortname = self.player + 'p'

    def moves(self):
        moves = []
        moves2 = []
        if self.player == 'w':
            moves2.append([1,0])
            if self.move_history == []:
                moves2.append([2,0])
        else:
            moves2.append([-1, 0])
            if self.move_history == []:
                moves2.append([-2,0])

        for i in (1, -1):
            if self.player == 'w':
                try:
                    if self.board.status[self.position[0]+1][self.position[1] + i]:
                        moves2.append([1, i])
                except:
                    continue
            else:
                try:
                    if self.board.status[self.position[0] - 1][self.position[1] + i]:
                        moves2.append([-1, i])
                except:
                    continue
        moves.append(moves2)
        return moves

class Rooke(Chesspiece):
    def __init__(self, id=0, position = [0,0], player='w', board=Gameboard()):
        super().__init__(id, player, position, board)
        self.startpositions = [(0,0), (0,7)]
        self.base_moves =  [(1,0), (0,1), (-1,0), (0,-1)]
        self.shortname = self.player + 'r'

class Bishop(Chesspiece):
    def __init__(self, id=0, position = [0,0], player='w', board=Gameboard()):
        super().__init__(id, player, position, board)
        self.startpositions = [(0,2), (0,5)]
        self.base_moves = [(1, 1), (-1, -1), (-1, 1), (1, -1)]
        self.shortname = self.player + 'b'

class Knight(Chesspiece):
    def __init__(self, id=0, position = [0,0], player='w', board=Gameboard()):
        super().__init__(id, player, position, board)
        self.startpositions = [(0,1), (0,6)]
        self.base_moves = [[[2,1], [2,-1], [1,2], [1,-2],[-2,1], [-2,-1], [-1,2], [-1,-2]]]
        self.shortname = self.player + 'k'

class King(Chesspiece):
    def __init__(self, id=0, position = [0,0], player='w', board=Gameboard()):
        super().__init__(id, player, position, board)
        self.startpositions = [(0,3)]
        self.base_moves = [(1,0), (0,1), (-1,0), (0,-1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        self.shortname = self.player + 'K'

        def moves(self):
            return self.base_moves

class Queen(Chesspiece):
    def __init__(self, id=0, position = [0,0], player='w', board=Gameboard()):
        super().__init__(id, player, position, board)
        self.base_moves = [(1,0), (0,1), (-1,0), (0,-1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        self.startpositions = [(0,4)]
        self.shortname = self.player + 'Q'

def play():
    board = Gameboard()
    board.reset()
    print(board.status)
    board.render('shortname')
    i = 1
    while i != 5:
        board.make_a_move()
        board.render('shortname')
        board.test_check()
play()


