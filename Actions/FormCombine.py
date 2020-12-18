from rasa_sdk import Action
from .UnisecForm import UnisecForm
from .UnisecValidator import UnisecValidator
from typing import Any, Text, Dict, List, Union
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered, FollowupAction
import pymongo
import re
client = pymongo.MongoClient("localhost", 27017)
db=client["unisec-db"]

class FormCombine(UnisecForm):
   def name(self):
      return "form_combine"

   @staticmethod
   def required_validation_slot():
       return ['entity_university', 'entity_major']
   
   def required_slots(self, tracker):
      # if tracker.get_slot('entity_university') == None:
      #    return ['entity_university']
      
      return ['entity_university','entity_major']

   def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
      """A dictionary to map required slots to
          - an extracted entity
          - intent: value pairs
          - a whole message
          or a list of them, where a first match will be picked"""

      return {
         "entity_university": [
            self.from_entity(entity="entity_university", intent=["intent_combine", "inform"])],
         "entity_major": [
            self.from_entity(entity="entity_major", intent=["intent_combine", "inform"])],
      }

   def before_slot_fill(self, dispatcher, tracker, domain):
      
      return []

   def submit(self, dispatcher, tracker, domain):
      # utter universities fited with current slot.
      res = self.getResponse()
      dispatcher.utter_message(res[0])
      # if len(res[1]) >1:
      #    dispatcher.utter_message(json_message={"data":{"table" : res[1]}})
      return [AllSlotsReset()]

   ##
   ## query db. 
   ##
   def getResponse(self):
      try:
         university = self.get_slot('entity_university')[0]
         university_validated =  self.get_slot('entity_university_validated')[0]
      except:
         university = None
         university_validated = None
      try:
         major =  str(self.get_slot('entity_major')[0])
         major_validated =  str(self.get_slot('entity_major_validated')[0])
      except:
         major = None
         major_validated = None

      mes = "Ngành "
      query = {}
      if major_validated != None:
          query['major_group_id'] = re.compile('^' + major_validated + '$', re.IGNORECASE)
          mes += major

      if university_validated != None:
          query['university_id'] =  re.compile('^' + university_validated + '$', re.IGNORECASE)
          mes += " trường " + university
      mes += ' xét tuyển khối '
      query['year'] = '2019'
      data = db.admission_scores.find(query)
      ret = []
      com = ""
      for entry in data:
         try:
            for i in entry['combine']:
               com += ' '
               com += i
         except:
            print("vukihai:error while loading admision score: FormHoiDiemChuan - get response")
         break
      if len(com) == 0:
         mes = "Không tìm thấy thông tin tổ hợp xét tuyển"
      mes += com
      return (mes, ret)
