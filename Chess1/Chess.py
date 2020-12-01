import pygame
import os
import sys

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Force static position of screen

# Constants
WIN_W = 8 * 100
WIN_H = 8 * 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BOX_DIM = WIN_W / 8
PIECEWIDTH = 100
PIECEHEIGHT = 100

# Global Variables
check_for_50_move_rule = 0
loop = 0                                                                        # How many iterations of the while loop
init_mx, init_my = (-1, -1)                                                     # First mouse click for selecting piece
dest_mx, dest_my = (-1, -1)                                                     # Second mouse click for placing piece
end = (-1, -1)                                                                  # Not used yet
whiteturn = True                                                                # White or Black turn
waitforsecondbutton = False                                                     # Check if first button or second button
blocked = False                                                                 # piece between initial and destination
counter = 0
index = 0


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Player:
    def __init__(self, name):
        self.castle_long = False
        self.castle_short = False


class Game(Entity):
    def __init__(self):
        Entity.__init__(self)


class Block(Entity):
    def __init__(self, xpos, ypos, l):
        Entity.__init__(self)
        self.image = self.set_image(l)
        self.image.convert()
        self.rect = pygame.Rect(xpos, ypos, BOX_DIM, BOX_DIM)

    def set_image(self, letter):
        if letter == "B":
            # print "black"
            sur = pygame.image.load("blocks/black_square.png").convert_alpha()
            sur = pygame.transform.scale(sur, (PIECEWIDTH, PIECEHEIGHT))
            return sur
        else:
            # print "white"
            sur = pygame.image.load("blocks/white_square.png").convert_alpha()
            sur = pygame.transform.scale(sur, (PIECEWIDTH, PIECEHEIGHT))
            return sur



class PieceBoard(Entity):
    def __init__(self, xpos, ypos, piece_object):
        Entity.__init__(self)
        self.image = self.set_image(piece_object)
        self.rect = pygame.Rect(xpos, ypos, BOX_DIM, BOX_DIM)

    def set_image(self, piece_object):
        sur = piece_object.image
        sur = pygame.transform.scale(sur, (BOX_DIM, BOX_DIM))
        return sur


def blit_pieces(piece, col, row, screen):
    piece = pygame.transform.scale(piece, (PIECEWIDTH, PIECEHEIGHT))
    piece_rect = pygame.Rect(col * PIECEHEIGHT, row * PIECEWIDTH, BOX_DIM, BOX_DIM)
    screen.blit(piece, piece_rect)


def piece_move(init_mousepos, dest_mousepos, board_pieces):
    global whiteturn
    board_pieces[dest_mousepos[0]][dest_mousepos[1]] = board_pieces[init_mousepos[0]][init_mousepos[1]]
    board_pieces[init_mousepos[0]][init_mousepos[1]] = 'e'
    whiteturn = not whiteturn


# Rules of pieces
def pawn_check(init_mousepos, dest_mousepos, board_pieces, whiteturn):
    if whiteturn:
        if board_pieces[dest_mousepos[0]][dest_mousepos[1]] == 'e' and dest_mousepos[1] == init_mousepos[1]:
            if init_mousepos[0] - dest_mousepos[0] == 1:
                piece_move(init_mousepos, dest_mousepos, board_pieces)
            elif init_mousepos[0] == 6 and init_mousepos[0] - dest_mousepos[0] < 3:
                if clear_line(init_mousepos, dest_mousepos, board_pieces):
                    piece_move(init_mousepos, dest_mousepos, board_pieces)
        elif board_pieces[dest_mousepos[0]][dest_mousepos[1]] != 'e' and (dest_mousepos[1] - init_mousepos[1]) ** 2 == 1:
            if init_mousepos[0] - dest_mousepos[0] == 1:
                piece_move(init_mousepos, dest_mousepos, board_pieces)
    elif not whiteturn:
        if board_pieces[dest_mousepos[0]][dest_mousepos[1]] == 'e' and dest_mousepos[1] == init_mousepos[1]:
            if dest_mousepos[0] - init_mousepos[0] == 1:
                piece_move(init_mousepos, dest_mousepos, board_pieces)
            elif init_mousepos[0] == 1 and dest_mousepos[0] - init_mousepos[0] < 3:
                if clear_line(init_mousepos, dest_mousepos, board_pieces):
                    piece_move(init_mousepos, dest_mousepos, board_pieces)
        elif board_pieces[dest_mousepos[0]][dest_mousepos[1]] != 'e' and (dest_mousepos[1] - init_mousepos[1]) ** 2 == 1:
            if dest_mousepos[0] - init_mousepos[0] == 1:
                piece_move(init_mousepos, dest_mousepos, board_pieces)


def knight_check(init_mousepos, dest_mousepos, board_pieces):
    if (dest_mousepos[1] - init_mousepos[1]) ** 2 + (dest_mousepos[0] - init_mousepos[0]) ** 2 == 5:
        piece_move(init_mousepos, dest_mousepos, board_pieces)


