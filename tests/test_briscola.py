#!/usr/bin/python
#
# Copyright (C) 2008 Emanuele Rocca <ema@linux.it>
#
# This file is part of Pryscola.
#
# Pryscola is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Pryscola is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""Unit testing of 'briscola', Pryscola's main module."""

import os
import sys
import unittest

MAINDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(MAINDIR)

import briscola

class CardCheck(unittest.TestCase):

    def setUp(self):
        """Here we set the 'cards' list and a 'curbriscola'."""
        self.cards = briscola.Deck().getcardlist()
        self.curbriscola = briscola.Card('CUORI', 'TRE')

    def testValidCardSeed(self):
        """seed should belong to briscola.SEEDS"""
        for card in self.cards:
            self.failUnless(card.seed in briscola.SEEDS)

    def testValidCardValues(self):
        """value should belong to briscola.CARDSNAMES"""
        for card in self.cards:
            self.failUnless(card.value in briscola.CARDSNAMES)

    def testValidCardPoints(self):
        """points should belong to briscola.CARDPOINTS values, plus zero."""

        valid_points = briscola.CARDSPOINTS.values() + [ 0 ]

        for card in self.cards:
            self.failUnless(card.points in valid_points)

    def testCardComparison(self):
        """card comparison should compare card.points"""
        card1 = briscola.Card('CUORI', 'DUE')
        card2 = briscola.Card('CUORI', 'ASSO')
        self.failUnless(card1 < card2)

        card1 = briscola.Card('QUADRI', 'ASSO')
        card2 = briscola.Card('FIORI', 'ASSO')
        self.assertEqual(card1, card2)

        card1 = briscola.Card('PICCHE', 'DONNA')
        card2 = briscola.Card('CUORI', 'JACK')
        self.failUnless(card1 > card2)
    
    def testCardIsBriscola(self):
        """isbriscola() should return True if briscola.seed equals card.seed"""
        card = briscola.Card('CUORI', 'ASSO')
        self.failUnless(card.isbriscola(self.curbriscola))

        card = briscola.Card('QUADRI', 'ASSO')
        self.failIf(card.isbriscola(self.curbriscola))

    def testCardBeatsOtherCard(self):
        """beats() should follow Briscola's rules"""
        # card 1 beats card 2
        card1 = briscola.Card('PICCHE', 'TRE')
        card2 = briscola.Card('PICCHE', 'CINQUE')
        self.failUnless(card1.beats(card2, self.curbriscola))

        # card 2 beats card 1
        card1 = briscola.Card('FIORI', 'DUE')
        card2 = briscola.Card('FIORI', 'ASSO')
        self.failIf(card1.beats(card2, self.curbriscola))

        # card 2 is briscola
        card1 = briscola.Card('QUADRI', 'ASSO')
        card2 = briscola.Card('CUORI', 'DUE')
        self.failIf(card1.beats(card2, self.curbriscola))

        # if neither the first nor the second card is briscola, and their seeds
        # differ, the first one wins
        card1 = briscola.Card('QUADRI', 'DUE')
        card2 = briscola.Card('PICCHE', 'ASSO')
        self.failUnless(card1.beats(card2, self.curbriscola))

class DeckCheck(unittest.TestCase):
    pass

class GameCheck(unittest.TestCase):
    pass

class PlayerCheck(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()
