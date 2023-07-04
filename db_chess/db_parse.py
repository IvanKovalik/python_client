import chess.pgn
from stockfish import Stockfish
from io import StringIO


class Game:
    def __init__(self, path: StringIO = None, analyzing_ai: Stockfish = None):
        self.path = path
        self.stockfish = analyzing_ai
        self.done_moves = []

    def read_and_parse_game(self) -> None:
        """
        Reads the game and changes self.done_moves
        """

        game = chess.pgn.read_game(self.path)
        moves = game.mainline_moves()
        for move in moves:
            self.done_moves.append(move)
