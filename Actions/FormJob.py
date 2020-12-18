from rasa_sdk import Action
from .UnisecForm import UnisecForm
from .UnisecValidator import UnisecValidator
from typing import Any, Text, Dict, List, Union
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered, FollowupAction
import pymongo
import re
client = pymongo.MongoClient("localhost", 27017)
db=client["unisec-db"]

class FormJob(UnisecForm):
   def name(self):
      return "form_job"

   @staticmethod
   def required_validation_slot():
       return ['entity_major']

   def required_slots(self, tracker):
      if tracker.get_slot('entity_major') == None:
         return ['entity_major']
      return []

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
            dt = db.major_info.find_one({'id': re.compile('^' + entity_major_validated + '$', re.IGNORECASE)})
            res = dt['job']
            dispatcher.utter_message("sau đây là thông tin về cơ hội việc làm của " + entity_major)
            dispatcher.utter_message(res)
         except:
             dispatcher.utter_message("không tìm thấy thông tin về cơ hội việc làm ngành " + entity_major)
    
      return [AllSlotsReset()]
      

      



