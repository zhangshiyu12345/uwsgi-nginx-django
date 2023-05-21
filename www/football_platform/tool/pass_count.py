import base64
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO,BytesIO
from django.shortcuts import render
from django.views.generic import View
import os
from .data_preprocessing import Preprocessing
from sklearn.metrics import confusion_matrix
import numpy as np
from matplotlib import rcParams
from pylab import *
import random
sum = '',
sum3 = 0
coordinate_list = []
coordinate_distance = []
total_list = []
time_chart1 = ''
info1 = ''
outcome = ''
outcome1 = ''
matrix1 = ''
changed = ''
minIndex = ''
newCentroids = '',
tream2 = '',
info = '',
time_chart = '',
matrix = '',
newCentroids = ''

def draw(tream,treams_member_dict,file_name1):

    data1 = pd.read_excel(file_name1)
    tream_member = treams_member_dict[tream]

   # tream_member.sort()
    print(tream_member)
    print('第一队')

    member_G = []
    member_D = []
    member_M = []
    member_F = []

    # 后卫
    for j in tream_member:
       if isinstance(j,list) == False:
           if j.find('G') != -1:
               member_G.append(j)
           if j.find('D') != -1:
               member_D.append(j)
           if j.find('M') != -1:
               member_M.append(j)
           if j.find('F') != -1:
               member_F.append(j)
       else:
           if j[0].find('G') != -1:
               member_G.append(j)
           if j[0].find('D') != -1:
               member_D.append(j)
           if j[0].find('M') != -1:
               member_M.append(j)
           if j[0].find('F') != -1:
               member_F.append(j)
    print(member_D)
    print(member_M)
    print(member_F)

    print(member_G)


    #换人后的总表
    tream_member_last = []
    for j in tream_member:
        if isinstance(j,list) == False:
            tream_member_last.append(j)
        else:
            tream_member_last.append(j[1])
    print('换人后总表')
    global total_list
    total_list = tream_member_last
    print(tream_member_last)



    plt.clf()  # 清空图像

    #门将
    fig = plt.figure()
    plt.axis('off')

    plt.plot(12.5,50,'o')


    dot_list = {}
    dot_list[member_G[0]] = [12.5,50]

    #后卫
    d = 0
    if len(member_D) == 4:
        h = 0
        for j in range(9):
            d = d + 10
            if j % 2 != 0:
                if isinstance(member_D[h],list) == True:
                    dot_list[member_D[h][0]] = [25, d]
                    dot_list[member_D[h][1]] = [25,d]
                else:
                    dot_list[member_D[h]] = [25,d]
                h = h + 1
                plt.plot(25,d,'o')
    d = 0
    if len(member_D) == 5:
        h = 0
        for j in range(9):
            d = d + 10
            if j % 2 == 0:
                if isinstance(member_D[h],list) == True:
                    dot_list[member_D[h][1]] = [25,d]
                    dot_list[member_D[h][0]] = [25, d]
                else:
                    dot_list[member_D[h]] = [25,d]
                h = h + 1
                plt.plot(25,d,'o')

    d = 0
    if len(member_D) == 3:
        h = 0
        for j in range(9):
            d = d + 10
            if j == 2 or j == 4 or j == 6:
                if isinstance(member_D[h],list) == True:
                    dot_list[member_D[h][1]] = [25,d]
                    dot_list[member_D[h][1]] = [25, d]
                else:
                    dot_list[member_D[h]] = [25,d]
                h = h + 1
                plt.plot(25,d,'o')

    print('D')
    print(dot_list)
    #中锋
    m = 0
    if len(member_M) == 4:
        h = 0
        for j in range(9):
            m = m + 10
            if j % 2 != 0:
                if isinstance(member_M[h],list) == True:
                    dot_list[member_M[h][1]] = [37.5,m]
                    dot_list[member_M[h][0]] = [37.5, m]
                else:
                    dot_list[member_M[h]] = [37.5,m]
                h = h + 1
                plt.plot(37.5, m, 'o')

    m = 0
    if len(member_M) == 5:
        h = 0
        for j in range(9):
            m = m + 10
            if j % 2 == 0:
                if isinstance(member_M[h],list) == True:
                    dot_list[member_M[h][1]] = [37.5,m]
                    dot_list[member_M[h][0]] = [37.5, m]
                else:
                    dot_list[member_M[h]] = [37.5, m]
            h = h + 1
            plt.plot(37.5, m, 'o')

    m = 0
    if len(member_M) == 3:
        h = 0
        for j in range(9):
            m = m + 10
            if j == 2 or j == 4 or j == 6:
                if isinstance(member_M[h],list) == True:
                    dot_list[member_M[h][1]] = [37.5,m]
                    dot_list[member_M[h][0]] = [37.5, m]
                else:
                    dot_list[member_M[h]] = [37.5,m]
                h = h + 1
                plt.plot(37.5, m, 'o')

    # 前锋
    f = 0
    if len(member_F) == 3:
        h = 0
        for j in range(9):
            f = f + 10
            if j == 2 or j == 4 or j == 6:
                if isinstance(member_F[h],list) == True:
                    dot_list[member_F[h][1]] = [50,f]
                    dot_list[member_F[h][0]] = [50, f]
                else:
                    dot_list[member_F[h]] = [50,f]
                h = h + 1
                plt.plot(50, f, 'o')

    f = 0
    if len(member_F) == 2:
        h = 0
        for j in range(9):
            f = f + 10
            if j == 3 or j == 5:
                if isinstance(member_F[h], list) == True:
                    dot_list[member_F[h][1]] = [50, f]
                    dot_list[member_F[h][0]] = [50, f]
                else:
                    dot_list[member_F[h]] = [50, f]
                h = h + 1
                plt.plot(50, f, 'o')

    f = 0
    if len(member_F) == 1:
        h = 0
        for j in range(9):
            f = f + 10
            if j == 4:
                if isinstance(member_F[h], list) == True:
                    dot_list[member_F[h][1]] = [50, f]
                    dot_list[member_F[h][0]] = [50, f]
                else:
                    dot_list[member_F[h]] = [50, f]
                h = h + 1
                plt.plot(50, f, 'o')

    print('坐标列表')
    global coordinate_list
    coordinate_list = dot_list
    print(dot_list)

    dic = dot_list.keys()
    print(dic)


    try:

        dict1 = {}


        count = 0
        dict1 = {}
        for j in dic:
            dict1[j] = {}

        print(dict1)

        for j in dic:
            for i in dic:
                temp = {}
                temp[i] = 0
                dict1[j].update(temp)
        print(dict1)

        #传球矩阵

        for j in range(len(data1.index.values)):
            if data1.iloc[j, 2] in dic:
                temp = dict1[data1.iloc[j, 2]]
                num = temp[data1.iloc[j, 3]]
                num = num + 1
                temp[data1.iloc[j, 3]] = num

        print(dict1)




        global sum
        sum = 0  # 传球总数
        for j in dic:
            for i in dic:
                temp = dict1[j]
                num = temp[i]
                sum = sum + num

        print(sum)

        #画图
        for j in range(len(data1.index.values)):
            x = []
            y = []
            if data1.iloc[j, 2] in dic:
                x.append(dot_list[data1.iloc[j, 2]][0])
                y.append(dot_list[data1.iloc[j, 2]][1])
            if data1.iloc[j, 3] in dic:
                x.append(dot_list[data1.iloc[j, 3]][0])
                y.append(dot_list[data1.iloc[j, 3]][1])

                temp = dict1[data1.iloc[j, 2]]
                deep = temp[data1.iloc[j, 3]]
                plt.plot(x, y,linewidth=deep)









    except Exception as e:
        print(e)

        #plt.plot
    #plt.show()

    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data) #对plot_data进行编码
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    print(imd)

    info = {
        'imd':imd,
        'dict1':dict1,
        'sum':sum,
    }

    return info


