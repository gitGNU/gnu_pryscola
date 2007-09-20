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

"""
Pygame based menu allowing the user to choose an option with the mouse
"""

__revision__ = "20070920"

import sys
import pygame

class Menu(object):

    """Basic pugame based menu. Even slightly configurable."""

    bgcolor = 0, 0, 0
    textcolor = 255, 255, 255
    overcolor = 255, 0, 0
    
    def __init__(self, size, options, caption):
        """
        menu = Menu(size=(640, 480), options=[ "ham", "spam", "eggs" ], 
                    caption="Here's a shiny menu")

        When the user chooses an option its index is available in
        menu.choosen, while menu.opts[menu.choosen] cointains the label.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(size)

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(self.bgcolor)
        self.background_pos = self.background.get_rect()
        
        self.font = pygame.font.Font(pygame.font.match_font('Arial'), 36)
        title = self.font.render(caption, 1, self.textcolor)
        title_pos = title.get_rect()
        title_pos.centerx = self.background_pos.centerx

        self.background.blit(title, title_pos)
        
        self.opts = options
        self.opts_pos = list(range(0, len(options)))
        
        self.over = None
        self.choosen = self.getchoice()
    
    def isover(self, cursor_pos):
        """isover(cursor_pos) -> idx"""
        for idx, opt_pos in enumerate(self.opts_pos):
            if opt_pos.collidepoint(cursor_pos):
                return idx
    
    def drawopt(self, idx, color):
        """Draw self.opts[idx]"""

        opt = self.font.render(self.opts[idx], 1, color)
        opt_pos = opt.get_rect()
        opt_pos.centerx = self.background_pos.centerx
        opt_pos.y = 60 + idx * 60
        # update self.opts_pos[idx] position
        self.opts_pos[idx] = opt_pos
        
        cover = pygame.Surface((opt_pos.width, opt_pos.height))
        cover.fill(self.bgcolor)
        cover_pos = cover.get_rect()
        cover_pos.x, cover_pos.y = opt_pos.x, opt_pos.y
        self.background.blit(cover, cover_pos)

        # now we can blit the option
        self.background.blit(opt, opt_pos)

    def drawopts(self):
        """Draw every option available in self.opts"""
        for idx in range(len(self.opts)):
            if idx == self.over:
                self.drawopt(idx, self.overcolor)
            else:
                self.drawopt(idx, self.textcolor)

        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def getchoice(self):
        """getchoice() -> choice_idx
        
        Show a graphical menu and return user choice."""

        self.drawopts()

        while True:
   
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()

            event = pygame.event.wait()

            if event.type == pygame.QUIT: 
                sys.exit()

            if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                self.over = self.isover(event.pos)

            if self.over is not None and event.type == pygame.MOUSEBUTTONDOWN:
                return self.over

            if event.type == pygame.MOUSEMOTION:
                self.drawopts()

if __name__ == "__main__":

    menu = Menu(size=(640, 480), options=[ "ham", "spam", "eggs" ], 
                caption="Here's a shiny menu")
    print menu.choosen, menu.opts[menu.choosen]
