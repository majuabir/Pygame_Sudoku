import os
import pygame
import time
from pprint import pprint
import solver
import copy

program_exec = time.time()
TILE_SIZE = 30
TILES = 9
curTime = 0
"""
LOADED TEXTURES:
numbers_keyed.png -> numSprites
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
        sprite.set_colorkey((255,0,255)) #FF00FF COLOR KEY
        #sprite.fill((255,255,255))
        #blit (spritesheet in mem, location to draw, portion of image(xi*TILE_SIZE, yi*TILESIZE, TILE_SIZE, TILE_SIZE))
        sprite.blit(self.sheet, (0, 0), (i*TILE_SIZE,j*TILE_SIZE, TILE_SIZE,TILE_SIZE))
        return sprite

class Game:
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
    
    def __init__(self):
        self.mousePos = None
        self.clicked = False
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

        pprint(self.solved)
        self.slotTypes = self.__getSlotTypes(self.board)
        self.rows = len(self.board[0])
        self.cols = len(self.board)
        self.timer = 0
        self.wrongCount = 0
        self.hover = [-1,-1]
        self.selection = [-1,-1]
        self.selNum = -1
        self.win = False
        self.selLock = False

    def updateBoard(self, num):
        if self.slotTypes[self.selection[1]][self.selection[0]] != 1:
            self.selNum = num
            self.board[self.selection[1]][self.selection[0]] = num

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
                numSprite.set_alpha(alpha)
                screen.blit(numSprite, (j*TILE_SIZE, i*TILE_SIZE))

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
    screen.set_colorkey((255,0,255))

    #textures
    textures["squareImage"] = SpriteSheet(os.path.join(TEXTURE_PATH, "square.png"))
    textures["numSprites"] = SpriteSheet(os.path.join(TEXTURE_PATH, "numbers_keyed.png"))

    keyIn = {pygame.K_0: 0,pygame.K_1: 1,pygame.K_2: 2,pygame.K_3: 3,pygame.K_4: 4,pygame.K_5: 5,pygame.K_6: 6,pygame.K_7: 7,
    pygame.K_8: 8,pygame.K_9: 9}
    
    #game init
    game = Game()
    
    running = True

    while running:
        #STEPS: input -> logic -> render
        ####### INPUT #########
        click = False
        numIn = -1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            elif event.type == pygame.KEYDOWN:
                try:
                    if game.isSelected():
                        game.updateBoard(keyIn[event.key])
                        pprint(game.board)
                except:
                    pass
                if event.key == pygame.K_ESCAPE:
                    game.selection = [-1,-1]
                    game.selNum = -1
        
        ####### LOGIC ##########
        #check hover over square
        game.highlight(pygame.mouse.get_pos(), click)

        ####### RENDER #########
        game.render(screen)
     

if __name__=="__main__":
    main()