from rasa_sdk import Action
from .UnisecForm import UnisecForm
from .UnisecValidator import UnisecValidator
from typing import Any, Text, Dict, List, Union
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered, FollowupAction
import pymongo
import re
client = pymongo.MongoClient("localhost", 27017)
db=client["unisec-db"]

class FormMajorList(UnisecForm):
   def name(self):
      return "form_major_list"

   @staticmethod
   def required_validation_slot():
       return ['entity_university']

   def required_slots(self, tracker):
      return ['entity_university']

   def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
      """A dictionary to map required slots to
          - an extracted entity
          - intent: value pairs
          - a whole message
          or a list of them, where a first match will be picked"""

      return {
         "entity_university": [
            self.from_entity(entity="entity_university", intent=["intent_major_list", "inform"])],
      }

   def before_slot_fill(self, dispatcher, tracker, domain): 
      return []

   def submit(self, dispatcher, tracker, domain):
      try:
         entity_university = self.get_slot('entity_university')[0]
         entity_university_validated =  self.get_slot('entity_university_validated')[0]
      except:
         entity_university = None
         entity_university_validated = None
      
      if entity_university_validated != None:   
         res = []
         res.append(['mã ngành', 'tên ngành', 'tổ hợp'])
         try:
            dt = db.universities.find_one({'abbreviation':entity_university_validated})
            dt = dt['majors']
            for i in dt:
                res.append([i['major_id'], i['major_name'], i['major_combine']])
         except:
             dispatcher.utter_message("không tìm thấy thông tin về khung đào tạo ngành " + entity_university)
             return [AllSlotsReset()]
         if len(res) == 1:
             dispatcher.utter_message("không tìm thấy thông tin về khung đào tạo ngành " + entity_university)
             return [AllSlotsReset()]
         dispatcher.utter_message("Trường " + entity_university + " hiện đang đào tạo các ngành sau:")
         dispatcher.utter_message(json_message={"data":{"table" : res}})
      return [AllSlotsReset()]
      

      



