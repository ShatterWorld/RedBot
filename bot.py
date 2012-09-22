#!/usr/bin/python
import sys, math

def recruitSoldier ():
	print('v')

def recruitFarmer ():
	print('r')

def upgradeArmy ():
	print('z')

def upgradeFarm ():
	print('f')

def upgradeSpy ():
	print('t')

def harvest ():
	print('s')

def attack (target = Null):
	#if (targer == Null):
		#selectTarget()
		#if !calculate():
			#return False

	soldiers = player['soldiers']
	print ('u {0} {1}'.format(target, soldiers))
	return True

def investigate ():
	print('i')

def steal (target):
	print('l {0}'.format(target))

def getAttackPower (soldiers, player):
	return soldiers * (player['armyLevel'] // 3)

def getDefensePower (player):
	return math.floor(1.5 * player['soldiers'] * (player['armyLevel'] // 3))

def getProduction ():
	return math.floor(player['farmers'] * (player['farmLevel'] // 3))

def getFoodTimeout ():
	return math.floor(player['food'] / (player['soldiers'] + player['farmers']))

def isHungry ():
	return True if getFoodTimeout() < 3 else False

def increaseArmyPower ():
	if(player['soldiers'] > player['armyLevel'] / 3):
		upgradeArmy()
	else:
		recruitSoldier()

def increaseProduction ():
	if(player['farmers'] > player['farmLevel'] / 3):
		upgradeFarm()
	else:
		recruitFarmer()

def readFile (filename):
	with open(filename, 'r') as source:
		return {tuple(line.split('=')) for line in source if '=' in line}

def wasAttacked ():
	report = readFile('obrana.txt')
	return False if len(report) <= 0 else report 			#dá se takhle rozpoznat prázdné pole?

#======================================================================
player = {}
player['remaining'], player['land'], player['soldiers'], player['farmers'], player['armyLevel'], player['farmLevel'], player['food'], player['spyLevel'] = map(int, sys.argv[1:])


if (report = wasAttacked()):
	if (report['ztraty_ja_uzemi'] <= 0):
		attack(report['utocnici'])			#vyřešit pro víc útočníku, resp. vybrat jakéhokoli z nich
elif isHungry():
	if !attack():
		harvest()
elif (getProduction() / (player['soldiers'] + player['farmers']) < 3):
	increaseProduction()
else:
	increaseArmyPower()

