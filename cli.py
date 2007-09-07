#!/usr/bin/python
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

__revision__ = "20070906"

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
            cardidx = sys.stdin.readline()

        return int(cardidx.replace('\n',''))

class CliGame(briscola.Game):
    
    def showplayedcard(self, idxplayer, idxcard):
        print self.players[idxplayer].name, "plays", \
            showcard(self.players[idxplayer].hand[idxcard])
    
    def showplayed(self):
        print "played cards:"
        for idx, card in enumerate(self.cardsplayed):
            print self.players[idx].name, showcard(card)
        print "---"

    def showresults(self):
        if len(self.players) < 4:
            # no teams
            self.players.sort()
            for player in self.players:
                print player.name, player.points
            print "vince", self.players[-1].name
            return

        points = {}

        for player in self.players:
            if not points.has_key(player.team):
                points[player.team] = 0
            else:
                points[player.team] += player.points
        
        teams = points.keys()
        for team in teams:
            print "Squadra", team, points[team], "punti"

        if points[teams[0]] > points[teams[1]]:
            print "vince", teams[0]
        elif points[teams[0]] < points[teams[1]]:
            print "vince", teams[1]
        else:
            print "pareggio"
    
    def mainloop(self):
        
        print "\nBRISCOLA:", showcard(self.deck.briscola)

        while len(self.players[0].hand):
            self.resetplayed()

            for idxplayer, player in enumerate(self.players):
                player.showname()
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

    print "Please enter the user name"
    username = sys.stdin.readline()

    players = [ CliPlayer(name=username), 
                CliPlayer(name='subzero', ishuman=False) ]

    game = CliGame(players)
    try:
        game.mainloop()
    except KeyboardInterrupt:
        print "\nExiting"
