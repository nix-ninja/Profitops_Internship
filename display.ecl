#OPTION('obfuscateOutput', TRUE);
import MongoDB,$;
server:='cluster0.smthng.mongodb.net';
user:='user';
pwd:= 'pwd';
databaseName:='mydb';
collectionName:='myCollection1';



rec2:=RECORD
   string first;
   string last;
   decimal salary;
END;

recv2:=RECORD
   dataset(rec2) updatedFields;
   dataset(rec2) removedFields;
   dataset(rec2) truncatedArrays;
   string operation;
END;










dataset({integer id,string first,string last,integer version, dataset(recv2) v2,dataset(recv2) v3,dataset(recv2) v4}) getAll() := EMBED(mongodb : user(user), password(pwd), server(server), database('historydb'),  collection('historyVersion'))
   find({});
ENDEMBED;

sequential(
output(getAll(),,'hthor::display1',named('all_documents'),OVERWRITE);
);
