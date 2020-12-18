from rasa_sdk import Action
from .UnisecForm import UnisecForm
from .UnisecValidator import UnisecValidator
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered, FollowupAction
import pymongo
import re
client = pymongo.MongoClient("localhost", 27017)
db=client["unisec-db"]

class FormDemo(UnisecForm):
   def name(self):
      return "form_hoi_diem_chuan"

   @staticmethod
   def required_validation_slot():
       return ['entity_truong_dai_hoc', 'entity_nganh_hoc']

   def required_slots(self, tracker):
      return []
   

   def before_slot_fill(self, dispatcher, tracker, domain): 
      return []

   def submit(self, dispatcher, tracker, domain):
      return [AllSlotsReset()]

      



