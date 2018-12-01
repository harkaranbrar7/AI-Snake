from snakeGameComponents import snakeGameComponents
GINPUTTYPE = 0
GWORLDSIZE = 6
GVISUALIZE = True
GGATHERREWARD = False
gPreviousScore = None
gDebugging = [False, False, False]

def parseInput():
	retCoordinates = []
	keyPressed = None
	
	if GINPUTTYPE == 0:
		keyPressed = input('Enter command\n')
	elif GINPUTTYPE == 1:
		print ("nothing value iteration")
	elif GINPUTTYPE == 2:
		print ("nothing q learning")
	elif GINPUTTYPE == 3:
		print ("nothing approximate q learning")
	
	if len(keyPressed) < 1:
		retCoordinates.append(0)
		retCoordinates.append(-1)
	elif keyPressed[0] == 'w':
		retCoordinates.append(0)
		retCoordinates.append(-1)
	elif keyPressed[0] == 'a':
		retCoordinates.append(-1)
		retCoordinates.append(0)
	elif keyPressed[0] == 's':
		retCoordinates.append(0)
		retCoordinates.append(1)
	elif keyPressed[0] == 'd':
		retCoordinates.append(1)
		retCoordinates.append(0)
	else:
		retCoordinates.append(0)
		retCoordinates.append(-1)
	#print (keyPressed)
	return retCoordinates
	
def mainLoop():
	gameData = snakeGameComponents()
	gameData.initializeGameData(GWORLDSIZE)
	gameData.drawGraph(gameData.gGraph)
	gPreviousScore = 0
	while (gameData.gGameDone == False):
		tmpAction = parseInput()
		gameData.gameLogicIteration(tmpAction[0], tmpAction[1])
		if GVISUALIZE:
			gameData.drawGraph(gameData.gGraph)
		if GGATHERREWARD:
			print("gather the reward data after action")
			#gameData.gScore vs previousScore
		if gDebugging[0]:
			print(gameData.getHeadLocation())
			print(gameData.getHeadDirection())
			print(gameData.getFoodLocation())
			print(gameData.getTailListLocation())
			print(gameData.getWallListLocation())
		if gDebugging[1]:
			tmpGame = gameData.copyGameState()
			print(tmpGame.gHead)
			print(gameData.gHead)
			print(tmpGame.getHeadLocation())
			print(tmpGame.gFood)
			print(gameData.gFood)
			print(tmpGame.getFoodLocation())
			print(tmpGame.gTailList)
			print(gameData.gTailList)
			print(tmpGame.getTailListLocation())
			if gDebugging[2]:
				print(tmpGame.gWallList)
				print(gameData.gWallList)
			print(tmpGame.getWallListLocation())
			print(tmpGame.gScore)
			print(tmpGame.gGameDone)
		
mainLoop()