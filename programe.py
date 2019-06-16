#!usr/bin/python3.6
#!encoding:utf_8
import numpy as np 
import matplotlib.pyplot
import pandas as pd
from math import ceil 

from sklearn.ensemble import RandomForestClassifier
df=pd.read_csv('customer_data.csv')
x=df[['Periodicity','total_amount','Recency','threshold_annulation']]
y=df['clusters']
rf=RandomForestClassifier(n_estimators=40,max_features=3)
rf.fit(x,y)
fichier=input("Entrer le nom de fichier contenant la séquence temporelle du client.")

if fichier[-3:]=='csv':
    data=pd.read_csv(fichier)
else:
    data=pd.read_excel(fichier)
data.drop(data[(data['Quantity']<0) & (data['StockCode']=='D')].index)
data['total_amount']=data['Quantity']*data['UnitPrice']
data['purchase_amount']=[sum(data[data['InvoiceNo']==c]['total_amount']) for c in data['InvoiceNo']]
data['total_amount']=[sum(data['total_amount']) for i in range(len(data))]
data['Periodicity']=[ceil(365/len(data['InvoiceNo'].unique())) for i in range(len(data))]
month={'01':0,'02':31,'03':59,'04':80,'05':120,'06':151,'07':181,'08':212,'09':243,'10':273,'11':304,'12':334}
data['n_jour']=[month[str(c)[5:7]] + int(str(c)[8:10]) for c in data['InvoiceDate']]
data['Recency']=[365-max(data['n_jour']) for i in range(len(data))]
data['purchasing']=[1 if c>0 else 0 for c in data['purchase_amount']]
df=data[['InvoiceDate','purchase_amount','purchasing']]
df=df.drop_duplicates()
data['threshold_annulation']=[(sum(df['purchasing'])/len(df)) for i in range(len(data))]
data=data[['CustomerID','Periodicity','total_amount','Recency','threshold_annulation']]
data=data.drop_duplicates()
categ=rf.predict(data[['Periodicity','total_amount','Recency','threshold_annulation']])
print('Le client de code {}, fait partie de la catégorie {}.'.format(data['CustomerID'].iloc[0],categ))


