#This project is still a work in progress.
It is based on diplomacy-mapper from ericl which allows drawing diplomacy maps.

The tactical evaluator will have two main processes: attack potential and defence potential.
For each nation two maps will get created one coulored for best places to attack and the other for places lacking defence.

The algorithm for the defence calculator is pretty much ready, I'm trying to implement it, but it takes time as I'm no programmer.

I've also written part of the algorithm for the attack but I'm still trying to improve it a bit.

If you can program better than me (you probably can) and you want to help finish this project you can contact me, your help is welcome!

NATION STRENGTH ALGORITHM
[] Number of supply centers evaluation
[] Border stability
	[x] Roads to Supply Centers #Evaluates the number of open roads to one SC and the number of enemies in proximity
	[]  Sure losses #Evaluates the number of sure losses in the borders
	[]  Key territories under attack #Same as Roads to Supply Centers but for territories who border with 2 SC
	[]  Locked armies #Evaluates the number of armies who cannot move as they have to defend or support
	[]  Enemy Attack Potential
[] Attack Potential
	Still to be well defined

If someone has advices to improve the algorithm I'd be happy to hear them!

Quick-and-dirty diplomacy map maker.

This program uses the excellent map from webdiplomacy,
and so falls under the same license it does.

Usage:

	The following sequence of commands in python:
		from map import *
		[commands]
		done()
	will write a file called 'out.png' in this directory.

	Run 'run.py' to see an example rendering.

Example command sequence:

	context(ENGLAND)
	fleet_move_failed('nth', 'bel')
	army_hold('yor')
	fleet_move('nor', 'nwy')
	set('nwy')
	destroy('nwy')

	context(ITALY)
	fleet_support_hold('iri', 'nao')
	fleet_support_hold('nao', 'iri')
	
All location and nation names can be found in 'data.py'.

List of commands:
	
	disable_symbols()
        do not draw arrows, etc

	context(NATION)
        set further commands to apply to NATION

	set(loc)
        mark a location as owned by a nation

	dislodge(loc)
        mark pending unit destruction/retreat
		another unit of a different nation may be present at the loc

	destroy(loc)
        mark a unit destroyed/disbanded at location
		used in conjunction with a move command with destination at loc
		another unit of a different nation may be present at the loc

	fleet_create(loc)
	fleet_hold(loc)
	fleet_move(loc, dest)
	fleet_retreat(loc, dest)
	fleet_move_failed(loc, dest)
	fleet_support_hold(loc, dest)
	fleet_support_move(loc, attacker, dest)
	fleet_convoy(loc, attacker, dest)

	army_create(loc)
	army_hold(loc)
	army_move(loc, dest)
	army_retreat(loc, dest)
	army_move_failed(loc, dest)
	army_support_hold(loc, dest)
	army_support_move(loc, attacker, dest)
