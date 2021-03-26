from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered, FollowupAction
import pymongo
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing,metrics,linear_model,svm,naive_bayes,ensemble
from sklearn.neighbors import KNeighborsClassifier
import joblib
from pyvi import ViTokenizer
import heapq
client = pymongo.MongoClient("localhost", 27017)
db = client["unisec_chatbot"]

class FormFindMajor(FormAction):

    def name(self):
        return "form_find_major"

    def required_slots(self, tracker):
        return ["concern", "skill", "criterion", "workspace"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "concern": [
                self.from_text()],
            "skill": [
               self.from_text()],
            "criterion": [
                self.from_text()],
            "workspace": [
                self.from_text()],
        }

    def submit(self, dispatcher, tracker, domain):
        # dispatcher.utter_message("Tính năng đang phát triển :v")
        # dispatcher.utter_message("slot concern : "+str(tracker.get_slot("concern")))
        # dispatcher.utter_message("slot skill : "+str(tracker.get_slot("skill")))
        # dispatcher.utter_message("slot criterion : "+str(tracker.get_slot("criterion")))
        # dispatcher.utter_message("slot workspace : "+str(tracker.get_slot("workspace")))

        input = str(tracker.get_slot("concern")) + ', ' + str(tracker.get_slot("skill")) + ', ' + str(
            tracker.get_slot("criterion")) + ', ' + str(tracker.get_slot("workspace"))

        model = joblib.load('Actions/model.pkl')
        tfidf_vect = joblib.load('Actions/tfidf_vect.pkl')
        encoder = joblib.load('Actions/encoder.pkl')

        token = ViTokenizer.tokenize(input)
        x_test = tfidf_vect.transform([token])
        proba = model.predict_proba(x_test)[0]

        label = model.predict(x_test)
        print(encoder.inverse_transform(label)[0])

        pos = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        res = heapq.nlargest(3, zip(proba, pos))
        mes = "Các ngành học phù hợp với bạn là : "
        counter = 0
        for major in res:
            print(major)
            counter += 1
            if counter == 3:
                mes = mes + encoder.inverse_transform([major[1]])[0]
            else:
                mes = mes + encoder.inverse_transform([major[1]])[0] + ', '
        dispatcher.utter_message(mes)
        dispatcher.utter_message("Hope it help :3")
        return []
