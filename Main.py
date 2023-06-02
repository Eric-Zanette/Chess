import ChessObjects

def play():
    board = ChessObjects.Gameboard()
    board.reset()
    print(board.status)
    board.render('shortname')

    while 1 = 1:
        #makes a move, renders the new board and switches players
        board.make_a_move()
        board.render('shortname')
        board.player_swap()

        #Tests to see if player is in checkmate, if so asks for another game
        if board.test_check() == True:
            board.player_swap()
            print(f'Game Over {self.player} Wins!')
            board.reset()
            if input("Another Game?") == "y":
                continue
            else:
                break

play()
