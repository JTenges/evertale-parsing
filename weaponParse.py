import json

from localEnglishReader import localEnglishReader

class packageReader:
    englishReader = localEnglishReader()

    def __init__(self):
        self.packages = {}
        with open('Package.json', 'r') as file:
            self.packages = json.load(file)["package"]
    
    def getPackageDetails(self, packageName):
        detailList = []
        package = self.packages[packageName]
        for item in package.keys():
            if isinstance(package[item], dict):
                subItems = package[item]
                for key in subItems.keys():
                    detailList.append("{} x {}".format(self.englishReader.get(key), subItems[key]))
            else:
                detailList.append("{} x {}".format(self.englishReader.get(item), package[item]))
        return detailList

class weapon:
    englishReader = localEnglishReader()
    packReader = packageReader()

    def __init__(self, weaponJsonEntries):
        self.name = ""
        self.id = ""
        self.description = ""
        self.weaponClass = ""
        self.minRarity = -1
        self.maxRarity = -1
        self.costs = []
        self.stats = []
        self.evoSets = []
        self.passives = []

        self.id = weaponJsonEntries[0]["name"]
        for i in range(0, len(weaponJsonEntries)):
            currentEntry = weaponJsonEntries[i]
            
            if i == 0:
                self.name = self.englishReader.getNameKey(self.id)
                if self.englishReader.keyExists(self.id + "SecondNameKey"):
                    self.name += " - " + self.englishReader.get(self.id + "SecondNameKey")
                
                if self.englishReader.keyExists(self.id + "DescriptionKey"):
                    self.description += self.englishReader.getDescriptionKey(self.id)

                self.weaponClass = currentEntry["weaponPref"]
                self.minRarity = currentEntry["stars"]
                self.maxRarity = currentEntry["evolvedStars"]
                
            
            if i != len(weaponJsonEntries) - 1:
                self.evoSets.append(self.packReader.getPackageDetails(currentEntry["superEvolve1Package"]))
            
            self.costs.append(currentEntry["cost"])
            self.stats.append((currentEntry["baseAttack"], currentEntry["baseMaxHp"]))

            currentPassives = currentEntry["passives"]
            for abilityIndex in currentPassives.keys():
                if self.englishReader.keyExists(currentPassives[abilityIndex] + "NameKey"):
                    self.passives.append((currentEntry["stars"], *self.englishReader.getItemData(currentPassives[abilityIndex])))

        self.evolutions = self.maxRarity - self.minRarity
    
    def __str__(self):
        fieldFormat = "|{field} = {value}\n"
        fieldFormatEnd = "|{field} = {value}"
        stats = ""
        passives = ""
        evosets = ""

        for i in range(0, self.evolutions + 1):
            stat = self.stats[i]
            stats += fieldFormat.format(field=f"attack{i+1}", value=stat[0])
            stats += fieldFormat.format(field=f"hp{i+1}", value=stat[1])
            stats += fieldFormatEnd.format(field=f"cost{i+1}", value=self.costs[i])

            if i < len(self.passives):
                passive = self.passives[i]
                passives += fieldFormat.format(field=f"p_skill{i+1}_rarity", value=passive[0])
                passives += fieldFormat.format(field=f"p_skill{i+1}_name", value=passive[1])
                passives += fieldFormatEnd.format(field=f"p_skill{i+1}_description", value=passive[2])
                
            if i < self.evolutions:
                stats += "\n"
                passives += "\n"

                items = ""
                evoset = self.evoSets[i]
                for j in range(0, len(evoset)):
                    items += evoset[j]
                    if j != len(evoset) - 1:
                        items += "\n\n"
                evosets += fieldFormatEnd.format(field=f"evo{i+1}", value=items)
                if i < self.evolutions - 1:
                    evosets += "\n"
        if passives != "":
            passives = "\n" + passives
        if evosets != "":
            evosets = "\n" + evosets
        string = f"""{{{{-start-}}}}
\'\'\'{self.name}\'\'\'
{{{{Weapon
|image = {self.id}-full.png
|min_rarity = {self.minRarity}
|max_rarity = {self.maxRarity}
|weapon_type = {self.weaponClass}
|description = {self.description}
{stats}{passives}{evosets}
}}}}
{{{{-stop-}}}}
"""
        return string

if __name__ == "__main__":
    # packReader = packageReader()
    # print(packReader.getPackageDetails("superevosrset14"))

    weaponList = []
    with open('Weapon.json', 'r') as file:
        weaponList = json.load(file)["Weapon"]
        # weapon1 = weapon(weaponList[-3:])
    # print(weapon1.name)
    # print(weapon1.costs)
    # print(weapon1.description)
    # print(weapon1.evoSets)
    # print(weapon1.evolutions)
    # print(weapon1.maxRarity)
    # print(weapon1.minRarity)
    # print(weapon1.passives)
    # print(weapon1.stats)
    # print(weapon1.weaponClass)
    # print(weapon1)

    with open("weapons.txt", "w") as file:
        family = weaponList[0]["family"]
        weaponJSONS = []
        for w in weaponList:
            if w["family"] != family and family != "":
                if weapon.englishReader.keyExists(weaponJSONS[0]["name"] + "NameKey"):
                    weaponEntry = weapon(weaponJSONS)
                    file.write(weaponEntry.__str__())
                family = w["family"]
                weaponJSONS = [w]
            else:
                weaponJSONS.append(w)