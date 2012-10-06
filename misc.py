import os, random

class NoTargetError (Exception):
	pass

class NoReportError (Exception):
	pass

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