import curses
from pubnub import Pubnub
import random
import time
import sys

teams = ["Cleveland Cavaliers","Toronto Raptors"]

'''****************************************************************************************
Function Name 	:	error
Description		:	If error in the channel, prints the error
Parameters 		:	message - error message
****************************************************************************************'''
def error(message):
    print("ERROR : " + str(message))

'''****************************************************************************************
Function Name 	:	reconnect
Description		:	Responds if server connects with pubnub
Parameters 		:	message
****************************************************************************************'''
def reconnect(message):
    print("RECONNECTED")

'''****************************************************************************************
Function Name 	:	disconnect
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


'''****************************************************************************************
Function Name 	:   hide
Description		:	This function will hide the statistics text from the screen
Parameters 		:	None
****************************************************************************************'''
def hide():
	global screen
	screen.refresh()
	screen.clear()
'''****************************************************************************************
Function Name 	:   stat
Description		:	This function will help to show the statistics
Parameters 		:	None
****************************************************************************************'''
def stat():
	global screen
	screen.refresh()
	screen.addstr(scorestartpoint+13,30,"0 -Cleveland Cavaliers\n\t\t\t      1 -Toronto Raptors")
	input = screen.getstr(height-6, 2)	
	return input	
'''****************************************************************************************
Function Name 	:   stat
Description		:	This function sends the message to block to get the statistics of 
					the selected team
Parameters 		:	Team choice (either 0 or 1)
****************************************************************************************'''
def pub(r):
	global pubnub
	try:
		if int(r) in [0,1]:
			pubnub.publish(channel = statspubchannel,message = {"messagetype":"req","team":teams[int(r)]})
	except Exception as e:
		pass
	

'''****************************************************************************************
Function Name 	:   show_param_live
Description		:	This function will show the live score board on the screen
Parameters 		:	live score message from the pubnub
****************************************************************************************'''
def show_param_live(param):
	global screen
	screen.refresh()
	screen.border(0)
	screen.addstr(scorestartpoint-2,10,"LIVE SCORE BOARD")
	screen.addstr(scorestartpoint,8, "-------------------------------------------------------------")
	screen.addstr(scorestartpoint+1,8,"|")
	screen.addstr(scorestartpoint+2,8,"|")
	screen.addstr(scorestartpoint+3,8,"|")
	screen.addstr(scorestartpoint+4,8,"|")
	screen.addstr(scorestartpoint+5,8,"|")
	screen.addstr(scorestartpoint+6,8,"|")
	screen.addstr(scorestartpoint+7,8,"|")
	screen.addstr(scorestartpoint+8,8,"|")
	
	screen.addstr(scorestartpoint+1,68,"|")
	screen.addstr(scorestartpoint+2,68,"|")
	screen.addstr(scorestartpoint+3,68,"|")
	screen.addstr(scorestartpoint+4,68,"|")
	screen.addstr(scorestartpoint+5,68,"|")
	screen.addstr(scorestartpoint+6,68,"|")
	screen.addstr(scorestartpoint+7,68,"|")
	screen.addstr(scorestartpoint+8,68,"|")
	
	screen.addstr(scorestartpoint+9,8,"-------------------------------------------------------------")
	screen.addstr(scorestartpoint+1,22,"BASKET BALL GAME SEASON 2017-18")

	screen.addstr(scorestartpoint+6,10,"Home")
	screen.addstr(scorestartpoint+6,60,"Guest")
	screen.addstr(scorestartpoint+6,35,"Timer")

	''' STATISTICS '''
	# status bar
	statusbarstr = " 'q' - EXIT 's' - SHOW STATISTICS 'h' - HIDE STATISTICS"
	# status bar
	screen.addstr(height-4, 5, statusbarstr)
	# title
	title = "Basket Ball Game Simulation"
	# Rendering title
	screen.addstr(scorestartpoint-1, 50, title)
	screen.addstr(height-6, 2,"")

	

	if (param["Live"] == "Yes"): 
		screen.addstr(scorestartpoint+7,10,"")
		screen.addstr(scorestartpoint+7,60,"")
		screen.addstr(scorestartpoint+7,35,"")	
		screen.addstr(scorestartpoint+7,10,param["HomeScore"])
		screen.addstr(scorestartpoint+7,60,param["GuestScore"])
		screen.addstr(scorestartpoint+7,35,param["Timer"])
		screen.addstr(scorestartpoint+3,15,"Home Team -- " + param["Home"] )
		screen.addstr(scorestartpoint+4,15,"Guest Team -- " + param["Guest"])
		screen.addstr(height-6, 2,"")
		screen.refresh()
	if (param["Live"] == "No"):
		screen.addstr(scorestartpoint+11,27,"GAME OVER !!!!")
		screen.addstr(scorestartpoint+12,20,param["Result"])
		screen.addstr(height-6, 2,"")
		screen.refresh()

'''****************************************************************************************
Function Name 	:   show_param_stats
Description		:	This function will show the statistics on the screen
Parameters 		:	statistics message from the block
****************************************************************************************'''
def show_param_stats(param):
	global screen
	try:
		screen.clear()
		screen.border(0)	
		screen.refresh()
		screen.addstr(statsstartpoint-2,10,"STATISTICS")
		screen.addstr(statsstartpoint,8, "-------------------------------------------------------------")
		screen.addstr(statsstartpoint+1,8,"|")
		screen.addstr(statsstartpoint+2,8,"|")
		screen.addstr(statsstartpoint+3,8,"|")
		screen.addstr(statsstartpoint+4,8,"|")
		screen.addstr(statsstartpoint+5,8,"|")
		screen.addstr(statsstartpoint+6,8,"|")
		screen.addstr(statsstartpoint+7,8,"|")
		screen.addstr(statsstartpoint+8,8,"|")

		screen.addstr(statsstartpoint+1,68,"|")
		screen.addstr(statsstartpoint+2,68,"|")
		screen.addstr(statsstartpoint+3,68,"|")
		screen.addstr(statsstartpoint+4,68,"|")
		screen.addstr(statsstartpoint+5,68,"|")
		screen.addstr(statsstartpoint+6,68,"|")
		screen.addstr(statsstartpoint+7,68,"|")
		screen.addstr(statsstartpoint+8,68,"|")

		screen.addstr(statsstartpoint+9,8,"-------------------------------------------------------------")
		screen.addstr(statsstartpoint+1,18,"BASKET BALL GAME SEASON 2017-18 STATISTICS")

		screen.addstr(statsstartpoint+5,10,"Gamesplayed")
		screen.addstr(statsstartpoint+5,25,"Wins")
		screen.addstr(statsstartpoint+5,35,"Losses")
		screen.addstr(statsstartpoint+5,45,"Maxscore")
		screen.addstr(statsstartpoint+5,60,"Win%")

		''' STATISTICS '''
		# status bar
		statusbarstr = " 'q' - EXIT 's' - SHOW STATISTICS 'h' - HIDE STATISTICS"
		# status bar
		screen.addstr(height-4, 5, statusbarstr)
		# title
		title = "Basket Ball Game Simulation"
		# Rendering title
		screen.addstr(scorestartpoint-1, 50, title)
		screen.addstr(height-6, 2,"")


		screen.addstr(statsstartpoint+3,18,"TEAM   -- "+param["Team"])
		screen.addstr(statsstartpoint+7,10,str(param["PlayedGames"]))
		if type(param["Winpercentage"]) == float:
			winlosspercn = round(param["Winpercentage"],2)
		else:
			winlosspercn = param["Winpercentage"]
		screen.addstr(statsstartpoint+7,25,str(param["Win"]))
		screen.addstr(statsstartpoint+7,35,str(param["Loss"]))
		screen.addstr(statsstartpoint+7,45,str(param["Maxscore"]))
		screen.addstr(statsstartpoint+7,60,str(winlosspercn))
		screen.addstr(height-6, 2,"")	
		screen.refresh()
	except curses.error as e:
		print e	

'''****************************************************************************************
Function Name 	:   callbackLive
Description		:	This pubnub function will receive messages of the live score
Parameters 		:	message  - message came through the pubnub
					channels - channel used for the communication
