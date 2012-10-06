#!/usr/bin/python3
import os, sys, math, random

class NoTargetError (Exception):
	pass

class NoReportError (Exception):
	pass

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
	nextRound(actions['soldier'])

def recruitFarmer ():
	nextRound(actions['farmer'])

def upgradeArmy ():
	nextRound(actions['army'])

def upgradeFarm ():
	nextRound(actions['farm'])

def upgradeSpy ():
	nextRound(actions['spy'])

def harvest ():
	nextRound(actions['harvest'])

def attack (target):
	nextRound((actions['attack'] + ' {0} {1}').format(int(target), player['soldiers']))

def investigate ():
	nextRound(actions['investigate'])

def steal (target):
	nextRound((actions['steal'] + ' {0}').format(target))

def getAttackPower (soldiers, armyLevel):
	return soldiers * (armyLevel // 3)

def getDefensePower (soldiers, armyLevel):
	return math.floor(soldiers * (armyLevel // 3) * 1.5)

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

def selectOptimalTarget (report):
	if (report):
		target = None
		targetPower = 0
		for name, enemy in report.items():
			enemyDefPower = getDefensePower(int(enemy['soldiers']), int(enemy['armyLevel']))
			if enemyDefPower < getAttackPower(player['soldiers'], player['armyLevel']) and ((target is None) or (enemyDefPower < targetPower and int(enemy['land']))):
				target = name
				targetPower = enemyDefPower
		if not target:
			raise NoTargetError()
		return target

def selectRandomTarget ():
	return random.randrange(1, 4)

def optimalAttack ():
	report = parseInvestigationFile()
	if report:
		target = selectOptimalTarget(report)
		attack(target)
	else:
		raise NoReportError()

def readFile (filename):
	try:
		with open(filename, 'r') as source:
			return dict([tuple(map(lambda x: x.strip(), line.split('='))) for line in source if '=' in line])
	except IOError:
		return {}

def parseInvestigationFile ():
	if os.path.isfile(files['investigationBackup']):
		with open(files['investigationBackup'], 'r') as backup:
			if (player['remaining'] >= int(next(backup))):
				return getInvestigationFileContents(backup)
	return {}

def checkInvestigationFile ():
	if os.path.isfile(files['investigation']):
		with open(files['investigation'], 'r') as source:
			return bool(list(source))
	return False

def getInvestigationFileContents (source):
	result = {}
	for line in source:
		id, data = line.split(':')
		values = {}
		values['land'], values['soldiers'], values['farmers'], values['armyLevel'], values['farmLevel'], values['food'], values['spyLevel'] = data.strip().split(' ')
		result[id] = values
	return result

def backupInvestigationFile ():
	if checkInvestigationFile():
		with open(files['investigation'], 'r') as source:
			with open(files['investigationBackup'], 'w') as destination:
				destination.write('{0}\n'.format(player['remaining'] - 15))
				destination.write(source.read())

#uloží toto a poslední kolo
def nextRound (action):
	with open(files['history'], 'a') as history:
		history.write(action + '\n')
	sys.stdout.write(action)
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

#======================================================================
player = {}
player['remaining'], player['land'], player['soldiers'], player['farmers'], player['armyLevel'], player['farmLevel'], player['food'], player['spyLevel'] = map(int, sys.argv[1:])

#TODO: odlišit chování pro majoritní území (neútočit) a posledních cca 5 kol (útoky)

defenseReport = readFile(files['defenseReport'])
attackReport = readFile(files['attackReport'])

backupInvestigationFile()

if isHungry(): 				#pokud mám jídlo na míň jak 3 kola, sklízim
	if lastRound() == actions['harvest']:
		increaseProduction()
	harvest()

if attackReport:							#pokud jsem někoho dobyl a mám pár vojáků, útočim na něj znova
	if (int(attackReport['zisk_ja_uzemi']) > 0 and player['soldiers'] > 2):
		attack(attackReport['cil'])

if defenseReport:						#pokud mě někdo napadl a neprošel a mám pár vojáků, útočim na něj zpátky
	if (int(defenseReport['ztraty_ja_uzemi']) == 0 and player['soldiers'] > 2):
		attack(defenseReport['utocnici'].split(',').pop().strip())

if getAttackPower(player['soldiers'], player['armyLevel']) < 15:
	increaseArmyPower()

if not findPastAction(actions['attack'], 10):
	attack(selectRandomTarget())

#if (player['soldiers'] / 3 > player['spyLevel'] + 1): #pokud mám míň jak agenta na 3 vojáky, upgrade špionů
	#upgradeSpy()

if (getProduction() < 6): 			#při malé produkci ji zvyšuju 
	increaseProduction()

#jinak zbrojim
increaseArmyPower()
