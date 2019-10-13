class GameConfig():
    game_speed = .1
    shotgun_appeared_at = 2020
    game_speed_axeleration_per_year = 1.01
    years_changing_speed = 5 # event loop cycles

    @classmethod
    def increase_game_speed(cls):
        cls.game_speed /= cls.game_speed_axeleration_per_year