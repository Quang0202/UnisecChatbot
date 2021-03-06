from rasa_sdk import Action
from .UnisecForm import UnisecForm
from .UnisecValidator import UnisecValidator
from typing import Any, Text, Dict, List, Union
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered, FollowupAction
import pymongo
import re

client = pymongo.MongoClient("localhost", 27017)
db = client["unisec-db"]


class FormAdmissionScore(UnisecForm):
    def name(self):
        return "form_admission_score"

    @staticmethod
    def required_validation_slot():
        return ['entity_university', 'entity_major', 'entity_year']

    def required_slots(self, tracker):
        # if tracker.get_slot('entity_university') == None:
        #    return ['entity_university']
        if tracker.get_slot('entity_university')==None:
            return ['entity_university']
        if tracker.get_slot('entity_major')==None:
            return['entity_major']
        return[]

    # def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
    #     """A dictionary to map required slots to
    #         - an extracted entity
    #         - intent: value pairs
    #         - a whole message
    #         or a list of them, where a first match will be picked"""
    #
    #     return {
    #         "entity_university": [
    #             self.from_entity(entity="entity_university", intent=["intent_admission_score", "inform"])],
    #         "entity_major": [
    #             self.from_entity(entity="entity_major", intent=["intent_admission_score", "inform"])],
    #         "entity_year": [
    #             self.from_entity(entity="entity_year", intent=["intent_admission_score", "inform"])],
    #     }

    def before_slot_fill(self, dispatcher, tracker, domain):
        # utter universities fited with current slot.
        university = tracker.get_slot('entity_university')
        major = tracker.get_slot('entity_major')
        if university == None and major == None:
            return []
        res = self.getResponse()
        dispatcher.utter_message(res[0])
        if len(res[1]) > 1:
            dispatcher.utter_message(json_message={"data": {"table": res[1]}})
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
            university_validated = self.get_slot('entity_university_validated')[0]
        except:
            university = None
            university_validated = None
        try:
            major = self.get_slot('entity_major')[0]
            major_validated = self.get_slot('entity_major_validated')[0]
        except:
            major = None
            major_validated = None
        mes = "Sau ????y l?? ??i???m chu???n"
        query = {}
        if university_validated != None:
            query['university_id'] =university_validated
            mes += " tr?????ng " + university
        if major_validated != None:
            major_validated_int = int(major_validated)
            query['majors_id'] = {'$in': [major_validated_int, major_validated]}
            mes += " ng??nh " + major
        ret = []
        ret.append(["n??m", "tr?????ng", "ng??nh h???c", "??i???m", "t??? h???p m??n"])
        if (university_validated != None and major_validated != None):
            # query['year'] = str(year_validated)
            # mes += " n??m " + str(year_validated)
            print(query)
            data = db.addmission_scores.find(query)
            for entry in data:
                try:
                    print(entry['university'])
                    ret.append([entry['year'], entry['university'], entry['major_name'], entry['score'], entry['combine']])
                except:
                    print("vukihai:error while loading admision score: FormHoiDiemChuan - get response")
            if len(ret) == 1:
                mes = "Ti???c qu??, t??i kh??ng t??m th???y th??ng tin ??i???m chu???n"
            print(ret)
        # else:
        #     query['year'] = str(year_validated)
        #     mes += " n??m " + str(year_validated)
        #     data = db.admission_scores.find(query)
        #     ret = []
        #     ret.append(["tr?????ng", "ng??nh h???c", "??i???m", "t??? h???p m??n"])
        #     for entry in data:
        #         try:
        #             ret.append([entry['university'], entry['major_name'], entry['score'], entry['combine']])
        #         except:
        #             print("vukihai:error while loading admision score: FormHoiDiemChuan - get response")
        #     print(query)
        return (mes, ret)