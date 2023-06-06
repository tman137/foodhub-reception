import pygame


class ReceptionInput:
    def __init__(self):
        self.code = ""

    def poll_qr_code(self):
        result = None
        event = pygame.event.wait(100)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                result = self.code
                self.code = ""
            else:
                self.code += event.unicode
        return result