def bishop_check(init_mousepos, dest_mousepos, board_pieces):
    if clear_diagonal(init_mousepos, dest_mousepos, board_pieces):
        piece_move(init_mousepos, dest_mousepos, board_pieces)


def rook_check(init_mousepos, dest_mousepos, board_pieces):
    if clear_line(init_mousepos, dest_mousepos, board_pieces):
        piece_move(init_mousepos, dest_mousepos, board_pieces)


def queen_check(init_mousepos, dest_mousepos, board_pieces):
    if clear_diagonal(init_mousepos, dest_mousepos, board_pieces):
        piece_move(init_mousepos, dest_mousepos, board_pieces)
    elif clear_line(init_mousepos, dest_mousepos, board_pieces):
        piece_move(init_mousepos, dest_mousepos, board_pieces)


def king_check(init_mousepos, dest_mousepos, board_pieces):
    if (dest_mousepos[1] - init_mousepos[1]) ** 2 + (dest_mousepos[0] - init_mousepos[0]) ** 2 in (1, 2):
        piece_move(init_mousepos, dest_mousepos, board_pieces)


def clear_diagonal(init_mousepos, dest_mousepos, board_piece):
    if abs(dest_mousepos[1] - init_mousepos[1]) != abs(dest_mousepos[0] - init_mousepos[0]):
        return False

    if (dest_mousepos[0]-init_mousepos[0])**2 + (dest_mousepos[1]-init_mousepos[1])**2 == 2:
        return True

    if dest_mousepos[0] > init_mousepos[0]:
        if dest_mousepos[1] > init_mousepos[1]:
            tmp = [init_mousepos[0]+1, init_mousepos[1]+1]
        else:
            tmp = [init_mousepos[0]+1, init_mousepos[1]-1]
    else:
        if dest_mousepos[1] > init_mousepos[1]:
            tmp = [init_mousepos[0]-1, init_mousepos[1]+1]
        else:
            tmp = [init_mousepos[0]-1, init_mousepos[1]-1]

    if board_piece[tmp[0]][tmp[1]] != 'e':
        return False
    else:
        return clear_diagonal(tmp, dest_mousepos, board_piece)


def clear_line(init_mousepos, dest_mousepos, board_piece):
    if dest_mousepos[0] != init_mousepos[0] and dest_mousepos[1] != init_mousepos[1]:
        return False

    if (dest_mousepos[0]-init_mousepos[0])**2 + (dest_mousepos[1]-init_mousepos[1])**2 == 1:
        return True

    if init_mousepos[0] == dest_mousepos[0]:
        if dest_mousepos[1] > init_mousepos[1]:
            tmp = [init_mousepos[0], init_mousepos[1]+1]
        else:
            tmp = [init_mousepos[0], init_mousepos[1]-1]
    else:
        if dest_mousepos[0] > init_mousepos[0]:
            tmp = [init_mousepos[0]+1, init_mousepos[1]]
        else:
            tmp = [init_mousepos[0]-1, init_mousepos[1]]

    if board_piece[tmp[0]][tmp[1]] != 'e':
        return False
    else:
        return clear_line(tmp, dest_mousepos, board_piece)


