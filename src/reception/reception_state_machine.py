from statemachine import StateMachine, State


class ReceptionStateMachine(StateMachine):
    redraw_necessary = True

    awaiting = State("Awaiting", initial=True)
    manual_input = State("Manual Input")
    green = State("Green")
    wrong_barcode = State("Wrong barcode")
    no_connection = State("No Connection")
    red = State("Red")
    member_not_found = State("Member not found")

    awaiting_to_shopping_status_ok = awaiting.to(green)
    ok_to_awaiting = green.to(awaiting)
    awaiting_to_wrong_barcode = awaiting.to(wrong_barcode)
    wrong_barcode_to_awaiting = wrong_barcode.to(awaiting)
    awaiting_to_shopping_status_not_ok = awaiting.to(red)
    not_ok_to_awaiting = red.to(awaiting)
    awaiting_to_no_connection = awaiting.to(no_connection)
    no_connection_to_awaiting = no_connection.to(awaiting)
    awaiting_to_manual_input = awaiting.to(manual_input)
    manual_input_to_green = manual_input.to(green)
    manual_input_to_red = manual_input.to(red)
    manual_input_to_awaiting = manual_input.to(awaiting)
    manual_input_to_no_connection = manual_input.to(no_connection)
    manual_input_to_member_not_found = manual_input.to(member_not_found)
    member_not_found_to_manual_input = member_not_found.to(manual_input)

    def on_enter_awaiting(self):
        self.redraw_necessary = True

    def is_redraw_necessary(self):
        value = self.redraw_necessary
        self.redraw_necessary = False
        return value
