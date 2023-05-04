"""Minecraft Villager Trade Data

This script connects to the Minecraft wiki, parses the villager trade
information, and saves it to a file for offline viewing.

If there is a file already present, it will simply read from the file.
Otherwise, it will connect to the website.

Dependencies:
* requests
* BeautifulSoup
* pyyaml
"""

# python native
import json, os.path, sys, re, getopt
from pathlib import Path
from typing import TextIO

# install required
import requests
from bs4 import BeautifulSoup, Tag

# in project
from classes.file_handler import FileHandler
from classes.file_json import JSONFile


SCRIPT_ROOT = sys.path[0]
FILE_PATH_VILLAGER_DATA = os.path.join(SCRIPT_ROOT, 'data', 'villager-data.json')
FILE_PATH_OUTPUT = os.path.join(SCRIPT_ROOT, 'data', 'data-output.txt')
DEVELOPING = True
MAX_WIDTH = 80
CONFIG = {
    'display-mode'     : 'simple',  # controls the display mode of data
    'display-job-site' : False
}
VILLAGER_DATA = FileHandler('villager-data.json', JSONFile())
# SAVED_DATA = FileHandler('data-output.txt', TxtFile())
# CONFIG = FileHandler('config.yaml', YAMLFile(), '')


#################################################
#                     Main                      #
#################################################

def main() -> None:
    """Driver function, runs the main script loop"""

    # if command line args were given, exit program after done
    if handle_args():
        exit(0)

    active = True  # controls the script runtime loop

    clear()
    print(  
            'Welcome to Minecraft Villager Trade Data!\n'+ 
            'This script saves villager trade data from the Minecraft Wiki ' +
            'in a JSON file for use with this script,\n' +
            'so that you can view the information offline.\n' +
            'The script will automatically ' +
            'create the file for you if it does not exist.\n'
        )
    
    while active:
        choice = display_menu()
        if choice == -1:
            clear()
            continue
        
        if choice == 1:
            display_all_trades()
        elif choice == 2:
            search()
        elif choice == 3:
            check_for_updates()
        elif choice == 4:
            change_display_mode()
        else:
            active = False
            continue

    return
    

     
#################################################
#                   Homepages                   #
#################################################

def display_menu() -> int:
    """Displays the menu options to the user and gets their response
    
    Returns
    -------
    int
        the choice the user selected
    """

    return display_options(
        'Please choose from the following options',
        [
            'Display all trades',
            'Search by criteria',
            'Check for updates',
            'Change display mode',
            'Exit'
        ]
    )
        

def display_all_trades() -> None:
    """Displays all villager trades to the user"""
    
    file = get_data()

    if file is None:
        print('Exiting...')
        exit(1)

    display_data(file)
    prompt_to_save(file)

    return


def search() -> None:
    """Enables the user to search for a trade based on criteria"""

    clear()
    
    choice = display_options(
        'What do you want to search by?',
        [
            'Item Wanted',
            'Item Given',
            'Profession',
        ],
        backable=True
    )

    if choice == 0:
        clear()
        return

    if choice == 3:
        query = input('Enter your desired professions, separated by spaces: ')
        queries = tuple([prof.lower() for prof in query.split(' ')])
    else:
        query = input('Enter the items, separated by commas: ')
        queries = tuple([item.strip().lower() for item in query.split(',')])

    execute_search(choice, queries)

    clear()
    return


def check_for_updates() -> None:
    """Checks for discrepancies between local and wiki data"""
    
    clear()

    # verify that file exists to compare in the first place
    if not os.path.isfile(FILE_PATH_VILLAGER_DATA):
        print(
            'There is no file to compare to, please first select ' +
            'option 1 on the main menu' 
        )
        return
    
    file = get_data()

    if file is None:
        print('Exiting...')
        sys.exit(1)

    # get data from wiki to compare
    dom = connect()
    job_sites, trade_tables = get_list(dom)
    data = make_into_dicts(job_sites, trade_tables)

    if file == data:
        print('Local data is up to date')
    else:
        print('Local data is out of sync with wiki.')

        choice = display_options(
            'Would you like to update the data?',
            [
                'Yes',
                'No'
            ],
            backable=False
        )

        if choice == 1:
            with open(FILE_PATH_VILLAGER_DATA, 'w') as f:
                write_to_file_json(f, data)
            print('data updated')

    etc()
    clear()

    return


