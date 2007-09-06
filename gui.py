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

from briscola import Card as BaseCard
from briscola import Deck as BaseDeck
from briscola import Game as BaseGame
from briscola import Player as BasePlayer

class Card(BaseCard):
    
    def __init__(self, seed, value, theme="default"):
        BaseCard.__init__(self, seed, value)
        filename = os.path.join(".", "cards", theme, 
            "%s_%s.gif" % (value.lower(), seed.lower()))

        self.image = pygame.image.load(filename).convert()

        filename = os.path.join(".", "cards", theme, "back.gif")
        self.backimage = pygame.image.load(filename).convert()

class Player(BasePlayer):

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

class Game(BaseGame):

    def __init__(self, players, size):
        """
        Set up graphics, build and display the field, put the cards on
        the field (briscola and deck).
        """
        BaseGame.__init__(self, players)

        pygame.init()
        self.screen = pygame.display.set_mode(size)

        self.field = self.getfield()
        field_rect = self.field.get_rect()
        
        # put the briscola on the field
        briscola = Card(self.deck.briscola.seed,
                        self.deck.briscola.value)
        briscola_rect = briscola.image.get_rect()
        briscola_rect.center = field_rect.center
        briscola.image = pygame.transform.rotate(briscola.image, 90)
        self.field.blit(briscola.image, briscola_rect)
        
        # put the deck over the briscola
        backimage = briscola.backimage
        backimage_rect = briscola.backimage.get_rect()
        backimage_rect.center = briscola_rect.center
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
        
        self.players[0].showhand(self.field)
        self.players[1].showhand(self.field)

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()

            self.screen.blit(self.field, (0, 0))
            pygame.display.flip()


if __name__ == "__main__":
    size = width, height = 640, 480

    players = [ Player(name='ema' ), 
                Player(name='subzero', ishuman=False) ]

    game = Game(players, size)
    game.mainloop()
