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
    * search by item wanted by villager
    * search by item given by villager
    * search by profession
    * check for updates
        * update data
* different display options (simple, complex, full)
* command line args for quick use


## Using the script
Download the code, and in the base directory, `/Minecraft-Villager-Trade-Data-1.x.x`, create the virtual environment and install dependencies:
```sh
$ pipenv install
```

Once the venv is created and you have installed the dependencies:
```sh
$ pipenv shell
```

Navigate to the `src` directory and run the script:
```sh
$ cd src
$ py main.py
```


## Command line args
To avoid having to navigate the menus, you can provide command line arguments to make a query run immediately. Supply arguments as follows:
```sh
$ py main.py [ARG] [QUERIES,]
```
* ARG - argument flag for the requested operation
* QUERIES - list of queries given to the respective operation

**ARG**
* -w : search for item wanted by villager
* -g : search for item given by villager
* -p : search for profession

**QUERIES**
* space separated list of items/jobs to search for
* *terms with spaces surrounded with double quotes*

Example Usage
```sh
$ py main.py -p mason
$ py main.py -g "enchanted diamond"
```


## Installing Python
Ensure you have Python installed (this script has been checked to work with Python 1.12.1, but it should also work with other Python versions). Follow [this guide](https://gist.github.com/danilo-montes/2a2239035e689dfeafa0b7a59fed8c60) to install Python if you don't have it (Python does not come by default in Windows, so you probably need to install it). 

Now, download the code of the project by clicking the "Code" button next to the "About" section and clicking "Download ZIP". Extract this zip where you want it, it's easiest to extract it to the Desktop.
Open your terminal (cmd.exe) / bash and navigate to the extracted folder. If it is on the Desktop, it will be at `C:\Users\<USERNAME>\Desktop\Minecraft-Villager-Trade-Data-1.x.x`, with the `x`s as standins for version numbers. To navigate to this folder, type the command `cd Desktop` and then `cd Minecraft-Villager-Trade-Data-1.x.x` (you should be able to press Tab to autocomplete the long name). The bar should read `C:\Users\<USERNAME>\Desktop\Minecraft-Villager-Trade-Data-1.x.x`.

If you would like to use `pipenv`, as the `Using the script` section describes, in `cmd.exe` or bash, run the command:
```sh
pip install pipenv
```
and then follow the instructions under the `Using the script` section.


Otherwise, you can use Python just the same, with a bit more setup.

First, you have to install the dependencies:
```sh
pip install PyYAML beautifulsoup4 requests
```

Then, to run the script:
```sh
cd src
py main.py
```