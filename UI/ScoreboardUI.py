import curses
from pubnub import Pubnub
import random
import time
import sys

teams = ["Cleveland Cavaliers","Toronto Raptors"]

def hide():
	global screen
	screen.refresh()
	screen.clear()
	
def stat():
	global screen
	screen.refresh()
	screen.addstr(scorestartpoint+13,30,"0 -Cleveland Cavaliers\n\t\t\t      1 -Toronto Raptors")
	input = screen.getstr(height-6, 2)	
	return input	
def pub(r):
	global pubnub
	try:
		if int(r) in [0,1]:
			pubnub.publish(channel = 'Gameplaystats',message = {"messagetype":"req","team":teams[int(r)]})
	except Exception as e:
		pass
	

def error(message):
    print("ERROR : " + str(message))
def connect(message):
	print("CONNECTED")
def reconnect(message):
    print("RECONNECTED")
def disconnect(message):
    print("DISCONNECTED")

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
	title = "OpenWhisk-Block Basket Ball Game Simulation"
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
		screen.addstr(statsstartpoint+5,60,"Winloss%")

		''' STATISTICS '''
		# status bar
		statusbarstr = " 'q' - EXIT 's' - SHOW STATISTICS 'h' - HIDE STATISTICS"
		# status bar
		screen.addstr(height-4, 5, statusbarstr)
		# title
		title = "OpenWhisk-Block Basket Ball Game Simulation"
		# Rendering title
		screen.addstr(scorestartpoint-1, 50, title)
		screen.addstr(height-6, 2,"")


		screen.addstr(statsstartpoint+3,18,"TEAM   -- "+param["Team"])
		screen.addstr(statsstartpoint+7,10,str(param["PlayedGames"]))
		winlosspercn = round(param["WinLosspercentage"],2)
		screen.addstr(statsstartpoint+7,25,str(param["Win"]))
		screen.addstr(statsstartpoint+7,35,str(param["Loss"]))
		screen.addstr(statsstartpoint+7,45,str(param["Maxscore"]))
		screen.addstr(statsstartpoint+7,60,str(winlosspercn))
		screen.addstr(height-6, 2,"")	
		screen.refresh()
	except curses.error as e:
		print e	

def callbackLive(message,channels):
	show_param_live(message["message"])

def callbackStats(message,channels):
	if (message["messagetype"] == "resp"):
		show_param_stats(message)	

def pub_Init():
	global pubnub
	try:
		pubnub = Pubnub(publish_key=pub_key,subscribe_key=sub_key) 
		pubnub.subscribe(channels='Gameplaystats_resp', callback=callbackStats,error=error,
		connect=connect, reconnect=reconnect, disconnect=disconnect)
		pubnub.subscribe(channels='Gameplaylive', callback=callbackLive,error=error,
		connect=connect, reconnect=reconnect, disconnect=disconnect)
	except Exception as e:
		print e	

	

if __name__ == '__main__':

	
	pub_key = 'pub-c-578b72c9-0ca2-4429-b7d4-313bbdf9b335'
	sub_key = 'sub-c-471f5e36-e1ef-11e6-ac69-0619f8945a4f'
	
	pub_Init()
	time.sleep(5)
	
	screen = curses.initscr()
		
	height, width = screen.getmaxyx()
	scorestartpoint = 5
	statsstartpoint = scorestartpoint+15
	

	x = 0
	while x != ord('q'):
		screen.clear()		
		screen.border(0)
		
		''' STATISTICS '''
		# status bar
		statusbarstr = " 'q' - EXIT 's' - SHOW STATISTICS 'h' - HIDE STATISTICS"
		# status bar
		screen.addstr(height-4, 5, statusbarstr)
		# title
		title = "OpenWhisk-Block Basket Ball Game Simulation"
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
	

		



	
	