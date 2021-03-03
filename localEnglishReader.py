class localEnglishReader:
    def __init__(self):
        self.dictionary = {}
        with open("Localizable_English.txt", "r", encoding="utf8") as file:
            for line in file:
                split_line = line.split("=")
                if len(split_line) == 2:
                    self.dictionary[split_line[0].strip("\"")] = split_line[1].strip("\"")

    def get(self, key):
        return self.dictionary[key][:-2].replace("\\n", "\n")
    
    def getDescriptionKey(self, itemName):
        return self.get(itemName + "DescriptionKey")
    
    def getNameKey(self, itemName):
        return self.get(itemName + "NameKey")
    
    def getItemData(self, itemName):
        return (self.getNameKey(itemName), self.getDescriptionKey(itemName))
    
    def keyExists(self, key):
        return key in self.dictionary.keys()

if __name__ == "__main__":
    lER = localEnglishReader()
    print(lER.get("evomirrormid"))