"""
Mastermind.py
Copyright 2015 - Michael Usner

This file contains a simple implementation of Donald Knuth's Mastermind
algorithm as published in the journal of recreational mathematics (1976).
This was originally given to me as a college assignment for
CS451 - Programming Paradigms.
https://www.cs.unm.edu/~darko/classes/2004s-451/index.html
Assignment: http://www.cs.unm.edu/~darko/classes/2004s-451/homework8.pdf
Had I known of the Knuth paper back then, I'd have gotten it.
My solution wasn't optimal however.

This program aims to complete my old homework assignment with the help of Knuth.
"""


from itertools import product
import random
import unittest


class MasterMind(object):
    """
    The main MasterMind class which encapsulates the game
    """
    def __init__(self, key=None, base=6, pegs=4, repeat=False):
        self.rows = []
        self.key = key
        self.pegs = pegs
        self.repeat = repeat
        self.searchspace = [(1, 1, 2, 2)]
        self.searchspace += [i for i in product(range(base), repeat=pegs) if i != (1, 1, 2, 2)]
        if key is None:
            self.key = random.choice(self.searchspace)

    def __repr__(self):
        board = ""
        count = 1
        for row in self.rows:
            board += str(count) + ": " + "".join([str(r) for r in row])
            count += 1
            board += "\n"
        board += "".join([str(k) for k in self.key])
        return board

    def guess(self, key):
        """
        return a guess
        """
        self.rows.append(key)
        score = self.score(self.rows[-1], self.key)
        print(str(self) + str(score))

    def reduce(self):
        """
        Reduce the solution searchspace
        """
        guess = self.rows[-1]
        cur_score = self.score(self.rows[-1], self.key)
        temp = [i for i in self.searchspace if self.score(i, guess) == cur_score]
        self.searchspace = temp
        print("reduced to {0} guesses".format(len(self.searchspace)))

    def score(self, guess, key):
        """
        Score the board
        """
        l_guess, l_key = list(guess), list(key)
        hit, miss = 0, 0
        for i in range(self.pegs):
            if l_guess[i] == l_key[i]:
                hit += 1
                l_key[i] = None
                l_guess[i] = -1
        for i in range(self.pegs):
            if l_guess[i] in l_key:
                miss += 1
                l_key[l_key.index(l_guess[i])] = None
        return hit, miss

    def play(self):
        """
        Main entry point
        """
        while len(self.searchspace) > 1:
            self.guess(self.searchspace[0])
            self.reduce()
        self.guess(self.searchspace[0])
        print("Solved in {0} guesses".format(len(self.rows)))
        return len(self.rows)


class MyTest(unittest.TestCase):
    """
    The test class for mastermind
    """
    @staticmethod
    def test1():
        """
        Test method for mastermind
        Run 10 iterations and calculate average.  It should match Knuth's paper
        of 5 moves or less.  Note that it doesn't.  Why?  I'll try to figure this out.
        Several runs produce 5.3, 5.8, etc.
        """
        iters = 100
        total = 0
        for _ in range(iters):
            game = MasterMind()
            total += game.play()
        print("\nAvg solution moves: {0}".format(float(total) / float(iters)))


if __name__ == "__main__":
    unittest.main()
