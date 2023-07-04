import io

from db_chess.db_parse import Game
import chess.pgn


def main():
    p = io.StringIO('test_games/test_game.pgn')
    game = Game(p)
    game.read_and_parse_game()
    print(game.done_moves)


if __name__ == '__main__':
    main()
