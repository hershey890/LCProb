"""Randomly selects a problem from either Grind75, Grind169, or Neetcode150
"""
from pathlib import Path
from argparse import ArgumentParser
import webbrowser
import pandas as pd


OPEN_BROWSER = False


class Problem:
    def __init__(
        self,
        success: bool = False,
        prob_list: str = "",
        num: int = -1,
        name: str = "",
        diff: str = "",
        link: str = "",
    ) -> None:
        self.success = success
        self.prob_list = prob_list
        self.num = num
        self.name = name
        self.diff = diff
        self.link = link

    def __str__(self) -> str:
        return f"Problem: {self.num}. {self.name} ({self.diff})\nLink: {self.link}\n"


def _get_prob(problems_df: pd.DataFrame) -> Problem:
    """Randomly selects an uncompleted problem"""
    prob_lists = ["Grind75", "Grind169", "Neetcode150"]

    for lst in prob_lists:
        df = problems_df[problems_df["List"] == lst]
        inds = df["Completed"] == 0
        if sum(~inds) == len(df):
            continue

        raw_prob = df[inds].sample(1)
        return Problem(
            True,
            lst,
            raw_prob["Number"].values[0],
            raw_prob["Name"].values[0],
            raw_prob["Difficulty"].values[0],
            raw_prob["Link"].values[0],
        )

    return Problem(False)


def _handle_response(df: pd.DataFrame, prob_num: int, response: str) -> bool:
    """Used for setting problem completion status

    Returns
    -------
    bool
        True if the response is valid, False otherwise
    """
    if response.lower() == "y":
        df.loc[df["Number"] == prob_num, "Date Completed"] = pd.Timestamp.now()
        df.loc[df["Number"] == prob_num, "Completed"] = 1
        return True
    elif response.lower() == "n":
        return True
    elif response.lower() == "r":
        df.loc[:, "Date Completed"] = ""
        df.loc[:, "Completed"] = 0
        return True
    elif response.isdigit():
        if int(response) not in df["Number"].values:
            print("Problem not found.")
            return False
        df.loc[df["Number"] == int(response), "Date Completed"] = ""
        df.loc[df["Number"] == int(response), "Completed"] = 0
        return True
    else:
        print("Invalid response. Please type 'y', 'n', 'r', or a problem number.")
        return False


def main() -> None:
    problems_file = Path(__file__).parent / Path("data/problems_unique.csv")
    df = pd.read_csv(problems_file, dtype={"Number": "int", "Date Completed": "str", "Completed": "int"})

    # Select a Problem
    prob = _get_prob(df)
    if not prob.success:  # if all problems are completed
        print("All problems completed! Resetting dates to None")
        df["Date Completed"] = ""
        df.to_csv(problems_file, index=False)
        prob = _get_prob(df)
        if not prob.success:
            raise RuntimeError("No problems found")

    print(prob)
    if OPEN_BROWSER:
        webbrowser.open(prob.link)

    # Handle User Input
    print("\tTo mark a problem as completed, type 'y' and press Enter")
    print("\tTo exit, type 'n' and press Enter")
    print("\tTo reset progress, type 'r' and press Enter")
    print(
        "\tTo set undo completion of a problem, type '{problem number}' and press Enter"
    )

    while True:
        response = input("Input (y/n/r/problem#): ")
        if _handle_response(df, prob.num, response):
            df.to_csv(problems_file, index=False)
            break


if __name__ == "__main__":
    parser = ArgumentParser(description="""Randomly select a problem to work on""")
    parser.add_argument('-r', '--repetition', action='store_true', default=False, help='Select problems using spaced repitition')
    args = parser.parse_args()

    main()