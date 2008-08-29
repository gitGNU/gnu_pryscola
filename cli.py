#!/usr/bin/python
#
# Copyright (C) 2007-2008 Emanuele Rocca <ema@linux.it>
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

"""Pryscola, command line interface"""

__revision__ = "20080829"

import sys
import briscola

def showcard(card):
    return card.value + " of " + card.seed

class CliPlayer(briscola.Player):
    
    def showname(self):
        print "Player", self.name
        if self.team:
            print "(team %s)" % self.team

    def showhand(self):
        if self.ishuman:
            for idx, card in enumerate(self.hand):
                print "%s) %s" % (idx, showcard(card))

    def getchoice(self, cardsplayed=None, curbriscola=None):
        """Interactive implementation of getchoice()."""
        
        ret = briscola.Player.getchoice(self, cardsplayed, curbriscola)
        
        # non interactive choice
        if ret == 0 or not self.ishuman:
            return ret

        cardidx = -1
        while cardidx not in [ '%s\n' % n for n in range(0,
         len(self.hand)) ]:
            sys.stdout.write("> ")
            cardidx = sys.stdin.readline()

        return int(cardidx.replace('\n',''))

class CliGame(briscola.Game):
    
    def getplayers(self):

        nplayers = -1
        while nplayers not in ('2\n', '3\n', '4\n'):
            print "How many players? (min 2, max 4)"
            sys.stdout.write("> ")
            nplayers = sys.stdin.readline()
        
        nplayers = int(nplayers.replace('\n', '')) - 1

        print "Please enter your name"
        sys.stdout.write("> ")
        username = sys.stdin.readline().replace('\n', '')

        self.players = [ CliPlayer(name=username, team='a', number=0) ]
        
        others = self.randomplayernames(nplayers)

        for idx, name in enumerate(others):
            self.players.append(CliPlayer(name, ishuman=False,
                team=idx % 2 and 'a' or 'b', number=idx+1))

    def showplayedcard(self, idxplayer, idxcard):
        print self.players[idxplayer].name, "plays", \
            showcard(self.players[idxplayer].hand[idxcard])

    def showresults(self):
        briscola.Game.showresults(self)

        print 

        for name, points in self.points.items():
            print name + ':', points, 'points'

        if not self.winnerplayer and not self.winnerteam:
            print "draw"
        
        if self.winnerplayer:
            print self.winnerplayer.name, 'wins'

        if self.winnerteam:
            print "Team", self.winnerteam, 'wins.'
            print "Players in team", self.winnerteam + ':'

            for player in self.players:
                if player.team == self.winnerteam:
                    print player.name, player.points, 'points'
    
    def mainloop(self):
        
        if len(self.players) == 3:
            print "Removed card:", showcard(self.deck.removedcard)

        while len(self.players[0].hand):
            self.resetplayed()

            for idxplayer, player in enumerate(self.players):
                print "\nBriscola:", showcard(self.deck.briscola)

                player.showhand()

                idxcarta = player.getchoice(self.cardsplayed, 
                                            self.deck.briscola)

                self.showplayedcard(idxplayer, idxcarta)
                self.playcard(idxplayer, idxcarta)

                if not player.ishuman:
                    print "press enter..."
                    sys.stdin.readline()

            idxwinner = briscola.handwinner(self.cardsplayed, 
                                            self.deck.briscola, 0, 1)

            for card in self.cardsplayed:
                self.players[idxwinner].points += card.points
            
            pwinner = self.players[idxwinner]

            while (self.players[0] != pwinner):
                self.players.append(self.players.pop(0))

            for player in self.players:
                card = self.deck.draw()
                if card is not None:
                    player.hand.append(card)

        self.showresults()
       
if __name__ == "__main__":

    print """pryscola v%s""" % __revision__

    game = CliGame()
    try:
        game.mainloop()
    except KeyboardInterrupt:
        print "\nExiting"
        game.showresults()
