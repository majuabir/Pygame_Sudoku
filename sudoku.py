import os
import pygame
import time
from pprint import pprint
import solver
import copy
from math import floor

TILE_SIZE = 30
TILES = 9
PINK_COLORKEY = (255,0,255)
"""
LOADED TEXTURES (as seen in main):
    textures["squareImage"] = SpriteSheet(os.path.join(TEXTURE_PATH, "square.png"))
    textures["numSprites"] = SpriteSheet(os.path.join(TEXTURE_PATH, "numbers_keyed.png"))
    textures["loading"] = SpriteSheet(os.path.join(TEXTURE_PATH, "loading.png"))
    textures["xmark"] = SpriteSheet(os.path.join(TEXTURE_PATH, "xmark.png"))
    textures["clock"] = SpriteSheet(os.path.join(TEXTURE_PATH, "clock.png"))
"""
textures = {}

class SpriteSheet:
    def __init__(self, path):
        self.sheet = pygame.image.load(path).convert()
        rect = self.sheet.get_rect()
        self.cols = rect.width // TILE_SIZE
        self.rows = rect.height // TILE_SIZE
    
    def getSprite(self, i, j) -> pygame.Surface:
        """
        Returns a sprite surface obj
        draw at location x,y
        index into sprite sheet with i,j
        """
        sprite = pygame.Surface((TILE_SIZE, TILE_SIZE))
        sprite.set_colorkey( PINK_COLORKEY ) #FF00FF COLOR KEY
        #sprite.fill((255,255,255))
        #blit (spritesheet in mem, location to draw, portion of image(xi*TILE_SIZE, yi*TILESIZE, TILE_SIZE, TILE_SIZE))
        sprite.blit(self.sheet, (0, 0), (i*TILE_SIZE,j*TILE_SIZE, TILE_SIZE,TILE_SIZE))
        return sprite

