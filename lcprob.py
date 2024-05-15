from pathlib import Path
import pandas as pd
import webbrowser


problems_file = Path(__file__).parent / Path("data/problems_unique.csv")


def _select_problem() -> str:
    """Randomly selects an uncompleted problem

    If all problems are completed, resets the dates to None and
    selects a new problem.

    Returns
    -------
    str
        str(selected problem number)
    """

    def _get_prob(problem_df: pd.DataFrame) -> tuple[str, int]:
        global problems_file
        prob_lists = ["Grind75", "Grind169", "Neetcode150"]

        for lst in prob_lists:
            # df = pd.read_excel(problems_file, sheet_name=sheet)
            df = problem_df[problem_df["List"] == lst]
            inds = df["Date Completed"].isna()
            if sum(~inds) == len(df):
                continue

            prob = df[inds].sample(1)
            num = prob["Number"].values[0]
            name = prob["Name"].values[0]
            link = prob["Link"].values[0]
            diff = prob["Difficulty"].values[0]

            print(f"\nProblem: {num}. {name} ({diff})\nLink: {link}\n")
            webbrowser.open(link)
            return lst, num
        return None, None

    problem_df = pd.read_csv(problems_file)
    prob_list, prob_num = _get_prob(problem_df)

    if not prob_list:
        print("All problems completed! Resetting dates to None")
        problem_df["Date Completed"] = ""
        problem_df.to_csv(problems_file, index=False)
        prob_list, prob_num = _get_prob(problem_df)

    return str(prob_num)


def _handle_response(prob_num: int, response: str) -> bool:
    """Used for setting problem completion status

    Returns
    -------
    bool
        True if the response is valid, False otherwise
    """
    df = pd.read_csv(problems_file, dtype={"Date Completed": "str"})

    if response.lower() == "y":
        df.loc[df["Number"] == prob_num, "Date Completed"] = pd.Timestamp.now()
        df.to_csv(problems_file, index=False)
        return True
    elif response.lower() == "n":
        return True
    elif response.lower() == "r":
        # reset all dates to None
        df["Date Completed"] = ""
        df.to_csv(problems_file, index=False)
        return True
    elif response.isdigit():
        if int(response) not in df["Number"].values:
            print("Problem not found.")
            return False
        df.loc[df["Number"] == int(response), "Date Completed"] = ""
        df.to_csv(problems_file, index=False)
        return True
    else:
        print("Invalid response. Please type 'y', 'n', 'r', or a problem number.")
        return False


def main() -> None:
    prob_num = _select_problem()

    print("\tTo mark a problem as completed, type 'y' and press Enter")
    print("\tTo exit, type 'n' and press Enter")
    print("\tTo reset progress, type 'r' and press Enter")
    print(
        "\tTo set undo completion of a problem, type '{problem number}' and press Enter"
    )

    while True:
        response = input("Input? (y/n/r/problem#): ")
        if _handle_response(prob_num, response):
            break


if __name__ == "__main__":
    main()