def change_display_mode() -> None:
    """Prompts the user to change the display mode"""

    display_mode = CONFIG['display-mode']

    clear()
    print(f'Current display mode: {display_mode}\n')
    print(
        'Display Modes\n' +
        '-------------\n' +
        '*Each display mode includes the features of the previous ones*\n\n' +
        'Simple:\n' +
        '   * item(s) wanted\n' +
        '   * item(s) given\n' +
        'Complex:\n' +
        '   * amount of item(s) wanted\n' +
        '   * amount of item(s) given\n' +
        '   * price multiplier\n' +
        'Full:\n' +
        '   * xp given to villager\n' +
        '   * trades until disabled\n' +
        '*You can also toggle displaying the respective job site block*\n'
    )

    options = [
        'Simple',
        'Complex',
        'Full',
        'Toggle Job Site Block'
    ]

    choice = display_options(
        'Choose a display mode',
        options,
        backable=True
    )

    if choice == 0:
        clear()
        return

    if choice == 4:
        site = CONFIG['display-job-site']
        CONFIG['display-job-site'], site = not site, not site

        if site:
            print('Job site is now: On')
        else:
            print('Job site is now: Off')
    
    else:
        CONFIG['display-mode'] = options[choice-1].lower()
        print(f'Display mode now: {CONFIG["display-mode"]}')

    etc()
    clear()
    return
    


#################################################
#               Homepage Functions              #
#################################################

def handle_args() -> bool:
    """Handles the command line arguments, if any are present

    Returns
    -------
    bool
        True, if there were command line arguments \n
        False, otherwise
    """

    args_list = sys.argv
    if len(args_list) == 1:
        return False
    
    try:
        options, queries = getopt.getopt(args_list[1:], 'wgp')
        if len(options) == 0 or len(queries) == 0:
            raise getopt.GetoptError('incorrect format')
    except getopt.GetoptError:
        print(
            'Use the following format for command line arguments:\n\n' +
            'py main.py [ARG] [QUERIES,]\n' +
            '* ARG - argument flag for the requested operation\n' +
            '* QUERIES - list of queries given to the respective operation\n' +
            '\nARG\n' +
            '* -w : search for item wanted\n' +
            '* -g : search for item given\n' +
            '* -p : search for profession\n' +
            '\nQUERIES\n' +
            'space separated list of items/jobs to search for, ' +
            'terms with spaces surrounded with double quotes\n' +
            '\nExample Usage\n' +
            'py main.py -p mason\n' +
            'py main.py -g "enchanted diamond"\n'
        )
        exit(2)

    flag = options[0][0]
    flags = ['', '-w', '-g', '-p']

    print(flag)
    print(queries)

    execute_search(flags.index(flag), queries)

    return True


def get_data() -> list[dict]:
    """Gets the file containing villager info

    Returns
    -------
    list
        list of dicts containing villager data
    """

    if not os.path.isfile(FILE_PATH_VILLAGER_DATA):
        if not create_dir() or not create_file(FILE_PATH_VILLAGER_DATA):
            return None

        with open(FILE_PATH_VILLAGER_DATA, 'w') as f:
            dom = connect()
            job_sites, trade_tables = get_list(dom)
            data = make_into_dicts(job_sites, trade_tables)
            write_to_file_json(f, data)

    return open_file_json(FILE_PATH_VILLAGER_DATA)


