## Import 
from requests import Session
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep import Client
from zeep.transports import Transport

session = Session()
session.auth = HTTPBasicAuth('username', 'passwd')
client = Client('https://xxxxxxxxxxx.php?wsdl',
    transport=Transport(session=session))
#Get Event Data
VehicleList = client.service.getClassData()


from zeep import helpers 
import pandas as pd 
pyl = helpers.serialize_object(VehicleList)

df = pd.DataFrame(pyl)
df


ClassList = client.service.getClassData()

pyl = helpers.serialize_object(ClassList)

df = pd.DataFrame(pyl)

classdata= df['code'].apply(pd.Series)

#print(len(classdata))
class_vehicle=[]

for i in range(len(classdata)):
    #print(classdata.iloc[i,0])
    VehicleList = client.service.getVehicleData(classdata.iloc[i,0])
    pyl = helpers.serialize_object(VehicleList)
    df = pd.DataFrame(pyl)
    df['class_name']= pd.Series(classdata.iloc[i,0], index=df.index)
    #print(df['name'])
    class_vehicle.append(df[['name', 'class_name']])
    
    
appended_df = pd.concat(class_vehicle, axis=0)

print(appended_df)



StartTime='2017-07-01 00:00:00'
EndTime='2017-07-31 23:59:59'

EventList=['Low_Voltage_Event_1000', 'Low_Voltage_Event_1150', 'Low_Voltage_Event_1350']

EventData=[]

for i in range(len(appended_df)):
    VehicleName = appended_df.iloc[i,0]
    #print(VehicleName)
    ClassName = appended_df.iloc[i,1]
    #print(ClassName)
    
    for Event in EventList:    
        result = client.service.getEventData(ClassName, VehicleName, StartTime, 
                                   EndTime, Event, "", "")
    
        pyl = helpers.serialize_object(result)
        df = pd.DataFrame(pyl)
        EventData.append(df)


df = pd.concat(EventData, axis=0)
df


df1= df['location'].apply(pd.Series)
df1

final_df = pd.concat([df, df1], axis=1).drop('location', axis=1)
final_df 

final_df['start_time'] = pd.to_datetime(final_df['start_time'])
final_df['end_time'] = pd.to_datetime(final_df['end_time'])
final_df.dtypes
final_df.to_csv("RCM_All_Low_Volatge_Event_July2017.CSV", sep=',', encoding='utf-8', date_format='%Y-%m-%d %H:%M:%S')
