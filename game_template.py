import random
from AI import AI
from map_template import *
from time import sleep


class Game:
    def __init__(self):
        self.game_map = Map()
        self.player_sign = None
        self.enemy_sign = None

        self.ai = AI()
        self.place_number = None
        self.current_segment = None
        self.turn_number = 0

    def choose_segment(self, player=False, ai=False):
        if player:
            pass
        elif ai:
            self.current_segment = self.ai.choose_segment(self.game_map)[0]

    def place_sign(self, segment_number, place_number, sign):
        self.game_map.segments[segment_number].places[place_number] = sign
        self.game_map.update()

    def player_turn(self):
        self.game_map.print()

        if self.current_segment in self.game_map.taken_places:
            self.choose_segment(player=True)

        self.place_number = place_number
        self.place_sign(self.current_segment, self.place_number, self.player_sign)

        self.current_segment = self.place_number
        self.game_map.update()
        self.turn_number += 1

    def ai_pick_place_number(self, game_mode):
        segment, game_map = self.game_map.segments[self.current_segment], self.game_map
        if game_mode == "ai_hard":
            if self.turn_number < 15:
                self.turn_number += 1
                return self.ai.pick_best_move(segment, game_map)[0]
            else:
                return self.ai.pick_best_move_algorithm(game_map, segment)[0]
        elif game_mode == "ai_normal":
            return self.ai.pick_best_move(segment, game_map)[0]
        elif game_mode == "ai_easy":
            val = random.randint(1, 9)
            while self.game_map.segments[self.current_segment].places[str(val)]:
                val = random.randint(1, 9)
            return str(val)

    def ai_turn(self):
        self.game_map.print()

        if self.current_segment in self.game_map.taken_places:
            self.choose_segment(ai=True)

        self.place_number = self.ai_pick_place_number()

        self.place_sign(self.current_segment, self.place_number, self.enemy_sign)

        self.current_segment = self.place_number
        self.game_map.update()
        self.turn_number += 2