def topology(data1,tream,treams_member_dict):
    print('##################')
    tream_member = treams_member_dict[tream]
    print(tream_member)

    #将换人后的球员换回来
    for j in tream_member:
        if isinstance(j,list) == True:
            for i in range(len(data1.index.values)):
                if data1.iloc[i, 2] == j[0]:
                    data1.iloc[i, 2] = j[1]
                if data1.iloc[i, 3] == j[0]:
                    data1.iloc[i, 3] = j[1]

    #去除数组的全体队员
    tream_member_change = tream_member
    for j in range(len(tream_member_change)):
        if isinstance(tream_member_change[j],list) == True:
            tream_member_change[j] = tream_member_change[j][1]

    print(tream_member_change)
    tream_member_change.sort()

    matr = {}
    for j in tream_member_change:
        matr[j] = {}

    for j in tream_member_change:
        for i in tream_member_change:
            temp = {}
            temp[i] = 0
            matr[j].update(temp)

    print(matr)

    #矩阵
    for j in range(len(data1.index.values)):
        if data1.iloc[j, 2] in tream_member_change:
            temp = matr[data1.iloc[j, 2]]
            num = temp[data1.iloc[j, 3]]
            num = num + 1
            temp[data1.iloc[j, 3]] = num

            temp = matr[data1.iloc[j, 3]]
            num = temp[data1.iloc[j, 2]]
            num = num + 1
            temp[data1.iloc[j, 2]] = num
    print('矩阵')
    global coordinate_distance
    coordinate_distance = matr
    print(matr)

    sum1 = 0  # 传球总数
    matr_list = []
    for j in tream_member_change:
        temp_list = []
        for i in tream_member_change:
            temp = matr[j]
            num = temp[i]
            sum1 = sum1 + num

            temp_list.append(num)
        matr_list.append(temp_list)
    global sum3
    sum3 = sum1
    print(sum1)
    global distance_list
    distance_list = matr_list
    print(matr_list)

    # confusion_matrix
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    plt.clf()  # 清空图像
    # 门将
    fig = plt.figure()
    classes = tream_member_change
    for j in range(len(classes)):
        classes[j] = classes[j][-2] + classes[j][-1]
    print('中')
    print(classes)
    print(treams_member_dict)
    confusion_matrix = np.array(matr_list, dtype=np.int64)  # 输入特征矩阵
    proportion = confusion_matrix
    length = len(confusion_matrix)
    print(length)
    proportion = np.array(proportion).reshape(length, length)  # reshape(列的长度，行的长度)

    plt.imshow(proportion, interpolation='nearest', cmap=plt.cm.Greens)  # 按照像素显示出矩阵
    plt.colorbar()
    plt.axis('equal')
    tick_marks = np.arange(len(classes))
    print(tick_marks)
    plt.xticks(tick_marks,classes)
    plt.yticks(tick_marks,classes)

    iters = np.reshape([[[i, j] for j in range(length)] for i in range(length)], (confusion_matrix.size, 2))
    for i, j in iters:
        if (i == j):
            plt.text(j, i, '∞',va='center',ha='center',fontsize=10)
        else:
            if proportion[j][i] == 0:
                plt.text(j, i, '∞',va='center',ha='center',fontsize=10)
            elif proportion[j][i] == 1:
                plt.text(j, i, proportion[j][i], va='center', ha='center', fontsize=10)
            else:
                plt.text(j, i, '1/%d'%(proportion[j][i]), va='center', ha='center', fontsize=10)

    #plt.show()
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)  # 对plot_data进行编码
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    print(imd)

    return imd

