#!/usr/bin/python
#
# Copyright (C) 2007 Emanuele Rocca <ema@linux.it>
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

"""Pryscola, game server"""

__revision__ = "20071223"

from twisted.internet import protocol, reactor
from twisted.protocols import basic
import briscola

class BriscolaProtocol(basic.LineReceiver):
    cmds = [ 
            'help', 'quit', 'start', 'players', 
            'hand', 'field', 'play #', 'handwinner',
           ]

    def connectionMade(self):
        self.playername = None
        self.transport.write("username -> ")

    def lineReceived(self, line):
        if line == 'quit':
            self.transport.loseConnection()

        if line == 'help':
            self.transport.write("Commands: \n%s\n\n" % "\n".join(self.cmds))
            return
            
        if not self.playername:
            self.playername = line
            self.factory.addPlayer(line)
            self.transport.write("Hello %s\n" % line)
            return

        if line == 'start':
            self.factory.start()
            return

        if line == 'players':
            self.transport.write(self.factory.showPlayers())
            return

        if line == 'hand':
            self.transport.write(self.factory.showHand(self.playername))
            return

        if line.startswith('play'):
            self.transport.write(
                self.factory.playCard(self.playername, line)
            )
            return

        if line == 'field':
            self.transport.write(self.factory.showField())
            return

        if line == 'handwinner':
            self.transport.write(self.factory.showHandWinner())
            return

    def connectionLost(self, reason):
        self.factory.delPlayer(self.playername)


class BriscolaFactory(protocol.ServerFactory):

    protocol = BriscolaProtocol
    
    def __init__(self):
        self.game = None
        self.players = []
        # id of the current player
        self.curplayer = 0
        self.handwinner = None

    def __getplayeridx(self, player):
        return self.players.index(player)

    def addPlayer(self, player):
        self.players.append(player)

    def delPlayer(self, player):
        self.players.remove(player)
    
    def showPlayers(self):
        return " ".join(self.players) + "\n"

    def start(self):
        players = [ briscola.Player(name) for name in self.players ]
        self.game = briscola.Game(players)

    def showHand(self, player):
        if not self.game: 
            return "\n"

        hand = " ".join([ "%s: %s di %s" % (idx, card.value, card.seed)
         for idx, card in enumerate(self.game.getplayer(player).hand) ]) 

        return hand + "\n"

    def playCard(self, player, line):
        if not self.game: 
            return "\n"

        playeridx = self.__getplayeridx(player)

        if playeridx != self.curplayer:
            return "Not your turn!\n"

        cardidx = int(line.split()[1])
        self.game.playcard(playeridx, cardidx)
        
        if len(self.game.cardsplayed) != len(self.players):
            self.handwinner = None
        else:
            # no players left
            self.handwinner = briscola.handwinner(self.game.cardsplayed,
                self.game.deck.briscola, 0, 1)

            for card in self.game.cardsplayed:
                self.game.players[self.handwinner].points += card.points

            winner = self.game.players[self.handwinner]
            while self.game.players != winner:
                self.game.players.append(self.game.players.pop(0))
            
            for player in self.game.players:
                card = self.game.deck.draw()
                if card:
                    player.hand.append(card)
        
        self.curplayer = (playeridx + 1) % len(self.players)
        return "%s played\n" % cardidx

    def showField(self):
        if not self.game: 
            return "\n"

        briscola = self.game.deck.briscola
        field = "turn: %s briscola: %s of %s " % (
            self.game.players[self.curplayer].name,
            briscola.value, briscola.seed
        )

        for idxcard, card in enumerate(self.game.cardsplayed):
            field += "%s: %s di %s" % (idxcard, card.value, card.seed)

        return field + "\n"

    def showHandWinner(self):
        return self.handwinner and "%s\n" % self.handwinner or "\n"


if __name__ == "__main__":
    reactor.listenTCP(1042, BriscolaFactory())
    reactor.run()
