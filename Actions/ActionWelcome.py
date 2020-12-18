from rasa_sdk.events import SlotSet
from rasa_sdk import Action
class ActionWelcome(Action):
    def name(self):
        return "action_welcome"

    def run(self,dispatcher, tracker, domain):
        data = []
        data.append({'img':"https://searchengineland.com/figz/wp-content/seloads/2017/12/compare-seo-ss-1920-800x450.jpg", 'name': 'chọn trường', 'payload':'chọn trường'})
        # data.append({'img':"https://daihoc.fpt.edu.vn/media/2019/02/img20161006041230575.jpg", 'name': 'chọn ngành', 'payload':'chọn ngành'})
        data.append({'img':'https://newshop.vn/public/uploads/news/untitled-7.png', 'name': 'điểm chuẩn', 'payload': 'điểm chuẩn'})
        data.append({'img':'a', 'name': 'mã trường', 'payload': 'mã trường'})
        # data.append({'img':' img', 'name': 'thông tin tuyển sinh', 'payload': 'thông tin tuyển sinh'})
        data.append({'img':'https://www.wraltechwire.com/wp-content/uploads/2019/02/jobs-hiring-help-wanter.jpg', 'name': 'việc làm', 'payload': 'việc làm'})
        data.append({'img':'https://www.gannett-cdn.com/-mm-/389f33b6050a2664d0a5c4c7964c4fab0747cd63/c=0-38-2024-1181/local/-/media/2015/10/26/USATODAY/USATODAY/635814567737908846-salary.jpg?width=660&height=373&fit=crop&format=pjpg&auto=webp', 'name': 'mức lương', 'payload': 'mức lương'})
        data.append({'img':'https://englishstudyonline.org/wp-content/uploads/2019/07/School-Subjects.jpg', 'name': 'khung đào tạo', 'payload': 'khung đào tạo'})
        data.append({'img':'https://dropshipnewbie.com/wp-content/uploads/2019/07/rankings-ribbons.jpg', 'name': 'xếp hạng', 'payload': 'xếp hạng'})
        data.append({'img':'https://saigonpixel.vn/Upload/images/Blog/mapfolding_lg.gif', 'name': 'địa chỉ trường', 'payload': 'địa chỉ trường'})

        dispatcher.utter_message(json_message={"data":{"slider" : data}})
        return []