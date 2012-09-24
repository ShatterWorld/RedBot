#!/usr/bin/python3
import os, sys, math

# musíme ukládat poslední tah!!!

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
	if (report):
		target = None
		targetMinPower = None
		for id in report:
			enemyDefPower = id['soldiers'] * id['armyLevel'] * 1.5
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
	with open(filename, 'r') as source:
		return {tuple(line.split('=')) for line in source if '=' in line}

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
			player = {}
			player['land'], player['soldiers'], player['farmers'], player['armyLevel'], player['farmLevel'], player['food'], player['spyLevel'] = data.strip().split(' ')
			result[id] = player
	return result

def backupInvestigationFile (): #nefunguje ukládání
	with open('informace.txt', 'r') as source:
		with open('informace.old.txt', 'w') as destination:
			destination.write('{0}\n'.format(player['remaining'] - 15))
			destination.write(source.read)
	os.remove('informace.txt')

def nextRound (action):
	with open('last-round.txt', 'w') as target:
		target.write(action)
	print(action)

#======================================================================
player = {}
player['remaining'], player['land'], player['soldiers'], player['farmers'], player['armyLevel'], player['farmLevel'], player['food'], player['spyLevel'] = map(int, sys.argv[1:])


report = False
try:
	report = readFile('obrana.txt')
except IOError:
	pass
if report:
	if (not report['ztraty_ja_uzemi']):
		attack(report['utocnici'].split(',').pop())
#elif jestli byl poslední tah úspěšný útok, útoč znova na stejného soupeře
elif getFoodTimeout() == 3: #nebo minulé kolo bya infiltrace
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

