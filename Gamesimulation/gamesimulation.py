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

'''****************************************************************************************
Function Name 	:connect
Description		:	Responds if server connects with pubnub
Parameters 		:	message
****************************************************************************************'''
def connect(message):
    print("CONNECTED")



'''
	The Game Duration is 48 secs
	we update the live score every one sec
'''		

'''****************************************************************************************
Function Name 	:   scorepublish
Description		:	Function will publish the live score to the score board
Parameters 		:	Home       - Team that selected as Home team
					Guest      - Team that selected as Guest team
					HomeScore  - Score of the Home team
					GuestScore - Score of the Guest team
					i          - Time(in secs)
****************************************************************************************'''
def scorepublish(Home,Guest,HomeScore,GuestScore,i):
	# Message format to the score board
	message = {"message":{
		"Timer":"00:"+str(i),
		"Home":Home,
		"Guest":Guest,
		"HomeScore":str(HomeScore),
		"GuestScore":str(GuestScore),
		"Live":"Yes"

	}}

	print message
	# publishing message to scoreboard
	pubnub.publish(channel = scoreboardlivepubchannel,message = message)


'''****************************************************************************************
Function Name 	:	gamesimulation
Description		:	Function simulates the basket ball game scenario
Parameters 		:	None
****************************************************************************************'''
def gamesimulation():
	try:
		# Initializing the variables
		i = 0
		HomeScore = 0 #Home team score
		GuestScore = 0 #Guest team score
		gameduration = 48 # duration of the game

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
		# Out of two teams selecting one as Home and other as Guest team randomly.
		hometeamselect = random.choice([0,1])
		guestteamselect = hometeamselect^1
		Home = Teams.keys()[hometeamselect]
		Guest = Teams.keys()[guestteamselect]	

		
		# simulation will run for gameduration(defined above) time 
		while (i<=gameduration):
			# Simulation process generating the points
			# Basket ball game possible point structure. 
			PointType = {'2P':2,'3P':3}
			# Selecting a random team to score the goal
			SelectedTeam = random.choice(Teams.keys())
			# Selecting a random point from the possible points
			SelectedPoint = random.choice(PointType.keys())
			point = PointType[SelectedPoint]
			# Assiging score to the respective team
			if SelectedTeam == Home:
				HomeScore+=point
			if SelectedTeam == Guest:
				GuestScore+=point

			# calling scorepublish function to send the score to the live scor board 
			scorepublish(Home,Guest,HomeScore,GuestScore,i)	
				
			i+=1
			time.sleep(1)
		# calling cloudant_update function to store the game score details 
		cloudantdb_update(HomeScore,GuestScore,Home,Guest)	
	except Exception as e:
		print e,"Error in gamesimulation"		

'''****************************************************************************************
Function Name 	:	cloudantdb_update
Description		:	function to store the game score details
Parameters 		:	HomeScore  - Score of the Home team 
					GuestScore - Score of the Guest team
					Home       - Team that selected as Home team
					Guest      - Team that selected as Guest team
****************************************************************************************'''
def cloudantdb_update(HomeScore,GuestScore,Home,Guest):	

	# sending game stats to cloudantdb

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

	# Incase if scores becomes equal in the random score simulation
	# We will give extra points for randomly selected time
	# creating the extra time scenario. 
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

if __name__ == '__main__':
	# Cloudant DB credentials
	# Modify the three variables below to update the Cloudant DB credentials
	USERNAME = 'ada1d5dc-2d9c-4bdb-8098-eb1814bea372-bluemix'
	PASSWORD = '138917f496921df5a30bf85f79d9d37315df23ace5f456a48b47998b4f8ca23e'
	ACCOUNT_NAME = 'ada1d5dc-2d9c-4bdb-8098-eb1814bea372-bluemix'

	# Pubnub publish subscribe credentials
	# Modify the two variables below to update the PubNub credentials
	pub_key = 'pub-c-dd56bf78-3a88-4f6a-a7a4-c1b078b82bf6'
	sub_key = 'sub-c-266f139a-29c3-11e7-a9ec-0619f8945a4f'
	scoreboardlivepubchannel = 'Gameplaylive'

	# Initialisation of pubnub
	pubnub = Pubnub(publish_key=pub_key,subscribe_key=sub_key) 
	# Initialisation of cloudantdb
	client = Cloudant(USERNAME, PASSWORD, account=ACCOUNT_NAME, connect=True)
	session = client.session()

	# Open an existing database
	database_name = 'gameplaystats'
	my_database = client[database_name]
	# calling gamesimulation function
	gamesimulation()
