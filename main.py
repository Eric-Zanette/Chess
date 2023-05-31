import numpy as np

#Gameboard
class Gameboard:
    def __init__(self):
        self.status = [[0] * 8 for _ in range(8)]
        self.player = 'w'
        self.columns = {'a' : 0, 'b' : 1, 'c' : 2, 'd' : 3, 'e' : 4, 'f' : 5, 'g' : 6, 'h' : 7}
        self.wking = None
        self.bking = None

    def translate(self, move):
        row = int(move[1]) - 1
        column = self.columns[move[0]]
        return[row, column]



    def slice(self, attribute):
        return [[getattr(x, attribute) if not isinstance(x, int) else x for x in sublist] for sublist in self.status]

    def reset(self):
        for cls in Chesspiece.__subclasses__():
            dum = cls(id=0, player=0)
            i = 0
            for (x, y) in dum.startpositions:
                p = cls(id=i, player='w', position=[x,y])
                self.status[x][y] = p
                p2 = cls(id = -i, player='b', position=[7-x,7-y])
                self.status[-(x+1)][-(y+1)] = p2
                i += 1
            self.wking = self.status[0][3]
            self.bking = self.status[7][4]

    def render(self, attribute):
        row = 8
        for i in self.slice(attribute)[::-1]:
            print(row, end=' ')
            row -=1
            for j in i:
                if j == 0:
                    j = ' '
                print('|' + str(j), end = '')
            print('|', end='')
            print()

        print('  ', end='')
        for i in range(8):
            print('-' + list(self.columns.keys())[i], end ='')
        print('')



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
                print('invalid input')
                continue

            if self.check_move(start,end):
                break

        self.status[start[0]][start[1]] = 0
        self.status[end[0]][end[1]] = piece
        piece.position = end
        piece.move_history.append(start)

        if self.player == 'w':
            self.player = 'b'
        else:
            self.player = 'w'


    def check_move(self, start, end):
        piece = self.status[start[0]][start[1]]
        where = list(np.array(end) - np.array(start))
        try:
            if self.status[end[0]][end[1]].player == self.player:
                print("can't eat your piece!")
                return False
        except:
            pass
        for element in piece.moves:
            if where in element:
                track = [x[element.index(where)] for x in piece.moves]
                for i in track[1:track.index(where)]:
                    path = list(np.array(start)+np.array(i))
                    if self.status[path[0]][path[1]] != 0:
                        print('Move blocked by other Piece!')
                        return False
                return True
        print('Not a Valid Move!')
        return False


    def test_check(self):
        piecelist = [x for element in self.status for x in element if x != 0]
        if player == 'w':
            king = self.wking
        else:
            king = self.bking
        for x in piecelist:
            self.check_move(start=x.position, end=king.position)
        print(piecelist)


#Chess Pieces
class Chesspiece:
    def __init__(self, id=0, player='w', position = [0,0], board=None):
        self.moves = []
        self.player = player
        self.id = id
        self.name = self.__class__.__name__
        self.move_history = []
        self.position = position
        self.board = board

    def move_range(self, moves, num):
        return [(np.array(moves) * n).tolist() for n in range(num)]

class Pawn(Chesspiece):
    def __init__(self, id=0, position = [0,0], player='w', board=None):
        super().__init__(id, player, position, board)
        self.startpositions = [(1, x) for x in range(8)]
        self.moves = self.move_range()
        self.shortname = 'p'

    def move_range(self):
        if self.player == 'w':
            if self.move_history == []:
                return [[[1,0], [2,0]]]
            else:
                return [[[1,0]]]
        else:
            if self.move_history == []:
                return [[[-2,0], [-1,0]]]
            else:
                return [[[-1,0]]]


class Rooke(Chesspiece):
    def __init__(self, id=0, position = [0,0], player='w', board=None):
        super().__init__(id, player, position, board)
        self.startpositions = [(0,0), (0,7)]
        self.moves =  self.move_range([(1,0), (0,1), (-1,0), (0,-1)], 9)
        self.shortname = 'r'

class Bishop(Chesspiece):
    def __init__(self, id=0, position = [0,0], player='w', board=None):
        super().__init__(id, player, position, board)
        self.startpositions = [(0,2), (0,5)]
        self.moves = self.move_range([(1, 1), (-1, -1), (-1, 1), (1, -1)], 9)
        self.shortname = 'b'

class Knight(Chesspiece):
    def __init__(self, id=0, position = [0,0], player='w', board=None):
        super().__init__(id, player, position, board)
        self.startpositions = [(0,1), (0,6)]
        self.moves = [(2,3), (3,2), (-3,2), (-2,3)]
        self.shortname = 'k'

class King(Chesspiece):
    def __init__(self, id=0, position = [0,0], player='w', board=None):
        super().__init__(id, player, position, board)
        self.startpositions = [(0,3)]
        self.moves = self.move_range([(1,1), (1,-1), (-1,1), (-1,-1)], 9)
        self.shortname = 'K'

class Queen(Chesspiece):
    def __init__(self, id=0, position = [0,0], player='w', board=None):
        super().__init__(id, player, position, board)
        self.moves = self.move_range([(1,0), (0,1), (-1,0), (0,-1), (1, 1), (-1, -1), (-1, 1), (1, -1)], 9)
        self.startpositions = [(0,4)]
        self.shortname = 'Q'

def play():
    board = Gameboard()
    board.reset()
    board.render('shortname')
    pawn = board.status[1][1]
    i = 1
    while i != 5:
        board.make_a_move()
        board.render('shortname')
        try:
            print(board.status[0][2].position)
            print(board.status[0][2].move_history)
        except:
            print("meh")


play()


