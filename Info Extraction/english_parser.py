import json

def get_english_dict():
    english_dict = {}
    with open("com.zigzagame.evertale/files/Localizable_English.txt", "r", encoding="utf-8") as file:
        for line in file:
            split_line = line.split("=")
            if len(split_line) == 2:
                english_dict[split_line[0][1:len(split_line[0]) - 1]] = split_line[1][1:len(split_line[1]) - 2]
    return english_dict
        