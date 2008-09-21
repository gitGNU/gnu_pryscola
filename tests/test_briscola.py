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
        """Here we set the 'cards' list."""
        self.cards = briscola.Deck().getcardlist()

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
        pass
    
    def testCardIsBriscola(self):
        pass

    def testCardBeatsOtherCard(self):
        pass

if __name__ == "__main__":
    unittest.main()
