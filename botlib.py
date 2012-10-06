import os, sys, math

actions = {
	'soldier': 'v',
	'farmer': 'r',
	'army': 'z',
	'farm': 'f',
	'spy': 't',
	'harvest': 's',
	'attack': 'u',
	'investigate': 'i',
	'steal': 'l'
}

files = {
	'investigation': 'informace.txt',
	'investigationBackup': 'informace.old.txt',
	'history': 'history.txt',
	'attackReport': 'utok.txt',
	'defenseReport': 'obrana.txt'
}

def recruitSoldier ():
	nextRound('soldier')

def recruitFarmer ():
	nextRound('farmer')

def upgradeArmy ():
	nextRound('army')

def upgradeFarm ():
	nextRound('farm')

def upgradeSpy ():
	nextRound('spy')

def harvest ():
	nextRound('harvest')

def attack (target):
	nextRound('attack', int(target), player['soldiers'])

def investigate ():
	nextRound('investigate')

def steal (target):
	nextRound('steal', target)

def getAttackPower (soldiers, armyLevel):
	return soldiers * (armyLevel // 3)

def getDefensePower (soldiers, armyLevel):
	return math.floor(soldiers * (armyLevel // 3) * 1.5)

def getProduction ():
	return math.floor(player['farmers'] * (player['farmLevel'] // 3))

def getFoodTimeout ():
	if (getConsumption()  <= 0):
		return 100
	else:
		return math.floor(player['food'] / getConsumption())

def getConsumption ():
	return player['soldiers'] + player['farmers']

def isHungry ():
	return getFoodTimeout() <= 2

def increaseArmyPower ():
	if player['soldiers'] > (player['armyLevel'] / 3):
		upgradeArmy()
	else:
		recruitSoldier()

def increaseProduction ():
	if player['farmers'] > (player['farmLevel'] / 3):
		upgradeFarm()
	else:
		recruitFarmer()

#uloží toto a poslední kolo
def nextRound (action, *args):
	with open(files['history'], 'a') as history:
		history.write(action + '\n')
	sys.stdout.write(actions[action] + str().join(map(lambda x: ' ' + str(x), args)))
	sys.exit(0)

#vrací poslední dvě kola
def getHistory ():
	if os.path.isfile(files['history']):
		with open(files['history']) as source:
			return [line.strip() for line in source if line != '\n']
	return []

def findPastAction (action, offset = 0):
	history = getHistory()
	if not offset:
		offset = len(history)
	
	history = history[-offset : ]
	pivot = action[0]
	i = -1
	
	for item in history:
		i += 1
		if item.startswith(pivot):
			j = i
			found = True
			for nextAction in action[1 : ]:
				j += 1
				if not history[j].startswith(nextAction):
					found = False
					break
			if found:
				return True
	return False

def lastRound (offset = 1):
	data = getHistory()
	return data[-offset] if offset < len(data) else 'x'

def readFile (filename):
	try:
		with open(filename, 'r') as source:
			return dict([tuple(map(lambda x: x.strip(), line.split('='))) for line in source if '=' in line])
	except IOError:
		return {}

def setPlayer (player):
	globals()['player'] = player