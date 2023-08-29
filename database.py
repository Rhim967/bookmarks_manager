import sqlite3

class DatabaseManager:
    ''' class for managing database, (CRUD) operations for our app \
            we can write, change, delete data to/from database'''

    def __init__(self, db_filename):
        ''' init and create our DB '''

        self.connection = sqlite3.connect(db_filename)
        #print(f'DB { db_filename } created successfull')

    def _execute(self, statement, values=None):
        ''' func for exicuting one of out (CRUD) operation '''

        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor

    def create_table(self, table_name, columns):
        ''' func for creating table in DB '''

        col_with_types = [
                f'{col_name} {col_type}'
                for col_name, col_type in columns.items()
                ]
        self._execute(
                f'''
                CREATE TABLE IF NOT EXISTS {table_name}
                ({', '.join(col_with_types)})
                '''
                )

    def add(self, table_name, data):
        ''' func for adding memory in tabe '''

        self._execute(
                f'''
                INSERT INTO {table_name}
                ({', '.join(data.keys())})
                VALUES ({', '.join('?' * len(data))})
                ''',
                tuple(data.values()) # create tuple from values of our dict
                )

    def delete(self, table_name, criteria):
        ''' func for deleting member from db table '''

        placeholders = [f'{col} = ?' for col in criteria.keys()]
        delete_criteria = ' AND '.join(placeholders)
        self._execute(
                f'''
                DELETE FROM {table_name} 
                WHERE {delete_criteria};
                ''',
                tuple(criteria.values())
                )

    def select(self, table_name, criteria=None, ordered_by=None):
        criteria = criteria or {}
        query = f'SELECT * FROM {table_name}'

        if criteria:
            placeholder = [f'{col} = ?' for col in criteria.keys()]
            select_criteria = ' AND '.join(placeholder)
            query += f' WHERE {select_criteria}'

        if ordered_by:
            query += f' ORDER BY {ordered_by}'

        return self._execute(
                query,
                tuple(criteria.values())
                )

    def __del__(self):
        self.connection.close()



#CREATE TABLE IF NOT EXIST Bookmarks (
#        id INTEGER PRIMARY KEY AUTOINCREMENT,
#        title TEXT NOT NULL,
#        url TEXT NOT NULL,
#        notes TEXT
#        date_added TEXT NOT NULL,
#        )

