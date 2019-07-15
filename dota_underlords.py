from collections import defaultdict
import math
from itertools import combinations 
import operator

# 1. Find the maximum number of tier 1 color Alliancees that can be achieved in a team of 10
# 2. Rank the benefits of all Alliances, find the best combo

class Alliance:
	def __init__(self, num_tiers, num_per_tier, weight):
		self.num_tiers = num_tiers
		self.num_per_tier = num_per_tier
		self.weight = weight

alliances = {
	'assassin' : Alliance(3, 3, 3),
	'elusive' : Alliance(3, 3, 3),
	'warrior' : Alliance(3, 3, 3),

	# above average
	'hunter' : Alliance(2, 3, 2),
	'savage' : Alliance(3, 2, 2),
	'dragon' : Alliance(1, 2, 2),
	'heartless' : Alliance(3, 2, 2),
	'druid' : Alliance(2, 2, 2),
	'knight' : Alliance(3, 2, 2),
	'warlock' : Alliance(3, 2, 2),

	#average
	'mage' : Alliance(2, 3, 1),
	'scaled' : Alliance(2, 2, 1),
	'demon' : Alliance(1, 1, 1),
	'demon hunter': Alliance(2, 1, 1),
	'troll' : Alliance(2, 2, 1),
	'primordial' : Alliance(2, 2, 1),
	'brawny' : Alliance(2, 2, 1),
	'human' : Alliance(3, 2, 1),
	
	# Below average
	'scrappy' : Alliance(2, 3, .5),
	'deadeye' : Alliance(1, 2, .5),
	'inventor' : Alliance(2, 2, .5),
	'shaman' : Alliance(1, 3, .5),

	# Bad
	'blood bound' : Alliance(1, 2, .25), }

# heroes
class Hero:
	def __init__(self, name, alliances):
		self.name = name
		self.alliances = alliances

assassin = 'assassin'
blood_bound = 'blood bound'
brawny = 'brawny'
deadeye = 'deadeye'
druid = 'druid'
heartless = 'heartless'
hunter = 'hunter'
inventor = 'inventor'
knight = 'knight'
mage = 'mage'
savage = 'savage'
shaman = 'shaman'
troll = 'troll'
warlock = 'warlock'
warrior = 'warrior'
human = 'human'
scrappy = 'scrappy'
primordial = 'primordial'
elusive = 'elusive'
demon = 'demon'
demon_hunter = 'demon hunter'
scaled = 'scaled'
dragon = 'dragon'

# heroes are a graph where edges are alliances

heroes = [
	Hero("Bloodseeker", [assassin, human]),
	Hero("Bounty Hunter", [assassin, scrappy]),
	Hero("Morphling", [assassin, primordial]),
	Hero("Phantom Assassin", [assassin, elusive]),
	Hero("Queen of Pain", [assassin, demon]),
	Hero("Slark", [assassin, scaled]),
	Hero("Templar Assassin", [assassin, elusive]),
	Hero("Viper", [assassin, dragon]),
	Hero("Ogre Magi", [blood_bound, mage]),
	Hero("Warlock", [blood_bound, warlock]),
	Hero("Axe", [brawny, warrior]),
	Hero("Beastmaster", [brawny, hunter]),
	Hero("Disruptor", [brawny, shaman, warlock]),
	Hero("Juggernaut", [brawny, warrior]),
	Hero("Gyrocopter", [deadeye, inventor]),
	Hero("Sniper", [deadeye, hunter]),
	Hero("Chaos Knight", [demon, knight]),
	Hero("Doom", [demon, warrior]),
	Hero("Shadow Fiend", [demon, warlock]),
	Hero("Terrorblade", [demon, demon_hunter]),
	Hero("Dragon Knight", [dragon, human, knight]),
	Hero("Puck", [dragon, elusive, mage]),
	Hero("Enchantress", [druid, savage]),
	Hero("Lone Druid", [druid, savage]),
	Hero("Nature's Prophet", [druid, elusive]),
	Hero("Treant Protector", [druid, elusive]),
	Hero("Anti-Mage", [demon_hunter, elusive]),
	Hero("Luna", [elusive, knight]),
	Hero("Mirana", [elusive, hunter]),
	Hero("Windranger", [elusive, hunter]),
	Hero("Abaddon", [heartless, knight]),
	Hero("Drow Ranger", [heartless, hunter]),
	Hero("Necrophos", [heartless, warlock]),
	Hero("Pudge", [heartless, warrior]),
	Hero("Crystal Maiden", [human, mage]),
	Hero("Keeper of the Light", [human, mage]),
	Hero("Kunkka", [human, warrior]),
	Hero("Lina", [human, mage]),
	Hero("Lycan", [human, savage, warrior]),
	Hero("Omniknight", [human, knight]),
	Hero("Medusa", [hunter, scaled]),
	Hero("Tidehunter", [hunter, scaled]),
	Hero("Clockwerk", [inventor, scrappy]),
	Hero("Techies", [inventor, scrappy]),
	Hero("Timbersaw", [inventor, scrappy]),
	Hero("Tinker", [inventor, scrappy]),
	Hero("Batrider", [knight, troll]),
	Hero("Lich", [mage, heartless]),
	Hero("Razor", [mage, primordial]),
	Hero("Arc Warden", [primordial, shaman]),
	Hero("Enigma", [primordial, warlock]),
	Hero("Morphling", [mage, primordial]),
	Hero("Tiny", [primordial, warrior]),
	Hero("Sand King", [savage, assassin]),
	Hero("Tusk", [savage, warrior]),
	Hero("Venomancer", [savage, warlock]),
	Hero("Slardar", [scaled, warrior]),
	Hero("Alchemist", [scrappy, warlock]),
	Hero("Shadow Shaman", [shaman, troll]),
	Hero("Troll Warlord", [troll, warrior]),
	Hero("Witch Doctor", [troll, warlock]) ]

max_slots = 10

def hero_list_hasher(hero_list):
	hero_names=';'.join(sorted([hero.name for hero in hero_list]))
	return hero_names
	
def get_alliance_score(hero_list, known_scores):
	hashed_list = hero_list_hasher(hero_list)
	if hashed_list in known_scores:
		return known_scores[hashed_list]
	alliance_dict=defaultdict(int)
	total_score = 0
	for hero in hero_list:
		for alliance in hero.alliances:
			alliance_dict[alliance]+=(1*alliances[alliance].weight)
	for alliance, total in alliance_dict.items():
		completed_tiers = math.floor(total/alliances[alliance].num_per_tier)
		total_score+=min([completed_tiers, alliances[alliance].num_tiers])
	
	return total_score

def hero_optimizer(list_of_heros, max_heroes):
	scores={}

	i = 0
	for hero_list in combinations(list_of_heros, max_heroes):

		i+=1
		if i % 100000 == 0:
			print(i)

		scores[hero_list_hasher(hero_list)]=get_alliance_score(hero_list, scores)
	
	sorted_list = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
	max=sorted_list[0][1]
	final_list=[]
	for elem in sorted_list:
		if elem[1]>=max:
			final_list.append(elem[0])
	return final_list, max

best_combos = hero_optimizer(heroes, 5)
top_heroes = {}
for combo in best_combos[0]:
	combo_as_list = combo.split(';')
	for hero in combo_as_list:
		if hero in top_heroes.keys():
			top_heroes[hero] += 1
		else:
			top_heroes[hero] = 1
top_heroes = sorted([(rank, hero) for (hero, rank) in top_heroes.items()], reverse = True)

print(top_heroes)