def prompt_to_save(data: list[dict], path: str=FILE_PATH_OUTPUT) -> None:
    """Prompt the user to save the console output to a file

    Parameters
    ----------
    data : list[dict]
        the data to be saved
    path : str
        the path of the file to save into
    """

    option = display_options(
        'Would you like to save the output to a file?',
        [
            'Yes',
            'No'
        ],
        backable=False
    )

    if option == 1:
        if create_file(path):
            with open(path, 'w') as f:
                out = sys.stdout
                sys.stdout = f
                display_data(data)
                sys.stdout = out
            etc()

    clear()
    return


def execute_search(choice: int, queries: tuple[str]) -> None:
    """Gets the data and performs the search based on given queries
    
    Parameters
    ----------
    choice : int
        the int corresponding to the user's search query
    queries : tuple(str)
        the individual search queries
    """

    data = get_data()

    if data is None:
        print('Exiting...')
        exit(1)

    results = []

    if choice == 3:
        for profession in data:
            if profession['profession'] in queries:
                results.append(profession)

    else:
        for profession in data:
            temp_prof = {
                'profession'     : profession['profession'],
                'job-site-block' : profession['job-site-block'],
                'trades'         : []
            }

            for trade in profession['trades']:
                temp_trade_level = {
                    'level'     : trade['level'],
                    'exchanges' : []
                }

                for exchange in trade['exchanges']:
                    if choice == 1:
                        for item in exchange['wanted']['item']:
                            found = False
                            # gets cases of only part of item being in query
                            # i.e. 'quartz' in 'quartz pillar'
                            for query in queries: 
                                if query in item.lower():
                                    temp_trade_level['exchanges'].append(exchange)
                                    found = True
                                    break

                            if found:
                                break
                    else:
                        for query in queries: 
                            if query in exchange['given']['item'].lower():
                                temp_trade_level['exchanges'].append(exchange)
                                break
                    
                if temp_trade_level['exchanges'] != []:
                    temp_prof['trades'].append(temp_trade_level)

            if temp_prof['trades'] != []:
                results.append(temp_prof)
                    
    
    if results == []:
        print('no results found')
        etc()
    else:        
        display_data(results)
        prompt_to_save(results)


    return



#################################################
#                 File Handling                 #
#################################################

def create_dir(path: str = 'data') -> bool: 
    """Create directory from the root of the script

    Parameters
    ----------
    path : str
        path of the directory to be created

    Returns
    -------
    bool
        True,  if directory was created successfully \n
        False, otherwise
    """

    ret = False
    try:
        Path(path).mkdir()
        ret = True

    except FileExistsError as e:
        handle_error(e, 'create_dir()', 
                     'error creating data directory')

    except Exception as e:
        handle_error(e, 'create_dir()', 
                     'erroneous error creating data directory')

    finally:
        return ret


def create_file(path: str) -> bool:
    """Create file for local storage of villager data

    Parameters
    ----------
    path : str
        path of the file to be created

    Returns
    -------
    bool
        True,  if file was created successfully \n
        False, otherwise
    """

    try:
        with open(path, 'w'):
            ret = True
        print('file created successfully')

    except IOError as e:
        handle_error(e, 'create_file()', 'error creating file')
        ret = False

    except Exception as e:
        handle_error(e, 'create_file()', 'erroneous error creating file')
        ret = False

    finally:
        return ret


def open_file_json(path: str) -> list[dict]:
    """Opens JSON file for reading

    Parameters
    ----------
    path : str
        path of the file to be opened

    Returns
    -------
    list[dict]
        data from file \n
        None, if there was an error opening the file
    """

    try:
        with open(path, 'r') as f:
            data = json.load(f)

    except IOError as e:
        handle_error(e, 'open_file()', 'error opening file')
        data = None

    except Exception as e:
        handle_error(e, 'open_file()', 'erroneous error opening file')
        data = None

    finally:
        return data
    

