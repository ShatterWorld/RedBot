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

def attack (target = Null, soldiers = Null):
	#selectTarget()
	#calculate()

	print ('u {0} {1}'.format(target, soldiers))
	#return true/false

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
	result = {}
	with open(filename, 'r') as source:
		for line in source:
			key, value = line.split('=')
			result[key] = value
	return result

#======================================================================
player = {}
player['remaining'], player['land'], player['soldiers'], player['farmers'], player['armyLevel'], player['farmLevel'], player['food'], player['spyLevel'] = map(int, sys.argv[1:])


#if (attacked())
if isHungry():
	#if !attack():

	harvest()
else if (getProduction() / (player['soldiers'] + player['farmers']) < 3):
	increaseProduction()
else:
	increaseArmyPower()

