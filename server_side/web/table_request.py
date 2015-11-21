import psycopg2

from server_side.sql_scripts import SQLGenerator

conn = psycopg2.connect("dbname=postgres user=Muratov")
cur = conn.cursor()


def run_request(query=None):
    if not query:
        query = {}

    if query['operation'] == 'select':
        title = []
        db_request = ""

        if query['table'] == 'article':
            db_request = articles_select(query)
            title = [('id', 'title', 'year', 'venue')]

        if query['table'] == 'author':
            db_request = authors_select(query)
            title = [('id', 'name')]

        if query['table'] == 'venue':
            db_request = venues_select(query)
            title = [('id', 'origin')]

        if query['table'] == 'links':
            db_request = links_select(query)
            title = [('id', 'reference')]

        print("<<SQL REQUEST: \n" + db_request + " >>")

        cur.execute(db_request)
        db_response = {"req": title + cur.fetchall()}
        print(db_response)
        return db_response


def articles_select(query=None):
    if not query:
        query = {}
    return SQLGenerator.generate_select("id, title, year, origin", "articles NATURAL JOIN venues",
                                        {'id': query['id'], 'title': query['title'], 'year': query['year'],
                                         'venue': query['venue'], },
                                        query['page_size'], 0, {})


def authors_select(query=None):
    if not query:
        query = {}
    return SQLGenerator.generate_select('id, name', 'authors', {'id': query['id'], 'name': query['namea']},
                                        query['page_size'], 0, {})


def venues_select(query=None):
    if not query:
        query = {}
    return SQLGenerator.generate_select('id, origin', 'venues', {'id': query['id'], 'origin': query['origin']},
                                        query['page_size'], 0, {})


def links_select(query=None):
    if not query:
        query = {}
    return SQLGenerator.generate_select('source_id, dest_id', 'links',
                                        {'source_id': query['id'], 'dest_id': query['link_id']},
                                        query['page_size'], 0, {})
