import pygame
import datetime

BLACK = (0, 0, 0)
GREEN = (0, 153, 0)
RED = (204, 0, 0)


class ReceptionVisualizer:
    def __init__(self):
        pygame.display.init()
        pygame.mixer.init()
        pygame.font.init()
        pygame.mouse.set_visible(False)

        self.width = 1920
        self.heigth = 1080
        self.size = self.width, self.heigth
        self.display = pygame.display.set_mode(self.size, flags=pygame.FULLSCREEN)
        self.background = pygame.image.load("res/background.png").convert()
        self.default_font = pygame.font.SysFont("Barlow", 100)
        self.font = self.default_font
        self.clock_font = pygame.font.SysFont("Barlow", 60)
        self.alpha_start = 220
        self.alpha_step = -7
        self.time_to_blink_color = 100
        self.red_reason = ""
        self.second_line_offset = 100

    def set_red_reason(self, reason):
        self.red_reason = reason

    def _draw_time(self):
        time = datetime.datetime.now().time()
        text = self.clock_font.render(
            "{hours:02}:{minutes:02}".format(hours=time.hour, minutes=time.minute),
            True,
            BLACK,
        )
        self.display.blit(text, (50, 30))

    def _draw_background(self):
        self.display.blit(self.background, (0, 0))
        self._draw_time()

    def _draw_rectangle(self, alpha, color):
        green_rectangle = pygame.Surface((self.width, self.heigth))
        green_rectangle.set_alpha(alpha)
        green_rectangle.fill(color)
        self.display.blit(green_rectangle, (0, 0))

    def _draw_text(self, text, start_point, font=None):
        if font:
            self.font = font
        text = self.font.render(text, True, BLACK)
        self.display.blit(text, (start_point))
        self.font = self.default_font

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
        self._draw_text("Warte auf Ausweis", (450, 350))
        self._draw_text(
            "F1 drücken, um den Mitgliedernamen manuell einzugeben",
            (50, 1030),
            pygame.font.SysFont("Barlow", 30),
        )
        pygame.display.flip()

    def show_no_internet_connection(self):
        self._show_animation(
            "res/wrong_barcode.wav", "Keine Internetverbindung", "", (350, 350), RED
        )

    def show_green(self):
        self._show_animation(
            "res/green.wav", "Person ist einkaufsberechtigt", "", (270, 350), GREEN
        )

    def show_wrong_barcode(self):
        self._show_animation(
            "res/wrong_barcode.wav", "Code ist nicht im System!", "", (350, 350), RED
        )

    def show_red(self):
        self._show_animation(
            "res/red.wav",
            "Einkaufsstatus nicht ok!",
            "Grund: {}".format(self.red_reason),
            (300, 350),
            RED,
        )

    def show_manual_input(self, member_name):
        self._draw_background()
        self._draw_text("Namen eingeben:", (400, 350))
        self._draw_text(member_name, (400, 450))
        self._draw_text(
            "ESC drücken, um zurück zum Scannen zu gehen",
            (50, 1030),
            pygame.font.SysFont("Barlow", 30),
        )
        pygame.display.flip()

    def show_member_not_found(self):
        self._show_animation(
            "res/wrong_barcode.wav",
            "Mitglied nicht gefunden!",
            "",
            (350, 350),
            RED,
        )
