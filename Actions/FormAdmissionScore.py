from rasa_sdk import Action
from .UnisecForm import UnisecForm
from .UnisecValidator import UnisecValidator
from typing import Any, Text, Dict, List, Union
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered, FollowupAction
import pymongo
import re
client = pymongo.MongoClient("localhost", 27017)
db=client["unisec-db"]

class FormAdmissionScore(UnisecForm):
   def name(self):
      return "form_admission_score"

   @staticmethod
   def required_validation_slot():
       return ['entity_university', 'entity_major', 'entity_year']
   
   def required_slots(self, tracker):
      # if tracker.get_slot('entity_university') == None:
      #    return ['entity_university']
      
      return ['entity_university']

   def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
      """A dictionary to map required slots to
          - an extracted entity
          - intent: value pairs
          - a whole message
          or a list of them, where a first match will be picked"""

      return {
         "entity_university": [
            self.from_entity(entity="entity_university", intent=["intent_admission_score", "inform"])],
         "entity_major": [
            self.from_entity(entity="entity_major", intent=["intent_admission_score", "inform"])],
         "entity_year": [
            self.from_entity(entity="entity_year", intent=["intent_admission_score", "inform"])],
      }

   def before_slot_fill(self, dispatcher, tracker, domain):
      # utter universities fited with current slot.
      university = tracker.get_slot('entity_university')
      major = tracker.get_slot('entity_major')
      if university == None and major == None:
          return []
      res = self.getResponse()
      dispatcher.utter_message(res[0])
      if len(res[1]) >1:
         dispatcher.utter_message(json_message={"data":{"table" : res[1]}})
      return []

   def submit(self, dispatcher, tracker, domain):
      # reset all slot if needed
      # add utter_chao_mung
      # finish form
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
      try:
         year_validated =  self.get_slot('entity_year_validated')[0]
      except:
         year_validated = '2020'
      mes = "Sau đây là điểm chuẩn"
      query = {}
      if university_validated != None:
          query['university_id'] = re.compile('^' + university_validated + '$', re.IGNORECASE)
          mes += " trường " + university
      if major_validated != None:
          query['major_group_id'] = re.compile('^' + major_validated + '$', re.IGNORECASE)
          mes += " ngành " + major

      if (university_validated != None and major_validated != None):
         # query['year'] = str(year_validated)
         # mes += " năm " + str(year_validated)
         data = db.admission_scores.find(query)
         ret = []
         ret.append(["năm", "trường", "ngành học", "điểm", "tổ hợp môn"])
         for entry in data:
            try:
               ret.append([entry['year'],entry['university'], entry['major_name'],entry['score'], entry['combine']])
            except:
               print("vukihai:error while loading admision score: FormHoiDiemChuan - get response")
      else:
         query['year'] = str(year_validated)
         mes += " năm " + str(year_validated)
         data = db.admission_scores.find(query)
         ret = []
         ret.append(["trường", "ngành học", "điểm", "tổ hợp môn"])
         for entry in data:
            try:
               ret.append([entry['university'], entry['major_name'],entry['score'], entry['combine']])
            except:
               print("vukihai:error while loading admision score: FormHoiDiemChuan - get response")
         print(query)
      if len(ret) == 1:
         mes = "Tiếc quá, tôi không tìm thấy thông tin điểm chuẩn"
      print(ret)
      return (mes, ret)
