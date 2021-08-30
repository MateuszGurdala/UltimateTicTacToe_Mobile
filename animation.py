from kivy.clock import Clock


class Animation:
    def __init__(self):
        self.cross_animation = {str(i): f"graphics/cross_map/{i}.png" for i in range(1, 25)}

    # Sign animations

    def place_sign_animation(self, place_button, i, animation_pictures):
        if i == 25:
            return

        place_button.source = animation_pictures[str(i)]
        i += 1
        Clock.schedule_once(lambda a: self.place_sign_animation(place_button, i, animation_pictures), 0.01)

    # Button entrance animations

    def button_entrance_animation(self, place_button):
        place_button.size_hint = (0, 0)
        self.change_button_size(place_button, 0)

    def change_button_size(self, place_button, val):
        if val > 1:
            place_button.size_hint = 1, 1
            return

        val += 0.05
        place_button.size_hint = val, val
        Clock.schedule_once(lambda a: self.change_button_size(place_button, val), 0.01)

    def segment_entrance_animation(self, segment):
        # For loop doesn't work here, idk why
        delay = 0.2
        Clock.schedule_once(lambda a: self.button_entrance_animation(segment.places["1"]), delay * 0)
        Clock.schedule_once(lambda a: self.button_entrance_animation(segment.places["2"]), delay * 1)
        Clock.schedule_once(lambda a: self.button_entrance_animation(segment.places["3"]), delay * 2)
        Clock.schedule_once(lambda a: self.button_entrance_animation(segment.places["4"]), delay * 3)
        Clock.schedule_once(lambda a: self.button_entrance_animation(segment.places["5"]), delay * 4)
        Clock.schedule_once(lambda a: self.button_entrance_animation(segment.places["6"]), delay * 5)
        Clock.schedule_once(lambda a: self.button_entrance_animation(segment.places["7"]), delay * 6)
        Clock.schedule_once(lambda a: self.button_entrance_animation(segment.places["8"]), delay * 7)
        Clock.schedule_once(lambda a: self.button_entrance_animation(segment.places["9"]), delay * 8)

    # Log extend/hide animations

    def extend_log(self, game_log, game_map, val):
        if val >= 12.5 / 13:
            game_log.size_hint = 1, 12.5 / 13
            game_map.size_hint = 1, 0.5 / 13
            return

        val += 0.075

        game_log.size_hint = 1, val
        game_map.size_hint = 1, 1 - val

        Clock.schedule_once(lambda a: self.extend_log(game_log, game_map, val), 0.001)

    def hide_log(self, game_log, game_map, val):
        print(game_log.size_hint, game_map.size_hint)
        if val <= 3 / 13:
            game_log.size_hint = 1, 3 / 13
            game_map.size_hint = 1, 10 / 13
            return

        val -= 0.075

        game_log.size_hint = 1, val
        game_map.size_hint = 1, 1 - val

        Clock.schedule_once(lambda a: self.hide_log(game_log, game_map, val), 0.001)


animation = Animation()
