from rasa_sdk import Action
from .UnisecForm import UnisecForm
from .UnisecValidator import UnisecValidator
from typing import Any, Text, Dict, List, Union
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered, FollowupAction
import pymongo
import re

client = pymongo.MongoClient("localhost", 27017)
db = client["unisec-db"]


class FormAdmission(UnisecForm):
    def name(self):
        return "form_admission"

    @staticmethod
    def required_validation_slot():
        return ['entity_university']

    def required_slots(self, tracker):
        if tracker.get_slot('entity_university') == None:
            return ['entity_university']
        return []

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "entity_university": [
                self.from_entity(entity="entity_university", intent=["intent_admission", "inform"])],
        }

    def before_slot_fill(self, dispatcher, tracker, domain):
        return []

    def submit(self, dispatcher, tracker, domain):
        try:
            entity_university = self.get_slot('entity_university')[0]
            entity_university_validated = self.get_slot('entity_university_validated')[0]
        except:
            entity_university = None
            entity_university_validated = None

        if entity_university_validated != None:
            try:
                dt = db.admission.find_one({ 'university_id': entity_university_validated})
                data = dt['admission']
                dispatcher.utter_message("sau đây là thông tin chỉ tiêu trường " + entity_university)
                dispatcher.utter_message(data)
            except:
                dispatcher.utter_message("không tìm thấy thông tin tuyển sinh trường " + entity_university)

        return [AllSlotsReset()]
