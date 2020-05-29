import sqlite3


class Connector:
    def __init__(self, database_url):
        conn = sqlite3.connect(database_url)
        #print("Connector.database_url is {}".format(database_url))
        self.cursor = conn.cursor()

    def execute(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def executeList(self, query):
        self.cursor.execute(query)
        fetchall = self.cursor.fetchall()
        return list(sum(fetchall, ()))

    def create_table(self, name, *args):
        conn.excute('INSERT {0}, ({1})'.format(name, *args))
