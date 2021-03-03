import json
from english_parser import get_english_dict

class Ability():
    @staticmethod
    def parse_abilities(english_dict):
        ability_json = None
        with open('com.zigzagame.evertale/files/Ability.json', 'r') as file:
            ability_json = json.load(file)["Ability"]

        ablility_dict = {}
        for ability_obj in ability_json:
            if ability_obj['name'] not in ablility_dict:
                ablility_dict[ability_obj['name']] = Ability(ability_obj)
                ablility_dict[ability_obj['name']].get_name_and_desc(english_dict)
        return ablility_dict
    
    def __init__(self, ability_obj):
        self.nameKey = ability_obj['name']
        self.useLimit = ability_obj['useLimit']

        if 'tuCost' in ability_obj:
            self.tuCost = ability_obj['tuCost']
        else:
            self.tuCost = 0

        if 'spiritGain' in ability_obj:
            self.spirit = ability_obj['spiritGain']
        elif 'spiritCost' in ability_obj:
            self.spirit = -1 * ability_obj['spiritCost']

        self.name = None
        self.description = None
    
    def get_name_and_desc(self, english_dict):
        name_key_value = self.nameKey + "NameKey"
        desc_value = self.nameKey + "DescriptionKey"

        if name_key_value in english_dict:
            self.name = english_dict[name_key_value]
        
        if desc_value in english_dict:
            self.description = english_dict[desc_value]
    
    def __str__(self):
        ability_string = ""

        ability_string += f"name:           {self.name}\n"
        ability_string += f"nameKey:        {self.nameKey}\n"
        ability_string += f"description:    {self.description}\n"
        ability_string += f"tuCost:         {self.tuCost}\n"
        ability_string += f"useLimit:       {self.useLimit}\n"
        ability_string += f"spirit:         {self.spirit}\n"

        return ability_string

if __name__ == "__main__":
    english_dict = get_english_dict()
    ability_dict = Ability.parse_abilities(english_dict)
    print(ability_dict['PoisonChargeA'])