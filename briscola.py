#!/usr/bin/python
#
# Copyright (C) 2007 2008 Emanuele Rocca <ema@linux.it>
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

"""Basic features of briscola, an Italian trick-taking card game. 
See http://en.wikipedia.org/wiki/Briscola."""

__revision__ = "20080921"

from random import Random, sample

SEEDS = ( 'CUORI', 'QUADRI', 'PICCHE', 'FIORI' )
CARDSNAMES = [ 'DUE', 'QUATTRO', 'CINQUE', 'SEI', 'SETTE', 
               'JACK', 'DONNA', 'RE', 'TRE', 'ASSO' ]

CARDSPOINTS = { 'ASSO': 11, 'TRE': 10, 'RE': 4, 'DONNA': 3, 'JACK': 2 }        

def handwinner(cardlist, briscola, first, second):
    """handwinner(cardlist, briscola, first, second) -> winner_idx

    Given a list of played cards, a briscola, and the index of two
    adjacent players, return which index is the winner."""

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
    """Represents card objects and methods to compare two cards."""
    
    def __init__(self, seed, value):
        """Create a new card instance with the given seed and value."""
        self.seed = seed
        self.value = value   
        self.points = CARDSPOINTS.get(value, 0)
    
    def __cmp__(self, othercard):
        """__cmp__(othercard) -> int
        Compare the current card with 'othercard'."""
        return cmp(self.points, othercard.points)

    def isbriscola(self, briscola):
        """isbriscola(briscola) -> boolean
        Return True if this card is briscola"""
        return self.seed == briscola.seed
    
    def beats(self, othercard, briscola):
        """beats(othercard, briscola) -> boolean
        Return True if this card wins over othercard"""

        if self.isbriscola(briscola) and not othercard.isbriscola(briscola):
            return True
        
        if not self.isbriscola(briscola) and othercard.isbriscola(briscola):
            return False
        
        if self.seed == othercard.seed:
            return CARDSNAMES.index(self.value) > \
                CARDSNAMES.index(othercard.value)

        return True

