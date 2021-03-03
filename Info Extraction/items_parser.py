import json
from english_parser import get_english_dict



class Item():
    name_to_rarity = {
        "high": 6,
        "mid": 5,
        "low": 4,
    }
    @staticmethod
    def parse_items(english_dict):
        package_json = None
        with open('com.zigzagame.evertale/files/Package.json', 'r') as file:
            package_json = json.load(file)['package']
        
        item_dict = {}
        for package_name in package_json:
            package_obj = package_json[package_name]
            if 'evoitems' in package_obj:
                evoitems = package_obj['evoitems']
                for nameKey in evoitems:
                    if nameKey not in item_dict:
                        item_dict[nameKey] = Item(nameKey)
            if 'fuseitems' in package_obj:
                fuseitems = package_obj['fuseitems']
                for nameKey in fuseitems:
                    if nameKey not in item_dict:
                        item_dict[nameKey] = Item(nameKey)
        
        for item in item_dict.values():
            item.get_details(english_dict)

        return item_dict

    def __init__(self, nameKey):
        self.nameKey = nameKey

        self.name = None
        self.category = None
        self.sources = []
        self.description = None
        self.rarity = None
        self.uses = None

    def set_rarity(self):
        if self.nameKey[-4:] in self.name_to_rarity:
            self.rarity = self.name_to_rarity[self.nameKey[-4:]]
        elif self.nameKey[-3:] in self.name_to_rarity:
            self.rarity = self.name_to_rarity[self.nameKey[-3:]]
    
    def set_uses(self):
        if self.nameKey[:4] == "stam":
            self.uses = "Restore " + self.nameKey[4:] + " stamina."
        elif self.nameKey[:6] == "wepexp":
            self.uses = self.nameKey[6].upper() + self.nameKey[7:] + " level weapon experience."
        elif self.nameKey[:6] == "mobexp":
            self.uses = self.nameKey[6].upper() + self.nameKey[7:] + " level character experience."
        elif self.nameKey[:3] == "evo":
            if self.nameKey[-4:] in self.name_to_rarity and self.nameKey[-4:] == "high":
                self.uses = self.nameKey[-4].upper() + self.nameKey[-3:] + " level evolution material."
            elif self.nameKey[-3:] in self.name_to_rarity:
                self.uses = self.nameKey[-3].upper() + self.nameKey[-2:] + " level evolution material."
    
    def set_sources(self):
        quest_drops = {
            "Sanctobox": ["Grenzor Claw", "Flortuga Flower"],
            "Terrabox": ["Rashanar Horn", "Sakura Branch"],
            "Hydrobox": ["Kirin Tail Hair", "Rossé Apple", "Chardinal's Feather"],
            "Prismbox": ["Bottled Fairy Dust", "Hot Silverdrake Cider"],
            "Vultobox": ["Elven Tome", "Flortuga Flower"],
            "Pyrrobox": ["Bikki Mud", "Hot Silverdrake Cider"],
            "Necrobox": ["Rossé Apple", "Chardinal's Feather", "Mirror"],
            "Character Experience": ["Rossé Apple", "Chardinal's Feather", "Bikki Mud", "Mirror"],
            "Weapon Experience": ["Elven Tome", "Sakura Branch"],
            "Gold Quest": ["Hot Silverdrake Cider", "Flortuga Flower", "Bottled Fairy Dust"]
        }

        for quest, drops in quest_drops.items():
            if self.name in drops:
                self.sources.append(quest + " quest")
        
        if self.description == "Weapon Experience Item":
            self.sources.append("Weapon Experience quest")
        elif self.description == "Character Experience Item":
            self.sources.append("Character Experience quest")
    
    def get_details(self, english_dict):
        self.name = english_dict[self.nameKey]

        details = english_dict[self.nameKey + 'DescriptionKey'].split('\\n')

        for detail in details:
            if 'Category: ' in detail:
                self.category = detail.replace('Category: ', '')
            elif 'Primary Source: ' in detail:
                self.sources.append(detail.replace('Primary Source: ', ''))
            else:
                self.description = detail
        
        self.set_rarity()
        self.set_uses()
        self.set_sources()
    
    
    def __str__(self):
        item_string = "{{-start-}}\n"
        item_string += f"'''{self.name}'''\n"

        item_string += "{{Item\n"

        item_string += f"|image={self.nameKey}.png\n"
        item_string += f"|description={self.description}\n"
        item_string += f"|type={self.category}\n"
        if self.rarity is not None:
            item_string += f"|rarity={self.rarity}\n"
        item_string += f"|uses={self.uses}\n"
        item_string += f"|how_to_get=\n"
        for source in self.sources:
            item_string += f"*{source}\n"

        item_string += "}}\n"

        item_string += "{{-stop-}}\n"

        return item_string


if __name__ == "__main__":
    english_dict = get_english_dict()
    item_dict = Item.parse_items(english_dict)

    for nameKey, item in item_dict.items():
        # print(f"('{item.name} x ', '*[[{item.name}]] x '),")
        # print(f"('{item.name} x ', '*[[File:{item.nameKey}.png|{item.name}|link={item.name} |50px]] x '),")
        print(f"('{item.name} x [0-9]*', get_evo_mat),")
    
    # import os
    # with open(os.path.join("Wiki Pages", "Items.txt"), 'w') as file:
    #     for nameKey, item in item_dict.items():
    #         if item.name not in ["Bikki Mud", "Chardinal's Feather", "Flortuga Flower", "Hot Silverdrake Cider", "Rossé Apple"]:
    #             file.write(str(item))
    
    

        