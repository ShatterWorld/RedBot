#!/usr/bin/python3
import sys
import botlib
from botlib import *

player = {}
player['remaining'], player['land'], player['soldiers'], player['farmers'], player['armyLevel'], player['farmLevel'], player['food'], player['spyLevel'] = map(int, sys.argv[1:])

setPlayer(player)

#TODO: odlišit chování pro majoritní území (neútočit) a posledních cca 5 kol (útoky)

defenseReport = readFile(files['defenseReport'])
attackReport = readFile(files['attackReport'])

if getFoodTimeout() <= 1:
	harvest()
elif attackReport and int(attackReport['zisk_ja_uzemi']) > 0 and player['soldiers'] > 2:
	attack(attackReport['cil'])
elif defenseReport and (int(defenseReport['ztraty_ja_uzemi']) == 0 and player['soldiers'] > 3):
	attack(defenseReport['utocnici'].split(',').pop().strip())		
elif 2 * getAttackPower(player['soldiers'], player['armyLevel']) > getProduction() and getFoodTimeout() < 5:
	increaseProduction()
else:
	increaseArmyPower()