def time_than_figure(data1,tream,treams_member_dict):
    print('**********************')
    tream_member = treams_member_dict[tream]
    print(tream_member)

    #记录上半场和下半场时间列表
    h1_list = []
    h2_list = []
    for j in range(len(data1.index.values)):
        if data1.iloc[j, 1] == tream:
            if data1.iloc[j, 4] == '1H':
                h1_list.append(data1.iloc[j, 5] // 60)    #地板除
            if data1.iloc[j, 4] == '2H':
                h2_list.append(data1.iloc[j, 5] // 60)

    h1_list.sort()
    h2_list.sort()
    print(h1_list)
    print(h2_list)

    #每十分钟统计一次传球,40-45分钟为两个半场的间隔时间
    group_pass = []
    sum_pass = 0
    for j in range(5):
        temp = {}
        temp[j * 10] = 0
        group_pass.append(temp)
    print(group_pass)

    temp = {}
    temp[45] = 0
    group_pass.append(temp)

    temp = {}
    temp[55] = 0
    group_pass.append(temp)

    temp = {}
    temp[65] = 0
    group_pass.append(temp)

    temp = {}
    temp[75] = 0
    group_pass.append(temp)

    temp = {}
    temp[85] = 0
    group_pass.append(temp)

    temp = {}
    temp[95] = 0
    group_pass.append(temp)

    temp = {}
    temp[105] = 0
    group_pass.append(temp)

    print(group_pass)

    for j in h1_list:
        if j <= 10:
            h = group_pass[1]
            h[10] = h[10] + 1
        if j > 10 and j <= 20:
            h = group_pass[2]
            h[20] = h[20] + 1
        if j > 20 and j <= 30:
            h = group_pass[3]
            h[30] = h[30] + 1
        if j > 30 and j <= 40:
            h = group_pass[4]
            h[40] = h[40] + 1


    for j in h2_list:
        if j <= 10:
            h = group_pass[6]
            h[55] = h[55] + 1
        if j > 10 and j <= 20:
            h = group_pass[7]
            h[65] = h[65] + 1
        if j > 20 and j <= 30:
            h = group_pass[8]
            h[75] = h[75] + 1
        if j > 30 and j <= 40:
            h = group_pass[9]
            h[85] = h[85] + 1
        if j > 40 and j <= 50:
            h = group_pass[10]
            h[95] = h[95] + 1
        if j > 50 and j <= 60:
            h = group_pass[11]
            h[105] = h[105] + 1

    print(group_pass)

    distance = []
    for j in group_pass:
        for i in j.keys():
            distance.append(j[i])
    print(distance)

    #画图
    plt.clf()  # 清空图像
    plt.rcParams['font.sans-serif'] = ['SimHei'] # 显示中文标签
    matplotlib.rcParams['axes.unicode_minus']=False
    print(matplotlib.rcParams['font.family'])
    plt.plot(distance, color='green')
    x = [0,1,2,3,4,5,6,7,8,9,10,11]
    y = [0,10,20,30,40,45,55,65,75,85,95,105]
    plt.xticks(x,y)

    plt.fill_between(x=range(12),y1=0,y2=distance,facecolor='green',alpha=0.3)
    plt.xlabel('比赛时间')
    plt.ylabel('传球次数')

    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)  # 对plot_data进行编码
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    print(imd)

    return imd




def compute(data1,tream):
    global coordinate_list
    global coordinate_distance
    print(sum3)
    L = sum3 / 2 #链数总数
    p = L / 55   #网络密度

    #k-means聚类算法
    print(coordinate_list)  # 坐标列表
    print(total_list)
    except_list = []
    for i in coordinate_list.keys():
        if i not in total_list:
            except_list.append(i)
    for j in except_list:
        coordinate_list.pop(j)

    print('list')
    print(coordinate_list)

    dataset = [] #数据集
    for j in  coordinate_list.keys():
        dataset.append(coordinate_list[j])
    print(dataset)

    #包含坐标点的拓扑距离列表
    print(coordinate_distance)

    for j in coordinate_distance:
        dict1 = coordinate_distance[j]
        for i in dict1.keys():
            if dict1[i] == 0:
                dict1[i] = 10
            else:
                dict1[i] = 1 / dict1[i]
    print(coordinate_distance)

    #k-means聚类算法
    list_name = coordinate_list.keys()
    print(list_name)
    center_list = []
    distance_list = []

    # 拓扑距离
    def Distance(dataSet, centroids, k) -> np.array:
        global  coordinate_distance
        distance_list = []
        for j in coordinate_distance.keys():
            dict1 = coordinate_distance[j]
            if j == center_list[0]:
                for i in dict1.keys():
                    temp = []
                    temp.append(dict1[i])
                    distance_list.append(temp)
            if j == center_list[1]:
                count = 0
                for i in dict1.keys():
                    g = distance_list[count]
                    g.append(dict1[i])
                    count = count + 1
            if j == center_list[2]:
                count = 0
                for i in dict1.keys():
                    g = distance_list[count]
                    g.append(dict1[i])
                    count = count + 1

        distance_list = np.array(distance_list)
        print(distance_list)
        dis = distance_list

        return dis

    def Update_cen(dataSet, centroids, k):
        # 计算每个样本到质心的距离，返回值是array数组
        distance = Distance(dataSet, centroids, k)
        # print("输出所有样本到质心的距离：", distance)
        # 分组并计算新的质心
        print(13)
        minIndex = np.argmin(distance, axis=1)  # axis=1 返回每行最小值的索引
        # print("输出最小值索引", minIndex)
        print(14)
        print(dataSet)
        global newCentroids
        try:
            newCentroids = pd.DataFrame(dataSet).groupby(minIndex).mean()
        except Exception as e:
            print(e)
        # print("新的质心(dataframe)：", newCentroids)
        print(15)
        newCentroids = newCentroids.values
        print(16)
        # print("新的质心(值）：", newCentroids)

        # 计算变化量
        changed = newCentroids - centroids
        return changed, newCentroids

    # k-means 算法实现
    def kmeans(dataSet, k):
        global coordinate_list
        # (1) 随机选定k个质心
        centroids = random.sample(dataSet, 3)
        #center_list = []
        for j in coordinate_list.keys():
            if coordinate_list[j] == centroids[0]:
                center_list.append(j)
            if coordinate_list[j] == centroids[1]:
                center_list.append(j)
            if coordinate_list[j] == centroids[2]:
                center_list.append(j)
        print('质心名称')
        print(center_list)
        print("随机选定三个质心：", centroids)
        print(dataSet)
        # (2) 计算样本值到质心之间的距离，直到质心的位置不再改变
        global changed
        global newCentroids
        try:
            changed, newCentroids = Update_cen(dataSet, centroids, k)
        except Exception as e:
            print(e)
        print(12)
        try:
            while np.any(changed):
                changed, newCentroids = Update_cen(dataSet, newCentroids, k)
        except Exception as e:
            print(e)
        try:
            centroids = sorted(newCentroids.tolist())
        except Exception as e:
            print(e)
        print(1)

        # (3) 根据最终的质心，计算每个集群的样本
        try:
            global minIndex
            cluster = []
            dis = Distance(dataSet, centroids, k)  # 调用欧拉距离
            minIndex = np.argmin(dis, axis=1)
        except Exception as e:
            print(e)
        print(2)
        for i in range(k):
            cluster.append([])
        for i, j in enumerate(minIndex):  # enumerate()可同时遍历索引和遍历元素
            cluster[j].append(dataSet[i])

        return centroids, cluster

    # 创建数据集
    def createDataSet():
        global coordinate_list
        data2 = []
        for j in coordinate_list.keys():
            data2.append(coordinate_list[j])
        data3 = []
        [data3.append(i) for i in data2 if i not in data3]
        return data3

    dataset = createDataSet()  # type(dataset)='list'
    for j in range(20):
        center_list = []
        centroids, cluster = kmeans(dataset, 3)  #3 代表的是分为2类=2个质心

    print('质心为：%s' % centroids)
    print('集群为：%s' % cluster)
    # x = list(np.array(dataset).T[0])
    # y = list(np.array(dataset).T[1])
    # plt.scatter(list(np.array(dataset).T[0]), list(np.array(dataset).T[1]), marker='o', color='green', label="数据集" )
    plt.clf()  # 清空图像
    plt.scatter(list(np.array(centroids).T[0]), list(np.array(centroids).T[1]), marker='x', color='red', label="质心")
    colors = ['r.', 'g.', 'b.', 'k.', 'y.']
    count1 = 0
    for i in cluster:
        for j in i:
            plt.plot(j[0], j[1], colors[count1])
        count1 = count1 + 1
    #plt.text打上名字
    for j in coordinate_list.keys():
        if j in total_list:
            plt.text(coordinate_list[j][0],coordinate_list[j][1]+1,j)
    #plt.show()
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)  # 对plot_data进行编码
    ims = imb.decode()
    imd = "data:image/png;base64," + ims

    #plt.show()
    print(imd)

    return imd