class Game:
    
    def __init__(self, reset=False):
        self.mousePos = None
        self.clicked = False
        if reset:
            self.board = copy.deepcopy(self.boardInit)
        else:
            self.board = self.__generate()
            self.board = [
                [0,8,5,3,0,0,0,0,0],
                [7,0,0,0,0,0,0,2,0],
                [2,0,9,0,4,0,0,8,3],
                [0,0,0,1,0,0,0,0,8],
                [0,0,0,0,0,4,9,3,0],
                [1,0,0,0,3,0,0,4,0],
                [9,0,0,7,0,0,0,0,0],
                [0,0,3,5,0,0,0,0,9],
                [0,0,1,0,0,0,7,0,0]
            ]
            self.solved = copy.deepcopy(self.board)
            solver.solve(self.solved)        
        self.boardInit = copy.deepcopy(self.board)

        self.slotTypes = self.__getSlotTypes(self.board)
        self.rows = len(self.board[0])
        self.cols = len(self.board)

        self.startTime = time.time()
        self.timer = 0
        self.mins = 0
        self.sec = 0

        self.wrongCount = 0
        self.hover = [-1,-1]
        self.selection = [-1,-1]
        self.selNum = -1
        self.win = False
        self.selLock = False
        self.w, self.h = pygame.display.get_surface().get_size()

    def __generate(self):
        pass

    def __validateEntry(self, num):
        #row check
        valid = True
        x = self.selection[0]
        y = self.selection[1]
        if num in self.board[y]:
            valid = False
        #col check
        for j in range(len(self.board)):
            if num == self.board[j][x]:
                valid = False
        #box check, find box to check
        big_y = (y // 3) * 3 #big y
        big_x = (x // 3) * 3 #big x
        for y in range(big_y, big_y + 3):
            for x in range(big_x, big_x + 3):
                if num == self.board[y][x]:
                    valid = False
        return valid

    def __getSlotTypes(self, board):
        out = [[False for i in range(TILES)] for j in range(TILES)]
        for i in range(TILES):
            for j in range(TILES):
                if board[i][j] != 0:
                    out[i][j] = 1
                else:
                    out[i][j] = 0
                pass
        return out

    def updateBoard(self, num):
        if self.slotTypes[self.selection[1]][self.selection[0]] != 1:
            if self.__validateEntry(num) or num == 0:
                self.selNum = num
                self.board[self.selection[1]][self.selection[0]] = num
            else:
                if self.wrongCount < 999:
                    self.wrongCount += 1
            
    def updateTimer(self):
        self.timer = time.time() - self.startTime
        self.mins = int(self.timer / 60)
        self.sec = int(self.timer % 60)
        if self.sec >= 60:
            self.mins += 1

    def isSelected(self):
        if self.selection[0] != -1:
            return True
        return False

    def highlight(self, pos, click):
        self.hover[0], self.hover[1] = pos[0] // TILE_SIZE, pos[1] // TILE_SIZE
        if self.hover[0] > 8:
            self.hover[0] = 8
        if self.hover[1] > 8:
            self.hover[1] = 8

        if click:
            self.selection[0], self.selection[1] = self.hover


    def render(self, screen):
        #order: background fill, tile selections, number sprites
        screen.fill((255,255,255))

        #column line draw
        for i in range(TILES + 1):
            width = 1
            if i % 3 == 0:
                width = 3
            pygame.draw.line(screen, (0,0,0,0), (i*TILE_SIZE, 0), (i*TILE_SIZE, TILES*TILE_SIZE), width= width)
        
        #row line draw
        for j in range(0, TILES + 1):
            width = 1
            if j % 3 == 0:
                width = 3
            pygame.draw.line(screen, (0,0,0,0), (0, j*TILE_SIZE), (TILES*TILE_SIZE, j*TILE_SIZE), width=width)
        
        #numbers, #grey out starting numbers
        for i in range(TILES):
            for j in range(TILES):
                num = self.board[i][j]
                alpha = 255
                #if true, make semi transparent
                if self.slotTypes[i][j]:
                    alpha = 128
                numSprite = textures["numSprites"].getSprite(num, 0)
                if num == 0:
                    numSprite.fill((255,0,255))
                numSprite.set_alpha(alpha)
                screen.blit(numSprite, (j*TILE_SIZE, i*TILE_SIZE))
        
        #wrong count
        xmark = textures["xmark"].getSprite(0,0)
        screen.blit(xmark, (0, self.h - TILE_SIZE))
        wrongString = str(self.wrongCount)
        for i in range(len(wrongString)):
            numSprite = textures["numSprites"].getSprite(int(wrongString[i]), 0)
            screen.blit(numSprite, ((i+1) * TILE_SIZE, 9*TILE_SIZE))
            

        #timer
        clock = textures["clock"].getSprite(0,0)
        screen.blit(clock, (self.w - TILE_SIZE*5, (self.h - TILE_SIZE)))
        clockString = f"{self.mins}{self.sec:02}"
        for i in range(len(clockString)):
            
            numSprite = textures["numSprites"].getSprite(int(clockString[i]), 0)
            screen.blit(numSprite, ((i+5) * TILE_SIZE, 9*TILE_SIZE))
            if i == len(clockString) - 2:
                screen.blit(textures["colon"].getSprite(0,0), ((i+5) * TILE_SIZE - TILE_SIZE // 2, 9*TILE_SIZE))


        # tile hover 
        hover = pygame.Surface((TILE_SIZE, TILE_SIZE))
        hover.set_alpha(128)
        sqColor = self.slotTypes[self.hover[1]][self.hover[0]]
        if sqColor == 1:
            hover.fill((255,0,0))
        elif sqColor == 0:
            hover.fill((0,0,255))
        screen.blit(hover, (self.hover[0]*TILE_SIZE, self.hover[1]*TILE_SIZE))

        # tile select
        if self.selection[0] != -1:
            select = pygame.Surface((TILE_SIZE, TILE_SIZE))
            select.set_alpha(128)
            select.fill((0,255,0))
            screen.blit(select, (self.selection[0]*TILE_SIZE, self.selection[1]*TILE_SIZE))
        
        pygame.display.flip()



# define a main function
def main():

    ########## SETUP ###########

    # initialize the pygame module
    pygame.init()
    TEXTURE_PATH = os.path.join(os.getcwd(), 'textures')

    #window
    pygame.display.set_caption("Sudoku")
    pygame.display.set_icon(pygame.image.load(os.path.join(TEXTURE_PATH, "square.png")))
    screen = pygame.display.set_mode((TILE_SIZE * 9, TILE_SIZE * 10))
    screen.set_colorkey( PINK_COLORKEY )

    #textures
    textures["numSprites"] = SpriteSheet(os.path.join(TEXTURE_PATH, "numbers_keyed.png"))
    textures["xmark"] = SpriteSheet(os.path.join(TEXTURE_PATH, "xmark.png"))
    textures["clock"] = SpriteSheet(os.path.join(TEXTURE_PATH, "clock.png"))
    textures["colon"] = SpriteSheet(os.path.join(TEXTURE_PATH, "colon.png"))

    #loading texture
    load = pygame.Surface((120, 60))
    load.set_colorkey( PINK_COLORKEY )
    load.blit(pygame.image.load(os.path.join(TEXTURE_PATH, "loading.png")), (0,0))
    
    screen.blit(load, (0, TILE_SIZE*8))
    pygame.display.flip()

    keyIn = {pygame.K_0: 0,pygame.K_1: 1,pygame.K_2: 2,pygame.K_3: 3,pygame.K_4: 4,pygame.K_5: 5,pygame.K_6: 6,pygame.K_7: 7,
    pygame.K_8: 8,pygame.K_9: 9}
    
    #game init
    game = Game()
    running = True

    while running:
        #STEPS: input -> logic -> render
        ####### INPUT & LOGIC #########
        click = False
        numIn = -1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = event.button == 1
            elif event.type == pygame.KEYDOWN:
                try:
                    if game.isSelected():
                        game.updateBoard(keyIn[event.key])
                except:
                    pass
                if event.key == pygame.K_ESCAPE:
                    game.selection = [-1,-1]
                    game.selNum = -1
                elif event.key == pygame.K_r:
                    game.__init__(reset=True)
        ####### RECURRING LOGIC ##########
        #check hover over square
        game.highlight(pygame.mouse.get_pos(), click)
        if not game.win:
            game.updateTimer()

        ####### RENDER #########
        game.render(screen)
     

if __name__=="__main__":
    main()