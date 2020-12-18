from rasa_sdk import Action
from .UnisecForm import UnisecForm
from .UnisecValidator import UnisecValidator
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered, FollowupAction
import pymongo
import re
client = pymongo.MongoClient("localhost", 27017)
db=client["unisec-db"]

class FormUniversityRank(UnisecForm):
   def name(self):
      return "form_university_rank"

   @staticmethod
   def required_validation_slot():
       return ['entity_university']

   def required_slots(self, tracker):
      if tracker.get_slot('entity_university') == None:
         return ['entity_university']
      return []

   def before_slot_fill(self, dispatcher, tracker, domain): 
      return []

   def submit(self, dispatcher, tracker, domain):
      try:
         university = self.get_slot('entity_university')[0]
         university_validated =  self.get_slot('entity_university_validated')[0]
      except:
         university = None
         university_validated = None
      
      if university_validated != None:
         ret = "Trường " + university
         dt = db.rank_uni.find_one({'id': re.compile('^' + university_validated + '$', re.IGNORECASE)})
         if dt != None:
             ret += " xếp thứ " + str(dt['rank']) + " theo xếp hạng của unirank"
         dt2 = db.rank_metric.find_one({'id': re.compile('^' + university_validated + '$', re.IGNORECASE)})
         if dt != None:
             if dt2 != None :
                ret += " và"
                ret += " xếp thứ " + str(dt2['rank']) + " theo xếp hạng của webometrics"
      if dt == None and dt2 == None:
         ret = "Không tìm thấy thông tin thứ hạng trường " + university
      dispatcher.utter_message(ret)
      return [AllSlotsReset()]
      

      



