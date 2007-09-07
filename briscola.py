#!/usr/bin/python
#
# briscola - Module implementing the basic features of "Briscola",
#            a trick-taking card game. 
#            See http://en.wikipedia.org/wiki/Briscola
#
# Copyright (C) 2007 Emanuele Rocca <ema@linux.it>
# Copyright (C) 2007 Davide Pellerano <cycl0psg@gmail.com>
# Copyright (C) 2007 Alessandro Arcidiacono <spidermacg@gmail.com>
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

__revision__ = "20070907"

from random import Random, sample

seeds = ( 'CUORI', 'QUADRI', 'PICCHE', 'FIORI' )
cardsnames = [ 'DUE', 'QUATTRO', 'CINQUE', 'SEI', 'SETTE', 
               'JACK', 'DONNA', 'RE', 'TRE', 'ASSO' ]

cardspoints = { 'ASSO': 11, 'TRE': 10, 'RE': 4, 'DONNA': 3, 'JACK': 2 }        

def handwinner(cardlist, briscola, first, second):
    """
    Given a list of played cards, a briscola, and the index of two
    adjacent players, return which one is the winner.
    """
    if len(cardlist) == 1:
        # if only one card has been played
        return first

    if ( cardlist[first].beats(cardlist[second], briscola) ):
        # the first card beats the second one
        if (second+1 == len(cardlist)):
            # no more players
            return first
        
        return handwinner(cardlist, briscola, first, second+1)
     
    if (second+1 == len(cardlist)):
        return second

    return handwinner(cardlist, briscola, second, second+1)

class Card:
    
    def __init__(self, seed='', value=None):
        self.seed = seed
        self.value = value   
        self.points = cardspoints.get(value, 0)
    
    def __cmp__(self, othercard):
        if self.points > othercard.points:
            return 1
        if self.points == othercard.points:
            return 0
        return -1
    
    def beats(self, othercard, briscola):
        """If this card wins over othercard"""

        if self.seed == briscola.seed and othercard.seed != briscola.seed:
            return True
        
        if self.seed != briscola.seed and othercard.seed == briscola.seed:
            return False
        
        if self.seed == othercard.seed:
            return cardsnames.index(self.value) > \
                cardsnames.index(othercard.value)

        return True

class Deck:

    def __init__(self):
        self.briscola = None

        self.cards = []
        for seed in seeds:
            for value in cardsnames:
                self.cards.append(Card(seed, value))

        # shuffle cards
        rand = Random()
        rand.shuffle(self.cards)
    
    def __str__(self):
        return "\n".join([ str(card) for card in self.cards ])

    def setbriscola(self):
        card = self.cards.pop()
        self.briscola = card
        self.cards.insert(0, card)
    
    def nomorecards(self):
        return len(self.cards) == 0

    def draw(self):
        try:
            return self.cards.pop()
        except IndexError:
            return None            

    def removetwo(self):
        """
        Remove the first 'two' encountered.
        Needed when nplayers == 3.
        """
        for idx, card in enumerate(self.cards):
            if card.value == 'DUE':
                self.removedcard = self.cards.pop(idx)
                break

class MazzoAcinque(Deck):
    def setbriscola(self):
        pass

    def nomorecards(self):
        pass

    def draw(self):
        pass

class Game:
    
    nonhumans = ( 'Kano', 'Sub-Zero', 'Scorpion', 'Sonya' )

    def __init__(self, players=None):
        """
        deck, players
        """
        
        if players:
            self.players = players
        else:
            self.getplayers()
        
        nplayers = len(self.players)
        
        if nplayers > 6:
            raise InvalidNumberOfPlayers, nplayers

        if nplayers != 5:
            self.deck = Deck()
            self.ncards = 3

            if nplayers == 3:
                self.deck.removetwo()
        else:
            # FIXME: to implement
            self.deck = MazzoAcinque()
            self.ncards = 8

        self.givecards()

        self.deck.setbriscola()

    def getplayers(self):
        """Set self.players"""
        pass

    def randomplayernames(self, n):
        return sample(self.nonhumans, n)
    
    def givecards(self):

        for player in self.players:
            player.hand = []

            for idx in range(0, self.ncards):
                player.hand.append(self.deck.cards.pop())
    
    def playcard(self, idxplayer, idxcard):
        self.cardsplayed.append(self.players[idxplayer].hand.pop(idxcard))
    
    def resetplayed(self):
        self.cardsplayed = []

    def showplayed(self):
        pass

    def showplayedcard(self):
        pass

    def showresults(self):
        pass
                   
class InvalidNumberOfPlayers(Exception):
    def __init__(self, nplayers=0):
        self.nplayers = nplayers

    def __str__(self):
        return "Invalid number of players: " + nplayers

class Player:
    
    def __init__(self, name, ishuman=True, team=None):
        self.hand = []
        self.points = 0
        self.name = name
        self.ishuman = ishuman
        self.team = team

    def __cmp__(self, player2):
        if self.points > player2.points:
            return 1

        if self.points == player2.points:
            return 0

        return -1
    
    def showname(self):
        pass
    
    def showhand(self):
        pass
    
    def aiplaycard(self, cardsplayed, briscola):
        self.hand.sort()
        winnercard = cardsplayed[handwinner(cardsplayed, briscola, 0, 1)]
        #except IndexError:
            # no cards has been played yet
        #    print "NO CARDS PLAYED YET, I DO NOT KNOW WHAT TO DO!"
        #    return 0

        #if winnercard.points:
        for idx, card in enumerate(self.hand):
            if (winnercard.seed == card.seed and 
                winnercard.points < card.points) or \
               (winnercard.points > 0 and
                winnercard.seed != briscola.seed and
                card.seed == briscola.seed):
                return idx
        
        return 0

    def getchoice(self, cardsplayed=None, briscola=None):
        """Only non-interactive actions here."""

        if len(self.hand) == 1:
            return 0
        
        if not self.ishuman:    
            # if we cannot compute the best card index
            if not cardsplayed or not briscola:
                return 0

            return self.aiplaycard(cardsplayed, briscola)

        # each heir class need to provide their implementation
