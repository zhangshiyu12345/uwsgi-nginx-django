import pandas as pd
import numpy as np
import os
from django.conf import settings


class Preprocessing():

    def read_csv(self,file_path):

        file_name1 = os.path.join(file_path,'passingevents.xlsx')
        file_name2 = os.path.join(file_path,'fullevents.xlsx')
        print(file_name1)
        print(file_name2)

        try:
            data1 = pd.read_excel(file_name1)
            data2 = pd.read_excel(file_name2)

            #处理data1,记录两支队伍名称,和队员名称
            treams = set()
            for j in range(len(data1.index.values)):
                treams.add(data1.iloc[j,1])
            treams = list(treams)
            print(treams)

            # 记录双方队员身份
            treams_member1 = set()
            treams_member2 = set()
            for j in range(len(data1.index.values)):
                if treams[0] == data1.iloc[j,1]:
                    treams_member1.add(data1.iloc[j, 2])
                    treams_member1.add(data1.iloc[j, 3])
                if treams[1] == data1.iloc[j,1]:
                    treams_member2.add(data1.iloc[j, 2])
                    treams_member2.add(data1.iloc[j, 3])

            #将队员与团队组合形成字典
            treams_member_dict = {}
            treams_member_dict[treams[0]] = list(treams_member1)
            treams_member_dict[treams[1]] = list(treams_member2)
            print(treams_member_dict)

            # 处理data2,换人,拿到换人列表
            treams_member1_data2 = {}
            treams_member2_data2 = {}
            for i in range(len(data2.index.values)):
                if data2.iloc[i, 7] == 'Substitution' and data2.iloc[i,1] == treams[0]:
                    treams_member1_data2[data2.iloc[i, 2]] = data2.iloc[i, 3]
                if data2.iloc[i, 7] == 'Substitution' and data2.iloc[i,1] == treams[1]:
                    treams_member2_data2[data2.iloc[i, 2]] = data2.iloc[i, 3]
            print('替换字典')
            print(treams_member1_data2)

            #将换人列表1和队伍1字典进行整合,得出完整队伍
            for member in treams_member1_data2:
                if member in treams_member_dict[treams[0]]:
                    temp = list()
                    temp.append(member)
                    temp.append(treams_member1_data2[member])
                    print(temp)
                    treams_member_dict[treams[0]].remove(member)
                    treams_member_dict[treams[0]].remove(treams_member1_data2[member])
                    treams_member_dict[treams[0]].append(temp)
            print(treams_member_dict[treams[0]])

            for member in treams_member2_data2:
                if member in treams_member_dict[treams[1]]:
                    temp = list()
                    temp.append(member)
                    temp.append(treams_member2_data2[member])
                    print(temp)
                    treams_member_dict[treams[1]].remove(member)
                    treams_member_dict[treams[1]].remove(treams_member2_data2[member])
                    treams_member_dict[treams[1]].append(temp)
            print(treams_member_dict[treams[1]])


            return treams_member_dict

        except Exception as e:
            print('文件上传不全')
            print(e)

        #print(data7.MatchID)









if __name__ == '__main__':
    pre = Preprocessing()
    pre.read_csv('/home/zh/football_platform/football_platform/media/files/')