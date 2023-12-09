from chessboard import Chessboard
import time
import random
from chesspiece import KING_VAL, ROOK_VAL, PAWN_VAL, BISHOP_VAL, QUEEN_VAL, KNIGHT_VAL

class MinimaxAgent():

    def __init__(self):
        self.depth = 3
        self.time_limit = 100
        self.start_time = 0
    

    def get_next_move(self, gameState: Chessboard):
        alpha = -9999999999
        beta = 9999999999
        self.start_time = time.time()
        score, piece_move = self.minimax_alpha_beta(gameState, False, None, 0, alpha, beta, self.start_time)
        return piece_move

    def minimax_alpha_beta(self, gameState: Chessboard, isPlayer, piece_move, cur_depth, alpha, beta, cur_time):

            #terminal state, return score. 
            if gameState.isWin() or gameState.isLose() or cur_depth == self.depth or cur_time - self.start_time >= self.time_limit:
                return self.evaluation_function(gameState), piece_move
            
            successor_scores = []
            legalActions = gameState.GetLegalMoves(isPlayer)
            new_alpha = -9999999999
            new_beta = 9999999999
            for piece_moves in legalActions:
                
                cur_piece = piece_moves[0]
                moves = piece_moves[1]
                for move in moves:
                    piece_move = (cur_piece, move)

                    successor_state = gameState.GenerateSuccessor(piece_move)
                    score = None

                    new_time = time.time()
                    #Player to AI, transfer alpha from AI to beta in player.
                    if isPlayer:
                        score, new_piece_move = self.minimax_alpha_beta(successor_state, not isPlayer, piece_move, cur_depth + 1, alpha, beta, new_time)
                        new_beta = min(score, new_beta)
                        if new_beta < alpha: return new_beta, piece_move
                        beta = min(beta, new_beta)
                    #AI to player, transfer beta from player to alpha in AI.
                    else:
                        score, new_piece_move = self.minimax_alpha_beta(successor_state, not isPlayer, piece_move, cur_depth + 1, alpha, beta, new_time)
                        new_alpha = max(score, new_alpha)
                        if new_alpha > beta: return new_alpha, piece_move
                        alpha = max(alpha, new_alpha)

                    successor_scores.append((score, piece_move))
            
            #find the min or max score.
            if isPlayer:
                minAction = (9999999999, "None")
                for item in successor_scores:
                    if item[0] < minAction[0]:
                        minAction = item
                return minAction[0], minAction[1]
            else:
                maxAction = (-9999999999, "None")
                for item in successor_scores:
                    if item[0] > maxAction[0]:
                        maxAction = item
                return maxAction[0], maxAction[1]
    
    def evaluation_function(self, gameState: Chessboard):
        black_mat = sum(piece.value for piece in gameState.black_pieces)
        white_mat = sum(piece.value for piece in gameState.white_pieces)
        
        # Initialize the evaluation score based on material balance
        score = black_mat - white_mat
        
        # Check for terminal states
        if gameState.isWin():
            return 100000000
        elif gameState.isLose():
            return -100000000
        
        # Prioritize controlling the center, especially for knights and bishops
        middle_tiles = [(3, 3), (3, 4), (4, 3), (4, 4), (2, 5), (2, 2)]
        for black_piece in gameState.black_pieces:

            if black_piece.value == KING_VAL and black_piece.castled:
                score += 1000
                
            mobility_bonus = len(black_piece.GetLegalMoves(gameState))
            score += mobility_bonus

            if black_piece.position in middle_tiles:
                if black_piece.value == PAWN_VAL:
                    score += 150
                elif black_piece.value == KNIGHT_VAL:
                    score += 200
        
        return score
    

