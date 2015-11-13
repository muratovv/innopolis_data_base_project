__author__ = 'Muratov'


class Parser:
    def __init__(self, path):
        self.prefixCodes = {"#*": self.title,
                            "#@": self.authors,
                            "#t": self.year,
                            "#c": self.venue,
                            "#index": self.index,
                            "#%": self.references,
                            "#!": self.abstract}
        self.file = open(path)
        self.next = True

    def getNext(self):
        paper = Paper()
        created = False
        while True:
            next_line = self.file.readline().strip()
            self.parseLine(paper, next_line)
            if next_line is None or next_line == "":
                break
            created = True
        if created:
            return paper if paper.isCorrect() else None
        else:
            self.next = False
            return None

    def hasNext(self):
        return self.next

    def close(self):
        if self.file is not None:
            self.file.close()

    def parseLine(self, paper, line):
        for code in self.prefixCodes:
            if line.startswith(code):
                forParse = line.replace(code, "").strip()
                if forParse != "":
                    self.prefixCodes[code](paper, forParse)
                break

    @staticmethod
    def title(paper, line):
        paper.title = line.replace("'", "")

    @staticmethod
    def authors(paper, line):
        paper.authors.extend([x.strip().replace("'", "") for x in line.split(",")])

    @staticmethod
    def year(paper, line):
        paper.year = int(line)

    @staticmethod
    def venue(paper, line):
        paper.venue = line.replace("'", "")

    @staticmethod
    def index(paper, line):
        paper.index = int(line)

    @staticmethod
    def references(paper, line):
        paper.references.append(int(line))

    @staticmethod
    def abstract(paper, line):
        paper.abstract = line.replace("'", "")


class Paper:
    def __init__(self):
        self.title = ""
        self.authors = []
        self.year = -1
        self.venue = ""
        self.references = []
        self.index = -1
        self.abstract = ""

    def __str__(self):
        return """\t[{5}] {0}
        {1}
        {2} - {3}
        References: {4}""".format(self.title, self.authors, self.year, self.venue, self.references, self.index)

    def isCorrect(self):
        return self.title != "" and self.title is not None \
               and self.year > 0 \
               and self.venue != "" and self.venue is not None \
               and len(self.authors) > 0