class Deck:
    """Represents a deck of cards."""

    def __init__(self):
        """Set up a new deck. The 'cards' list holds a list of objects whose
        type is Card. After instantiating the whole deck, the list is shuffled
        with the shuffle method of random.Random."""
        self.briscola = None
        # will be set only if nplayers == 3
        self.removedcard = None

        self.cards = []
        for seed in SEEDS:
            for value in CARDSNAMES:
                self.cards.append(Card(seed, value))

        # shuffle cards
        rand = Random()
        rand.shuffle(self.cards)
    
    def __str__(self):
        return "\n".join([ str(card) for card in self.cards ])

    def setbriscola(self):
        """Pop the first card from the deck and set the 'briscola'
        attribute. Then, reinsert the card into the deck."""
        card = self.cards.pop()
        self.briscola = card
        self.cards.insert(0, card)
    
    def nomorecards(self):
        """nomorecards() -> boolean
        Returns True if there's no card left."""
        return len(self.cards) == 0

    def draw(self):
        """draw() -> Card
        Pop a card from the deck."""
        try:
            return self.cards.pop()
        except IndexError:
            return None            

    def removetwo(self):
        """Remove the first 'two' encountered.
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
    """Represents a game instance. Basically, a game is made by a list of
    players and a deck of cards."""
    
    nonhumans = ( 'Kano', 'Sub-Zero', 'Scorpion', 'Sonya' )

    def __init__(self, players=None):
        """Create a new game, to be played by the given players. If players is
        None, call getplayers()."""
        
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
            # XXX: to implement
            self.deck = MazzoAcinque()
            self.ncards = 8

        self.givecards()
        self.deck.setbriscola()

        self.cardsplayed = []

        self.points = None
        self.winnerplayer = None
        self.winnerplayers, self.winnerteam = None, None

    def getplayer(self, name):
        """getplayer(name) -> Player"""
        for player in self.players:
            if player.name == name:
                return player

    def randomplayernames(self, num):
        """randomplayernames(num) -> list
        Returns a list of 'num' random player names."""
        return sample(self.nonhumans, num)
    
    def givecards(self):
        """Set player.hand for each Player. player.hand is a list of 'ncards'
        cards."""
        for player in self.players:
            player.hand = [ self.deck.cards.pop() 
                for idx in range(0, self.ncards) ]
    
    def playcard(self, idxplayer, idxcard):
        """Add card identified by 'idxcard' to 'cardsplayed'."""
        self.cardsplayed.append(self.players[idxplayer].hand.pop(idxcard))
    
    def resetplayed(self):
        """Empty 'cardsplayed'."""
        self.cardsplayed = []

    def computeresults(self):
        """Compute final results, setting 'winnerplayer' (or 'winnerteam' and
        'winnerplayers') and 'points'."""

        self.points = {}

        if len(self.players) < 4:
            # no teams
            self.players.sort()
            for player in self.players:
                self.points[player.name] = player.points
            
            if self.players[-1].points != self.players[-2].points:
                # set winnerplayer only if someone actually won
                self.winnerplayer = self.players[-1]
            return

        # teams
        for player in self.players:
            if not self.points.has_key(player.team):
                self.points[player.team] = player.points
            else:
                self.points[player.team] += player.points

        teams = self.points.keys()
        if self.points[teams[0]] > self.points[teams[1]]:
            self.winnerteam = teams[0]
        elif self.points[teams[0]] < self.points[teams[1]]:
            self.winnerteam = teams[1]
        
        self.winnerplayers = [ 
            player for player in self.players 
                if player.team == self.winnerteam 
        ]

    def getplayers(self):
        """Get player names and set 'players' list. This function has to be
        implemented by the subclassing user interface, here we set 'players' to
        a random list of non-human players."""
        human = False

        for idx, name in enumerate(self.randomplayernames(4)):
            team = idx % 2 and 'a' or 'b'
            number = idx + 1

            self.players.append(Player(name, human, team, number))

    def showplayedcard(self):
        """Show played card. This function has to be implemented by the
        subclassing user interface."""
        pass

    def mainloop(self):
        """Main loop. This function has to be implemented by the subclassing
        user interface."""
        pass
    
    def showresults(self):
        """Each subclassing module needs to implement the proper way to
        present final results. Here we just call computeresults()."""
        self.computeresults()
                   
class InvalidNumberOfPlayers(Exception):
    """Exception to be thrown when the number of players is not valid."""
    def __init__(self, nplayers=0):
        Exception.__init__(self)
        self.nplayers = nplayers

    def __str__(self):
        return "Invalid number of players: " + self.nplayers

class Player:
    """Represents a player. A player is distinguished by his hand (a list of
    Card objects), his points, his name and is team, where appropriate."""
    
    def __init__(self, name, ishuman=True, team=None, number=0):
        self.hand = []
        self.points = 0
        self.name = name
        self.ishuman = ishuman
        self.team = team
        self.number = number

    def __cmp__(self, player2):
        """Compare the points of player and 'player2'."""
        return cmp(self.points, player2.points)
    
    def aiplaycard(self, cardsplayed, briscola):
        """aiplaycard(cardsplayed, briscola) -> cardidx
        AI choice on the "best" card to play."""

        self.hand.sort()
        winnercard = cardsplayed[handwinner(cardsplayed, briscola, 0, 1)]

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
        """getchoice(cardsplayed, briscola) -> cardidx

        Each subclassing module needs to implement the user interaction
        needed to choose a card. Here we just call aiplaycard() if the
        player is not human."""

        if len(self.hand) == 1:
            return 0
        
        if not self.ishuman:    
            # if we cannot compute the best card index
            if not cardsplayed or not briscola:
                return 0

            return self.aiplaycard(cardsplayed, briscola)

        # each heir class need to provide their implementation
    
    def showname(self):
        """Show player name. This function has to be implemented by the
        subclassing user interface."""
        pass
    
    def showhand(self):
        """Show player hand. This function has to be implemented by the
        subclassing user interface."""
        pass
