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
	if (report):
		target = None
		targetMinPower = None
		for id in report:
			enemyDefPower = getDefensePower(int(report[id]['soldiers']), int(report[id]['armyLevel']))
			if ((enemyDefPower < getAttackPower()) and ((target is None) or (enemyDefPower < targetMinPower))):
				target = id
				targetMinPower = enemyDefPower
		return target if target else False
	else:
		if (player['spyLevel'] > 0 and prelastRound != 'i'):
			investigate()
		return False

def investigate ():
	nextRound('i')

def steal (target):
	nextRound('l {0}'.format(target))

def getAttackPower (soldiers = None, armyLevel = None):
	if ((soldiers is None) or (armyLevel is None)):
		soldiers = player['soldiers']
		armyLevel = player['armyLevel']
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

#uloží toto a poslední kolo
def nextRound (action):
	try:
		with open('last-round.txt', 'r') as original:
			last = original.read()[0]
		with open('last-round.txt', 'w') as modified:
			modified.write(action + last)
	except Exception:
		print('err1')

	print(action)
	sys.exit(0)

#vrací poslední dvě kola
def getLastRounds ():
	try:
		with open('tmp.txt', 'r') as target:
			text = target.read()
			stack = []
			for char in text:
				stack.append(char)
			return stack
	except Exception:
		return False

#======================================================================
player = {}
player['remaining'], player['land'], player['soldiers'], player['farmers'], player['armyLevel'], player['farmLevel'], player['food'], player['spyLevel'] = map(int, sys.argv[1:])

#TODO: odlišit chování pro majoritní území (neútočit) a posledních cca 5 kol (útoky)

lastRounds = getLastRounds()
lastRound = lastRounds.pop(0)			#poslední kolo
prelastRound = lastRounds.pop(0)		#předoslední kolo

defReport = readFile('obrana.txt')
attReport = readFile('utok.txt')

if defReport:							#pokud mě někdo napadl a neprošel a mám pár vojáků, útočim na něj zpátky
	if (not defReport['ztraty_ja_uzemi'] and player['soldiers'] > 3):
		attack(defReport['utocnici'].split(',').pop())
elif attReport:							#pokud jsem někoho dobyl a mám pár vojáků, útočim na něj znova
	if (attReport['zisk_ja_uzemi'] > 0 and player['soldiers'] > 3):
		attack(attReport['cil'])
elif (lastRound == 'i'):				#pokud jsem minule špionoval
	if (prelastRound == 'i'): 			#a předminule taky			#tohle se vyhodnocuje špatně, asi
		if (parseInvestigationFile()):	#a povedlo se
			if not attack():			#zkusim útok
				increaseArmyPower()		#jinak zbrojim
		else:							#když se nepovedlo, uprgrade špionů
			upgradeSpy()
	else:								#když předminule ne, tak znova špionuju
		investigate()
elif (getFoodTimeout() < 5 and getFoodTimeout() >= 3): #když mám jídlo na 3-4 kola
	if not attack(): 					#zkusim útok
		harvest() 						#jinak sklízim
elif getFoodTimeout() < 3: 				#pokud mám jídlo na míň jak 3 kola, sklízim
	harvest()
elif (player['soldiers'] / 3 > player['spyLevel'] + 1): #pokud mám míň jak agenta na 3 vojáky, upgrade špionů
	upgradeSpy()
elif (getProduction() < 6): 			#při malé produkci ji zvyšuju 
	increaseProduction()
else: #jinak zbrojim
	increaseArmyPower()
