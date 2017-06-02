# GameStream 

This code is the server backend for streaming live basketball scores and stats. It is based on the IBM Bluemix service stack and PubNub BLOCKs microservice. 

Following cloud services are used

1. IBM Cloudant DB

2. IBM OpenWhisk

3. PubNub BLOCKS

To test the application we have used two python scripts 

1. [gamesimulation.py](https://github.com/shyampurk/GameStream/blob/master/Gamesimulation/gamesimulation.py) : Game simulation script that simulates a 48 minute basketball game.

2. [ScoreboardUI.py](https://github.com/shyampurk/GameStream/blob/master/UI/ScoreboardUI.py) : Terminal UI script for viewing the live score. This works only on UNIX/LINUX based terminals. WINDOWS is not supported. 

Clone this repository and follow the steps below to setup the services. 

# Service Setup



## Cloudant DB creation.
<br>

Step 1 : Login to your Bluemix account with the valid credentials.<br>
Step 2 : Goto Catalog and under "Data & Analytics" select "Cloudant NoSQL DB".<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/cloudantdb/cl1.png)
Step 3 : Give a name to the Service.<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/cloudantdb/cl2.png)
Step 4 : Scroll down in the same page and Select the Free plan and click on the Create button.<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/cloudantdb/cl3.png)
Step 5 : After you create the service open it and click on the "Service credentials" and then, click on the "New credentials" and save those credentials.
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/cloudantdb/cl4.png)
Step 6 : After you got the new credentials, click on the "Manage" from the menu and select "LAUNCH" button.<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/cloudantdb/cl5.png)
Step 7 : Click on the "Create Database" and Give a name for the Database then click on the Create button.<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/cloudantdb/cl6.png)
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/cloudantdb/cl7.png)


## OpenWhisk service creation

Step 1 : Login to your Bluemix account with valid credentials.<br>
Step 2 : Goto catalog and under "Apps", select "OpenWhisk".<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/openwhisk/op1.png)
Step 3 : Click on the "Develop in your Browser".<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/openwhisk/op2.png)
Step 4 : Click on the "Create an Action" button to create new action.<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/openwhisk/op3.png)
Step 5 : Give a name to the action and select Nodejs Runtime. Select a blank slate to start with and then click on the "Create Action" button.<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/openwhisk/op4.png)
Step 6 : Copy the [code](https://github.com/shyampurk/GameStream/blob/master/Openwhisk/main.js) and paste in the code area in the newly created action then click on "Make it live" to update the action. Update the code to point to your Cloudant DB instance (Refer sub section Openwhisk Config).
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/openwhisk/op5.png)

To Test the newly created openwhisk action.

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

To invoke this openwhisk action through a REST call.

Step 10 : Click on the view REST Endpoint.<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/openwhisk/op9.png)

Step 11 : Copy this cURL command, save the URL & Authorization parameter values from the cURL command.<br>
![alt-tag](https://github.com/shyampurk/Gamestream/blob/master/screenshots/openwhisk/op10.png)



## PubNub BLOCK Creation

Refer [Block Readme file](https://github.com/shyampurk/GameStream/blob/master/Block/README.md) for the steps to create the two BLOCKS that we have used in this application.

# Application Credentials Setup

You need to make a note of the following credentials generated from the Cloudant, OpenWhisk and PubNub services . 

1. Cloudant service credentials : Refer Step 5 Under the section "Cloudant DB creation" above.

2. OpenWhisk Authorization : Refer Step 11 under "Open whisk creation" for the generated Authorization and the url that you generated.

3. PubNub Publish and Subscribe Key : Refer Step 4 under [Pubnub block creation](https://github.com/shyampurk/Gamestream/blob/master/Block/readme.md)

Before deploying, you need to add these credentials at specific places in the application code as guided below. 

## Simulation Code Configuration
Steps you should follow before running the game simulation and UI script. 

## Python Libraries

Both the scripts depend on a few python libraries. You can install them using the pip utility.

Step 1 : pip install pubnub==3.8.3

Step 2 : pip install cloudant (https://github.com/cloudant/python-cloudant)

### Game Simulation Script config

Before running the game simulation script make sure to update the code .


1.  Edit the following variable's values as per "Cloudant service credentials" in the
[game simulation code](https://github.com/shyampurk/Gamestream/blob/master/Gamesimulation/gamesimulation.py)

USERNAME  - line number 233

PASSWORD - line number 234 

ACCOUNT_NAME - line number 235

2. Edit the following variable's values as per "PubNub Publish and Subscribe Key" 

pub_key - line number 239 

sub_key - line number 240 


### Terminal UI Script config 
Before running the UI scoreboard script make sure to update the code .

Edit the following variable's values as per "PubNub Publish and Subscribe Key" in the [UI scoreboard code](https://github.com/shyampurk/GameStream/blob/master/UI/ScoreboardUI.py)

pub_key - line number 252 

sub_key - line number 253 


## Microservice Code Configuration

Steps you should follow to update the OpenWhisk and BLOCK code before launching these services.

### Openwhisk Config


Edit the following variable's values as per "Cloudant service credentials" in the [OpenWhisk action code](https://github.com/shyampurk/Gamestream/blob/master/Openwhisk/main.js) 

url - line number 5

### BLOCK code

Edit the following variable's values as per "OpenWhisk Authorization" in the [BLOCK code](https://github.com/shyampurk/GameStream/blob/master/Block/main.js)

auth - line number 10

url - line number 48 


	
