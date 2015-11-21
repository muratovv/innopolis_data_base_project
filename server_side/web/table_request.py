import psycopg2

from server_side.sql_scripts import SQLGenerator

conn = psycopg2.connect("dbname=postgres user=Muratov")
conn.autocommit = True
cur = conn.cursor()


def run_request(query=None):
    if not query:
        query = {}
    db_request = ""
    if query['operation'] == 'select':
        title = []
        db_request = ""

        if query['table'] == 'article':
            db_request = Select.articles(query)
            title = [('id', 'title', 'year', 'venue')]

        if query['table'] == 'author':
            db_request = Select.authors(query)
            title = [('id', 'name')]

        if query['table'] == 'venue':
            db_request = Select.venues(query)
            title = [('id', 'origin')]

        if query['table'] == 'links':
            db_request = Select.links(query)
            title = [('id', 'reference')]

        print("<<SQL REQUEST: \n" + str(db_request) + " >>")

        cur.execute(db_request)
        db_response = {"req": title + cur.fetchall()}
        print(db_response)
        return db_response

    if query['operation'] == 'insert':

        if query['table'] == 'article':
            db_request = Insert.articles(query)

        if query['table'] == 'author':
            db_request = Insert.authors(query)

        if query['table'] == 'venue':
            db_request = Insert.venues(query)

        if query['table'] == 'links':
            db_request = Insert.links(query)

        print("<<SQL REQUEST: \n" + str(db_request) + " >>")

        print(db_request)
        db_response = {"req": 'ok'}
        try:
            cur.execute(db_request)
        except:
            db_response['req'] = 'fail'
        print(db_response)
        return db_response

    if query['operation'] == 'update':

        if query['table'] == 'article':
            db_request = Update.articles(query)

        if query['table'] == 'author':
            db_request = Update.authors(query)

        if query['table'] == 'venue':
            db_request = Update.venues(query)

        print("<<SQL REQUEST: \n" + str(db_request) + " >>")

        print(db_request)
        db_response = {"req": 'ok'}
        try:
            cur.execute(db_request)
            pass
        except:
            db_response['req'] = 'fail'
        print(db_response)
        return db_response

    if query['operation'] == 'delete':

        if query['table'] == 'article':
            db_request = Delete.articles(query)

        if query['table'] == 'author':
            db_request = Delete.authors(query)

        if query['table'] == 'venue':
            db_request = Delete.venues(query)

        if query['table'] == 'links':
            db_request = Delete.links(query)

        print("<<SQL REQUEST: \n" + str(db_request) + " >>")

        print(db_request)
        db_response = {"req": 'ok'}
        try:
            cur.execute(db_request)
        except:
            db_response['req'] = 'fail'
        print(db_response)
        return db_response


class Select:
    @staticmethod
    def articles(query=None):
        if not query:
            query = {}
        return SQLGenerator.generate_select("id, title, year, origin", "articles NATURAL JOIN venues",
                                            {'id': query['id'], 'title': query['title'], 'year': query['year'],
                                             'venue': query['venue_str'], },
                                            query['page_size'], compute_offset(query['page'], query['page_size']), {})

    @staticmethod
    def authors(query=None):
        if not query:
            query = {}
        return SQLGenerator.generate_select('id, name', 'authors', {'id': query['id'], 'name': query['namea']},
                                            query['page_size'], compute_offset(query['page'], query['page_size']), {})

    @staticmethod
    def venues(query=None):
        if not query:
            query = {}
        return SQLGenerator.generate_select('id, origin', 'venues', {'id': query['id'], 'origin': query['origin']},
                                            query['page_size'], compute_offset(query['page'], query['page_size']), {})

    @staticmethod
    def links(query=None):
        if not query:
            query = {}
        return SQLGenerator.generate_select('source_id, dest_id', 'links',
                                            {'source_id': query['id'], 'dest_id': query['link_id']},
                                            query['page_size'], compute_offset(query['page'], query['page_size']), {})


class Insert:
    @staticmethod
    def articles(query=None):
        if not query:
            query = {}
        return SQLGenerator.generate_insert('articles', ['title', 'year', 'venueid'],
                                            [query['title'], query['year'], query['venue']])

    @staticmethod
    def authors(query=None):
        if not query:
            query = {}
        return SQLGenerator.generate_insert('authors', ['name'],
                                            [query['namea']])

    @staticmethod
    def venues(query=None):
        if not query:
            query = {}
        return SQLGenerator.generate_insert('venues', ['origin'],
                                            [query['origin']])

    @staticmethod
    def links(query=None):
        if not query:
            query = {}
        return SQLGenerator.generate_insert('links', ['source_id', 'dest_id'],
                                            [query['id'], query['link_id']])


class Update:
    @staticmethod
    def articles(query=None):
        if not query:
            query = {}
        return SQLGenerator.generate_update('articles',
                                            {'title': query['title'], 'year': query['year'], 'venueid': query['venue']},
                                            ('id', query['id']), ['title'])

    @staticmethod
    def authors(query=None):
        if not query:
            query = {}
        return SQLGenerator.generate_update('authors', {'name': query['namea']}, ('id', query['id']), ['name'])

    @staticmethod
    def venues(query=None):
        if not query:
            query = {}
        return SQLGenerator.generate_update('venues', {'origin': query['origin']}, ('id', query['id']), ['origin'])


class Delete:
    @staticmethod
    def articles(query=None):
        if not query:
            query = {}
        return SQLGenerator.generate_delete('articles', {'id': query['id']})

    @staticmethod
    def authors(query=None):
        if not query:
            query = {}
        return SQLGenerator.generate_delete('authors', {'id': query['id']})

    @staticmethod
    def venues(query=None):
        if not query:
            query = {}
        return SQLGenerator.generate_delete('venues', {'id': query['id']})

    @staticmethod
    def links(query=None):
        if not query:
            query = {}
        return SQLGenerator.generate_delete('links', {'source_id': query['id'], 'dest_id': query['link_id']})


def compute_offset(page_str, page_size_str):
    return int(page_str) * int(page_size_str)
