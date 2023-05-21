import numpy as np
import pymongo
import random
import re
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
from mpl_toolkits.mplot3d import axes3d
import random

class Mongo():

    def connectdb(self,file,id):
        try:
            MongoClient = pymongo.MongoClient('mongodb://175.178.248.34:27017')
            print(MongoClient.list_database_names())
            db = MongoClient['user']
            collection = db.files
            data = {'id':id,'file':file}
            collection.insert_one(data)
            print(collection.find())
            return db
        except Exception as e:
            print(e)

        finally:
            MongoClient.close()


    def analysis(self,id):
        MongoClient = pymongo.MongoClient('mongodb://175.178.248.34:27017')
        print(MongoClient.list_database_names())
        db = MongoClient['user']
        collection = db.files
        data = collection.find({'id':id})
        for each in data:
            print(each['file'])
            files = each['file'].split('\\r\\n')
            IR = []
            TEMP = []
            AX = []
            AY = []
            AZ = []
            GX = []
            GY = []
            GZ = []
            NODE = []
            for data in files:
                if data.find('IR') != -1:
                    m = re.search('IR = (.+)',data)
                    IR.append(float(m.groups()[0]))
                if data.find('TEMP') != -1:
                    m = re.search('TEMP = (.+)',data)
                    TEMP.append(float(m.groups()[0]))
                if data.find('AX') != -1:
                    m = re.search('AX = (.+)',data)
                    AX.append(float(m.groups()[0]))
                if data.find('AY') != -1:
                    m = re.search('AY = (.+)',data)
                    AY.append(float(m.groups()[0]))
                if data.find('AZ') != -1:
                    m = re.search('AZ = (.+)', data)
                    AZ.append(float(m.groups()[0]))
                if data.find('GX') != -1:
                    m = re.search('GX = (.+)', data)
                    GX.append(float(m.groups()[0]))
                if data.find('GY') != -1:
                    m = re.search('GY = (.+)', data)
                    GY.append(float(m.groups()[0]))
                if data.find('GZ') != -1:
                    m = re.search('GZ = (.+)', data)
                    GZ.append(float(m.groups()[0]))
                if data.find('NODE') != -1:
                    m = re.search('NODE = (.+)', data)
                    NODE.append(float(m.groups()[0]))
            print(IR)
            print(TEMP)
            print(AX)
            print(AY)
            print(AZ)
            print(GX)
            print(GY)
            print(GZ)
            print(NODE)

            #IR(血氧浓度)
            count = 0
            sum = 0
            IR_avg = []
            for ir in IR:
                sum = sum + ir
                count = count + 1
                if count == 4:
                    IR_avg.append(sum / 4)
                    count = 0
                    sum = 0

            print(IR_avg)
            x1 = np.arange(0,41)
            plt.clf()  # 清空图像
            plt.plot(x1,IR_avg,marker=',',color='blue')
            plt.xlabel('比赛时间(半场)')
            plt.ylabel('球员平均血氧浓度')
            plt.title('球员比赛时血氧浓度变化')
            #plt.show()
            buffer = BytesIO()
            plt.savefig(buffer)
            plot_data = buffer.getvalue()
            imb = base64.b64encode(plot_data)  # 对plot_data进行编码
            ims = imb.decode()
            IR_img = "data:image/png;base64," + ims
            print(IR_img)

            #人体温度
            count1 = 0
            sum1 = 0
            TEMP_avg = []
            for temp in TEMP:
                sum1 = sum1 + temp
                count1 = count1 + 1
                if count1 == 4:
                    TEMP_avg.append(sum1 / 4)
                    sum1 = 0
                    count1 = 0
            print(TEMP_avg)

            x2 = np.arange(0,41)
            plt.clf()
            plt.plot(x1,TEMP_avg,marker=',',color='red')
            plt.xlabel('比赛时间(半场)')
            plt.ylabel('球员平均体温')
            plt.title('球员比赛时平均体温变化')
            #plt.show()
            buffer = BytesIO()
            plt.savefig(buffer)
            plot_data = buffer.getvalue()
            imb = base64.b64encode(plot_data)  # 对plot_data进行编码
            ims = imb.decode()
            TEMP_img = "data:image/png;base64," + ims
            print(TEMP_img)

            #角速度
            fig = plt.figure()
            ax3d = fig.add_subplot(projection="3d")
            ax3d.scatter(AX,AY,AZ,marker="o",cmap='jet')
            ax3d.set_xlabel('x',fontsize=14)
            ax3d.set_ylabel('y',fontsize=14)
            ax3d.set_zlabel('z',fontsize=14)
            #plt.title('球员角速度')
            ax3d.set_title('球员角速度')
            plt.tick_params(labelsize=10)
            #plt.show()
            buffer = BytesIO()
            plt.savefig(buffer)
            plot_data = buffer.getvalue()
            imb = base64.b64encode(plot_data)  # 对plot_data进行编码
            ims = imb.decode()
            A_img = "data:image/png;base64," + ims
            print(A_img)

            #加速度
            fig1 = plt.figure()
            ax3d1 = fig1.add_subplot(projection="3d")
            ax3d1.scatter(GX,GY,GZ,marker="o",cmap='jet')
            ax3d1.set_xlabel('x', fontsize=14)
            ax3d1.set_ylabel('y', fontsize=14)
            ax3d1.set_zlabel('z', fontsize=14)
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['axes.unicode_minus'] = False
            plt.title("加速度")
            plt.tick_params(labelsize=10)
            #plt.show()
            buffer = BytesIO()
            plt.savefig(buffer)
            plot_data = buffer.getvalue()
            imb = base64.b64encode(plot_data)  # 对plot_data进行编码
            ims = imb.decode()
            G_img = "data:image/png;base64," + ims
            print(G_img)


            data7 = {
                'IR_img':IR_img,
                'TEMP_img':TEMP_img,
                'A_img':A_img,
                'G_img':G_img,
            }
            print(data7)

            return data7



















if __name__ == '__main__':
    mongo = Mongo()
    #db = mongo.connectdb()
    mongo.analysis(26)
    #print(db)