def open_file_txt(path: str) -> list[str]:
    """Opens text file for reading

    Parameters
    ----------
    path : str
        path of the file to be opened

    Returns
    -------
    list[str]
        lines from file \n
        None, if there was an error opening the file
    """

    try:
        with open(path, 'r') as f:
            data = f.readlines()

    except IOError as e:
        handle_error(e, 'open_file()', 'error opening file')
        data = None

    except Exception as e:
        handle_error(e, 'open_file()', 'erroneous error opening file')
        data = None

    finally:
        return data
    

def write_to_file_json(file: TextIO, data: list[dict]) -> None:
    """Writes JSON to file
    
    Parameters
    ----------
    file : TextIO
        file to write data to
    data : list[dict]
        list of dictionaries to write to file
    """
    
    try:
        json.dump(data, file, ensure_ascii=False, indent=2)
        print('success writing to file')

    except Exception as e:
        handle_error(e, 'write_to_file_json()', 'error writing to file')
    
    return


def write_to_file_txt(file: TextIO, data: list[str]) -> None:
    """Writes text to file
    
    Parameters
    ----------
    file : TextIO
        file to write data to
    data : list[str]
        lines of text to write to file
    """
    
    try:
        file.writelines(line + '\n' for line in data)
        print('success writing to file')

    except Exception as e:
        handle_error(e, 'write_to_file_text()', 'error writing to file')
    
    return



#################################################
#              Connecting and DOM               #
#################################################

def connect() -> BeautifulSoup:
    """Connects to the Minecraft Wiki Trading page

    Returns
    -------
    BeautifulSoup
        a BeautifulSoup object representing the DOM of the website
    """

    URL = "https://minecraft.fandom.com/wiki/Trading"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    return soup


def get_list(dom: BeautifulSoup) -> tuple[list[str], list[Tag]]:
    """Parses the DOM to get the required tables and job sites

    Parameters
    ----------
    dom : BeautifulSoup
        the DOM of the website

    Returns
    -------
    tuple[list[str], list[Tag]
        a tuple that contains both job sites and trade tables
    """

    ##### The wiki is *very* annoyingly formatted so parsing isn't as
    ##### simple as it should be

    # get job sites for each profession
    job_sites_span = dom.select(
        'h3 ~ p > a[href^="/wiki/"] > span > span.sprite-text'
    )

    job_sites = []
    for job in job_sites_span:
        job_sites.append(job.get_text().lower())

    job_sites = job_sites[:13]

    # get tables related to villager trades
    tables = dom.select('h3 + p + figure + table.wikitable')

    # get mason table (due to extra note making it not appear before)
    mason_table = dom.select_one('h3 + p + figure + div + table.wikitable')
    tables = tables[:13]

    # shift array down and place mason in right position
    for i in range(len(tables) - 1, 8, -1):
        tables[i] = tables[i-1]
    tables[9] = mason_table

    return (job_sites, tables)



#################################################
#                 Data Handling                 #
#################################################

