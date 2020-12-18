import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
class UnisecValidator:
    #impliment singleton
    __instance = None
    patterns = {'[àáảãạăắằẵặẳâầấậẫẩ]': 'a','[đ]': 'd','[èéẻẽẹêềếểễệ]': 'e','[ìíỉĩị]': 'i','[òóỏõọôồốổỗộơờớởỡợ]': 'o','[ùúủũụưừứửữự]': 'u','[ỳýỷỹỵ]': 'y'}
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if UnisecValidator.__instance == None:
            UnisecValidator()
        return UnisecValidator.__instance
    def __init__(self):
        if UnisecValidator.__instance != None:
            raise Exception("This class is a singleton!")
        else:  
            print("vukihai: instantiated Unisec Validator")
            self.path = os.path.abspath(os.path.dirname(__file__))
            self.loadData()
            UnisecValidator.__instance = self
    
    # load & train data once time
    def loadData(self):
        ## university name
        self.uniDataframe = pd.read_csv(self.path + '/university_lookup.csv')
        self.uniVectorizer = TfidfVectorizer(ngram_range=(1,4), analyzer='char')
        self.uniModel = self.uniVectorizer.fit_transform(self.uniDataframe.iloc[:,1])
        self.uniAbbr = self.gen_abbr_lookup(self.path + '/university_lookup.csv')
        ## region
        self.regionDataframe = pd.read_csv(self.path + '/macro_region_lookup.csv')
        self.regionVectorizer = TfidfVectorizer(ngram_range=(1,3), analyzer='char')
        self.regionModel = self.regionVectorizer.fit_transform(self.regionDataframe.iloc[:,1])

        ## majors
        self.majorDataframe = pd.read_csv(self.path + '/major_lookup.csv')
        self.majorVectorizer = TfidfVectorizer(ngram_range=(1,5), analyzer='char')
        self.majorModel = self.majorVectorizer.fit_transform(self.majorDataframe.iloc[:,1])
        self.majorAbbr = self.gen_abbr_lookup(self.path + '/major_lookup.csv')
        ## province
        self.provinceDataframe = pd.read_csv(self.path + '/province_lookup.csv')
        self.provinceVectorizer = TfidfVectorizer(ngram_range=(1,3), analyzer='char')
        self.provinceModel = self.provinceVectorizer.fit_transform(self.provinceDataframe.iloc[:,1])

        ## combine
        self.gradeDataframe = pd.read_csv(self.path + '/khoi_lookup.csv')
        self.gradeVectorizer = TfidfVectorizer(ngram_range=(1,3), analyzer='char')
        self.gradeModel = self.gradeVectorizer.fit_transform(self.gradeDataframe.iloc[:,1])

        
    def remove_vn_mark(self, text):
        output = text
        for regex, replace in self.patterns.items():
            output = re.sub(regex, replace, output)
            # deal with upper case
            output = re.sub(regex.upper(), replace.upper(), output)
        return output
    def gen_abbr_lookup(self, lookup_file):
        df = pd.read_csv(lookup_file)
        df = df.iloc[:,1]
        ans = {}
        for u in range(len(df)):
            unio = df[u]
            uni = list(unio.lower())
            for i in range(len(uni)):
                if uni[i].isdigit() or uni[i].isalpha():
                    pass
                else:
                    uni[i] = ' '
            list_str = ''.join(c for c in uni).split()

            for i in range(len(list_str)):
                pref = ''
                full = ''
                for j in range(len(list_str)):
                    if i + j < len(list_str):
                        pref += list_str[i+j][0]
                        full += list_str[i+j] + ' '
                        try:
                            ans[pref]
                        except:
                            ans[pref] = set()
                        ans[pref].add(full[:-1])
                        tvkd = self.remove_vn_mark(pref)
                        try:
                            ans[tvkd]
                        except:
                            ans[tvkd] = set()
                        ans[tvkd].add(full[:-1])
        return ans    
            
    def validate_entity_score(self, name):
        return (1, name, name)
    def validate_entity_university_id(self, name):
        return (1, name, name)
        
    def validate_entity_gender(self, name):
        return (1, name, name)
    def validate_entity_combine(self, name):
        vec = self.gradeVectorizer.transform([name])
        cos = cosine_similarity(self.gradeModel, vec)
        index = cos.argmax()
        li = list(name)
        #print(len(li))
        name = self.gradeDataframe.iloc[index,1]
        num = len(name)
        if num == 1:
            ch = name.upper() + "00"
            return (1,name,ch)
        if num == 2:
            #li = list(name)
            ch = li[0].upper() + "0" + li[1]
            return (1,name,ch)
        #li = list(name)
        ch = li[0].upper() + li[1] + li[2]
        return (1,name,ch)
        
    def validate_entity_subject(self, name):
        return (1, name, name)
    def validate_entity_year(self, name):
        return (1, name, name)
    


    # def validate_entity_vung_mien(self, name):
    #     vec = self.regionVectorizer.transform([name])
    #     cos = cosine_similarity(self.regionModel, vec)
    #     index = cos.argmax()
    #     return (cos[index][0],self.regionDataframe.iloc[index,1],self.regionDataframe.iloc[index,2])
    
    def validate_entity_province(self, name):
        vec = self.provinceVectorizer.transform([name])
        cos = cosine_similarity(self.provinceModel, vec)
        index = cos.argmax()
        return (cos[index][0],self.provinceDataframe.iloc[index,1], self.provinceDataframe.iloc[index,1])
    def validate_entity_macro_region(self, name):
        vec = self.regionVectorizer.transform([name])
        cos = cosine_similarity(self.regionModel, vec)
        index = cos.argmax()
        return (cos[index][0],self.regionDataframe.iloc[index,0],str(self.regionDataframe.iloc[index,1]))
        
    def validate_entity_univeristy_id(self, name):
        return (1,name, name)

    def validate_entity_university(self, name):
        #abbr
        list_str = name.split()
        list_abbr = self.match_abbr(list_str, self.uniAbbr, 0)
        ret = (-1, 0, 0)
        for i in list_abbr:
            vec = self.uniVectorizer.transform([i])
            cos = cosine_similarity(self.uniModel, vec)
            index = cos.argmax()
            # print((cos[index][0],i,self.uniDataframe.iloc[index,1]))
            if cos[index][0] > ret[0]:
                ret = (cos[index][0],self.uniDataframe.iloc[index,1],self.uniDataframe.iloc[index,2])
        return ret
    def validate_entity_major(self, name):
        #abbr
        list_str = name.split()
        list_abbr = self.match_abbr(list_str, self.majorAbbr, 0)
        ret = (-1, 0, 0)
        for i in list_abbr:
            vec = self.majorVectorizer.transform([i])
            cos = cosine_similarity(self.majorModel, vec)
            index = cos.argmax()
            #print((cos[index][0],i,self.majorDataframe.iloc[index,1]))
            if cos[index][0] > ret[0]:
                ret = (cos[index][0],self.majorDataframe.iloc[index,1],str(self.majorDataframe.iloc[index,2]))
        return ret

    def match_abbr(self, origin, dict, i):
        if i >= len(origin):
            return ['']

        pos = self.match_abbr( origin, dict, i+1)

        case = [origin[i]]
        if origin[i] in dict:
            for ab in dict[origin[i]]:
                case.append(ab)
        ret = []
        for c in case:
            for p in pos:
                ret.append(c+" " + p)
        return ret
        
        
# UnisecValidator.getInstance() # load & train data immediately after import
test = "học viện công nghệ bưu chính viễn thông phía Bắc"
print(UnisecValidator.getInstance().validate_entity_university(test))
