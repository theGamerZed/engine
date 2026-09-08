class chess_piece:
    def __init__(self, name, u_value, color, player,font,screen, x=0, y=0):
        self.name = name
        self.u_value = u_value
        self.color = color
        self.player = player
        self.font = font
        self.screen = screen
        self.x = x
        self.y = y
    def render_piece(self, font):
        piece = font.render(self.u_value, True, self.color)
        self.screen.blit(piece, (self.x, self.y))