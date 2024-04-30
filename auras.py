class AuraEngine:
    # needs to access the game time to process decay
    def __init__(self, innate_gauge, game_state):
        self.innate_gauge = innate_gauge
        self.game_state = game_state

    def decay_aura(self, time_delta):
        pass

    def update_aura(self):
        pass