class Count_pass():

    #传球过程显现
    def return_graph(self,file_path):

        file_name1 = os.path.join(file_path, 'passingevents.xlsx')
        print(file_name1)

        #获取双方球员
        pre = Preprocessing()
        treams_member_dict = pre.read_csv(file_path)
        print(treams_member_dict)



        try:
            data1 = pd.read_excel(file_name1)

            # 处理data1,记录两支队伍名称,和队员名称
            treams = set()
            for j in range(len(data1.index.values)):
                treams.add(data1.iloc[j, 1])
            treams = list(treams)
            print(treams)

            #第一队传球矩阵
            tream1 = treams[0]
            global info
            info = draw(tream1,treams_member_dict,file_name1)

            print(treams_member_dict)
            # 第一队时间比图
            global time_chart
            time_chart = time_than_figure(data1,tream1,treams_member_dict)

            #第一队拓扑距离矩阵
            global matrix
            matrix = topology(data1,tream1,treams_member_dict)

            #第一队计算结果
            global outcome
            outcome  = compute(data1,tream1)


            #第二队传队矩阵
            global tream2
            tream2 = treams[1]
            global info1
            info1 = draw(tream2, treams_member_dict, file_name1)
            print('info')
            #print(info)
            #第二队时间比图
            global time_chart1
            time_chart1 = time_than_figure(data1, tream2, treams_member_dict)
            print('time_chart1')
            print(time_chart1)
            # 第二队拓扑距离矩阵
            global matrix1
            matrix1 = topology(data1, tream2, treams_member_dict)

            #第二队计算结果
            global outcome1
            outcome1 = compute(data1, tream2)





        except Exception as e:
            print(e)


        data = {
            'tream1':tream1,
            'tream2':tream2,
            'info':info,
            'info1':info1,
            'time_cart':time_chart,
            'time_cart1':time_chart1,
            'matrix':matrix,
            'matrix1':matrix1,
            'outcome':outcome,
            'outcome1':outcome1,
        }

        return data





if __name__ == '__main__':
    count = Count_pass()
    count.return_graph('/home/zh/football_platform/football_platform/media/files/')