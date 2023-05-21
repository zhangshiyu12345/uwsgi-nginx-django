import base64
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO,BytesIO
from django.shortcuts import render
from django.views.generic import View
import os
from sklearn.metrics import confusion_matrix
import numpy as np
from matplotlib import rcParams
from pylab import *
import random



class Player_ana():

    def player_contrail(self,file_path):
        file_name1 = os.path.join(file_path, 'contrail.xlsx')
        print(file_name1)

        data1 = pd.read_excel(file_name1)

        for j in range(len(data1.index.values)):
            plt.plot(data1.iloc[j, 2],data1.iloc[j, 3],'o')
        plt.show()









if __name__ == '__main__':
    player = Player_ana()
    player.player_contrail('/home/zh/football_platform/football_platform/media/players/')