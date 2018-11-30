from snakeGameComponents import snakeGameComponents

def parseInput():
	retCoordinates = []
	keyPressed = input('Enter command\n')
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
	print (keyPressed)
	return retCoordinates
	
def mainLoop():
	gameData = snakeGameComponents()
	gameData.initializeGameData(6)
	gameData.drawGraph(gameData.gGraph)
	while (gameData.gGameDone == False):
		tmpAction = parseInput()
		gameData.gameLogicIteration(tmpAction[0], tmpAction[1])
		gameData.drawGraph(gameData.gGraph)
		
mainLoop()