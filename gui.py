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

"""Pryscola, graphical user interface"""

__revision__ = "20080829"

import os
import sys

import pygame
#from pygame.locals import *

import briscola
import guimenu

XRES = 800
YRES = 600

class GuiCard(briscola.Card):
    
    def __init__(self, seed, value, theme="default", orientation='vertical'):
        briscola.Card.__init__(self, seed, value)
        filename = os.path.join(".", "cards", theme, 
            "%s_%s.gif" % (value.lower(), seed.lower()))

        self.image = pygame.image.load(filename).convert()
        self.backimage = pygame.image.load(filename).convert()

        filename = os.path.join(".", "cards", theme, "back.gif")
        self.backimage = pygame.image.load(filename).convert()

        if orientation == 'horizontal':
            self.image = pygame.transform.rotate(self.image, 90)
            self.backimage = pygame.transform.rotate(self.backimage, 90)
        
        self.card_rect = self.image.get_rect()

class GuiPlayer(briscola.Player):
    
    def showname(self, field):
        field_rect = field.get_rect()

        playername = self.name 
        #if self.team:
        #    playername += " (team %s)" % self.team

        myfnt = pygame.font.match_font('Arial')
        font = pygame.font.Font(myfnt, 36)
        text = font.render(playername, 1, (10, 10, 10))
        text_rect = text.get_rect()

        if self.number == 0:
            text_rect.bottom = field_rect.bottom - 5
            text_rect.right = field_rect.centerx - 150

        elif self.number == 1:
            text_rect.left = field_rect.left + 5
            text_rect.y = field_rect.centery + 110

        elif self.number == 2:
            text_rect.top = field_rect.top + 5
            text_rect.right = field_rect.centerx - 150

        elif self.number == 3:
            text_rect.right = field_rect.right - 5
            text_rect.y = field_rect.centery + 110

        field.blit(text, text_rect)

    def showhand(self, field):
        field_rect = field.get_rect()

        for idx, card in enumerate(self.hand):

            if self.number == 0:
                image = card.image
                card.card_rect.centerx = (field_rect.centerx + idx * 80) - 96
                card.card_rect.bottom = field_rect.bottom - 5
            else:
                image = card.backimage

            if self.number == 1:
                card.card_rect.x = field_rect.left + 10
                card.card_rect.centery = (field_rect.centery + idx * 80) - 90

            elif self.number == 2:
                card.card_rect.centerx = (field_rect.centerx + idx * 80) - 96
                card.card_rect.top = field_rect.top + 5

            elif self.number == 3:
                card.card_rect.x = field_rect.right - 100
                card.card_rect.centery = (field_rect.centery + idx * 80) - 90
                
            field.blit(image, card.card_rect)

    def getchoice(self, cardsplayed=None, curbriscola=None, event=None):
        """Interactive implementation of getchoice(). event cointains a
        MOUSEBUTTONDOWN event."""
        
        ret = briscola.Player.getchoice(self, cardsplayed, curbriscola)
        
        # non interactive choice
        if ret == 0 or not self.ishuman:
            return ret
        
        for cardidx, card in enumerate(self.hand):
            if card.card_rect.collidepoint(event.pos):
                return cardidx