'''
JSON format of villager records
{
    "profession" : <PROFESSION>,
    'job-site-block' : <JOB SITE BLOCK>,
    "trades" : [
        {
            "level" : <LEVEL>,
            "exchanges" : [
                {
                    "wanted" : {
                        'item' : [<ITEM>],
                        'default-quantity' : [<NUMBER>],
                        'price-multiplier' : <NUMBER>
                    },
                    "given"  : {
                        'item' : <ITEM>,
                        'quantity' : <NUMBER>,
                    },
                    'trades-until-disabled' : <NUMBER>,
                    'xp-to-villager' : <NUMBER>
                },
                ...
            ]
        },
        ...
    ]
}
'''
def make_into_dicts(job_sites: list[str], data: list[Tag]) -> list[dict]:
    """Traverses the tables to assemble the JSON for storage

    Parameters
    ----------
    job_sites : list[str]
        list of job site blocks for each villager
    data : list[Tag]
        list of tables containing villager trade info

    Returns
    -------
    list[dict]
        a list of dicts holding the data of villager trades
    """

    villager_data = []  # stores all the villager trade data

    # traverse the tables
    for i, table in enumerate(data):

        info = {}
        table_rows = table.select('tr')

        # tr[0] = <PROFESSION> Economic Trade
        profession = table_rows[0].contents[1] \
                    .get_text().split(' ')[0].lower().strip()
        info['profession'] = profession
        info['job-site-block'] = job_sites[i]


        # tr[2] = Novice row, includes first trade
        #         has attr 'rowspan' that holds the number of trades

        row_tracker = 2  # track the rows in the table
        trades = []  # holds the trade info

        # handle each level of trade
        for i in range(5):

            trade_level = {}

            top_row = table_rows[row_tracker].contents[1]
            if top_row.has_attr('rowspan'):
                num_of_trades = int(top_row['rowspan'])
            else:
                num_of_trades = 1

            trade_level_string = top_row.get_text().lower().strip()
            trade_level['level'] = trade_level_string

            rows = table_rows[row_tracker : row_tracker+num_of_trades]
            row_tracker += num_of_trades

            exchanges = []

            # handle each trade within a level
            first_row = True
            for row in rows:

                exchange_info = {}
                columns = [
                    content for content in row.contents 
                    if content.get_text() != '\n'
                ]

                # first row has additional table header changing format
                if first_row:
                    columns = columns[1:]
                    first_row = False

                # actually get the trade info
                remove_notes = '\[note \d+\]'

                wanted = columns[0]
                # if there are multiple items wanted for a trade
                if wanted.find('br'):
                    if not (profession == 'fisherman'
                            and trade_level_string == 'master'):
                        item_wanted  = [
                            re.sub(remove_notes, ' ', item) 
                            for item in columns[0]
                            .get_text(separator='\n', strip=True).split('\n')
                        ]
                    # handle case of fisherman trade with 
                    # multiple possible items given
                    else:
                        res = ' '.join(
                            columns[0].get_text(separator='\n', strip=True)
                            .split('\n')
                        )
                        item_wanted  = [re.sub(remove_notes, ' ', res).strip()]

                    default_quantity = [
                        re.sub(remove_notes, ' ', quantity)
                        for quantity 
                        in columns[1].get_text(separator='\n', strip=True)
                        .split('\n')
                    ]
                else: 
                    item_wanted       = [re.sub(remove_notes, ' ', 
                                                columns[0]
                                                .get_text(strip=True)).strip()]
                    default_quantity  = [re.sub(remove_notes, ' ', 
                                                columns[1]
                                                .get_text(strip=True)).strip()]

                price_multiplier      = re.sub(remove_notes, ' ', 
                                               columns[2]
                                               .get_text(strip=True)).strip()

                give = columns[3]
                if give.find('br'):
                    res = ' '.join(
                        give.get_text(separator='\n', strip=True).split('\n')
                    )
                    item_given        = re.sub(remove_notes, ' ', res).strip()
                else:
                    item_given        = re.sub(remove_notes, ' ', 
                                               columns[3]
                                               .get_text(strip=True)).strip()
                quantity              = re.sub(remove_notes, ' ', 
                                               columns[4]
                                               .get_text(strip=True)).strip()
                trades_until_disabled = re.sub(remove_notes, ' ', 
                                               columns[5]
                                               .get_text(strip=True)).strip()
                xp_to_villager        = re.sub(remove_notes, ' ', 
                                               columns[6]
                                               .get_text(strip=True)).strip()

                exchange_info['wanted'] = {
                    'item'             : item_wanted,
                    'default-quantity' : default_quantity,
                    'price-multiplier' : price_multiplier
                }
                exchange_info['given'] = {
                    'item'     : item_given,
                    'quantity' : quantity
                }
                exchange_info['trades-until-disabled'] = trades_until_disabled
                exchange_info['xp-to-villager'] = xp_to_villager

                exchanges.append(exchange_info)


            trade_level['exchanges'] = exchanges


            trades.append(trade_level)

        info['trades'] = trades

        villager_data.append(info)

    return villager_data



#################################################
#                    Display                    #
#################################################

