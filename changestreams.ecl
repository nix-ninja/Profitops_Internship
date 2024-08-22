//this ecl job runs embedeed python and is  an implementation of changestreams in an ecl job.It utilise the pymongo library.
import python3 as py;
INTEGER MAE(integer a) := EMBED(PY)
    

from pymongo import MongoClient
Connection_string='mongodb+srv://<user>:<pwd>@cluster0.smthng.mongodb.net/'
client = MongoClient(Connection_string)              # Replace with your MongoDB connection string
mainDatabase='mydb' #enter database for historization here
mainCollection='myCollection'                         #enter the collection within the main database
history_db='historydb'                                #enter the database within which history will be stored
history_Collection='historyVersion'                   #collection within which history is to be stored 



maindb=client[mainDatabase]                               #CHECK THE CHANGESTREAMS.PY FILE FOR COMMENTS AND EXPLANATIONS OF THE PYTHON CODE.
Collection =maindb[mainCollection]
historydb=client[history_db]
historyCollection=historydb[history_Collection]

def doc_is_exist(objectid):
    doc=historyCollection.find_one({'_id':objectid})
    if doc:
        return True
    else:
        return False

pipeline=maindb.watch()
for change in pipeline:
    print(change)
    if(change['operationType']=='insert'):
        data=change['fullDocument']
        data['version']=1
        
        result=historyCollection.insert_one(data)
        print(f'the id of the doc is:{result.inserted_id}')

    elif(change['operationType']=='update'):
        id=change['documentKey']['_id']
        if(doc_is_exist(id)):
            doc=historyCollection.find_one({'_id':id})
            doc['version']+=1
            currentVersion=doc['version']
            updateFieldName='v'+str(currentVersion)
            doc[updateFieldName]=change['updateDescription']
            doc[updateFieldName]['operation']='update'
            data=doc
            result=historyCollection.replace_one({'_id':id},data)
            print(f'the id of the doc is:{result.upserted_id}')
        else:
            print("continuity error ,history for this document couldnt be recorded")
    

     
    elif(change['operationType']=='delete'):
        id=change['documentKey']['_id']
        doc=historyCollection.find_one({'_id':id})
        print(doc)
        doc['version']+=1
        currentVersion=doc['version']
        currentVersion=doc['version']
        deleteFieldName='v'+str(currentVersion)
        doc[deleteFieldName]={'operation':'delete'}
        result=historyCollection.replace_one({'_id':id},doc)
         


    else:
        break


return 5   
ENDEMBED;

x:=cron('* * * * *');
mae(2):WHEN(x,count(3));

/*ONCE THE changestreams.ecl CODE IS SUBMITTED ON LOCAL HPCC CLUSTER , IT WILL BE 'RUNNING' CONTINUOUSLY(FIRST IT WILL BE AT 'WAIT') , MAKE SURE IT DOES'NT FAIL .
IF IT'S RUNNING WITHOUT ISSUES, USE THE MONGODB PLUGIN TO INSERT ,DELETE AND UPDATE DOCUMENTS .
USE THE mongodb_demo.ecl FILE TO TEST THIS.CHECK THE MONGO M0/M2/M5 CLUSTER THROUGH COMPASS /ATLAS/SHELL TO MONITOR FOR VERSION HISTORIES CREATED.
TO STOP CHANGE STREAMS, TERMINATE THE LOCAL HPCC CLUSTER AND RESTART FOR FURTHER USAGE.
*/

//THE CRON COMMAND SCHEDULES THE ECL PYTHON EMBED CODE EVERY MINUTE IN THIS CASE (REPRESENTED BY * * * * *), THIS CAN BE SEEN IN 'EVENT SCHEDULER' IN ECL WATCH.
