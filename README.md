# LCProb: Leetcode Problem Selector
This project randomly selects a leetcode problem from either the Grind 75, Grind 169, or Neetcode 150 list.  

Leetcode lists aren't great for tracking repition of problems so this project aims to address that. LCProb randomly select essential problems for repetition without revealing the problem type. It tracks the last date a problem has been completed.

1. LCProb randomly selects an uncompleted problem from Grind75.
2. Once Grind75 is completed, LCProb randomly selects an uncompleted problem from Grind 169 NOT IN Grind75.
3. Once Grind75 and Grind169 are completed, LCProb randomly selects a problem from Neetcode150 NOT IN Grind75 or Grind169
4. Once all are completed, goes back to 1.

## Installation
**Requirements**  
- Python 3
- Pandas
- (I personally used Python 3.12.3 and Pandas 2.2.1)

**Installation**  
Use one of the following depending on if you use conda or pip
```bash
$ conda install pandas
# OR (you really should use a virtual environment as well)
$ pip install pandas
```

If there are some issues (due to dependency issues/package version mismatch), use the following to create a virtual environment.
```bash
# If using conda:
$ conda env create -f environment.yml
# creates a virtual environment (venv) called "table"

# If using pip
# Create a venv:
$ python3 -m venv table
# Activate venv:
$ source table/bin/activate
# Install requirements
$ pip install requirements.txt
```
\* Note you don't have to use a virtual environment and can directly just use `pip install requirements.txt` but I really recommend that you do not unless you use a seperate Python install from your system's default installation.

## Usage
Running LCProb opens a the problem in your default web browser and give you the option of tracking your progress.
```bash
$ python lcprob.py 

Problem: 543. Diameter of Binary Tree (Easy)
Link: https://leetcode.com/problems/diameter-of-binary-tree/

    To mark a problem as completed, type 'y' and press Enter
    To exit, type 'n' and press Enter
    To reset progress, type 'r' and press Enter
    To set undo completion of a problem, type '{problem number}' and press Enter
    Input? (y/n/r/problem#): 
```

## Stats
- 213 problems total
- Grind169 is Grind75 + 94 problems
- Neetcode 150 has 44 problems not in Grind169

## Todo
- unittests
- Add as Python package to PyPI