def display_data(villagers: list[dict]) -> None:
    """Displays the given villager data

    Parameters
    ----------
    villagers : list[dict]
        list of infomation regarding villager trades to be printed
    """

    display_mode = CONFIG['display-mode']
    display_job_site = CONFIG['display-job-site']

    for profession in villagers:
        print_centered( '+--------------------------------------+')
        print_centered(f'|{profession["profession"].title().center(38)}|')
        if display_job_site:
            print_centered('|' + f'Job Site: {profession["job-site-block"].title()}'.center(38) + '|')
        print_centered( '+--------------------------------------+')

        trades = profession['trades']

        for trade in trades:
            print_centered( '+-----------------------+')
            print_centered(f'|{trade["level"].title().center(23)}|')
            print_centered( '+-----------------------+')

            for exchange in trade['exchanges']:
                wanted = exchange['wanted']
                given = exchange['given']
               
                if display_mode == 'simple':
                    wanted_string = ', '.join(wanted['item'])
                    print_centered(wanted_string + ' -> ' + given['item'])
                    continue

                # complex
                wanted_parts = []

                for i in range(len(wanted['item'])):
                    wanted_parts.append(
                        wanted['default-quantity'][i] + ' ' + wanted['item'][i])

                wanted_string = ', '.join(wanted_parts)
                given_string = given['quantity'] + ' ' + given['item']

                print_centered(wanted_string + 
                                ' -<' + wanted['price-multiplier'] + '>-> ' +
                                given_string)

                if display_mode == 'complex':
                    continue

                full_string = exchange['xp-to-villager'] + ' XP to villager' \
                            + ', ' + exchange['trades-until-disabled'] + \
                              ' until disabled'
                            
                # full
                print_centered(full_string)
                print()
                
        print('=' * MAX_WIDTH)

    return


def print_centered(text: str) -> None:
    """Prints the given text with a center value of 50

    Parameters
    ----------
    text : str
        the text to be printed
    """

    print(text.center(MAX_WIDTH))
    return


def clear() -> None:
    """Clears the interpreter console"""

    print('-'*int(MAX_WIDTH*5/4))
    return



#################################################
#                Runtime Handling               #
#################################################

def handle_error(error: Exception, function: str, default_error: str) -> None:
    """Displays error message and what function the error occurred in.
    Either displays the full error message or just the error text,
    depending on whether the script is being developed or not.

    Parameters
    ----------
    error : Exception
        the exception that was raised
    function : str
        the name of the function that the expection was raised in
    default_error : str
        the error message to be displayed to the user, non-technical
        such that the user can more obviously know what to do
    """

    if DEVELOPING:
        print('Error in function: ' + function)
        print(type(error))
        print(error)
    else:
        print(default_error)

    etc()
    return


def display_options(
        prompt: str, 
        options: list[str], 
        backable: bool=False) -> int:
    """Displays the list of options to the user.
    Repeats until a valid option is given.

    Parameters
    ----------
    prompt : str
        question prompt for the user
    options : list[str]
        ordered list of options for the user
    backable : bool
        True,  if the user can go back from the options screen 
        / False, otherwise 

    Returns
    -------
    int
        the option selected by the user \n
        -1 if error raised or invalid response
    """
    
    last_option = len(options)
    option = -1

    while option == -1:
        print(f'{prompt}:')
        if backable:
            print(' (0) Go back')

        for i in range(last_option):
            print(f' ({i+1}) {options[i]}')

        try:
            option = int(input())
            if backable and option == 0:
                continue
            if option < 1 or option > last_option:
                raise TypeError('number out of bounds')
        
        except Exception as e:
            if backable:
                handle_error(e, 'display_options()', 
                             f'Please enter an option from 0 to {last_option}')
            else:
                handle_error(e, 'display_options()', 
                             f'Please enter an option from 1 to {last_option}')
        
    return option


def etc() -> None:
    """Displays prompt to user to press Enter to continue"""

    input('Press Enter to continue\n')
    return



if __name__ == '__main__':
    main()