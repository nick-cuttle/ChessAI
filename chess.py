import graphics
import pygame
import chessboard
from minimax import MinimaxAgent
from chesspiece import KING_VAL
pygame.init()

ai_on = True


running = True
if __name__ == "__main__":

    curGameState = chessboard.Chessboard()
    curGameState.init_board()
    g = graphics.Graphics()
    minimaxAgent = MinimaxAgent()
    
    isPlayer = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LALT:
                    ai_on = not ai_on

            if isPlayer and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                col = mouse_x // g.TILE_SIZE
                row = mouse_y // g.TILE_SIZE


                selected_piece = curGameState.board[row][col]

                #be able to deselect by clicking tile again
                if (row, col) == g.selected_tile:
                    g.selected_tile = None
                    g.move_tiles = []
                
                #select a chess piece if the tile has a piece
                elif g.selected_tile == None and selected_piece != None:
                    threat_list = curGameState.isCheck(isPlayer)
                    if len(threat_list) == 0 or selected_piece.value == KING_VAL:
                        g.selected_tile = (row, col)
                        g.move_tiles = selected_piece.GetLegalMoves(curGameState)

                    elif len(threat_list) != 0 or selected_piece == KING_VAL:
                        move_tiles = selected_piece.GetLegalMoves(curGameState)

                        for move in move_tiles:
                            clone_state = curGameState.clone()
                            cloned_piece = clone_state.board[selected_piece.position[0]][selected_piece.position[1]]
                            clone_state.move_piece(cloned_piece, move)

                            if not clone_state.isCheck(isPlayer):
                                g.selected_tile = (row, col)
                                g.move_tiles.append(move)
                
                    #prevent king from moving in check positions
                    if selected_piece.value == KING_VAL:
                        move_tiles = selected_piece.GetLegalMoves(curGameState)
                        for move in move_tiles:
                            clone_state = curGameState.clone()
                            cloned_piece = clone_state.board[selected_piece.position[0]][selected_piece.position[1]]
                            clone_state.move_piece(cloned_piece, move)
                            if clone_state.isCheck(isPlayer):
                                g.move_tiles.remove(move)

                             
                #move the pawn if possible
                elif g.selected_tile != None:


                    move_piece = curGameState.board[g.selected_tile[0]][g.selected_tile[1]]

                    # if selected_piece in g.move_tiles:
                    if (row, col) not in g.move_tiles:
                        g.selected_tile = None
                        g.move_tiles = []
                    else:
                        curGameState.move_piece(move_piece, (row, col))
                        g.selected_tile = None
                        g.move_tiles = []
                        if ai_on:
                            isPlayer = not isPlayer
                                

            #is AI run minimax to update board
            elif not isPlayer:
                g.selected_tile = None
                g.move_tiles = []
                piece_move = minimaxAgent.get_next_move(curGameState)
                l = len(piece_move[1])
                move = piece_move[1]
                print(f"piece location {piece_move[0]}, move: {move}")
                curGameState.move_piece(piece_move[0], move)
                isPlayer = not isPlayer

                #print(f"({row}, {col})")
        
        g.draw_screen(curGameState)

pygame.quit()