****************************************************************************************'''
def callbackLive(message,channels):
	show_param_live(message["message"])
'''****************************************************************************************
Function Name 	:   callbackStats
Description		:	This pubnub function will receive messages of the statistics
Parameters 		:	message  - message came through the pubnub
					channels - channel used for the communication
****************************************************************************************'''
def callbackStats(message,channels):
	if (message["messagetype"] == "resp"):
		show_param_stats(message)	
'''****************************************************************************************
Function Name 	:   pub_Init
Description		:	This function is to initialise the pubnub and start subscribing for the messages
Parameters 		:	None
****************************************************************************************'''
def pub_Init():
	global pubnub
	try:
		pubnub = Pubnub(publish_key=pub_key,subscribe_key=sub_key) 
		pubnub.subscribe(channels=statsresponsepubchannel, callback=callbackStats,error=error,
		connect=connect, reconnect=reconnect, disconnect=disconnect)
		pubnub.subscribe(channels=livepubchannel, callback=callbackLive,error=error,
		connect=connect, reconnect=reconnect, disconnect=disconnect)
	except Exception as e:
		print e	

	
'''****************************************************************************************
Function Name 	:   _main_
Description		:	The progrm starts executing here.
****************************************************************************************'''
if __name__ == '__main__':

	# Pubnub publish subscribe credentials
	# Refer Step 4 under Gamesimulation in README file in repo root folder
	pub_key = 'pub-c-dd56bf78-3a88-4f6a-a7a4-c1b078b82bf6'
	sub_key = 'sub-c-266f139a-29c3-11e7-a9ec-0619f8945a4f'
	
	statsresponsepubchannel = 'Gameplaystats_resp'
	livepubchannel = 'Gameplaylive'
	statspubchannel = 'Gameplaystats'
	# calling the pubnub initialisation function
	pub_Init()
	time.sleep(5)
	# initialising the screen
	screen = curses.initscr()
	# Getting the maximum height and width of the screen 
	height, width = screen.getmaxyx()
	# fixing the screen liveboard start point and statistics board start point
	scorestartpoint = 5
	statsstartpoint = scorestartpoint+15
	

	x = 0
	# Listening to the key press on the screen
	while x != ord('q'):
		screen.clear()		
		screen.border(0)
		
		''' STATISTICS '''
		# status bar
		statusbarstr = " 'q' - EXIT 's' - SHOW STATISTICS 'h' - HIDE STATISTICS"
		# status bar
		screen.addstr(height-4, 5, statusbarstr)
		# title
		title = "Basket Ball Game Simulation"
		# Rendering title
		screen.addstr(scorestartpoint-1, 50, title)
		screen.addstr(height-6, 2,"")


		
		screen.refresh()
		x = screen.getch()		
		if x == ord('h'):
			hide()
		if x == ord('s'):
			r = stat()
			pub(r)
		
	curses.endwin()
	

		



	
	