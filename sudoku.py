import os
import pygame
import time
from pprint import pprint

program_exec = time.time()
TILE_SIZE = 30
TILES = 9
time = 0
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
                    out[i][j] = True
                else:
                    out[i][j] = False
                pass
        return out
    
    def __init__(self):
        self.mousePos = None
        self.clicked = False
        self.board = [
            [0,1,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]
        ]
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
        self.slotTypes = self.__getSlotTypes(self.board)
        self.rows = len(self.board[0])
        self.cols = len(self.board)
        self.timer = 0
        self.wrong = 0
        self.selection = [-1,-1]
        self.win = False

    def highlight(self, pos):
        self.selection[0], self.selection[1] = pos[0] // TILE_SIZE, pos[1] // TILE_SIZE
        if self.selection[0] > 8:
            self.selection[0] = 8
        if self.selection[1] > 8:
            self.selection[1] = 8

    def render(self, screen):
        #order: background fill, tile selections, number sprites
        screen.fill((255,255,255))

        # blank squares , Maybe switch to drawing lines later??
        # for i in range(TILES - 1):
        #     for j in range(TILES - 1):
        #         pass
        #         #screen.blit(textures["squareImage"].getSprite(0,0), (TILE_SIZE*i,TILE_SIZE*j))

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
                alpha = 0
                #if true, make semi transparent
                if self.slotTypes[i][j]:
                    alpha = 128
                numSprite = textures["numSprites"].getSprite(num, 0)
                numSprite.set_alpha(alpha)
                screen.blit(numSprite, (j*TILE_SIZE, i*TILE_SIZE))
        

        #TODO: tile select 
        select = pygame.Surface((TILE_SIZE, TILE_SIZE))
        select.set_alpha(128)
        if self.slotTypes[self.selection[1]][self.selection[0]]:
            select.fill((255,0,0))
        else:
            select.fill((0,0,255))
        screen.blit(select, (self.selection[0]*TILE_SIZE, self.selection[1]*TILE_SIZE))
        
        
        pygame.display.flip()



# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()
    TEXTURE_PATH = os.path.join(os.getcwd(), 'textures')
    print(TEXTURE_PATH)

    #window
    pygame.display.set_caption("Sudoku")
    pygame.display.set_icon(pygame.image.load(os.path.join(TEXTURE_PATH, "square.png")))
    screen = pygame.display.set_mode((TILE_SIZE * 9, TILE_SIZE * 10))
    screen.set_colorkey((255,0,255))

    #textures
    textures["squareImage"] = SpriteSheet(os.path.join(TEXTURE_PATH, "square.png"))
    textures["numSprites"] = SpriteSheet(os.path.join(TEXTURE_PATH, "numbers_keyed.png"))
    textures["redSelect"] = SpriteSheet(os.path.join(TEXTURE_PATH, "select.png"))

    #game init
    game = Game()

    
    
    
    running = True

    while running:
        #STEPS: input -> logic -> render
        ####### INPUT #########
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        ####### LOGIC ##########
        #check hover over square
        game.highlight(pygame.mouse.get_pos())

        ####### RENDER #########
        game.render(screen)
     

if __name__=="__main__":
    main()