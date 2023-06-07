from statemachine import StateMachine, State


class ReceptionStateMachine(StateMachine):
    awaiting = State("Awaiting", initial=True)
    green = State("Green")
    wrong_barcode = State("Wrong barcode")
    red = State("Red")

    shopping_status_ok = awaiting.to(green)
    ok_to_awaiting = green.to(awaiting)
    member_card_not_found = awaiting.to(wrong_barcode)
    wrong_barcode_to_awaiting = wrong_barcode.to(awaiting)
    shopping_status_not_ok = awaiting.to(red)
    not_ok_to_awaiting = red.to(awaiting)

    def on_enter_awaiting(self):
        self.redraw_necessary = True

    def is_redraw_necessary(self):
        value = self.redraw_necessary
        self.redraw_necessary = False
        return value
