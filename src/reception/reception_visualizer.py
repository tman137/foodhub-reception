import pygame

BLACK = (0, 0, 0)
GREEN = (0, 153, 0)
RED = (204, 0, 0)


class ReceptionVisualizer:
    def __init__(self):
        pygame.display.init()
        pygame.mixer.init()
        pygame.font.init()

        self.width = 1440
        self.heigth = 900
        self.size = self.width, self.heigth
        self.display = pygame.display.set_mode(self.size, flags=pygame.NOFRAME)
        self.background = pygame.image.load("res/background.png")
        self.font = pygame.font.SysFont("Barlow", 80)
        self.alpha_start = 220
        self.alpha_step = -7
        self.time_to_blink_color = 500
        self.red_reason = ""
        self.second_line_offset = 80

    def set_red_reason(self, reason):
        self.red_reason = reason

    def _draw_background(self):
        self.display.blit(self.background, (0, 0))

    def _draw_rectangle(self, alpha, color):
        green_rectangle = pygame.Surface((self.width, self.heigth))
        green_rectangle.set_alpha(alpha)
        green_rectangle.fill(color)
        self.display.blit(green_rectangle, (0, 0))

    def _draw_text(self, text, start_point):
        text = self.font.render(text, True, BLACK)
        self.display.blit(text, (start_point))

    def _draw(self, alpha, text, text_second_line, start_point, color):
        self._draw_background()
        self._draw_rectangle(alpha, color)
        self._draw_text(text, start_point)
        self._draw_text(
            text_second_line, (start_point[0], start_point[1] + self.second_line_offset)
        )
        pygame.display.flip()

    def _show_animation(self, sound, text, text_second_line, start_point, color):
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
        self._draw(self.alpha_start, text, text_second_line, start_point, color)
        pygame.time.wait(self.time_to_blink_color)
        for alpha in range(self.alpha_start, 0, self.alpha_step):
            self._draw(alpha, text, text_second_line, start_point, color)

    def show_awaiting(self):
        self._draw_background()
        self._draw_text("Warte auf Ausweis", (350, 350))
        pygame.display.flip()

    def show_green(self):
        self._show_animation(
            "res/green.wav", "Person ist einkaufsberechtigt", "", (200, 350), GREEN
        )

    def show_wrong_barcode(self):
        self._show_animation(
            "res/wrong_barcode.wav", "Code ist nicht im System!", "", (270, 350), RED
        )

    def show_red(self):
        self._show_animation(
            "res/red.wav",
            "Einkaufsstatus nicht ok!",
            "Grund: {}".format(self.red_reason),
            (270, 350),
            RED,
        )
