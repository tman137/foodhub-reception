import pygame
import datetime
import re
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
            "No Connection": self.no_connection,
            "Manual Input": self.manual_input,
            "Member not found": self.member_not_found,
            "Red": self.red,
            "Payment not received": self.cooperator_candidate,
            "Working mode not set": self.working_mode_not_set,
        }
        self.previous_minute = datetime.datetime.now().minute
        self.member_name = ""

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
        input = self.input.poll_qr_code()
        if input:
            if input == "[F1]":
                self.state_machine.awaiting_to_manual_input()
            else:
                qr_code = input
                try:
                    member_record = self.odoo_connector.get_member(qr_code)
                except:
                    self.state_machine.awaiting_to_no_connection()
                    return
                if not member_record.valid():
                    self.state_machine.awaiting_to_wrong_barcode()
                    return
                if not member_record.working_mode_set():
                    self.state_machine.awaiting_to_working_mode_not_set()
                    return
                if member_record.can_shop():
                    self.state_machine.awaiting_to_shopping_status_ok()
                else:
                    self._set_red_reason_for_visulization(member_record)
                    self.state_machine.awaiting_to_shopping_status_not_ok()
                return
        if self._redraw_necessery():
            self.visualizer.show_awaiting()

    def green(self):
        self.visualizer.show_green()
        self.state_machine.ok_to_awaiting()

    def wrong_barcode(self):
        self.visualizer.show_wrong_barcode()
        self.state_machine.wrong_barcode_to_awaiting()

    def no_connection(self):
        self.visualizer.show_no_internet_connection()
        self.state_machine.no_connection_to_awaiting()

    def _apply_backspaces(self, member_name):
        return re.sub(".\b|\b", "", member_name)

    def _remove_new_line(self, member_name):
        member_name = re.sub("\n", "", member_name)
        return re.sub("\^\[", "", member_name)

    def _clean_member_name(self, member_name):
        return self._remove_new_line(self._apply_backspaces(member_name))

    def manual_input(self):
        if re.search("\n", self.member_name):
            try:
                member_record = self.odoo_connector.get_member_from_name(
                    self.member_name.strip()
                )
            except:
                self.member_name = ""
                self.state_machine.manual_input_to_no_connection()
                return
            self.member_name = ""
            if not member_record.valid():
                self.state_machine.manual_input_to_member_not_found()
                return
            if member_record.is_cooperator_candiate():
                self.state_machine.manual_input_to_cooperator_candidate()
                return
            if not member_record.working_mode_set():
                self.state_machine.manual_input_to_working_mode_not_set()
                return
            if member_record.can_shop():
                self.state_machine.manual_input_to_green()
                return
            else:
                self._set_red_reason_for_visulization(member_record)
                self.state_machine.manual_input_to_red()
                return
        self.member_name = self._apply_backspaces(
            self.member_name + self.input.poll_member_name()
        )
        if re.search("\^\[", self.member_name):
            self.member_name = ""
            self.state_machine.manual_input_to_awaiting()
            return
        self.visualizer.show_manual_input(self._remove_new_line(self.member_name))

    def member_not_found(self):
        self.visualizer.show_member_not_found()
        self.state_machine.member_not_found_to_manual_input()

    def red(self):
        self.visualizer.show_red()
        self.state_machine.not_ok_to_awaiting()

    def cooperator_candidate(self):
        self.visualizer.show_cooperator_candidate()
        self.state_machine.cooperator_candidate_to_awaiting()

    def working_mode_not_set(self):
        self.visualizer.show_working_mode_not_set()
        self.state_machine.working_mode_not_set_to_awaiting()

    def loop(self):
        self.state_mapping[self.state_machine.current_state.name]()


if __name__ == "__main__":
    reception = Reception()
    clock = pygame.time.Clock()
    while True:
        reception.loop()
        clock.tick(30)
