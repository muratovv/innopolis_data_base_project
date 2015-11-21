# noinspection SqlDialectInspection,SqlNoDataSourceInspection
class SQLGenerator:
    @staticmethod
    def insertIntoVenues(str_):
        return """
INSERT INTO public.venues
    (origin)
SELECT '{0}'
WHERE
    NOT EXISTS (
        SELECT public.venues.origin FROM public.venues WHERE venues.origin = '{0}');
              """.format(str_)

    @staticmethod
    def getVenueId(str_):
        return """
SELECT public.venues.id FROM public.venues
    WHERE public.venues.origin = '{0}';
        """.format(str_)

    @staticmethod
    def insertIntoAuthors(str_):
        return """
INSERT INTO public.authors
(name)
  SELECT '{0}'
  WHERE
    NOT EXISTS(
        SELECT public.authors.name
        FROM public.authors
        WHERE public.authors.name = '{0}'
    );
    """.format(str_)

    def getAuthor(self, str_):
        return """
SELECT public.authors.id FROM public.authors
WHERE public.authors.name = '{0}';
""".format(str_)

    @staticmethod
    def insertIntoArticles(id, title, year, venueid):
        return """
INSERT INTO public.articles
(id, title, year, venueid)
  SELECT {0}, '{1}', {2}, {3}
  WHERE
    NOT EXISTS(
        SELECT
          public.articles.title,
          public.articles.year
        FROM public.articles
        WHERE public.articles.title = '{1}' AND public.articles.year = {2}
    );
    """.format(id, title, year, venueid)

    @staticmethod
    def insertIntoArticlesAuthors(article, author):
        return """INSERT INTO public.articles_authors
(article_id, author_id)
    SELECT {0}, {1};""".format(article, author)

    @staticmethod
    def insertIntoLink(source, dest):
        return """INSERT INTO public.links
(source_id, dest_id)
  SELECT {0}, {1};""".format(source, dest)

    @staticmethod
    def generate_dict(where_tuples=None, start_word="WHERE ", excepted_like_strings=None, separator=' AND '):
        if not excepted_like_strings:
            excepted_like_strings = []
        if not where_tuples:
            where_tuples = {}
        if len(where_tuples) == 0:
            return ""
        else:
            request = start_word
            lst = []
            for key, value in where_tuples.items():
                if value is not None and value != "":
                    temp = [key, value]
                    lst.append(temp)
            for i in range(len(lst)):
                if isinstance(lst[i][1], str):
                    if lst[i][0] not in excepted_like_strings:
                        request += lst[i][0] + " LIKE " + "'%{0}%'".format(lst[i][1])
                    else:
                        request += lst[i][0] + " = " + "'{0}'".format(lst[i][1])
                else:
                    request += lst[i][0] + " = " + "{0}".format(lst[i][1])
                if i < len(lst) - 1:
                    request += separator
            if len(lst) > 0:
                return request
            else:
                return ""

    @staticmethod
    def generate_enumerate(query=None, wrap_strings=False):
        if not query:
            query = []
        pass
        db_request = ""
        for i in range(len(query)):
            if isinstance(query[i], int) or is_int(query[i]):
                db_request += str(query[i])
            else:
                if wrap_strings:
                    db_request += "'" + query[i] + "'"
                else:
                    db_request += query[i]
            if i < len(query) - 1:
                db_request += ', '
        return db_request

    @staticmethod
    def generate_odrderby(orderby_dict=None):
        if not orderby_dict:
            orderby_dict = {}
        if len(orderby_dict) == 0 or orderby_dict['what'] == '' or orderby_dict['what']:
            return ""
        else:
            return "ORDER BY {0} {1}".format(orderby_dict['what'], orderby_dict['by'])

    @staticmethod
    def generate_select(what_str, from_str, where_dict, limit_int, skip_int, ordery_dict):
        return """
SELECT {0}
FROM {1}
{2}
{5}
LIMIT {3}
OFFSET {4};
        """.format(what_str, from_str, SQLGenerator.generate_dict(where_dict), limit_int, skip_int,
                   SQLGenerator.generate_odrderby(ordery_dict))

    @staticmethod
    def generate_insert(db_str, what_lst, values_lst):
        return """
INSERT INTO {0}({1})
  VALUES ({2});""".format(db_str, SQLGenerator.generate_enumerate(what_lst),
                          SQLGenerator.generate_enumerate(values_lst, True))

    @staticmethod
    def generate_update(db_str, set_lst, id_pair, excepted_like_lst=[]):
        return """
UPDATE {0} SET {1}
WHERE {2} = {3};""".format(db_str, SQLGenerator.generate_dict(set_lst, "", excepted_like_lst, ', '), id_pair[0],
                           id_pair[1])


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    print("main")
    print(SQLGenerator.generate_update('films', {'kind': 'dramatic'}, ('id', 123), ['kind']))
