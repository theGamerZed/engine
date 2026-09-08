class chess_piece:
    def __init__(self, name, u_value, color, player,font):
        self.name = name
        self.u_value = u_value
        self.color = color
        self.player = player
        self.font = font
    def render_piece(self, font):
        return font.render(self.u_value, True, self.color)