"""Minecraft-Villager-Trade-Data

This script connects to the Minecraft wiki, parses the villager trade
information, and saves it to a file for offline viewing.

If there is a file already present, it will simply read from the file.
Otherwise, it will connect to the website.

Dependencies:
* requests
* BeautifulSoup
"""

import requests, json, os.path, sys, re
from typing import TextIO
from bs4 import BeautifulSoup, Tag

file_path_villager_data = os.path.join(sys.path[0], 'villager-data.json')
active = True
display_mode = 'simple'


#################################################
#                     Main                      #
#################################################

def main() -> None:
    """driver function"""

    clear()
    print(  
            'Welcome to Minecraft Villager Trade Data! '+ 
            'This script saves villager trade data from the Minecraft Wiki ' +
            'in a JSON file for use with this script, so that you can ' +
            'view the information offline. The script will automatically ' +
            'create the file for you if it does not exist.'
        )
    
    while active:
        choice = display_options()
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
    

     
#################################################
#                   Homepages                   #
#################################################

def display_options() -> None:
    """Displays the menu options to the user
    """
    print(
            'Please choose from the following options:\n' +
            '(1) Display all trades\n',
            '(2) Search by criteria\n',
            '(3) Check for updates\n',
            '(4) Change display mode\n',
            '(5) Exit'
        )
    
    try:
        result = int(input())
        if result < 1 and result > 4:
            raise TypeError('Please enter an option from 1 to 4')
    except Exception as e:
        handle_error(e, 'display_options()')
        return -1


def display_all_trades():
    """Displays all villager trades to the user
    """
    file = get_data()

    if file is None:
        exit(1)

    display_data(file)


def search():
    pass


def check_for_updates():
    pass


def change_display_mode() -> None:
    """Prompts the user to change the display mode
    """

    print('Current display mode: ' + display_mode + '\n')
    print(
        'Display Modes\n' +
        '-------------\n' +
        '*Each display mode includes the features of the previous ones*\n' +
        'Simple:\n' +
        '   * item(s) wanted' +
        '   * item(s) given' +
        'Complex:\n' +
        '   * amount of item(s) wanted' +
        '   * amount of item(s) given' +
        'Full:\n' +
        '   * xp given to villager' +
        '\n'
    )
    print(
        'Choose a display mode:\n' + 
        '(1) Simple\n' +
        '(2) Complex\n' +
        '(3) Full'
    )
    


#################################################
#                 File Handling                 #
#################################################

def get_data() -> TextIO:
    """Gets the file containing villager info

    Returns
    -------
    TextIO
        file containing villager data
    """
    if not os.path.isfile(file_path_villager_data):
        if not create_file():
            return

        with open(file_path_villager_data, 'w') as f:
            dom = connect()
            job_sites, trade_tables = get_list(dom)
            data = make_into_dicts(job_sites, trade_tables)
            write_to_file(f, data)

    return open_file()


def create_file() -> bool:
    """Create file for local storage of villager data

    Returns
    -------
    bool
        true,  if file was created successfully /
        false, otherwise
    """
    try:
        with open(file_path_villager_data, 'w'):
            ret = True
        print('file created successfully')

    except IOError as e:
        handle_error(e, 'create_file()')
        print('error creating file')
        ret = False

    finally:
        return ret


def open_file() -> TextIO:
    """Opens file for reading

    Returns
    -------
    TextIO
        file that was opened,
        None, if there was an error opening the file
    """

    try:
        with open(file_path_villager_data, 'r') as f:
            data = json.load(f)
        print('file opened successfully')

    except IOError:
        print('error: could not read from file')
        data = None

    finally:
        return data
    

def write_to_file(file: TextIO, data: list[dict]) -> None:
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

    except:
        print('error writing to file')



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
    tuple
        a tuple that contains both job sites and trade tables
    """

    ##### The wiki is *very* annoyingly formatted so parsing isn't as
    ##### simple as it should be

    # get job sites for each profession
    job_sites_span = dom.select('h3 ~ p > a[href^="/wiki/"] > span > span.sprite-text')

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
    list
        a list of dicts holding the data of villager trades
    """

    villager_data = []  # stores all the villager trade data

    # traverse the tables
    for i, table in enumerate(data):

        info = {}
        table_rows = table.select('tr')

        # tr[0] = <PROFESSION> Economic Trade
        profession = table_rows[0].contents[1].get_text().split(' ')[0].lower().strip()
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

                # first row has additional table header changing format
                columns = [content for content in row.contents if content.get_text() != '\n']
                if first_row:
                    columns = columns[1:]
                    first_row = False

                # actually get the trade info
                remove_notes = '\[note \d\]'
                item_wanted           = [re.sub(remove_notes, '', columns[0].get_text().strip())]
                default_quantity      = [re.sub(remove_notes, '', columns[1].get_text().strip())]
                price_multiplier      = re.sub(remove_notes, '', columns[2].get_text().strip())
                item_given            = re.sub(remove_notes, '', columns[3].get_text().strip())
                quantity              = re.sub(remove_notes, '', columns[4].get_text().strip())
                trades_until_disabled = re.sub(remove_notes, '', columns[5].get_text().strip())
                xp_to_villager        = re.sub(remove_notes, '', columns[6].get_text().strip())

                # if there are multiple items wanted for a trade
                if '\n' in item_wanted[0]:
                    item_wanted = item_wanted[0].split('\n')
                    default_quantity = default_quantity[0].split(' ')

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

    # ─ │ ┌ ┐ └ ┘

    for profession in villagers:
        print_centered( '┌──────────────────────────────────────┐')
        print_centered(f'│{profession["profession"].title().center(38)}│')
        print_centered( '└──────────────────────────────────────┘')

        trades = profession['trades']

        for trade in trades:
            print_centered( '┌───────────────────────┐')
            print_centered(f'│{trade["level"].title().center(23)}│')
            print_centered( '└───────────────────────┘')

            for exchange in trade['exchanges']:
                # simple
                wanted = exchange['wanted']
                given = exchange['given']
                wanted_string = ', '.join(wanted['item'])
                if display_mode == 'simple':
                    print_centered(wanted_string + ' -> ' + given['item'])
                    continue

                # complex
                if display_mode == 'complex':
                    # TODO complex mode
                    continue

                # full
                # TODO full mode

        print('=' * 50)


def print_centered(text: str) -> None:
    """Prints the given text with a center value of 50

    Parameters
    ----------
    text : str
        the text to be printed
    """

    print(text.center(50))


def clear() -> None:
    """Clears the interpreter console
    """

    os.system('cls')


#################################################
#                Error Handling                 #
#################################################

def handle_error(error: Exception, function: str) -> None:
    """Displays error message and what function the error occurred in

    Parameters
    ----------
    error : Exception
        the exception that was raised
    function : str
        the name of the function that the expection was raised in
    """

    print('Error in function: ' + function)
    print(type(error))
    print(error)
    input('Press Enter to continue\n')




if __name__ == '__main__':
    main()