__doc__ = """
This script takes an issue containing:
    1) A variable name in the title 
    2) Pickled data in the form of a string of four-digit numbers (representing bytes)
And does the following:
    1) Create an entry for the data in a file with the name pointing to the respective ID 
    2) Create a file in the `global_objects` directory with the name of the ID and the information in the variable
"""
import os 
import github
import random

if __name__ == "__main__":

    NAME_TO_ID_SEP = ";;;"
    VARIABLE_NAME, CONFIDENCE = os.environ["ISSUE_TITLE"].removeprefix("Create Public Global: ").split(NAME_TO_ID_SEP)
    ISSUE_BODY = os.environ["ISSUE_BODY"]

    value_id = -1
    while value_id < 0 or value_id in os.listdir("global_objects"):
        value_id = random.randint(1, 1000000000)

    with open(f"./global_objects/{value_id}", 'w') as f:
        f.write(ISSUE_BODY)
    with open(f"./public_globals.txt", 'a') as f:
        f.write(f"{VARIABLE_NAME}{NAME_TO_ID_SEP}{value_id}{NAME_TO_ID_SEP}{CONFIDENCE}\n")

    g = github.Github(auth=github.Auth.Token(os.environ["TOKEN"]))
    issue = g.get_repo("vivaansinghvi07/dreamberd-interpreter-globals").get_issue(int(os.environ["ISSUE_NUMBER"]))
    issue.edit(state='closed')
