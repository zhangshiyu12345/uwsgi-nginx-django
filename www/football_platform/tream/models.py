from django.db import models

# Create your models here.

results = [
    [0,'win'],
    [1,'loss'],
    [2,'tie']
]

side = [
    [0,'home'],
    [1,'away']
]

period = [
    [0,'1H'],
    [1,'2H']
]

sub_type = [
    [0, 'Head pass'],
    [1, 'Simple pass'],
    [2, 'Launch'],
    [3, 'High pass'],
    [4, 'Hand pass'],
    [5, 'Smart pass'],
    [6, 'Cross'],
]

class Match(models.Model):
    match_id = models.IntegerField(verbose_name='比赛ID',unique=True,primary_key=True)
    name = models.CharField(verbose_name='比赛名称',max_length=256,default='当季比赛')
    home_name = models.CharField(verbose_name='己方球队队伍',max_length=64,default='Huskies')
    opponent_id = models.CharField(verbose_name='对方队伍ID',max_length=64)
    outcome = models.IntegerField(verbose_name='比赛结果',choices=results)
    ownScore = models.IntegerField(verbose_name='队伍进球数',default=0)
    opponentScore = models.IntegerField(verbose_name='对手进球数',default=0)
    side = models.IntegerField(verbose_name='比赛队伍身份',choices=side)
    coach_id = models.CharField(verbose_name='教练身份码',max_length=64)

    class Meta:
        db_table = 'Match'
        verbose_name_plural = '比赛'

class FootballTream(models.Model):
    name = models.CharField(verbose_name='球队名称',max_length=256)
    tream_emblem = models.ImageField(verbose_name='球队队徽',upload_to='tream',default='default.jpg')
    area = models.CharField(verbose_name='所属地区',max_length=256)
    home_hall = models.CharField(verbose_name='主场馆',max_length=256)
    famous_person = models.CharField(verbose_name='知名人物',max_length=1024)
    main_honor = models.CharField(verbose_name='主要荣誉',max_length=1024)
    chairman = models.CharField(verbose_name='主席',max_length=256)
    owner = models.CharField(verbose_name='拥有者',max_length=256)
    founding_time = models.CharField(verbose_name='成立时间',max_length=256)
    tream_history = models.TextField(verbose_name='球队历史')

    class Meta:
        db_table = 'Tream'
        verbose_name_plural = '球队'