class GuiGame(briscola.Game):

    def __init__(self, players, size):
        """Set up graphics, build and display the field, put the cards on
        the field (briscola and deck)."""

        pygame.init()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("priscola v%s" % __revision__)
                                    #, icontitle=None) 

        briscola.Game.__init__(self, players)

        self.field = self.getfield()
        field_rect = self.field.get_rect()
        
        # put the briscola on the field
        self.deck.briscola = GuiCard(self.deck.briscola.seed,
                                     self.deck.briscola.value,
                                     orientation='horizontal')

        self.deck.briscola.card_rect.centery = field_rect.centery
        self.deck.briscola.card_rect.centerx = field_rect.centerx

        self.field.blit(self.deck.briscola.image, 
                        self.deck.briscola.card_rect)
        
        # put the deck over the curbriscola
        backimage = self.deck.briscola.backimage
        backimage = pygame.transform.rotate(backimage, 90)
        backimage_rect = self.deck.briscola.card_rect
        backimage_rect.x -= 15
        backimage_rect.y -= 10
        self.field.blit(backimage, backimage_rect)

        self.blitscreen()

    def blitscreen(self):
        # blit everything to the screen
        self.screen.blit(self.field, (0, 0))
        pygame.display.flip()

    def getplayers(self):
        # FIXME
        self.players = [ GuiPlayer(name='ema', team='a', number=0) ]
        nplayers = 3

        others = self.randomplayernames(nplayers)

        for idx, name in enumerate(others):
            self.players.append(GuiPlayer(name, ishuman=False,
                team=idx % 2 and 'a' or 'b', number=idx+1))

    def getfield(self):
        """Return a pygame.Surface representing the field."""
        # field
        field = pygame.Surface(self.screen.get_size())
        field = field.convert()
        field.fill((0, 84, 0))
        return field
   
    def givecards(self):
        briscola.Game.givecards(self)

        for player in self.players:
            hand = player.hand
            player.hand = []
            
            for card in hand:
                if player.number in (1, 3):
                    card = GuiCard(card.seed, card.value, orientation='horizontal')
                else:
                    card = GuiCard(card.seed, card.value, orientation='vertical')
                player.hand.append(card)
    
    def showplayedcard(self, idxplayer, idxcard):
        player = self.players[idxplayer]
        card = player.hand[idxcard]

        #field_rect = self.field.get_rect()
        
        for step in range(20):
            self.field.blit(self.getfield(), card.card_rect, card.card_rect)

            if player.number == 0:
                card.card_rect = card.card_rect.move(0, -5)
            elif player.number == 2:
                card.card_rect = card.card_rect.move(0, 5)
            elif player.number == 1:
                card.card_rect = card.card_rect.move(5, 0)
            elif player.number == 3:
                card.card_rect = card.card_rect.move(-5, 0)
            
            self.field.blit(card.image, card.card_rect)
            self.blitscreen()

    def removefromfield(self):
        for card in self.cardsplayed:
            self.field.blit(self.getfield(), card.card_rect,
                            card.card_rect)
        self.blitscreen()

    def showresults(self):
        briscola.Game.showresults(self)

        if self.winnerplayer or self.winnerteam:
            myfnt = pygame.font.match_font('Arial')
            font = pygame.font.Font(myfnt, 36)
            
            if self.winnerplayer:
                text = font.render("%s WINS!" % self.winnerplayer.name, 
                                   1, (10, 10, 10))
            else:
                string = "%s! For greater justice!" % ' and '.join(
                    [ player.name for player in self.winnerplayers ]
                )
                text = font.render(string, 1, (10, 10, 10))
            
            text_rect = text.get_rect()

            field_rect = self.field.get_rect()

            text_rect.centerx = field_rect.centerx
            text_rect.centery = field_rect.centery

            self.field.blit(text, text_rect)
            self.blitscreen()
            
        print self.points

    def mainloop(self):
        """The main loop. Iterate until the user wants to quit. """
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if not len(self.players[0].hand):
                break

            self.resetplayed()

            for player in self.players:
                # show player names and cards
                player.showname(self.field)
                player.showhand(self.field)

                self.blitscreen()
                
            for idxplayer, player in enumerate(self.players):
                if player.ishuman:
                    # wait for card selection
                    while 1:
                        event = pygame.event.wait()

                        if event.type == pygame.QUIT:
                            sys.exit()

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            cardidx = player.getchoice(self.cardsplayed,
                                                       self.deck.briscola,
                                                       event)
                            if cardidx is not None:
                                break

                    self.showplayedcard(idxplayer, cardidx)
                    self.playcard(idxplayer, cardidx)

                else:
                    # AI choice
                    cardidx = player.getchoice(self.cardsplayed,
                                               self.deck.briscola)

                    self.showplayedcard(idxplayer, cardidx)
                    self.playcard(idxplayer, cardidx)

                
            idxwinner = briscola.handwinner(self.cardsplayed, 
                                            self.deck.briscola, 0, 1)

            while 1:
                event = pygame.event.wait()

                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    break

            self.removefromfield()

            # FIXME: this stuff should be put in briscola.py
            for card in self.cardsplayed:
                self.players[idxwinner].points += card.points
            
            pwinner = self.players[idxwinner]

            while (self.players[0] != pwinner):
                self.players.append(self.players.pop(0))

            for player in self.players:
                card = self.deck.draw()
                if card is not None:
                    if player.number in (1, 3):
                        card = GuiCard(card.seed, card.value, orientation='horizontal')
                    else:
                        card = GuiCard(card.seed, card.value, orientation='vertical')
                    player.hand.append(card)
        
        self.showresults()
        while 1:
            if pygame.event.wait().type == pygame.QUIT: 
                sys.exit()

if __name__ == "__main__":
#    menu = Menu(size=(XRES, YRES), options=[ "2", "4" ], 
#                caption="Number of players")
    
    game = GuiGame(players=[], size=(XRES, YRES))
    game.mainloop()
