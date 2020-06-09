import click

@click.command()
@click.option(
    "--date", required=True, help="Date (YYYY/MM/DD) to get data for.",
)
@click.option(
    "--outdir", required=True, help="Location to put the date into.",
)
def main(date: str):
    """
        Retrieve NYT Crossword data for a given date.
        The source is the github.com/doshea/nyt_crosswords repo.
        Args:
            date (str): Date (YYYY/MM/DD) to get data for.
    """
    return analyse_data()

def analyse_data():
    pass

if __name__ == "__main__":
    main()