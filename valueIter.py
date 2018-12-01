from snakeGameComponents import graphPoint

class valueIteration:
	gGoodReward = 10
	gBadReward = -100
	gLivingReward = 0
	gActionList = None
	gProbabilityList = None
	
	def initBasicList (self, inpLength, inpBase, inpIncrement):
		retList = []
		for i in range (inpLength):
			retList.append(inpBase + i * inpIncrement)
		return retList
		
	def rewardValue(self, inpLoc, inpGraph):
		retReward = 0
		if (inpGraph[inpLoc[1]][inpLoc[0]].isReward()):
			retReward += self.gGoodReward
		if (inpGraph[inpLoc[1]][inpLoc[0]].isHazard()):
			retReward += self.gBadReward
		retReward += self.gLivingReward
		return retReward
		
	def absDirToShort(self, inpDir):
		retShort = None
		if inpDir[0] == 0 and inpDir[1] < 0:
			retShort = 0
		elif inpDir[0] > 0 and inpDir[1] == 0:
			retShort = 1
		elif inpDir[0] == 0 and inpDir[1] > 0:
			retShort = 2
		elif inpDir[0] < 0 and inpDir[1] == 0:
			retShort = 3
		return retShort
		
	def shortToAbsDir(self, inpShort):
		retDir = None
		if inpShort == 0:
			retDir = [0, -1]
		elif inpShort == 1:
			retDir = [1, 0]
		elif inpShort == 2:
			retDir = [0, 1]
		elif inpShort == 3:
			retDir = [-1, 0]
		return retDir
	
	def relativeToAbsoluteDirection(self, inpPrevDir, inpRelDir):
		retDirection = self.shortToAbsDir((self.absDirToShort(inpPrevDir) + inpRelDir) % 4)
		return retDirection
	
	def directionToLocation(self, inpLoc, inpDirection):
		retLocation = [x + y for x, y in zip(inpLoc, inpDirection)]
		return retLocation
	
	def valIterRec(self, inpLoc, inpDir, inpGraph, inpIter, inpActList, inpProbList, inpDiscount):
		if inpIter <= 0:
			return 0
		localRewardList = []
		for i in range(len(inpActList)):
			localRewardList.append(0)
			localProbTotal = 0
			for j in range(len(inpProbList[i])):
				localNewDirection = self.relativeToAbsoluteDirection(inpDir, inpActList[j])
				#print(i)
				#print(inpProbList[i][j])
				#print(localNewDirection)
				localNewLocation = self.directionToLocation(inpLoc, localNewDirection)
				localReward = self.rewardValue(localNewLocation, inpGraph)
				if (localReward < 0):
					inpIter = 0
				localValIter = self.valIterRec(localNewLocation, localNewDirection, inpGraph, inpIter - 1, inpActList, inpProbList, inpDiscount)
				localRewardList[i] += inpProbList[i][j] * ( localReward + inpDiscount * localValIter )
				localProbTotal += inpProbList[i][j]
			localRewardList[i] /= localProbTotal

		tempRIndex = 0
		for i in range(1, len(localRewardList)):
			if (localRewardList[i] > localRewardList[tempRIndex]):
				tempRIndex = i
		return localRewardList[tempRIndex]
	
	def parseActionList(self, inpActionList):
		retList = []
		if inpActionList[0] == "left":
			retList.append(-1)
		if inpActionList[1] == "straight":
			retList.append(0)
		if inpActionList[2] == "right":
			retList.append(1)
		return retList
		
	def valIterRoot(self, inpLoc, inpDir, inpGraph, inpIter, inpProbList, inpDiscount):
		if inpIter <= 0:
			return inpDir
		localRewardList = []
		#-1 = left, 0 = straight, 1 = right
		localActList = [-1, 0, 1]
		for i in range(len(localActList)):
			localRewardList.append(0)
			localProbTotal = 0
			for j in range(len(inpProbList[i])):
				localNewDirection = self.relativeToAbsoluteDirection(inpDir, localActList[j])
				localNewLocation = self.directionToLocation(inpLoc, localNewDirection)
				localReward = self.rewardValue(localNewLocation, inpGraph)
				if (localReward < 0):
					inpIter = 0
				localValIter = self.valIterRec(localNewLocation, localNewDirection, inpGraph, inpIter - 1, localActList, inpProbList, inpDiscount)
				localRewardList[i] += inpProbList[i][j] * ( localReward + inpDiscount * localValIter )
				localProbTotal += inpProbList[i][j]
			localRewardList[i] /= localProbTotal

		tempRIndex = 0
		for i in range(1, len(localRewardList)):
			if (localRewardList[i] > localRewardList[tempRIndex]):
				tempRIndex = i
		if (localRewardList[1] == localRewardList[tempRIndex]):
				tempRIndex = 1
		return self.relativeToAbsoluteDirection(inpDir, localActList[tempRIndex])