import os
from os import listdir
from os.path import isfile, join
import json
from math import sqrt as s
import subprocess
import time
params = {
    "email_user": "example@gmail.com",
    "service": "gmail",  # or outlook or yahoo
    "save_dir_name": "mail_saved",
    "password": "123"
}

MAX_GAME_TIME = 20 #seconds

#returns tuple(first_name, second_name, who_won, game_time)
def test_for(fname1 : str, fname2 : str):
    wrapper_code = ""
    with open("wrapper.py", "r") as f:
        wrapper_code = f.read()

    with open("tmp_wrapper.py", "w") as f:
        f.write("from " + params["save_dir_name"] + "." + fname1[:-3] + " import func as F1\n")
        f.write("from " + params["save_dir_name"] + "." + fname2[:-3] + " import func as F2\n")
        f.write(wrapper_code)
    res = None
    f = open("tmp.tmp", "w")
    start = time.time()
    try:
        res = subprocess.run(['python', 'tmp_wrapper.py'], timeout=MAX_GAME_TIME, stdout=f)
    except subprocess.TimeoutExpired:
        print(fname1 + " " + fname2 + " takes too long to finish.")
        return (fname1, fname2, 0, 0)
    except subprocess.CalledProcessError:
        print(fname1 + " " + fname2 + " cannot compile")
        return (fname1, fname2, 0, 0)
    end = time.time()
    f.close()
    f = open("tmp.tmp", "r")
    try:
        q = int(f.read())
    except:
        print(fname1 + " " + fname2 + "someone printing data.")
        return (fname1, fname2, 0, 0)
    return (fname1, fname2, q, end-start)

def main(fname = "bot.json"):
    global params
    # at first I just load data from json
    with open(fname, "r") as f:
        params.update(json.loads(f.read()))

    if not os.path.exists(params["save_dir_name"]):
        os.mkdir(params["save_dir_name"])
    files_to_check = [f for f in listdir(params["save_dir_name"]) if isfile(join(params["save_dir_name"], f)) and f.endswith(".py")]
    all_res = []
    for i in range(len(files_to_check)):
        for j in range(len(files_to_check)):
            if i == j:
                continue
            res = test_for(files_to_check[i], files_to_check[j])
            all_res.append(res)
            print(str(len(all_res)) + "/" + str(len(files_to_check) * (len(files_to_check) - 1)))
    print("finished testing, now computing scoreboard")
    score_board = dict()
    for i in files_to_check:
      score_board[i] = 0

    for round in all_res:
        if (round[2] == 1):
            score_board[round[0]] += MAX_GAME_TIME - round[3]
        else:
            score_board[round[1]] += MAX_GAME_TIME - round[3]
    score_board_as_list = [(k, v) for k, v in score_board.items()]
    score_board_as_list = sorted(score_board_as_list, key = lambda tup : tup[1], reverse = True)

    with open("result.json", "w") as f:
        f.write(json.dumps(score_board_as_list))

if __name__ == "__main__":
    main()
