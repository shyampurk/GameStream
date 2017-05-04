# Gamestream 

# Cloudant DB creation.
<br>

Step 1 : Login to the Bluemix account with the valid credentials.<br>
Step 2 : Goto Catalog and under Data & Analytics select Cloudant NoSQL DB.<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/cloudantdb/cl1.png)
Step 3 : Give a name to the Service.<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/cloudantdb/cl2.png)
Step 4 : Scroll down in the same page and Select the Free plan and click on the Create button.<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/cloudantdb/cl3.png)
Step 5 : After you create the service open it and click on the Service credentials and click on the New credentials and save those credentials.
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/cloudantdb/cl4.png)
Step 6 : After you got the credentials click on the Manage from the menu and select LAUNCH button.<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/cloudantdb/cl5.png)
Step 7 : Click on the Create Database and Give a name for the Database then click on the Create button.<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/cloudantdb/cl6.png)
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/cloudantdb/cl7.png)


# Open whisk creation

Step 1 : Login to the Bluemix account with valid credentials.<br>
Step 2 : Goto catalog and under Apps select OpenWhisk.<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/openwhisk/op1.png)
Step 3 : Click on the Develop in your Browser.<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/openwhisk/op2.png)
Step 4 : Click on the Create an Action button to create new action.<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/openwhisk/op3.png)
Step 5 : Give a name to the action and select Nodejs Runtime,Select a blank to start with and then click on the Create Action button.<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/openwhisk/op4.png)
Step 6 : Copy the [code](https://github.com/shyampurk/Gamestream/blob/master/openwhisk/main.js) and paste in the code area in the newly created action then click on the Make it live to update the action. <br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/openwhisk/op5.png)
<br>To Test the newly created openwhisk action.<br> 
Step 7 : Click on the Run this Action.<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/openwhisk/op6.png)
Step 8 :  Give the following the JSON input area<br>
	{<br>
		"team":"Cleveland Cavaliers"<br>
	}<br>
and click on Run with this value.
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/openwhisk/op7.png)
Step 9 : You can see the result.<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/openwhisk/op8.png)
<br> To invoke this openwhisk action through a REST call.<br> 
Step 10 : Click on the view REST Endpoint.<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/openwhisk/op9.png)
Step 11 : Copy this cURL command, save the Authorization and URL.<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/openwhisk/op10.png)
Step 12 : Paste this Authorization in the [code](https://github.com/shyampurk/Gamestream/blob/master/Block/main.js) in line number 10, and URL in the line number 48.


# Gamesimulation code
Steps you should follow before running the Gamesimulation program.

Step 1 : pip install pubnub==3.8.3 <br>
Step 2 : pip install cloudant (https://github.com/cloudant/python-cloudant)<br>
Step 3 : From the above Step 5 Under the section "Cloudant DB creation", Enter the respective credentials in the
[code](https://github.com/shyampurk/Gamestream/blob/master/Gamesimulation/gamesimulation.py)

USERNAME  - line number 233 <br>
PASSWORD - line number 234 <br>
ACCOUNT_NAME - line number 235 <br>

Step 4 : Get the saved PubNub publish subscribe keys from the step 4 under Pubnub block creation from 
[readme](https://github.com/shyampurk/Gamestream/blob/master/Block/readme.md) and Enter those keys in the [code](https://github.com/shyampurk/Gamestream/blob/master/Gamesimulation/gamesimulation.py)
pub_key - line number 239 <br>
sub_key - line number 240 <br>


# Openwhisk code
Steps you should follow before running the openwhisk program.

Step 1 : From the above step 5 under "Cloudant db creation" section , out of those saved credentials Enter the url in the [code](https://github.com/shyampurk/Gamestream/blob/master/Openwhisk/main.js) 

url of the cloudant db - line number 5.<br>


# UI code
Steps you should follow before running the scoreboardUI program

Step 1 : Get the saved PubNub publish subscribe keys from the step 4 under "Pubnub block creation" from 
[readme](https://github.com/shyampurk/Gamestream/blob/master/Block/readme.md) and Enter those keys in the [code](https://github.com/shyampurk/GameStream/blob/master/UI/ScoreboardUI.py)

pub_key - line number 252 <br>
sub_key - line number 253 <br>

	
