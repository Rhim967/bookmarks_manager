from datetime import datetime
import sys, os
import requests
from database import DatabaseManager


# functional commands

def choice_option_is_valid(choice, options):
    return choice in options.keys() or choice.upper() in options.keys()

def choice_option(opts):
    choice = input('choose one option above: ')

    while not choice_option_is_valid(choice, opts):
        print(f'{">"*5} you typed wrong option {"<"*5}')
        choice = input('choose one option above: ')

    return opts[choice.upper()]

def get_user_input(label:str, required:bool=True) -> str|None:
    value = input(f'{label}: ') or None
    while required and not value:
        value = input(f'{label}: ') or None
    return value

def get_new_bookmark_data():
    return {
            'title' : get_user_input('Title'),
            'url' : get_user_input('Url'),
            'notes' : get_user_input('Note', required=False),
            }

def get_bookmark_id_for_delition():
    return get_user_input('enter a bookmark id for delete')

def clear_screen():
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)
# ---------------------------------------------------

db = DatabaseManager('sqlite_bark.db')

class CreateBookmarksTableCommands():
    ''' class for commands to create table '''

    def execute(self):
        db.create_table('bookmarks', {
            'id' : 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'title' : 'TEXT NOT NULL',
            'url' : 'TEXT NOT NULL',
            'notes' : 'TEXT',
            'created_data' : 'TEXT NOT NULL',
            })


class AddBookmarksCommand():
    ''' class for commands to create member in db_table '''

    def execute(self, data:dict, timestamp=None) -> str:

        data['created_data'] = timestamp or datetime.utcnow().isoformat()
        db.add('bookmarks', data)

        #print(data)
        message = f'{"*" * 5} {data["title"]} {"*" * 5} was added successfuly'
        return message


class ListBookmarksCommand():
    ''' class for displaing bookmarks from db '''

    def __init__(self, order_by='created_data', criteria={}):
        self.order_by = order_by
        self.criteria = criteria

    def execute(self) -> list:
        result = db.select('bookmarks', criteria=self.criteria, 
                ordered_by=self.order_by).fetchall()

        keys = ('id', 'title', 'url', 'note', 'created_at')
        list_of_bookmarks = []
        for vlues in result:
            bookmark_item = dict(zip(keys, vlues))
            list_of_bookmarks.append(bookmark_item)

        print(f'\n you have {len(list_of_bookmarks)} bookmarks \n')
        return list_of_bookmarks


class ImportGithubStars:
    def _get_bookmark_info(self, repo):
        return {
                'title': repo['name'],
                'url': repo['html_url'],
                'notes': repo['description'],
                }
    def execute(self, data:dict):
        bookmarks_imported = 0

        username = data['username']

        next_page_of_result = f'https://api.github.com/users/{username}/starred'

        while next_page_of_result:
            star_res = requests.get(
                next_page_of_result, 
                headers={'Accept':'application/vnd.github.v3.star+json'}
                )

            next_page_of_result = star_res.links.get('next', {}).get('url')

            for repo_info in star_res.json():
                repo = repo_info['repo']

                if data['preserve_timestamp']:
                    timestamp = datetime.strptime(repo_info['starred_at'], \
                            '%Y-%m-%dT%H:%M:%SZ')
                else:
                    timestamp = None

                AddBookmarksCommand().execute(
                        self._get_bookmark_info(repo),
                        timestamp=timestamp
                        )
                bookmarks_imported += 1

        return f'imported {bookmarks_imported} bookmarks from starred repo'



class DeleteBookmarksCommand():
    def execute(self, data):
        db.delete('bookmarks', {'id':data})
        return f'bookmark number {data} deleted succesfuly'


class QuitCommand():
    def execute(self):
        print('bye bye')
        sys.exit()




