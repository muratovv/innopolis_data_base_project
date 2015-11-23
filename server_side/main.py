from server_side.parser import Parser
from server_side.sql_scripts import SQLGenerator
import psycopg2

if __name__ == '__main__':
    fileName = "../publications.txt"
    # conn = psycopg2.connect("dbname=postgres user=Muratov")
    parser = Parser(fileName)
    generator = SQLGenerator()

    # cur = conn.cursor()

    counter = 0

    while parser.hasNext():
        p = parser.getNext()
        if p is None:
            continue
        print(p.__str__() + "\n")
        # cur.execute(generator.insertIntoVenues(p.venue))
        # conn.commit()
        # cur.execute(generator.getVenueId(p.venue))
        # venueId = cur.fetchall()[0][0]

        for author in p.authors:
            # cur.execute(generator.insertIntoAuthors(author))
            # conn.commit()
            # cur.execute(generator.getAuthor(author))
            # cur.execute(generator.insertIntoArticlesAuthors(p.index, cur.fetchall()[0][0]))
            # conn.commit()
        # cur.execute(generator.insertIntoArticles(p.index, p.title, p.year, venueId))
        # conn.commit()
        for reference in p.references:
            # cur.execute(generator.insertIntoLink(p.index, reference))
            # conn.commit()
        counter += 1
        if counter > 100:
            print(counter)
    # conn.commit()
    # cur.close()
    # conn.close()
    parser.close()
