# Profitops_Internship
<h1>MongoDB plugin</h1>

<h2>Installation on local HPCC Cluster</h2>
1.Install HPCC Platform,Client Tools for Linux(9.4.10 or higher current version).

2.Install the MongoDB embed for ur distribution from-( https://github.com/hpcc-systems/HPCC-Platform/releases/tag/community_9.4.10-1)
Make sure this is done after platform is installed.(sudo dpkg -i ./hpccsystems-plugin-mongodbembem_<version>.deb)

If overwrite error-
sudo dpkg -P <package-name>
sudo dpkg -i --force-overwrite <file-path>
sudo apt-get --fix-broken install
This will provide warnings but will fix the overwrite issues.

3.Avoid version mismatch .Ensure the presence of shared object file "libmongodbembed.so" in /HPCCSystems/Plugins

4.Can start the HPCC localhost:8010/ cluster using /etc/init.d/hpcc-init start(stop/restart can also be done).
Ensure 'OK'  for all servers.

5.Make sure the cluster is started after mongodb plugin installation or restart .(Open ECL watch to confirm, be in Root).

6.Test the code in VS Code/ECL IDE to ensure the mongodb plugin is working.






<h2>changestreams.ecl file</h2>

1.Unfortunately the MongoDB Plugin does'nt support the change streams feature yet, so we have embedded the python code in an ecl file which performs the same task.
We have raised this issue with the folks at LexisNexis.

2.Change streams is a feature native to MongoDb and is not limited to python.It can be impented through other languages and frameworks such as Node.js,php,motor,ruby etc.

3.It isnt compulsory to run the change streams in ecl.It can also be run independently as a python script .Also it is not compulsory for the change streams to be running on the HPCC cluster as an ecl job.It can run on anymachine as long as it is connected to the database.
For more info on changeStreams-(https://www.mongodb.com/docs/manual/changeStreams/#open-a-change-stream)





<h2>display.ecl file</h2>

*This display.ecl file connects to the MongoDB cluster , a RECORD structure has been created for a specific data schema , which is then sprayed onto the HPCC Cluster through the OUTPUT where the scope of Logical File has been mentioned .
*OVERWRITE helps to spray the latest versions of documents from the HistoryVersion Collection in MongoDB database.
*The HistoryVersion Collection contains the JSON documents with additional fields whenever new modifications has occured in the MyCollection Collection , where the change streams is watching for changes like insertion, deletion and updation.
