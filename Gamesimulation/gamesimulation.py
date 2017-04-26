import random
import time
import datetime

from pubnub import Pubnub
from cloudant.client import Cloudant

'''****************************************************************************************
Function Name 		:	error
Description		:	If error in the channel, prints the error
Parameters 		:	message - error message
****************************************************************************************'''
def error(message):
    print("ERROR : " + str(message))

'''****************************************************************************************
Function Name 		:	reconnect
Description		:	Responds if server connects with pubnub
Parameters 		:	message
****************************************************************************************'''
def reconnect(message):
    print("RECONNECTED")

'''****************************************************************************************
Function Name 		:	disconnect
Description		:	Responds if server disconnects from pubnub
Parameters 		:	message
****************************************************************************************'''
def disconnect(message):
    print("DISCONNECTED")


# Cloudant DB credentials
# Refer Step 3 under Gamesimulation in README file in repo root folder
USERNAME = 'ada1d5dc-2d9c-4bdb-8098-eb1814bea372-bluemix'
PASSWORD = '138917f496921df5a30bf85f79d9d37315df23ace5f456a48b47998b4f8ca23e'
ACCOUNT_NAME = 'ada1d5dc-2d9c-4bdb-8098-eb1814bea372-bluemix'

# Pubnub publish subscribe credentials
# Refer Step 4 under Gamesimulation in README file in repo root folder
pub_key = 'pub-c-578b72c9-0ca2-4429-b7d4-313bbdf9b335'
sub_key = 'sub-c-471f5e36-e1ef-11e6-ac69-0619f8945a4f'
scoreboardlivepubchannel = 'Gameplaylive'

# Initialisation of pubnub
pubnub = Pubnub(publish_key=pub_key,subscribe_key=sub_key) 
# Initialisation of cloudantdb
client = Cloudant(USERNAME, PASSWORD, account=ACCOUNT_NAME, connect=True)
session = client.session()

# Open an existing database
database_name = 'gameplaystats'
my_database = client[database_name]

'''
	The Game Duration is 48 secs
	we have to update the live score every one sec
'''
		
i = 0
HomeScore = 0
GuestScore = 0
gameduration = 5
# Team names and Team player names
Teams = {'Cleveland Cavaliers':
				[
					'Lebron James',
					'Kyrie Irving',
					'Kevin Love',
					'J.R Smith',
					'Channing Frye'
				],
			'Toronto Raptors':
				[
					'DeMar DeRozan',
					'Kyle Lowry',
					'Patrick Patterson',
					'DeMarre Carroll',
					'Cory Joseph'
				]
			}
# Randomly selecting a team 
hometeamselect = random.choice([0,1])
guestteamselect = hometeamselect^1
Home = Teams.keys()[hometeamselect]
Guest = Teams.keys()[guestteamselect]	

# Dictionary to store the Team score details
statsdict ={Home: {
		"Totalscore":0,
		"Minutesplayed":0,
		"Win":0,
		"Loss":0,
		},
		Guest:{
		"Totalscore":0,
		"Minutesplayed":0,
		"Win":0,
		"Loss":0,
		}
		}


while (i<=gameduration):
	# Simulation process generating the points 
	PointType = {'2P':2,'3P':3}
	SelectedTeam = random.choice(Teams.keys())
	SelectedPlayer = random.choice(Teams[SelectedTeam])
	SelectedPoint = random.choice(PointType.keys())
	point = PointType[SelectedPoint]

	if SelectedTeam == Home:
		HomeScore+=point
	if SelectedTeam == Guest:
		GuestScore+=point



	# Message format to the score board
	message = {"message":{
		"Timer":"00:"+str(i),
		"Home":Home,
		"Guest":Guest,
		"LastScorer":SelectedPlayer,
		"HomeScore":str(HomeScore),
		"GuestScore":str(GuestScore),
		"Live":"Yes"

	}}

	print message
	# publishing message to scoreboard
	pubnub.publish(channel = scoreboardlivepubchannel,message = message)
		
	i+=1
	time.sleep(1)



# sending game stats to cloudantdb

# Incase if scores are equal
if (HomeScore == GuestScore):
	extratimepoint = random.choice([2,3])
	extratimeteam = random.choice(Teams.keys())
	if extratimeteam == Home:
		HomeScore+=extratimepoint
	if extratimeteam == Guest:
		GuestScore+=extratimepoint

# Preparing Dictionary with the Team scores to store in the cloudant db
if (HomeScore > GuestScore):
	statsdict[Home] = {"_id":str(datetime.datetime.now()),
	"Game":1,
	"Team":Home,
	"Totalscore":HomeScore,
	"Minutesplayed":48,
	"Win":1,
	"Loss":0
	}
	statsdict[Guest] = {"_id":str(datetime.datetime.now()),
	"Game":1,
	"Team":Guest,
	"Totalscore":GuestScore,
	"Minutesplayed":48,
	"Win":0,
	"Loss":1
	}
elif(HomeScore < GuestScore):
	statsdict[Guest] = {"_id":str(datetime.datetime.now()),
	"Game":1,
	"Team":Guest,
	"Totalscore":GuestScore,
	"Minutesplayed":48,
	"Win":1,
	"Loss":0
	}
	statsdict[Home] = {"_id":str(datetime.datetime.now()),
	"Game":1,
	"Team":Home,
	"Totalscore":HomeScore,
	"Minutesplayed":48,
	"Win":0,
	"Loss":1
	}

# Sending a message live score board the Result of the match
if statsdict[Home]["Win"] == 1:
	teamwon = Home
else:
	teamwon = Guest

pubnub.publish(channel = 'Gameplaylive',message = {"message":{"Live":"No","Result":""+teamwon+" Won the Game"}})

# Pushing the data to the cloudant db
for val in statsdict.keys():
	# Create a document using the Database API
	print statsdict[val]
	my_document = my_database.create_document(statsdict[val])

	# Check that the document exists in the database
	if my_document.exists():
	    print 'SUCCESS!!'

