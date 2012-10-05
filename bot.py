#!/usr/bin/python3
import os, sys, math

class NoTargetError (Exception):
	pass

class NoReportError (Exception):
	pass

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

def attack (target):
	nextRound('u {0} {1}'.format(int(target), player['soldiers']))

def selectTarget (report):
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

def optimalAttack ():
	report = parseInvestigationFile()
	if report:
		target = selectTarget(report)
		attack(target)
	else:
		raise NoReportError()

def investigate ():
	nextRound('i')

def steal (target):
	nextRound('l {0}'.format(target))

def getAttackPower (soldiers, armyLevel):
	return soldiers * (armyLevel // 3)

def getDefensePower (soldiers = None, armyLevel = None):
	if ((soldiers is None) or (armyLevel is None)):
		soldiers = player['soldiers']
		armyLevel = player['armyLevel']
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

def readFile (filename):
	try:
		with open(filename, 'r') as source:
			return dict([tuple(line.split('=')) for line in source if '=' in line])
	except IOError:
		return False

def parseInvestigationFile ():
	if os.path.isfile('informace.old.txt'):
		with open('informace.old.txt', 'r') as backup:
			if (player['remaining'] >= int(next(backup))):
				return getInvestigationFileContents(backup)
	return {}

def checkInvestigationFile ():
	if os.path.isfile('informace.txt'):
		with open('informace.txt', 'r') as source:
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
		with open('informace.txt', 'r') as source:
			with open('informace.old.txt', 'w') as destination:
				destination.write('{0}\n'.format(player['remaining'] - 15))
				destination.write(source.read())

#uloží toto a poslední kolo
def nextRound (action):
	with open('history.txt', 'a') as history:
		history.write(action + '\n')
	print(action)
	sys.exit(0)

#vrací poslední dvě kola
def getHistory ():
	if os.path.isfile('history.txt'):
		with open('history.txt') as source:
			return [line for line in source if line != '\n']
	return []

def lastRound (offset = 1):
	data = getHistory()
	return data[-offset] if offset < len(data) else 'x'

#======================================================================
player = {}
player['remaining'], player['land'], player['soldiers'], player['farmers'], player['armyLevel'], player['farmLevel'], player['food'], player['spyLevel'] = map(int, sys.argv[1:])

#TODO: odlišit chování pro majoritní území (neútočit) a posledních cca 5 kol (útoky)

defReport = readFile('obrana.txt')
attReport = readFile('utok.txt')

backupInvestigationFile()

if getFoodTimeout() < 3: 				#pokud mám jídlo na míň jak 3 kola, sklízim
	if lastRound() == 's':
		increaseProduction()
	harvest()

if attReport:							#pokud jsem někoho dobyl a mám pár vojáků, útočim na něj znova
	if (int(attReport['zisk_ja_uzemi']) > 0 and player['soldiers'] > 2):
		attack(attReport['cil'])

if defReport:						#pokud mě někdo napadl a neprošel a mám pár vojáků, útočim na něj zpátky
	if (int(defReport['ztraty_ja_uzemi']) == 0 and player['soldiers'] > 2):
		attack(defReport['utocnici'].split(',').pop())

if (lastRound(1) == 'i'):				#pokud jsem minule špionoval
	if (lastRound(2) == 'i'):#a předminule taky
		try:
			optimalAttack()
		except NoReportError:
			upgradeSpy()
		except NoTargetError:
			increaseArmyPower()
	else:								#když předminule ne, tak znova špionuju
		investigate()

if (player['soldiers'] / 3 > player['spyLevel'] + 1): #pokud mám míň jak agenta na 3 vojáky, upgrade špionů
	upgradeSpy()

if (getProduction() < 6): 			#při malé produkci ji zvyšuju 
	increaseProduction()

#jinak zbrojim
increaseArmyPower()
