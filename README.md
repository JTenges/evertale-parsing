# Evertale to wiki parsers

This repository contains parsers to read in Evertale game files
and generate wikia pages from it.

The game files i have used were from the android version of the
game as of 01/08/2020.

The files generated are for the template on the evertale wikia
 - [Monster page](https://evertale.fandom.com/wiki/Template:Monster)
 - [Accessory page](https://evertale.fandom.com/wiki/Template:Accessory)
 - [Item page](https://evertale.fandom.com/wiki/Template:Item)

The monster parser on the main branch is not completed since the
one used in the 'old-monster' branch already parsed the monsters and i was lazy to redo it just to make it more readable.

You will have to modify the main methods of the parsers to get it to generate the wikia txt files.

To upload the pages i used the [PyWikiBot](https://www.mediawiki.org/wiki/Manual:Pywikibot) specifically the [upload](https://www.mediawiki.org/wiki/Manual:Pywikibot/upload.py) and [replace](https://www.mediawiki.org/wiki/Manual:Pywikibot/replace.py) scripts.

To run the bot first set it up as specified [here](https://www.mediawiki.org/wiki/Manual:Pywikibot/Installation) and run one of the following in your shell after running the parsers:
 - python pwb.py pagefromfile <path_to_wikia_folder> -notitle

If you have a lot of imaged to upload you can also run:
 - python pwb.py upload -keep <path_to_image_folder> <description>

The replace script is used to fix already made wiki pages so be careful with using it and used at your own discretion.