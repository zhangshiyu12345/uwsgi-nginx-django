import pandas as pd
import numpy as np
import os
from django.conf import settings
from football_platform.celery import app
from tool.data_preprocessing import Preprocessing
from tool.pass_count import Count_pass
from tool.player_analyse import Player_ana

@app.task
def csv_pre(file_path):
    pre = Preprocessing()
    tream_member_dict = pre.read_csv(file_path)
    print(tream_member_dict)

    return tream_member_dict

@app.task
def pass_count(file_path):
    count = Count_pass()
    data = count.return_graph(file_path)

    return data

@app.task
def player_anal(file_path):
    player = Player_ana()
    data = player.player_contrail()

    return data