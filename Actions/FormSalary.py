from rasa_sdk import Action
from .UnisecForm import UnisecForm
from .UnisecValidator import UnisecValidator
from typing import Any, Text, Dict, List, Union
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered, FollowupAction
import pymongo
import re
client = pymongo.MongoClient("localhost", 27017)
db=client["unisec-db"]

class FormSalary(UnisecForm):
   def name(self):
      return "form_salary"

   @staticmethod
   def required_validation_slot():
       return ['entity_major']

   def required_slots(self, tracker):
      if tracker.get_slot('entity_major') == None:
         return ['entity_major']
      return []

   def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
      """A dictionary to map required slots to
          - an extracted entity
          - intent: value pairs
          - a whole message
          or a list of them, where a first match will be picked"""

      return {
         "entity_major": [
            self.from_entity(entity="entity_major", intent=["intent_salary", "inform"])],
      }

   def before_slot_fill(self, dispatcher, tracker, domain): 
      return []

   def submit(self, dispatcher, tracker, domain):
      try:
         entity_major = self.get_slot('entity_major')[0]
         entity_major_validated =  self.get_slot('entity_major_validated')[0]
      except:
         entity_major = None
         entity_major_validated = None
      
      if entity_major_validated != None:   
         res = ""
         try:
            major_validated_int = int(entity_major_validated)
            dt = db.major_info.find_one({'major_id': {'$in': [major_validated_int, entity_major_validated]}})
            res = dt['salary']
            dispatcher.utter_message("sau đây là thông tin về mức lương của ngành " + entity_major)
            dispatcher.utter_message(res)
         except:
             dispatcher.utter_message("không tìm thấy thông tin về mức lương ngành " + entity_major)
    
      return [AllSlotsReset()]
      

      



