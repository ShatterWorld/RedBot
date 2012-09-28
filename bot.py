#!/usr/bin/python3
import os, sys, math

def recruitSoldier ():
	nextRound('v')

def recruitFarmer ():
	nextRound('r')

def upgradeArmy ():
	nextRound('z')

def upgradeFarm ():
	nextRound('f')

def upgradeSpy ():
	nextRound('t')

def harvest ():
	nextRound('s')

def attack (target = None):
	if (target is None):
		target = selectTarget()
		if (not target):
			return False

	soldiers = player['soldiers']
	nextRound ('u {0} {1}'.format(target, soldiers))
	return True

def selectTarget ():
	report = parseInvestigationFile()
	print(report)
	if (report):
		target = None
		targetMinPower = None
		for id in report:
			enemyDefPower = id['soldiers'] * id['armyLevel'] * 1.5 #TypeError: string indices must be integers
			if (enemyDefPower < getAttackPower() and (target is None or enemyDefPower < targetMinPower)):

				target = id
				targetMinPower = enemyDefPower
		return target if target else False
	else:
		if (player['spyLevel'] > 0):
			investigate()
		return False

def investigate ():
	nextRound('i')

def steal (target):
	nextRound('l {0}'.format(target))

def getAttackPower (soldiers, player):
	return soldiers * (player['armyLevel'] // 3)

def getDefensePower (player):
	return math.floor(1.5 * player['soldiers'] * (player['armyLevel'] // 3))

def getProduction ():
	return math.floor(player['farmers'] * (player['farmLevel'] // 3))

def getFoodTimeout ():
	if (player['soldiers'] + player['farmers'] <= 0):
		return 100
	else:
		return math.floor(player['food'] / (player['soldiers'] + player['farmers']))

def isHungry ():
	return getFoodTimeout() < 3

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

def readFile (filename):
	try:
		with open(filename, 'r') as source:
			return {tuple(line.split('=')) for line in source if '=' in line}
	except IOError:
		return False

def parseInvestigationFile ():
	result = {}
	report = None
	try:
		report = open('informace.txt', 'r')
		backupInvestigationFile()
	except IOError:
		try:
			backup = open('informace.old.txt', 'r')
			if (int(next(backup)) > player['remaining']):
				return {}
		except IOError:
			return {}
	with report if report else backup as source:
		for line in source:
			id, data = line.split(':')
			values = {}
			values['land'], values['soldiers'], values['farmers'], values['armyLevel'], values['farmLevel'], values['food'], values['spyLevel'] = data.strip().split(' ')
			result[id] = values
	return result

def backupInvestigationFile ():
	with open('informace.txt', 'r') as source:
		with open('informace.old.txt', 'w') as destination:
			destination.write('{0}\n'.format(player['remaining'] - 15))
			destination.write(source.read())
	#os.remove('informace.txt') trochu blbost si to odmazat, když to řádek potom chcem číst...

def nextRound (action):
	try:
		with open('last-round.txt', 'w') as target:
			target.write(action)
	except Exception:
		pass
	print(action)
	sys.exit(0)

def getLastRound ():
	try:
		with open('last-round.txt', 'r') as source:
			return source.read()
	except IOError:
		return False

#======================================================================
player = {}
player['remaining'], player['land'], player['soldiers'], player['farmers'], player['armyLevel'], player['farmLevel'], player['food'], player['spyLevel'] = map(int, sys.argv[1:])

lastRound = getLastRound()
defReport = readFile('obrana.txt')
attReport = readFile('utok.txt')

if defReport:
	if (not defReport['ztraty_ja_uzemi']):
		attack(defReport['utocnici'].split(',').pop())
elif attReport:
	if (attReport['zisk_ja_uzemi'] > 0 and player['soldiers'] > 3):
		attack(attReport['cil'])
elif ((getFoodTimeout() < 5 and getFoodTimeout() >= 3) or lastRound == 'i'):
	if not attack():
		harvest()
elif getFoodTimeout() < 3:
	harvest()
elif (player['soldiers'] / 3 > player['spyLevel'] + 1):
	upgradeSpy()
elif (getProduction() < 6 or getFoodTimeout() < 4):
	increaseProduction()
else:
	increaseArmyPower()
