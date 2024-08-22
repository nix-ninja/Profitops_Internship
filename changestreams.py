'''
This python program is an implementation of mongodb changestreams .It reads all the insert,update anddelete operations and creats history documents in anothe database.
'''
from pymongo import MongoClient
Connection_string=''mongodb+srv://<user>:<pwd>@cluster0.smthng.mongodb.net/'    #connection string for atlas cluster containing user and password
client = MongoClient(Connection_string)                       #initialising the mongoClient

#these variables are used to choose the concerd db's and collection
mainDatabase='mydb'                               #enter database for historization here
mainCollection='myCollection'                   #enter the collection within the main database
history_db='historydb'                           #enter the database within which history will be stored
history_Collection='historyVersion'                 #collection within which histor is to be stored 



maindb=client[mainDatabase]         
Collection =maindb[mainCollection]    
historydb=client[history_db]
historyCollection=historydb[history_Collection]

#Function which verifies if a document with a particular objectid exists,Returns boolean
def doc_is_exist(objectid):
    doc=historyCollection.find_one({'_id':objectid})
    if doc:
        return True
    else:
        return False


pipeline=maindb.watch()          #command for implementation of  change streams,returns an iterator object which returns changes occuring in the database in realtime
#the code below is a layer over the changestreams which reads the dictionaries and adds all the versions to the history db.This structure can be modified
for change in pipeline:      # change is a python dictinary
    print(change)    
    if(change['operationType']=='insert'):          #detecting an insert operation
        data=change['fullDocument']
        data['version']=1                           #version key added to the dictionary
        
        result=historyCollection.insert_one(data)      #history document inserted in the  history Collection
        print(f'the id of the doc is:{result.inserted_id}')

    elif(change['operationType']=='update'):        #detecting update operation update  
        id=change['documentKey']['_id']            #fetching id of the document
        if(doc_is_exist(id)):                      #verifying if the history doc exists in the history collection for the doc that was updated
            doc=historyCollection.find_one({'_id':id})        #fetching the history doc of the updated document
            doc['version']+=1                                  #incrementing the version by 1
            #add the new version info to the history document  and replacing the old document
            currentVersion=doc['version']
            updateFieldName='v'+str(currentVersion)
            doc[updateFieldName]=change['updateDescription']
            doc[updateFieldName]['operation']='update'
            data=doc
            result=historyCollection.replace_one({'_id':id},data)
            print(f'the id of the doc is:{result.upserted_id}')
        else:
            print("continuity error ,history for this document couldnt be recorded")
    

    elif(change['operationType']=='delete'):              #detecting delete operation
        id=change['documentKey']['_id']                    #fetching the id of the dovument from the dictionary
        doc=historyCollection.find_one({'_id':id})          #fetching the history doc from the history collection
        print(doc)
        doc['version']+=1                                    #Increasing the version by 1 
        currentVersion=doc['version']
        #creating the version field in the history doc and updating the history doc
        deleteFieldName='v'+str(currentVersion)  
        doc[deleteFieldName]={'operation':'delete'}
        result=historyCollection.replace_one({'_id':id},doc)
            


    else:
        continue



#output returned by changestrams iterator for different  database operations
'''
---insert---
{'_id': {'_data': '826566DF99000000012B022C0100296E5A10041FFFECA763BB47C8A9AFE24FAF51A0B146645F696400646566DF98788806890B4E60F70004'},
 'operationType': 'insert',
 'clusterTime': Timestamp(1701240729, 1), 
'wallTime': datetime.datetime(2023, 11, 29, 6, 52, 9, 95000), 
'fullDocument': {'_id': ObjectId('6566df98788806890b4e60f7'), 'firstname': 'sandep', 'lastname': 'vijayvergiya', 'marks': 10},
 'ns': {'db': 'mydb', 'coll': 'myCollection1'}, 
'documentKey': {'_id': ObjectId('6566df98788806890b4e60f7')}}

---delete---
{'_id': {'_data': '826566E061000000072B022C0100296E5A10041FFFECA763BB47C8A9AFE24FAF51A0B146645F696400646566A0112FC70D4A5DF5BE950004'},
 'operationType': 'delete',
 'clusterTime': Timestamp(1701240929, 7), 
'wallTime': datetime.datetime(2023, 11, 29, 6, 55, 29, 290000),
 'ns': {'db': 'mydb', 'coll': 'myCollection1'}, 
'documentKey': {'_id': ObjectId('6566a0112fc70d4a5df5be95')}}

---update---

{'_id': {'_data': '826566E0F00000000A2B022C0100296E5A10041FFFECA763BB47C8A9AFE24FAF51A0B146645F6964006465655F9D2398CA843949E0B50004'},
 'operationType': 'update',
 'clusterTime': Timestamp(1701241072, 10)
, 'wallTime': datetime.datetime(2023, 11, 29, 6, 57, 52, 590000),
 'ns': {'db': 'mydb', 'coll': 'myCollection1'},
 'documentKey': {'_id': ObjectId('65655f9d2398ca843949e0b5')}
, 'updateDescription': {'updatedFields': {'firstname': 'bansak'}, 'removedFields': [], 'truncatedArrays': []}}
'''


            
