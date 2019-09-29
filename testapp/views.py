from django.shortcuts import render
from django.http import HttpResponse
import csv
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy
from datetime import datetime, timedelta
import json
# Create your views here.

def details_on_id(request, data_id):
    path1="/home/zaid/zaid/solutions/python/thirdproject/Transaction_20180101101010.csv"
    path2="/home/zaid/zaid/solutions/python/thirdproject/ProductReference.csv"
    df1=pd.read_csv(path1)
    df2=pd.read_csv(path2)
   
    print (df1)
    print (df1,data_id)
    temp=int(data_id)
    #j = df1.to_json(orient='records')
   # print (j)
    row=df1.loc[df1.transactionId == temp]
    prodId=int(row[" productId"].values[0])
    row2=df2.loc[df2.productId ==prodId]
    json_row=row.to_json(orient='records')
    #print (json_row)
    resp={row.columns[0]:row["transactionId"].values[0],row2.columns[1]:row2[" productName"].values[0],row.columns[2]:row[" transactionAmount"].values[0],row.columns[3]:row["transactionDatetime"].values[0]}
 
    return HttpResponse("%s" %resp)
    #return  HttpResponse("<h1>HEY! Welcome to Edureka! %s </h1>" % data_id)
#df1['transactionDatetime']=pd.to_datetime(df1['transactionDatetime'])//changing type of column to datetime


def transactionSummaryByProducts(request,days):
    path1="/home/zaid/zaid/solutions/python/thirdproject/Transaction_20180101101010.csv"
    path2="/home/zaid/zaid/solutions/python/thirdproject/ProductReference.csv"
    
    df1=pd.read_csv(path1)
    df2=pd.read_csv(path2)
    df1.columns = df1.columns.str.replace(' ', '')  #remove blank space from column name
    df2.columns = df2.columns.str.replace(' ', '')
    df1['transactionDatetime']=pd.to_datetime(df1['transactionDatetime']) #changing type of column to datetime

    date_before_Ndays = datetime.now() - timedelta(days=int(days))
    response = df1.loc[df1.transactionDatetime >= date_before_Ndays]
    print (response)
    #x=df1["transactionId"].tolist()
    
    total_amt=[]
    
    for pId in df2["productId"].tolist():
        sum=0
        trans=response.loc[response.productId == pId]
        for amt in trans["transactionAmount"].tolist():
            sum+=amt
        total_amt.append(sum)
    product_name=[]
    for pName in df2["productName"].tolist():
        product_name.append(pName)
    print (total_amt)
    print (product_name)
    jsonList=[]
    for i in range(0,len(product_name)):
        jsonList.append({"productName":product_name[i],"totalAmount":total_amt[i]})
    print (jsonList)
    print ({"summary":jsonList})
    output={"summary":jsonList}
    print(json.dumps(jsonList, indent = 1))
    return HttpResponse("%s"%output)




def transactionSummaryByManufacturingCity(request,days):
    
    path1="/home/zaid/zaid/solutions/python/thirdproject/Transaction_20180101101010.csv"
    path2="/home/zaid/zaid/solutions/python/thirdproject/ProductReference.csv"
    
    df1=pd.read_csv(path1)
    df2=pd.read_csv(path2)
    df1.columns = df1.columns.str.replace(' ', '')  #remove blank space from column name
    df2.columns = df2.columns.str.replace(' ', '')
    df1['transactionDatetime']=pd.to_datetime(df1['transactionDatetime']) #changing type of column to datetime

    date_before_Ndays = datetime.now() - timedelta(days=int(days))
    response = df1.loc[df1.transactionDatetime >= date_before_Ndays]
    print (response)
    #x=df1["transactionId"].tolist()
    
    
    total_amt1=[]
    
    
    
    city_name=[]
    for cityName in df2["productManufacturingCity"].tolist():
        city_name.append(cityName)



    print ("-----------------------------------------------------------------")
    cityName_set=set(city_name)
    for i in cityName_set:
        product_ref=df2.loc[df2.productManufacturingCity == i]
        sum1=0
        for product_id in product_ref["productId"].tolist():
            transaction=response.loc[response.productId == product_id]
            #print(transaction)
            for amt in transaction["transactionAmount"].tolist():
                sum1 += amt
        total_amt1.append(sum1)
        print (sum1)

    jsonList=[]
    city_name=list(cityName_set)
    for i in range(0,len(city_name)):
        jsonList.append({"cityName":city_name[i],"totalAmount":total_amt1[i]})
   


    print (jsonList)
    print ({"summary":jsonList})
    output={"summary":jsonList}
    print(json.dumps(jsonList, indent = 1))
    return HttpResponse("%s"%output)