"""Randomly selects a problem from either Grind75, Grind169, or Neetcode150
"""
import warnings
from pathlib import Path
from argparse import ArgumentParser
import webbrowser
import json
import pandas as pd


OPEN_BROWSER = False
config_json = Path(__file__).parent / Path("data/config.json")
prob_lists = ["Grind75", "Grind169", "Neetcode150"]


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
    

# The completed column corresponds to the completion status of the problem
# Whether or not the program uses spaced repitition is determined by config.json
# Completion column values:
#   0: not completed
#   1: completed, either not on spaced rep, or on spaced repitition 1 (so day 1)
#   2: completed and on spaced repitition 2 (so day 3)
#   3: completed and on spaced repitition 3 (so day 7)
#   4: completed and on spaced repitition 4 (so day 16)
#   5: completed and on spaced repitition 5 (so day 45)
completion_statuses = [0, 1, 2, 3, 4, 5]
repitition_days = [0, 1, 3, 7, 16, 45] # spaced repition days


def _get_oldest_prob(df: pd.DataFrame) -> pd.DataFrame:
    """Returns the oldest uncompleted problem"""
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=pd.errors.SettingWithCopyWarning)
        df.loc[:, "Date Completed2"] = df.loc[:, "Date Completed"].dt.date
        return df.sort_values(by="Date Completed2").iloc[0]


def _get_spaced_rep_prob(df: pd.DataFrame) -> Problem:
    raw_prob = None

    for i, status in enumerate(completion_statuses):
        inds = df.loc[:, "Completed"] == status
        if sum(~inds) == len(df):
            continue
        
        for lst in prob_lists:
            inds = inds & (df["List"] == lst)
            if sum(inds) > 0:
                if i == 0 or i == len(repitition_days) - 1:
                    raw_prob = df[inds].sample(1).iloc[0]
                else:
                    raw_prob = _get_oldest_prob(df.loc[inds])
                break
        
        if raw_prob is not None:
            break

    if raw_prob is None:
        raise RuntimeError("Spaced Rep: No problems found")
    return Problem(
        True,
        lst,
        raw_prob["Number"],
        raw_prob["Name"],
        raw_prob["Difficulty"],
        raw_prob["Link"],
    )


def _get_prob(problems_df: pd.DataFrame, spaced_rep: bool) -> Problem:
    """Randomly selects an uncompleted problem

    Always returns a valid problem if `spaced_rep` is `True`
    """

    if spaced_rep:
        return _get_spaced_rep_prob(problems_df)
    else:
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


def _handle_response(df: pd.DataFrame, prob_num: int, response: str, spaced_rep: bool) -> bool:
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
    spaced_rep = json.load(open(config_json))["spaced_rep"]

    # Select a Problem
    prob = _get_prob(df, spaced_rep)
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
        if _handle_response(df, prob.num, response, spaced_rep):
            df.to_csv(problems_file, index=False)
            break


if __name__ == "__main__":
    parser = ArgumentParser(description="""Randomly select a problem to work on""")
    parser.add_argument('--spacedrep', type=str, choices=['enable', 'disable'], 
                        help='If enabled, permanently configures program to select with spaced repition rather than randomly until disabled'
    )
    args = parser.parse_args()

    if args.spacedrep == 'disable':
        json.dump({"spaced_rep": False}, open(config_json, "w"))
    elif args.spacedrep == 'enable':
        json.dump({"spaced_rep": True}, open(config_json, "w"))
    else:
        main()