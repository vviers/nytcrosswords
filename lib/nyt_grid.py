import logging
import re
import requests


class NYTGrid:

    DATA_BASE_URL = "https://raw.githubusercontent.com/doshea/nyt_crosswords/master/"

    def __init__(self, date: str):
        """
            NYT Grid class.
            Date must be in the format YYYY/MM/DD
        """
        datefmt = re.compile(r"(\d{4})\/(\d{2})\/(\d{2})")
        if not datefmt.match(date):
            raise ValueError("date must be in the format YYYY/MM/DD")
        ymd = date.split("/")
        self._year = ymd[0]
        self._month = ymd[1]
        self._day = ymd[2]
        self._raw_data = None
        self.title = None
        self.author = None
        self.answers = None
        self.clues = None

    def fetch_data(self):
        """
            Retrieve data from GitHub repo to populate object.
        """
        try:
            target = f"{self.DATA_BASE_URL}{self._year}/{self._month}/{self._day}.json"
            r = requests.get(target)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.error(
                f"Could not fetch data for date {self._year}/{self._month}/{self._day}. {e}"
            )
            return
        self._raw_data = r.json()
        self.title = self._raw_data["title"]
        self.author = self._raw_data["author"]
        self.size = self._raw_data["size"]
        self.answers = self._raw_data["answers"]
        self.clues = self._raw_data["clues"]

    def __len__(self):
        """
            This assumes that all grids are square. TODO: check this assumption.
        """
        return self.size["cols"]

    def __str__(self):
        out = "{:^50}".format(self.title)
        out += "\n"
        for i in range(self.size["rows"]):
            start = self.size["cols"] * (i)
            end = self.size["cols"] * (i + 1)
            out += "\n"
            out += " | ".join(self._raw_data["grid"][start:end]).replace(".", " ")
        return out

    def __repr__(self):
        if self.title:
            return f"NYTGrid: {self.title} by {self.author}"
        return f"NYTGrid for {self._year}/{self._month}/{self._day}"

    def print_questions_answers(self, orientation: str = "across"):
        for question, answer in zip(self.clues[orientation], self.answers[orientation]):
            print(f"{question.ljust(50)}: {answer.rjust(20)}")
