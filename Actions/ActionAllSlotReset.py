from rasa_sdk.events import AllSlotsReset
from rasa_sdk import Action
class ActionChaoMung(Action):
    def name(self):
        return "action_all_slot_reset"

    def run(self,dispatcher, tracker, domain):
        return [AllSlotsReset()]