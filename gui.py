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

import os
import sys

import pygame
from pygame.locals import *

import briscola

class Card(briscola.Card):
    
    def __init__(self, seed, value, theme="default"):
        briscola.Card.__init__(self, seed, value)
        filename = os.path.join(".", "cards", theme, 
            "%s_%s.gif" % (value.lower(), seed.lower()))

        self.image = pygame.image.load(filename).convert()

        filename = os.path.join(".", "cards", theme, "back.gif")
        self.backimage = pygame.image.load(filename).convert()

class GuiPlayer(briscola.Player):

    def showname(self, field):

        field_rect = field.get_rect()

        playername = self.name 
        if self.team:
            playername += " (team %s)" % self.team

        myfnt = pygame.font.match_font('Arial')
        font = pygame.font.Font(myfnt, 36)
        text = font.render(playername, 1, (10, 10, 10))
        text_rect = text.get_rect()

        if self.ishuman:
            text_rect.y = field_rect.bottom - 110    
        else:
            text_rect.y = field_rect.top + 20

        text_rect.x = 20 # field.get_width() / 2
        field.blit(text, text_rect)

    def showhand(self, field):

        field_rect = field.get_rect()

        for idx, card in enumerate(self.hand):
            card = Card(card.seed, card.value)

            if self.ishuman:
                image = card.image
            else:
                image = card.backimage

            card_rect = image.get_rect()

            if self.ishuman:
                card_rect.y = field_rect.bottom - 110
            else:
                card_rect.y = field_rect.top + 20
                
            card_rect.centerx = (field_rect.centerx + idx * 20) - 20
            #card.image = pygame.transform.rotate(card.image, 90)
            field.blit(image, card_rect)

class GuiGame(briscola.Game):

    def __init__(self, players, size):
        """
        Set up graphics, build and display the field, put the cards on
        the field (briscola and deck).
        """
        briscola.Game.__init__(self, players)

        pygame.init()
        self.screen = pygame.display.set_mode(size)

        self.field = self.getfield()
        field_rect = self.field.get_rect()
        
        # put the briscola on the field
        curbriscola = Card(self.deck.briscola.seed,
                           self.deck.briscola.value)
        curbriscola_rect = curbriscola.image.get_rect()
        curbriscola_rect.center = field_rect.center
        curbriscola.image = pygame.transform.rotate(curbriscola.image, 90)
        self.field.blit(curbriscola.image, curbriscola_rect)
        
        # put the deck over the curbriscola
        backimage = curbriscola.backimage
        backimage_rect = curbriscola.backimage.get_rect()
        backimage_rect.center = curbriscola_rect.center
        backimage_rect.x -= 15
        backimage_rect.y -= 10
        self.field.blit(backimage, backimage_rect)

        # blit everything to the screen
        self.screen.blit(self.field, (0, 0))
        pygame.display.flip()

    def getfield(self):
        """Return a pygame.Surface representing the field."""

        # field
        field = pygame.Surface(self.screen.get_size())
        field = field.convert()
        field.fill((0, 84, 0))
        return field

    def showplayed(self):
        for idx, card in enumerate(self.cardsplayed):
            #FIXME
            card

    def mainloop(self):
        """The main loop. Iterate until the user wants to quit. """
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()

            for idxplayer, player in enumerate(self.players):
                player.showname(self.field)
                player.showhand(self.field)

            self.screen.blit(self.field, (0, 0))
            pygame.display.flip()


if __name__ == "__main__":
    size = width, height = 640, 480

    players = [ GuiPlayer(name='ema' ), 
                GuiPlayer(name='subzero', ishuman=False) ]

    game = GuiGame(players, size)
    game.mainloop()
