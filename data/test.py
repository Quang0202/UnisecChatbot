# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 14:28:43 2019

@author: Huong
"""

import pymongo as pm
import pandas as pd

myMongoClient = pm.MongoClient("mongodb://localhost:27017")
myMongoDb = myMongoClient["unisec-db"]
uniCol = myMongoDb["ninu3"]


print("start insert university name & abbr")
uniDataframe = pd.read_csv("Danh_sach_truong.csv").iloc[:,1:3]
uniDict = uniDataframe.to_dict('record')

def split_combine(string1):
    string = list(string1)
    for i in range(len(string)):
        if string[i].isdigit() or string[i].isalpha():
            pass
        else:
            string[i] = ' '
    newstring = ''.join(c for c in string)
    return newstring.split()

error_list = []
for i in range(len(uniDict)):
    ok = False
    for j in range(2019, 2009, -1):
        try:
            major_file_name = uniDict[i]['abbreviation'] + "_"+ str(j)+".csv"
            df = pd.read_csv(major_file_name)
            major_id_list = df.iloc[:, 1]
            major_name = df.iloc[:,2]
            major_combine = df.iloc[:,3]
            score = df.iloc[:,4]
            major = []
            for k in range(major_id_list.size):
                m_id = ""
                m_name = ""
                m_combine = ""
                m_score = ""
                try:
                    m_id = major_id_list[k].split(": ")[1]
                except:
                    m_id = None
                try:
                    m_name = major_name[k][11:]
                except:
                    m_name = None
                try:
                    m_combine = split_combine(major_combine[k].split(': ')[1])
                except Exception as e:
                    print(e)
                    m_combine = None
                try:
                    m_score = float(score[k][5:])
                except:
                    m_score = None
                if len(m_id) > 1:
                    major.append({"major_id":m_id, "major_name":m_name, "major_combine": m_combine, "score": m_score})
            uniDict[i]["majors"] = major
            ok = True
            break
        except:
            print('err')
        if ok == True:
            break
    if ok == False:
        error_list.append(uniDict[i])
    
uniCol.insert_many(uniDict)
print(error_list)
print("finish")
