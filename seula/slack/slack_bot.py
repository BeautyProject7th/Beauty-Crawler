import sys, os

def get_slack_token(bot_name):
    token_path = "../token/{}_token.txt".format(bot_name)
    print(os.getcwd())
    print(token_path)

    try:
        f = open(token_path)
    except FileNotFoundError:
        print("No such token file.")
        sys.exit(0)
    
    token_list = f.readlines()
    token_cnt = len(token_list)
    
    if token_cnt is not 1:
        for num in range(token_cnt-1):
            token_list[num] = token_list[num][:-1]
            
    f.close()
    
    return token_list