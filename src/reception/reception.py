import pygame
import datetime
from reception_state_machine import ReceptionStateMachine
from reception_visualizer import ReceptionVisualizer
from reception_input import ReceptionInput
from src.odoo.odoo_connector import OdooConnector
from src.odoo.odoo_arguments import parse_odoo_arguments


class Reception:
    def __init__(self):
        args = self._parse_arguments()
        self.odoo_connector = OdooConnector(
            args.url, args.db, args.username, args.password
        )
        self.state_machine = ReceptionStateMachine()
        self.visualizer = ReceptionVisualizer()
        self.input = ReceptionInput()
        self.state_mapping = {
            "Awaiting": self.awaiting,
            "Green": self.green,
            "Wrong barcode": self.wrong_barcode,
            "Red": self.red,
        }
        self.previous_minute = datetime.datetime.now().minute

    def _parse_arguments(self):
        return parse_odoo_arguments()

    def _set_red_reason_for_visulization(self, member_record):
        cooperative_status = self.odoo_connector.get_cooperative_status(
            member_record.get_cooperative_status_ids()
        )
        if cooperative_status.valid():
            self.visualizer.set_red_reason(cooperative_status.get_status())

    def _new_minute(self):
        current_minute = datetime.datetime.now().minute
        result = current_minute != self.previous_minute
        self.previous_minute = current_minute
        return result

    def _redraw_necessery(self):
        return self._new_minute() or self.state_machine.is_redraw_necessary()

    def awaiting(self):
        qr_code = self.input.poll_qr_code()
        if qr_code:
            member_record = self.odoo_connector.get_member(qr_code)
            if not member_record.valid():
                self.state_machine.member_card_not_found()
                return
            if member_record.can_shop():
                self.state_machine.shopping_status_ok()
            else:
                self._set_red_reason_for_visulization(member_record)
                self.state_machine.shopping_status_not_ok()
            return
        if self._redraw_necessery():
            self.visualizer.show_awaiting()

    def green(self):
        self.visualizer.show_green()
        self.state_machine.ok_to_awaiting()

    def wrong_barcode(self):
        self.visualizer.show_wrong_barcode()
        self.state_machine.wrong_barcode_to_awaiting()

    def red(self):
        self.visualizer.show_red()
        self.state_machine.not_ok_to_awaiting()

    def loop(self):
        self.state_mapping[self.state_machine.current_state.name]()


if __name__ == "__main__":
    reception = Reception()
    clock = pygame.time.Clock()
    while True:
        reception.loop()
        clock.tick(30)
