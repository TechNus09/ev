import json
from db_helper import insert, retrieve
from datetime import datetime 
import time


def SortUp(old_log,new_log):
    #sort sata from old and new records to give xp gains of each player
    skills = ['mining_xp','woodcutting_xp']
    mining_unranked = {}
    wc_unranked = {}
    total_unranked = {}
    unranked = [mining_unranked,wc_unranked,total_unranked]

    for i in range(2):
        skill = skills[i]
        for j in new_log :
            new_xp = new_log[j][skill]
            old_xp = old_log[j][skill]
            xp = new_xp - old_xp
            unranked[i][j]=xp
            if i == 0 :
                unranked[2][j] = xp
            else:
                unranked[2][j] += xp
    return unranked

def RankUp(unsortedlb):
    #make a rankings of players based on their xp gain
    temp_dic = {}
    members_sorted = []
    temp_dic = {k: v for k, v in sorted(unsortedlb.items(), key=lambda item: item[1],reverse=True)}
    members_sorted.clear()
    total_xp = 0
    for key, value in temp_dic.items():
        if value != 0 :
            total_xp += value
            test = key + " <#> " + "{:,}".format(value)
            members_sorted.append(test)
    return members_sorted, total_xp

def create_file(data):
    #store records in json file form named data.json
    log_file = open("data.json", "w")
    log_file = json.dump(data, log_file, indent = 4)
    return True  

def jsing(dic):
    #convert dict variable to json object
    json_object = json.dumps(dic, indent = 4) 
    return json_object

def mmdd():
    #return date in str form 'mmdd'
    now = datetime.now()
    if now.month < 10 :
        mm = '0'+str(now.month)
    else:
        mm = str(now.month)
    if now.day < 10 :
        dd = '0'+str(now.day)
    else:
        dd = str(now.day)
    return mm+dd

def crt(data):
    log_file = open("data.json", "w")
    log_file = json.dump(data, log_file, indent = 4)
    return True     

def RankList(rl):
    msg = ""
    for i in range(len(rl)) :
        msg = msg + "Rank#"+str(i+1)+ '::: ' + rl[i] + '\n'
    return msg


