import pygame
pygame.init()
import chessboard;

class Graphics:

    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 800
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Chess")
        self.blue = (76, 123,  195)
        self.white = (255, 255, 255)
        self.TILE_SIZE = self.SCREEN_WIDTH // 8
        self.selected_tile = None
        self.move_tiles = []

    def draw_screen(self, board: chessboard.Chessboard):

        #draw the tiles and pieces
        for row in range(8):
            for column in range(8):
                x = column * self.TILE_SIZE
                y = self.SCREEN_HEIGHT - (8 - row) * (self.TILE_SIZE)
                if ( (row, column) == self.selected_tile):
                    pygame.draw.rect(self.screen, (255, 0, 0), (x, y, self.TILE_SIZE, self.TILE_SIZE))
                elif (row, column) in self.move_tiles:
                    pygame.draw.rect(self.screen, (0, 255, 0), (x, y, self.TILE_SIZE, self.TILE_SIZE))
                elif (row + column) % 2 == 1:
                    pygame.draw.rect(self.screen, self.blue, (x, y, self.TILE_SIZE, self.TILE_SIZE))
                else:
                    pygame.draw.rect(self.screen, self.white, (x, y, self.TILE_SIZE, self.TILE_SIZE))
        
        #draw all the pieces
        for row in range(8):
            for column in range(8):
                current_piece = board.board[row][column]
                if (current_piece != None):
                    blit_x = current_piece.position[1] * self.TILE_SIZE
                    blit_y = self.SCREEN_HEIGHT - (8 - current_piece.position[0]) * (self.TILE_SIZE)
                    self.screen.blit(current_piece.image, (blit_x, blit_y))
                    
        pygame.display.flip()



