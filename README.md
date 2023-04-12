# Minecraft-Villager-Trade-Data

Scrapes https://minecraft.fandom.com/wiki/Trading to get the villager trade information and saves the data to a file so I don't have to open the wiki 100 times a day. \
This is a command line tool.

## Features
* access https://minecraft.fandom.com/wiki/Trading
* write data to JSON file
* read data from JSON file
* display the data on the command line
* ask to write output to a file
* start menu
    * display all trades
    * search by item wanted
    * search by item given
    * search by profession
    * check for updates
        * update data
* different display options (simple, complex, full)
    

## Using the script
Download the code, and in the base directory, create the virtual environment:
```sh
$ pipenv shell
```

Once the venv is created and you have entered the shell, install the dependencies:
```sh
$ pipenv install
```

Now you can run the script itself:
```sh
$ py main.py
```

<!--
Ensure you have Python installed (this script has been checked to work with Python 1.11.2, but it should also work with other Python versions). Follow [this guide](https://gist.github.com/danilo-montes/2a2239035e689dfeafa0b7a59fed8c60) to install Python if you don't have it (Python does not come by default in Windows, so you probably need to install it). 

Now, download the code of the project by clicking the "Code" button next to the "About" section and clicking "Download ZIP". Extract this zip where you want it, it's easiest to extract it to the Desktop.
Open your terminal (cmd.exe) / bash and navigate to the extracted folder. If it is on the Desktop, it will be at `C:\Users\<USERNAME>\Desktop\Minecraft-Villager-Trade-Data-main`. To navigate to this folder, type the command `cd Desktop`. 

In `cmd.exe`:
```sh
py main.py
```

In bash:
```sh
$ py main.py
``` -->

## Planned Features
* grouping functions in classes, moving script to src/.../ format