import random
import time
import datetime

from pubnub import Pubnub
from cloudant.client import Cloudant

def error(message):
    print("ERROR : " + str(message))
def connect(message):
	print("CONNECTED")
def reconnect(message):
    print("RECONNECTED")
def disconnect(message):
    print("DISCONNECTED")




USERNAME = 'ada1d5dc-2d9c-4bdb-8098-eb1814bea372-bluemix'
PASSWORD = '138917f496921df5a30bf85f79d9d37315df23ace5f456a48b47998b4f8ca23e'
ACCOUNT_NAME = 'ada1d5dc-2d9c-4bdb-8098-eb1814bea372-bluemix'

pub_key = 'pub-c-578b72c9-0ca2-4429-b7d4-313bbdf9b335'
sub_key = 'sub-c-471f5e36-e1ef-11e6-ac69-0619f8945a4f'


pubnub = Pubnub(publish_key=pub_key,subscribe_key=sub_key) 

client = Cloudant(USERNAME, PASSWORD, account=ACCOUNT_NAME, connect=True)
session = client.session()
# print 'Username: {0}'.format(session['userCtx']['name'])
# print 'Databases: {0}'.format(client.all_dbs())

# Open an existing database
my_database = client['gameplaystats']


'''
	The Game Duration is 48 secs
	we have to update the live score every one sec
	and dashdb at the end of the game
	two blocks GamePlayLive,GamePlayStats

'''


		
# gamestartingtime = datetime.datetime.now()
# gameendingtime = datetime.datetime.now()+timedelta(seconds=48)
i = 0
HomeScore = 0
GuestScore = 0
# print gamestartingtime,gameendingtime

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

hometeamselect = random.choice([0,1])
guestteamselect = hometeamselect^1
Home = Teams.keys()[hometeamselect]
Guest = Teams.keys()[guestteamselect]	

# Home = Teams.keys()[0]
# Guest = Teams.keys()[1]	

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


while (i<=20):	
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
	
	pubnub.publish(channel = 'Gameplaylive',message = message)
		
	i+=1
	time.sleep(1)

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
else:
	print "OOPS !! MATCH DRAWN"
# else:
# 	statsdict[Guest] = {"_id":str(datetime.datetime.now()),
# 	"Game":1,
# 	"Team":Guest,
# 	"Totalscore":GuestScore,
# 	"Minutesplayed":48,
# 	"Win":1,
# 	"Loss":0
# 	}
# 	statsdict[Home] = {"_id":str(datetime.datetime.now()),
# 	"Game":1,
# 	"Team":Home,
# 	"Totalscore":HomeScore,
# 	"Minutesplayed":48,
# 	"Win":0,
# 	"Loss":1
# 	}

if statsdict[Home]["Win"] == 1:
	teamwon = Home
else:
	teamwon = Guest

pubnub.publish(channel = 'Gameplaylive',message = {"message":{"Live":"No","Result":""+teamwon+" Won the Game"}})


	
	
for val in statsdict.keys():
	# Create a document using the Database API
	print statsdict[val]
	my_document = my_database.create_document(statsdict[val])

	# Check that the document exists in the database
	if my_document.exists():
	    print 'SUCCESS!!'






























# ind =  Teams[SelectedTeam].index(SelectedPlayer)

# TempPlayerList = Teams[SelectedTeam]

# del TempPlayerList[ind]
# AssistPlayer =  random.choice(TempPlayerList)
# # print AssistPlayer

# FieldGoalAttempts = random.choice([1,2,3])
# # print FieldGoalAttempts


# selectedteamindex = Teams.keys().index(SelectedTeam)

# if selectedteamindex == 1:
# 	oppTeam = Teams.keys()[0]
# else:
# 	oppTeam = Teams.keys()[1]

# print oppTeam		

# oppPlayer = random.sample(Teams[oppTeam],FieldGoalAttempts)
# print oppPlayer


# d = dashDB()
# d.dashDB_Init()
# v = d.dBFetchall('XXX')
# print v

# curl --user "dash9765:0XswM$-bBtJ0" -X GET "http://dashdb-entry-yp-dal09-08.services.dal.bluemix.net:50000/dashdb-api/home"


# curl --user "dash9765:0XswM$-bBtJ0" -H "Content-Type: multipart/form-data" -X GET "http://dashdb-entry-yp-dal09-08.services.dal.bluemix.net:8443/dashdb-api/load/DASH9765.GAMEPLAYSTATS"

 
# curl --user "dash9765:0XswMbBtJ0" -H "Content-Type: multipart/form-data" -X POST -F loadFile1=@"/home/rajeev/WORK/openWhisk/dummydata.csv" "https://dashdb-entry-yp-dal09-08.services.dal.bluemix.net:50000/dashdb-api/load/DASH9765.GAMEPLAYSTATS?hasHeaderRow=true"
# 0XswM$-bBtJ0
