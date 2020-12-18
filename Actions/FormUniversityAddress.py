from rasa_sdk import Action
from .UnisecForm import UnisecForm
from .UnisecValidator import UnisecValidator
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered, FollowupAction
import pymongo
import re
client = pymongo.MongoClient("localhost", 27017)
db=client["unisec-db"]

class FormUniversityAddress(UnisecForm):
   def name(self):
      return "form_university_address"

   @staticmethod
   def required_validation_slot():
       return ['entity_university']

   def required_slots(self, tracker):
      return ['entity_university']
   

   def before_slot_fill(self, dispatcher, tracker, domain): 
      return []

   def submit(self, dispatcher, tracker, domain):
      try:
         university = self.get_slot('entity_university')[0]
         university_validated =  self.get_slot('entity_university_validated')[0]
      except:
         university = None
         university_validated =  None
      data = []
      if university_validated != None:
        data = db.universities.find({'abbreviation': re.compile('^' + university_validated + '$', re.IGNORECASE)})
      ret = []
      for entry in data:
          try:
              ret.append(entry['address'])
          except:
              pass
      if len(ret) != 1:
        dispatcher.utter_message("Tiếc quá, tôi không tìm thấy thông tin về địa chỉ trường " + university)
      else:
        dispatcher.utter_message("Địa chỉ trường "+ university + " là " + ret[0])

      return [AllSlotsReset()]

      



