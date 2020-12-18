from rasa_sdk.events import SlotSet
from rasa_sdk import Action
class ActionDefaulFallback(Action):
    def name(self):
        return "action_default_fallback"

    def run(self,dispatcher, tracker, domain):
        dispatcher.utter_message("Tôi chưa thể giúp bạn việc này. Tôi sẽ "
                                 "cố gắng cải thiện nhiều hơn trong tương lai.")
        return []