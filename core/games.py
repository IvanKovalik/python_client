import bz2
import collections.abc
import re

import chess.pgn

moveRegex = re.compile(r'\d+[.][ .](\S+) (?:{[^}]*} )?(\S+)')


class GamesFile(collections.abc.Iterable):
    def __init__(self, path, cacheGames=False):
        self.path = path
        self.file = bz2.open(self.path, 'rt')

        self.cache = cacheGames
        self.games = []
        self.num_read = 0

    def __iter__(self):
        for g in self.games:
            yield g
        while True:
            yield self.loadNextGame()

    def loadNextGame(self):
        game = chess.pgn.read_game(self.file)
        if game is None:
            raise StopIteration
        if self.cache:
            self.games.append(game)
        self.num_read += 1
        return game

    def __getitem__(self, val):
        if isinstance(val, slice):
            return [self[i] for i in range(*val.indices(10 ** 20))]
        elif isinstance(val, int):
            if len(self.games) < val:
                return self.games[val]
            elif val < 0:
                raise IndexError("Negative indexing is not supported") from None
            else:
                g = self.loadNextGame()
                for i in range(val - len(self.games)):
                    g = self.loadNextGame()
                return g
        else:
            raise IndexError("{} is not a valid input".format(val)) from None

    def __del__(self):
        try:
            self.file.close()
        except AttributeError:
            pass


class LightGamesFile(object):
    def __init__(self, path, parseMoves=True, just_games=False):
        if path.endswith('bz2'):
            self.file = bz2.open(path, 'rt')
        else:
            self.file = open(path, 'r')
        self.parseMoves = parseMoves
        self.just_games = just_games
        self._peek = None

    def __iter__(self):
        try:
            while True:
                yield self.readNextGame()
        except StopIteration:
            return

    def peekNextGame(self):
        if self._peek is None:
            self._peek = self.readNextGame()
        return self._peek

    def readNextGame(self):
        # self.f.readline()
        if self._peek is not None:
            game = self._peek
            self._peek = None
            return game
        ret = {}
        lines = ''
        if self.just_games:
            first_hit = False
            for line in self.file:
                lines += line
                if len(line) < 2:
                    if first_hit:
                        break
                    else:
                        first_hit = True
        else:
            for line in self.file:
                lines += line
                if len(line) < 2:
                    if len(ret) >= 2:
                        break
                    else:
                        raise RuntimeError(line)
                else:
                    k, v, _ = line.split('"')
                    ret[k[1:-1]] = v
            nl = self.file.readline()
            lines += nl
            if self.parseMoves:
                ret['moves'] = re.findall(moveRegex, nl)
            lines += self.file.readline()
        if len(lines) < 1:
            raise StopIteration
        return ret, lines

    def readBatch(self, n):
        ret = []
        for i in range(n):
            try:
                ret.append(self.readNextGame())
            except StopIteration:
                break
        return ret

    def getWinRates(self, extraKey=None):
        # Assumes same players in all games
        dat, _ = self.peekNextGame()
        p1, p2 = sorted((dat['White'], dat['Black']))
        d = {
            'name': f"{p1} v {p2}",
            'p1': p1,
            'p2': p2,
            'games': 0,
            'wins': 0,
            'ties': 0,
            'losses': 0,
        }
        if extraKey is not None:
            d[extraKey] = {}
        for dat, _ in self:
            d['games'] += 1
            if extraKey is not None and dat[extraKey] not in d[extraKey]:
                d[extraKey][dat[extraKey]] = []
            if p1 == dat['White']:
                if dat['Result'] == '1-0':
                    d['wins'] += 1
                    if extraKey is not None:
                        d[extraKey][dat[extraKey]].append(1)
                elif dat['Result'] == '0-1':
                    d['losses'] += 1
                    if extraKey is not None:
                        d[extraKey][dat[extraKey]].append(0)
                else:
                    d['ties'] += 1
                    if extraKey is not None:
                        d[extraKey][dat[extraKey]].append(.5)
            else:
                if dat['Result'] == '0-1':
                    d['wins'] += 1
                    if extraKey is not None:
                        d[extraKey][dat[extraKey]].append(1)
                elif dat['Result'] == '1-0':
                    d['losses'] += 1
                    if extraKey is not None:
                        d[extraKey][dat[extraKey]].append(0)
                else:
                    d['ties'] += 1
                    if extraKey is not None:
                        d[extraKey][dat[extraKey]].append(.5)
        return d

    def __del__(self):
        try:
            self.file.close()
        except AttributeError:
            pass


def getBoardMoveMap(game, maxMoves=None):
    d = {}
    board = game.board()
    for i, move in enumerate(game.main_line()):
        d[board.fen()] = move.uci()
        board.push(move)
        if maxMoves is not None and i > maxMoves:
            break
    return d
