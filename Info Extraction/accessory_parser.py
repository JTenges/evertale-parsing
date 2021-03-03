import json
import random

from english_parser import get_english_dict

class Accessory():
    @staticmethod
    def parse_accessories(english_dict):
        accessory_json = None
        with open('com.zigzagame.evertale/files/Equipment.json', 'r') as file:
            accessory_json = json.load(file)["Equipment"]
        
        package_json = None
        with open('com.zigzagame.evertale/files/Package.json', 'r') as file:
            package_json = json.load(file)["package"]

        accessory_dict = {}
        for accessory_obj in accessory_json:
            if accessory_obj['name'] not in accessory_dict:
                accessory_dict[accessory_obj['name']] = Accessory(accessory_obj)
                accessory_dict[accessory_obj['name']].get_name_and_desc(english_dict)
                accessory_dict[accessory_obj['name']].get_location(package_json)
        return accessory_dict

    def __init__(self, accessory_obj):
        self.nameKey = accessory_obj['name']
        self.attack = accessory_obj['flatAttack']
        self.hp = accessory_obj['flatMaxHp']
        self.speed = accessory_obj['flatSpeed']
        self.stars = accessory_obj['accessoryStars']

        self.name = None
        self.description = None

        self.locations = []
    
    def get_name_and_desc(self, english_dict):
        name_key_value = self.nameKey + "NameKey"
        desc_value = self.nameKey + "DescriptionKey"

        if name_key_value in english_dict:
            self.name = english_dict[name_key_value]
        
        if desc_value in english_dict:
            self.description = english_dict[desc_value]
            self.description = self.description.replace('\\n\\n', ' ')
            self.description = self.description.replace('\\n', ' ')
            self.description = self.description.replace('\\"', '\"')
    
    def get_location(self, package_json):
        for package_name in package_json:
            in_package = self.nameKey in package_json[package_name]
            in_equ = "equ" in package_json[package_name] and self.nameKey in package_json[package_name]["equ"]
            if in_package or in_equ:
                loc_name = None
                if package_name[:3] == "act":
                    loc_name = "Act " + package_name[3]
                elif package_name[:2] == "ch":
                    loc_name = "Chapter " + package_name[2]
                if loc_name is not None and loc_name not in self.locations:
                    self.locations.append(loc_name)
    
    def __str__(self):
        accessory_string = "{{-start-}}\n"
        accessory_string += f"'''{self.name}'''\n"

        accessory_string += "{{Accessory\n"

        accessory_string += f"|image={self.nameKey}.png\n"
        accessory_string += f"|description={self.description}\n"
        accessory_string += f"|attack={self.attack}\n"
        accessory_string += f"|hp={self.hp}\n"
        accessory_string += f"|speed={self.speed}\n"
        accessory_string += f"|rarity={self.stars}\n"

        accessory_string += f"|how_to_get=\n"

        # for location in self.locations:
        #     accessory_string += f"*{location}\n"

        accessory_string += "}}\n"

        accessory_string += "{{-stop-}}\n"
        return accessory_string

if __name__ == "__main__":
    english_dict = get_english_dict()
    accessory_dict = Accessory.parse_accessories(english_dict)

    accessory_list = list(accessory_dict.values())
    # print(accessory_list[random.randint(0, len(accessory_list) - 1)])

    # for accessory in accessory_dict.values():
        # print(accessory)
    for accessory in accessory_list:
        print(accessory)


    import os
    with open(os.path.join("Wiki Pages", "Accessories_1.txt"), 'w') as file:
        for accessory in accessory_list[:5]:
            file.write(str(accessory))

    with open(os.path.join("Wiki Pages", "Accessories_2.txt"), 'w') as file:
        for accessory in accessory_list[5:10]:
            file.write(str(accessory))
    
    with open(os.path.join("Wiki Pages", "Accessories_3.txt"), 'w') as file:
        for accessory in accessory_list[10:]:
            file.write(str(accessory))
    # print(os.listdir("."))
    # print(os.path.join("Wiki Pages", "Accessories.txt"))

