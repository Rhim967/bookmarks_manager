import commands
import collections

class Option():
    def __init__(self, name, command, prep_call=None):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None

        message = self.command.execute(data) if data \
                else self.command.execute()

        if 'list' in self.name.lower():
            for i in message:
                print('='*35)
                print(f"id: {i['id']}\ntitle: {i['title']}\nurl: {i['url']}\
                        \nnote: {i['note']}\ncreated: {i['created_at']}")
        else: 
            print(message)

    def __str__(self):
        return self.name

def print_options(options):
    for shortcut, option in options.items():
        print(f'({shortcut}) - {option} \n', end='')

options = collections.OrderedDict({
    'A' : Option('Add bookmark', commands.AddBookmarksCommand(), 
        prep_call=commands.get_new_bookmark_data),
    'B' : Option('Display list of marks ordered by date', 
        commands.ListBookmarksCommand()),
    'T' : Option('Display list of marks ordered by title', 
        commands.ListBookmarksCommand(order_by='title')),
    'D' : Option('Delete bookmark', commands.DeleteBookmarksCommand(), 
        prep_call=commands.get_bookmark_id_for_delition),
    'G' : Option('Save github stars', commands.ImportGithubStars(), 
        prep_call=commands.get_github_stars),
    #'S' : Option('search bookmark', commands.ListBookmarksCommand(criteria={'title':'dsf'})),
    'Q' : Option('Exit', commands.QuitCommand()),
    })

print('welcom to Bark application for managing your bookmarks! \n')
print()

if __name__ == '__main__':

    commands.CreateBookmarksTableCommands().execute()

    while True:
        commands.clear_screen()
        print_options(options)
        chosen_option = commands.choice_option(options)
        commands.clear_screen()
        data = chosen_option.choose()

        _ = input('press enter to return menu')

    
