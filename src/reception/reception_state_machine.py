from statemachine import StateMachine, State


class ReceptionStateMachine(StateMachine):
    redraw_necessary = True

    awaiting = State("Awaiting", initial=True)
    green = State("Green")
    wrong_barcode = State("Wrong barcode")
    no_connection = State("No Connection")
    red = State("Red")

    shopping_status_ok = awaiting.to(green)
    ok_to_awaiting = green.to(awaiting)
    member_card_not_found = awaiting.to(wrong_barcode)
    wrong_barcode_to_awaiting = wrong_barcode.to(awaiting)
    shopping_status_not_ok = awaiting.to(red)
    not_ok_to_awaiting = red.to(awaiting)
    awaiting_to_no_connection = awaiting.to(no_connection)
    no_connection_to_awaiting = no_connection.to(awaiting)

    def on_enter_awaiting(self):
        self.redraw_necessary = True

    def is_redraw_necessary(self):
        value = self.redraw_necessary
        self.redraw_necessary = False
        return value
