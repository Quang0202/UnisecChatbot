from rasa_sdk import Action
from .UnisecForm import UnisecForm
from .UnisecValidator import UnisecValidator
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered, FollowupAction
import pymongo
import re
client = pymongo.MongoClient("localhost", 27017)
db=client["unisec-db"]

class FormUniversityId(UnisecForm):
   def name(self):
      return "form_university_id"

   @staticmethod
   def required_validation_slot():
       return ['entity_university', 'entity_university_id']

   def required_slots(self, tracker):
      if tracker.get_slot('entity_university') == None and tracker.get_slot('entity_university_id') == None:
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
      try:
         university_id = self.get_slot('entity_university_id')[0]
      except:
         university_id = None

      
      if university_id != None:
         dt = db.universities.find_one({'abbreviation': re.compile('^' + university_id + '$', re.IGNORECASE)})
         if dt != None:
            dispatcher.utter_message("Mã " + university_id + " là của trường " + dt['name'])
         else:
            dispatcher.utter_message("Tôi không tìm thấy trường nào có mã là " + university_id)
         return [AllSlotsReset()]

      dispatcher.utter_message("Mã trường của " + university + " là " + university_validated)
      return [AllSlotsReset()]
      

      