# main
def main():
    global init_mx, init_my, dest_mx, dest_my, end, waitforsecondbutton, whiteturn
    pygame.init()

    # Create Game Variables

    fps = 60
    clock = pygame.time.Clock()
    play = True
    pygame.display.set_caption('Chess')
    screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.SRCALPHA)

    # Create Groups
    board_group = pygame.sprite.Group()
    # Load Background
    board = [
        "WBWBWBWB",
        "BWBWBWBW",
        "WBWBWBWB",
        "BWBWBWBW",
        "WBWBWBWB",
        "BWBWBWBW",
        "WBWBWBWB",
        "BWBWBWBW", ]

    # Load Initial Pieces on Board
    board_pieces = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'],
        ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'],
        ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'],
        ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]

    # Create Game Objects, Update

    # Build Background
    x = y = 0
    for row in board:
        for letter in row:
            b = Block(x, y, letter)
            board_group.add(b)
            x += BOX_DIM
        y += BOX_DIM
        x = 0

    # Game loop

    while play:
        global loop

        loop += 1                                                               # Not sure if useful

        # Checks if button pressed
        for event in pygame.event.get():
            # Checks if window exit button pressed
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            # Checks if mouse button pressed
            if event.type is pygame.MOUSEBUTTONDOWN:
                if not waitforsecondbutton:
                    init_my, init_mx = pygame.mouse.get_pos()
                    print(init_my, init_mx)
                    init_mousepos = (int(init_mx / 100), int(init_my / 100))
                    if whiteturn:
                        if board_pieces[init_mousepos[0]][init_mousepos[1]] in ['P', 'N', 'B', 'R', 'Q', 'K']:
                            waitforsecondbutton = True

                    else:
                        if board_pieces[init_mousepos[0]][init_mousepos[1]] in ['p', 'n', 'b', 'r', 'q', 'k']:
                            waitforsecondbutton = True

                else:
                    dest_my, dest_mx = pygame.mouse.get_pos()
                    dest_mousepos = (int(dest_mx / 100), int(dest_my / 100))
                    if whiteturn:
                        if board_pieces[dest_mousepos[0]][dest_mousepos[1]] not in ['P', 'N', 'B', 'R', 'Q', 'K']:

                            if board_pieces[init_mousepos[0]][init_mousepos[1]] == 'P':
                                pawn_check(init_mousepos, dest_mousepos, board_pieces, whiteturn)

                            elif board_pieces[init_mousepos[0]][init_mousepos[1]] == 'N':
                                knight_check(init_mousepos, dest_mousepos, board_pieces)

                            elif board_pieces[init_mousepos[0]][init_mousepos[1]] == 'B':
                                bishop_check(init_mousepos, dest_mousepos, board_pieces)

                            elif board_pieces[init_mousepos[0]][init_mousepos[1]] == 'R':
                                rook_check(init_mousepos, dest_mousepos, board_pieces)

                            elif board_pieces[init_mousepos[0]][init_mousepos[1]] == 'Q':
                                queen_check(init_mousepos, dest_mousepos, board_pieces)

                            elif board_pieces[init_mousepos[0]][init_mousepos[1]] == 'K':
                                king_check(init_mousepos, dest_mousepos, board_pieces)

                    else:
                        if board_pieces[dest_mousepos[0]][dest_mousepos[1]] not in ['p', 'n', 'b', 'r', 'q', 'k']:

                            if board_pieces[init_mousepos[0]][init_mousepos[1]] == 'p':
                                pawn_check(init_mousepos, dest_mousepos, board_pieces, whiteturn)

                            elif board_pieces[init_mousepos[0]][init_mousepos[1]] == 'n':
                                knight_check(init_mousepos, dest_mousepos, board_pieces)

                            elif board_pieces[init_mousepos[0]][init_mousepos[1]] == 'b':
                                bishop_check(init_mousepos, dest_mousepos, board_pieces)

                            elif board_pieces[init_mousepos[0]][init_mousepos[1]] == 'r':
                                rook_check(init_mousepos, dest_mousepos, board_pieces)

                            elif board_pieces[init_mousepos[0]][init_mousepos[1]] == 'q':
                                queen_check(init_mousepos, dest_mousepos, board_pieces)

                            elif board_pieces[init_mousepos[0]][init_mousepos[1]] == 'k':
                                king_check(init_mousepos, dest_mousepos, board_pieces)

                    waitforsecondbutton = False

        # Draw Everything
        screen.fill(WHITE)
        for b in board_group:
            screen.blit(b.image, b.rect)

        if waitforsecondbutton:
            #if board[row][col] = 'W' :
                piece = pygame.image.load("blocks/white_square_highlight.png").convert_alpha()
                blit_pieces(piece, init_mousepos[1], init_mousepos[0], screen)

        for row in range(0, 8):
            for col in range(0, 8):
                if board_pieces[row][col] != 'e':
                    if board_pieces[row][col] == 'p':
                        piece = pygame.image.load("chesspiecesimages/blackpawn.png").convert_alpha()
                    elif board_pieces[row][col] == 'P':
                        piece = pygame.image.load("chesspiecesimages/whitepawn.png").convert_alpha()
                    elif board_pieces[row][col] == 'n':
                        piece = pygame.image.load("chesspiecesimages/blackknight.png").convert_alpha()
                    elif board_pieces[row][col] == 'N':
                        piece = pygame.image.load("chesspiecesimages/whiteknight.png").convert_alpha()
                    elif board_pieces[row][col] == 'b':
                        piece = pygame.image.load("chesspiecesimages/blackbishop.png").convert_alpha()
                    elif board_pieces[row][col] == 'B':
                        piece = pygame.image.load("chesspiecesimages/whitebishop.png").convert_alpha()
                    elif board_pieces[row][col] == 'r':
                        piece = pygame.image.load("chesspiecesimages/blackrook.png").convert_alpha()
                    elif board_pieces[row][col] == 'R':
                        piece = pygame.image.load("chesspiecesimages/whiterook.png").convert_alpha()
                    elif board_pieces[row][col] == 'q':
                        piece = pygame.image.load("chesspiecesimages/blackqueen.png").convert_alpha()
                    elif board_pieces[row][col] == 'Q':
                        piece = pygame.image.load("chesspiecesimages/whitequeen.png").convert_alpha()
                    elif board_pieces[row][col] == 'k':
                        piece = pygame.image.load("chesspiecesimages/blackking.png").convert_alpha()
                    elif board_pieces[row][col] == 'K':
                        piece = pygame.image.load("chesspiecesimages/whiteking.png").convert_alpha()
                    blit_pieces(piece, col, row, screen)

        # Limits frames per iteration of while loop
        clock.tick(fps)
        # Writes to main surface
        pygame.display.flip()


if __name__ == "__main__":
    main()
