from position import determine_square_coordinates
class chess_piece:
    def __init__(self, name, ASCII_value, color, player, font, screen, file, rank):
        self.name = name
        self.ASCII_value = ASCII_value
        self.color = color
        self.player = player
        self.font = font
        self.screen = screen
        self.rank = rank
        self.file = file
        self.piece = self.font.render(self.ASCII_value, True, self.color)

    def render_piece(self):
        coordinates = determine_square_coordinates(self.file, self.rank)
        self.screen.blit(self.piece, coordinates)