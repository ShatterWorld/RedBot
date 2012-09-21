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

def attack (target, soldiers):
	print ('u {0} {1}'.format(target, soldiers))

def investigate ():
	print('i')

def steal (target):
	print('l {0}'.format(target))

def getAttackPower (soldiers, player):
	return soldiers * (player['armyLevel'] // 3)

def getDefensePower (player):
	return math.floor(1.5 * player.soldiers * (player['armyLevel'] // 3))

player = {}
player['remaining'], player['land'], player['soldiers'], player['farmers'], player['armyLevel'], player['farmLevel'], player['food'], player['spyLevel'] = map(int, sys.argv[1:])

