#!/usr/bin/env python

class GameMaster(object):
    def __init__(self, horizon):
        self.horizon   = horizon
        self.player1   = None
        self.player2   = None
        self.lastmove1 = None
        self.lastmove2 = None
        self.score1    = 0
        self.score2    = 0
        self.history = list()

    def register(self, player):
        assert not self.player1 or not self.player2
        #assert self.round == 0
        if not self.player1:
            self.player1 = player
            print('player 1 is {0}'.format(self.player1.__class__.__name__))
        elif not self.player2:
            self.player2 = player
            print('player 2 is {0}'.format(self.player2.__class__.__name__))

    def update(self,move1,move2):
        move1 = move1.upper()
        move2 = move2.upper()
        self.history.append((move1, move2))
        self.lastmove1 = move1
        self.lastmove2 = move2
        if move1 == "C":
            if move2 == "C":
                self.score1 = self.score1 + 1
                self.score2 = self.score2 + 1
            elif move2 == "D":
                self.score1 = self.score1 + 4
                self.score2 = self.score2 + 0
            else:
                assert False
        elif move1 == "D":
            if move2 == "C":
                self.score1 = self.score1 + 0
                self.score2 = self.score2 + 4
            elif move2 == "D":
                self.score1 = self.score1 + 3
                self.score2 = self.score2 + 3
            else:
                assert False
        else:
            assert False

    def playRound(self):
        assert self.player1 and self.player2
        move1 = self.player1.nextmove(self.lastmove2)
        move2 = self.player2.nextmove(self.lastmove1)
        self.update(move1,move2)

    def play(self):
        for round in range(self.horizon):
            self.playRound()
        print "Score of player 1: %d" % self.score1
        print "Score of player 2: %d" % self.score2
        


class Player():
    def __init__(self, horizon):
        self.horizon = horizon # number of times the game is played repeatedly
        self.history = []      # contains tuples representing players past moves
        self.previousmove = None

    def nextmove(self, opponentmove):
        """ returns the players next move, given the opponents previous move

        Arguments:
            opponentmove - string representing the opponents previous move, its
            value is either "C" (confess) or "D" (dont confess)

        Returns:
            either "C" or "D"

        """
        # TODO: implement your strategy
        pass

class SimpleBackStabber(Player):
    def nextmove(self, opponentmove):
        self.history.append((self.previousmove, opponentmove))
        move = None
        MEAN = 'C'
        NICE = 'D'
        self_moves = [x[0] for x in self.history]

        # r
        self_moves.reverse()
        nice_streak = 0
        if MEAN in self_moves:
            nice_streak = self_moves.index(MEAN)
        else:
            nice_streak = len(self_moves)+1
        self_moves.reverse()
        # /r

        if not opponentmove:
            move = NICE
        if opponentmove == MEAN or nice_streak > 12:
            move = MEAN
        else:
            move = NICE
        self.previousmove = move
        return move

class CalculatingBackStabber(Player):
    def nextmove(self, opponentmove):
        self.history.append((self.previousmove, opponentmove))
        move = None
        MEAN = 'C'
        NICE = 'D'
        o_moves = [x[1] for x in self.history]
        o_nice  = list(filter(lambda x: x == NICE, o_moves))
        o_mean  = list(filter(lambda x: x == MEAN, o_moves))
        if len(o_nice) > 0:
            o_nice_rat = len(o_moves)/len(o_nice)
        else:
            o_nice_rat = 0
        if len(o_mean) > 0:
            o_mean_rat = len(o_moves)/len(o_mean)
        else:
            o_mean_rat = 0

        if not opponentmove:
            move = MEAN
        if opponentmove == MEAN or o_mean_rat >= .1:
            move = MEAN
        else:
            move = NICE
        self.previousmove = move
        return move

class NicePlayer(Player):
    def nextmove(self, opponentmove):
        return 'D'

class MeanPlayer(Player):
    def nextmove(self, opponentmove):
        return 'C'

class TitForTatPlayer(Player):
    """ This player implements a tit-for-tat strategy

        Example:
        >>> player = Player(35)
        >>> move = player.nextmove("C")
        >>> move
        'C'
        >>> move = player.nextmove("D")
        >>> move
        'D'
    """
    def nextmove(self, opponentmove):
        self.history.append((self.previousmove, opponentmove))
        if not opponentmove:
            self.previousmove = "D"
            return "D"
        if opponentmove == "C":
            self.previousmove = "C"
            return "C"
        else:
            self.previousmove = "D"
            return "D"


if __name__ == "__main__":
    horizon = 100
    gm = GameMaster(horizon)
    p1 = SimpleBackStabber(horizon)
    p2 = CalculatingBackStabber(horizon)
    gm.register(p1)
    gm.register(p2)
    gm.play()
    print gm.history

