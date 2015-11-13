class SQLGenerator:
    @staticmethod
    def insertIntoVenues(str_):
        return """
INSERT INTO public.venues
    (origin)
SELECT '{0}'
WHERE
    NOT EXISTS (
        SELECT public.venues.origin FROM public.venues WHERE venues.origin = '{0}'
    );
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
