import json

def addfield(string, field, value):
	if isinstance(value, str):
		value = value.replace("\"", "").replace("\n", "").replace("\\n", "").replace("\\", "").replace("< ", "").replace(" >", "")
	string += "\n|{} = {}".format(field, value)
	return string

def findSkill(skill_name):
	for skill in skill_list:
		if skill["name"] == skill_name:
			return skill

def addActiveSkillFields(string, skill, index, rarity):
	skill_id = "a_skill{}_".format(index)
	skill_name = ""
	if "nameKey" in skill:
		skill_name = skill["nameKey"]
	else:
		skill_name = skill["name"]

	string = addfield(string, skill_id + "name", dictionary[skill_name + "NameKey"])
	string = addfield(string, skill_id + "description", dictionary[skill_name + "DescriptionKey"])
	string = addfield(string, skill_id + "rarity", rarity)
	if "tuCost" in skill:
		string = addfield(string, skill_id + "tucost", skill["tuCost"])
	else:
		string = addfield(string, skill_id + "tucost", "n/a")
	if "spiritCost" in skill:
		string = addfield(string, skill_id + "spiritg", "-" + str(skill["spiritCost"]))
	elif "spiritGain" in skill:
		string = addfield(string, skill_id + "spiritg", "+" + str(skill["spiritGain"]))
	else:
		string = addfield(string, skill_id + "spiritg", "NA")
	
	return string

dictionary = {}

# Make a dictionary using english text file

with open("Localizable_English.txt", "r", encoding="utf-8") as file:
	for line in file:
		split_line = line.split("=")
		if len(split_line) == 2:
			dictionary[split_line[0].strip("\"")] = split_line[1].strip("\"")
		
# print(dictionary)

# Parse character json file
char_list = []
with open('Monster.json', 'r') as file:
    char_list = json.load(file)["Monster"]

# Parse ability json file
skill_list = []
with open('Ability.json', 'r') as file:
    skill_list = json.load(file)["Ability"]

# Parse bundles
bundle_dic = {}
with open('Package.json', 'r') as file:
    bundle_dic = json.load(file)["package"]

file = open("monsters.txt", "w", encoding="utf-8")

page = "{{Monster"
family_index = 1
a_skill_index = 0
p_skill_index = 0
recorded_passives = []
for character in char_list:
	# Add if first traversal through character
	if page == "{{Monster":
		file.write("{{-start-}}\n")
		# page = addfield(page, "name", dictionary[character["name"] + "NameKey"])
		name = dictionary[character["name"] + "NameKey"].replace("\n", "").replace("\"", "")
		if character["name"] + "SecondNameKey" in dictionary:
			second_name = dictionary[character["name"] + "SecondNameKey"].replace("\n", "").replace("\"", "")
			if name == second_name:
				file.write("\'\'\'{}\'\'\'\n".format(name))
			else:
				file.write("\'\'\'{}\'\'\'\n".format(name + " - " + second_name))
		else:
			file.write("\'\'\'{}\'\'\'\n".format(name))

		try:
			# Add images
			max_rarity = character["evolvedStars"]
			min_rarity = character["stars"]
			if max_rarity == min_rarity:
				page = addfield(page, "image", character["name"] + "-full.png")
			else:
				page = addfield(page, "image", "<gallery>")
				images = ""
				for i in range(0, max_rarity - min_rarity + 1):
					images += "\n{}|{}★".format(character["name"][0:-1] + str(i + 1) + "-full.png", i + min_rarity)
				if max_rarity == 6:
					images += "\n{}|Max".format(character["name"][0:-1] + str(max_rarity - min_rarity + 2) + "-full.png")
				images += "\n</gallery>"
				page += images
				
			# Add leader skills
			if "leaderBuff" in character:
				ld_skill = character["leaderBuff"]
				page = addfield(page, "ldskillname", dictionary[ld_skill + "NameKey"])
				page = addfield(page, "ldskilldesc", dictionary[ld_skill + "DescriptionKey"])

			page = addfield(page, "min_rarity", character["stars"])
			page = addfield(page, "max_rarity", character["evolvedStars"])
			page = addfield(page, "element", character["element"])
			page = addfield(page, "weapon_pref", character["weaponPref"])
			page = addfield(page, "speed", character["speed"])
		
		# If any of the above are not found ignore that character
		except KeyError:
			page = "{{Monster"
			continue
	
	try:
		page = addfield(page, "description" + str(family_index), dictionary[character["name"] + "DescriptionKey"])
		if character["stars"] == character["evolvedStars"] and int(character["evolvedStars"]) == 6:
			max_index = family_index + 1
			page = addfield(page, "max_description", dictionary[f"{character['name'][:-1]}{max_index}DescriptionKey"])
	except KeyError:
		a_skill_index = 0
		p_skill_index = 0
		family_index = 1
		page = "{{Monster"
		continue
	
	# print(character)

	activeSkills = character["activeSkills"]
	for i in range(a_skill_index, len(activeSkills)):
		skill = findSkill(activeSkills[str(a_skill_index)])
		a_skill_index += 1
		try:
			page = addActiveSkillFields(page, skill, a_skill_index, character["stars"])
		except KeyError:
			print(skill)
	
	if "passives" in character:
		passive_skills = character["passives"]
		for key in passive_skills:
			if key in recorded_passives:
				continue
			recorded_passives.append(key)
			skill_name = passive_skills[key]
			p_skill_index += 1
			skill_id = "p_skill{}_".format(p_skill_index)
			page = addfield(page, skill_id + "name", dictionary[skill_name + "NameKey"])
			page = addfield(page, skill_id + "description", dictionary[skill_name + "DescriptionKey"])
			page = addfield(page, skill_id + "rarity", character["stars"])
	
	page = addfield(page, "cost" + str(family_index), character["cost"])
	page = addfield(page, "attack" + str(family_index), character["baseAttack"])
	page = addfield(page, "hp" + str(family_index), character["baseMaxHp"])

	# Add evolotion materials
	if "freeEvolve" in character:
		if "how_to_get" not in page:
			page = addfield(page, "how_to_get", "story")
		page = addfield(page, "evo" + str(family_index), character["freeEvolveLevel"])
	elif "superEvolve1Package" in character:
		if "how_to_get" not in page:
			page = addfield(page, "how_to_get", "gacha")
		try:
			evoset = bundle_dic[character["superEvolve1Package"]]
			page = addfield(page, "evo" + str(family_index), "Gold x " + str(evoset["gold"]))
			for item in evoset["evoitems"]:
				page += "\n{} x {}\n".format(dictionary[item].replace("\"", "").replace("\n", "") , evoset["evoitems"][item])
		except KeyError:
			page = addfield(page, "evo" + str(family_index), "n/a")
	else:
		if "how_to_get" not in page:
			page = addfield(page, "how_to_get", "story")
	# Continue to add to the page if not all evolved forms have been recorded
	if character["stars"] < character["evolvedStars"]:
		family_index += 1
		continue
	
	recorded_passives = []
	a_skill_index = 0
	p_skill_index = 0
	family_index = 1
	page += "\n}}"
	#TODO: add monster category
	# print(page)
	file.write(page + "\n")
	file.write("[[Category:Monster]]\n")
	file.write("[[Category:{}]]\n".format(character["element"]))
	file.write("[[Category:{} star]]\n".format(character["evolvedStars"]))
	file.write("{{-stop-}}\n")
	page = "{{Monster"

file.close()