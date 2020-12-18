from rasa_sdk import Action
from .UnisecForm import UnisecForm
from .UnisecValidator import UnisecValidator
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered, FollowupAction
import pymongo
import re
client = pymongo.MongoClient("localhost", 27017)
db=client["unisec-db"]

class FormPriorityPoint(UnisecForm):
   def name(self):
      return "form_priority_point"

   @staticmethod
   def required_validation_slot():
       return ['entity_province']

   def required_slots(self, tracker):
      return ['entity_province']

   def before_slot_fill(self, dispatcher, tracker, domain): 
      return []

   def submit(self, dispatcher, tracker, domain):
      try:
         entity_province = self.get_slot('entity_province')[0]
         entity_province_validated =  self.get_slot('entity_province_validated')[0]
      except:
         entity_province = None
         entity_province_validated = None
      print(entity_province_validated)
      if entity_province_validated != None:   
         
        dispatcher.utter_message("điểm cộng khu vực được tính như sau: Khu vực 1 (KV1): 0.75, Khu vực 2 (KV2): 0.25, Khu vực 2 nông thông (KV2-NT): 0.5, Khu vực 3 (KV3): không cộng")
        dispatcher.utter_message("tại " + entity_province_validated +", phân chia khu vực như sau")
        dt = db.priority_point.find({'province': re.compile('^' + entity_province_validated + '$', re.IGNORECASE)})
        for e in dt:
            res = ""
            res += e['area']
            res += ' '
            res += e['detail']
            dispatcher.utter_message(res)
    
      return [AllSlotsReset()]
      

      



