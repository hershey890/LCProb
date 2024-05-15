import sys
import pandas as pd
sys.path.append(sys.path[0] + "/../")
from lcprob import Problem, _get_prob, _handle_response

def _create_test_df():
    return pd.DataFrame({
        "Number": [4,2,1,6,5,3],
        "Name": ["Grind3", "Grind2", "Grind1", "Neet1", "Grind4", "Neet2"],
        "Difficulty": ["Easy", "Medium", "Medium", "Hard", "Easy", "Hard"],
        "Link": ["https://leetcode.com/problems/grind3/", 
                 "https://leetcode.com/problems/grind2/", 
                 "https://leetcode.com/problems/grind1/",
                 "https://leetcode.com/problems/neet1/",
                 "https://leetcode.com/problems/grind4/",
                "https://leetcode.com/problems/neet2/"
                ],
        "List": ["Grind75", "Grind169", "Grind75", "Neetcode150", "Grind75", "Neetcode150"],
        "Completed": [0, 0, 0, 0, 0, 0],
        "Date Completed": [pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT]
    })


def test_get_problem():
    df = _create_test_df()

    ## Spaced repetition = False ##
    # If only one problem is uncompleted, it should be selected
    df["Completed"] = 1
    df.loc[df["Number"] == 3, "Completed"] = 0
    prob = _get_prob(df, False)
    assert prob.success
    assert prob.num == 3
    assert prob.name == "Neet2"
    assert prob.diff == "Hard"
    assert prob.link == "https://leetcode.com/problems/neet2/"
    assert prob.prob_list == "Neetcode150"

    # If all problems are completed, return a failure
    df["Completed"] = 1
    prob = _get_prob(df, False)
    assert not prob.success

    ## Spaced repetition == True ##
    df["Completed"] = 1
    df["Date Completed"] = pd.Timestamp.now()
    df.loc[5, "Completed"] = 0
    df.loc[5, "Date Completed"] = pd.NaT
    prob = _get_prob(df, True)

    # df["Completed"] = [2, 2, 1, 1, 1, 1]


def test_handle_response():
    df = _create_test_df()

    # Test marking a problem as completed
    prob_num = 2
    _handle_response(df, prob_num, "y", False)
    assert df.loc[df["Number"] == prob_num, "Completed"].values[0] == 1
    assert not pd.isnull(df.loc[df["Number"] == prob_num, "Date Completed"].values[0])

    # Test marking a problem as not completed
    prob_num = 2
    _handle_response(df, prob_num, str(prob_num), False)
    assert df.loc[df["Number"] == prob_num, "Completed"].values[0] == 0
    assert pd.isnull(df.loc[df["Number"] == prob_num, "Date Completed"].values[0])

    # Test resetting all problems
    df["Completed"] = 1
    df["Date Completed"] = pd.Timestamp.now()
    _handle_response(df, 0, "r", False)
    assert sum(df["Completed"]) == 0
    assert sum(pd.isnull(df["Date Completed"])) == len(df)
