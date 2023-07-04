import io
from stockfish import Stockfish
import chess.pgn

stockfish = Stockfish()


def read_game():
    file = open('../test_games/test_game.pgn', 'r')
    game = chess.pgn.read_game(file)

    board = game.board()

    for move in game.mainline_moves():

        board.push(move)
        print(board, '\n\n')

    return board


print(read_game())
