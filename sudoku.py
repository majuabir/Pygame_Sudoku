import os
import pygame
import time


program_exec = time.time()
TILE_SIZE = 30
TILES = 9
time = 0
textures = {}

class SpriteSheet:
    def __init__(self, path):
        self.sheet = pygame.image.load(path).convert()
        rect = self.sheet.get_rect()
        self.cols = rect.width // TILE_SIZE
        self.rows = rect.height // TILE_SIZE
    
    def getSprite(self, i, j):
        """
        Returns a sprite surface obj
        draw at location x,y
        index into sprite sheet with i,j
        """
        sprite = pygame.Surface((TILE_SIZE, TILE_SIZE))
        sprite.set_colorkey((255,0,255))
        #sprite.fill((255,255,255))
        #blit (spritesheet in mem, location to draw, portion of image(xi*TILE_SIZE, yi*TILESIZE, TILE_SIZE, TILE_SIZE))
        sprite.blit(self.sheet, (0, 0), (i*TILE_SIZE,j*TILE_SIZE, TILE_SIZE,TILE_SIZE))
        return sprite




class Game:
    def __init__(self):
        
        self.board = [
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]
        ]
        self.rows = len(self.board[0])
        self.cols = len(self.board)
        self.timer = 0
        self.wrong = 0
        self.selection = [0,0]
        self.win = False

    def render(self, screen):
        #order: background fill, tile selections, number sprites
        screen.fill((255,255,255))

        # blank squares , Maybe switch to drawing lines later??
        for i in range(TILES - 1):
            for j in range(TILES - 1):
                pass
                screen.
                #screen.blit(textures["squareImage"].getSprite(0,0), (TILE_SIZE*i,TILE_SIZE*j))
        
        #TODO: tile select 


        #numbers
        screen.blit(textures["numSprites"].getSprite(1,0), (0,0))
        
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
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        game.render(screen)
     

if __name__=="__main__":
    main()