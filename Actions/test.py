import pandas as pd

majorDataframe = pd.read_csv('khoi_lookup.csv')

f = open("combie.txt", "a", encoding="utf-8")
list_uni=[]
list_uni=majorDataframe.iloc[:,1]
for uni in list_uni:
    f.write(uni+'\n')
f.close()