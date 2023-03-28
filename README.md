# Minecraft-Villager-Trade-Data

Scrapes https://minecraft.fandom.com/wiki/Trading to get the villager trade information and saves the data to a file so I don't have to open the wiki 100 times a day. \
This is a command line tool.

## Features
* access https://minecraft.fandom.com/wiki/Trading
* write data to JSON file
* read data from JSON file
* display the data on the command line

## Using the script
Ensure you have Python installed (this script has been checked to work with Python 1.11.2, but it should also work with other Python versions). Download Python [here](https://www.python.org/downloads/) if you do not have Python on your computer. If you are on Windows, **ensure you click the option to "add Python to PATH" when installing**, so your computer can find your Python installation.

Now, download the code of the project by clicking the "Code" button next to the "About" section and clicking "Download ZIP". Extract this zip where you want it, it's easiest to extract it to the Desktop.
Open your terminal (cmd.exe) / bash and navigate to the extracted folder. If it is on the Desktop, it will be at `C:\Users\<USERNAME>\Desktop\Minecraft-Villager-Trade-Data-main`.

In `cmd.exe`:
```sh
py main.py
```

In bash:
```sh
$ py main.py
```

## Planned Features
* command line arguments for getting only given professions
* different display options (simple, complex, full)
* ask to write output to a file (https://stackoverflow.com/questions/47699023/how-to-write-console-output-on-text-file)
* searching for trades via items wanted/given
* check for updated data