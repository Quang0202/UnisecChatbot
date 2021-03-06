from rasa_sdk import Action
from .UnisecForm import UnisecForm
from typing import Any, Text, Dict, List, Union
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered
import pymongo
import re
client = pymongo.MongoClient("localhost", 27017)
db=client["unisec-db"]

class FormFindUniveristy(UnisecForm):
   def name(self):
      return "form_find_university"

   @staticmethod
   def required_validation_slot():
      return ['entity_macro_region', 'entity_province', 'entity_score', 'entity_combine', 'entity_major']

   # def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
   #    """A dictionary to map required slots to
   #        - an extracted entity
   #        - intent: value pairs
   #        - a whole message
   #        or a list of them, where a first match will be picked"""
   
   #    return {
   #       "entity_macro_region": [
   #          self.from_entity(entity="entity_macro_region", intent=["intent_find_university", "inform"])],
   #       "entity_province": [
   #          self.from_entity(entity="entity_province", intent=["intent_find_university", "inform"])],
   #       "entity_score": [
   #          self.from_entity(entity="entity_score", intent=["intent_find_university", "inform"])],
   #       "entity_combine": [
   #          self.from_entity(entity="entity_combine", intent=["intent_find_university", "inform"])],
   #       "entity_major": [
   #          self.from_entity(entity="entity_major", intent=["intent_find_university", "inform"])],
   #    }

   def required_slots(self, tracker):
      print("slot fill called")
      if len(self.getResponse(tracker)[1]) < 10:
         return []
      #vukihai: if response is detail enough
      # return []
      # else request more slot in order
      # do not request all slot at the same time
      if tracker.get_slot('entity_macro_region') == None and tracker.get_slot('entity_province') == None:
         return ['entity_macro_region']
      if tracker.get_slot('entity_score') == None:
         return ['entity_score']
      if tracker.get_slot('entity_province') == None:
         return ['entity_province']
      if tracker.get_slot('entity_major') == None:
         return ['entity_major']
      return []
      

   def before_slot_fill(self, dispatcher, tracker, domain):
      try:
         # utter universities fited with current slot.
         res = self.getResponse(tracker)
         dispatcher.utter_message(res[0])
         if len(res[1]) < 30 and len(res[1]) >1:
            dispatcher.utter_message(json_message = {'data':{'table': res[1]}})
         return []
      except:
         return [AllSlotsReset()]
  

   def submit(self, dispatcher, tracker, domain):
      # reset all slot if needed
      # add utter_chao_mung
      # finish form
      # dispatcher.utter_message("active form ch???n tr?????ng")
      return [AllSlotsReset()]

   ##
   ## query db. 
   ##
   def getResponse(self, tracker):
      ### get slot
      try:
         macro_region = self.get_slot('entity_macro_region_validated')[0]
      except:
         macro_region = None
      try:
         province = self.get_slot('entity_province')[0]
      except:
         province = None
      try:
         score = self.get_slot('entity_score')[0]
         print(score)
      except:
         score = None
      try:
         combine = self.get_slot('entity_combine')[0]
      except:
         combine = None
      try:
         nganh_hoc = str(self.get_slot('entity_major')[0])
         nganh_hoc_validated = str(self.get_slot('entity_major_validated')[0])
      except:
         nganh_hoc = None
         nganh_hoc_validated = None

      if macro_region == None and province == None and score == None and combine == None and nganh_hoc == None:
         ret = db.universities.find({})
         mes = """Hi???n c??? n?????c c?? t???t c??? {} tr?????ng ?????i h???c.""".format(ret.count())
         list = []
         for entry in ret:
            list.append([entry['name']])
         return (mes, list)
      #gen query
      query = {}
      # dataScore=db.universities.find({})
      # query={}
      # for data in dataScore:
      #    try:
      #       dataMajor=db.addmission_scores.find({"university_id":data['abbreviation']})
      #       for datamajor in dataMajor:
      #          if datamajor['year']=="2018" or datamajor['year']=="2019" :
      #             intId=int(datamajor['majors_id'])
      #             strId=str(datamajor['majors_id'])
      #             i=0
      #             while i < len(data["majors"]):
      #                if data["majors"][i]["major_id"]==intId or data["majors"][i]["major_id"]==strId:
      #                   db.universities.update(
      #                      {"abbreviation":data['abbreviation']},
      #                      {'$set':{"majors."+str(i)+".score":datamajor['score']}}
      #                   )
      #                i=i+1
      #    except:
      #       print("error edit data")
      if province != None:
         query['province'] = province
      elif macro_region != None:
         query["macro_region"] = macro_region.title()
      if score != None:
         if not "majors" in query:
            query["majors"] = {}
         if not '$elemMatch' in query["majors"]:
            query["majors"]['$elemMatch'] = {}
         query["majors"]['$elemMatch']['score'] =  { '$gte': float(score) - 2, '$lt': float(score) + 2 }
      
      if nganh_hoc != None:
         if not "majors" in query:
            query["majors"] = {}
         if not '$elemMatch' in query["majors"]:
            query["majors"]['$elemMatch'] = {}
         query["majors"]['$elemMatch']['major_id'] = nganh_hoc_validated      
      data = db.universities.find(query)
      print(query)
      # for test in data:
      #    print(test['name'])
      #gen answer
      ret = []
      ret.append(["tr?????ng", "ng??nh"])
      numOfUni = 0
      for uni in data:
         try:
            numOfUni += 1
            for major in uni['majors']:
                  if nganh_hoc is not None and major['major_id'] != nganh_hoc_validated:
                     # print(uni['name'] + ' break 1')
                     continue
                  if score is not None and float(score)-2 > float(major['score']) and float(score) +2 < float(major['score']):
                     # print(uni['name'] + ' break 2')
                     continue
                  # if combine is not None and combine not in major['major_combine']:
                  #    # print(uni['name'] + ' break 3')
                  #    continue
                  ret.append([uni['name'], major['major_name']])
         except:
            print("vukihai: error while create response: FormChonTruong > getResponse > has majorslot")          
      mes =""
      if province != None:
         mes += "T???i " + province + " c?? "
      elif macro_region != None:
         mes += "??? mi???n " + macro_region + " c?? "
      else:
         mes += "Hi???n c??? n?????c c?? "
      mes += str(numOfUni) + " tr?????ng"
      if nganh_hoc is not None:
         mes += " ????o t???o " + nganh_hoc
      if score is not None:
         mes += " ph?? h???p v???i m???c ??i???m c???a b???n"
      print(query)

      if len(ret) == 1:
         mes = "T??i kh??ng t??m ???????c k???t qu??? n??o ph?? h???p v???i b???n c??? :("
      return (mes, ret)

      



