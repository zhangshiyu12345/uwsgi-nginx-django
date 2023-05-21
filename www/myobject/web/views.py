#模板中只负责输出
from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
import time
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime
from myadmin.models import User,Shop,Orders,OrderDetail,Payment,Category,Product,Member
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.db.models import Q
import csv


# Create your views here.
def index(request):
    '''项目前台大堂点餐首页'''
    return redirect(reverse("web_index"))

def login(request):
    '''加载登录表单页'''
    shoplist=Shop.objects.filter(status=1)
    context={"shoplist":shoplist}
    return render(request,'web/login.html',context)

def dologin(request):
    try:
        # 执行是否选择店铺判断
        if request.POST['shop_id'] == 0:
            return redirect(reverse("web_login") + "?errinfo=1")  # 报错模式

        #执行验证码的校验
        if request.POST['code'] != request.session['verifycode']:
            return redirect(reverse("web_login")+"?errinfo=2") #报错模式

        #根据登录帐号获取登录者信息
        user = User.objects.get(username=request.POST['username'])
        #判断当前用户是否是管理员或者正常
        if user.status == 6 or user.status == 1:
            #判断密码是否相同
            import hashlib
            md5=hashlib.md5()
            s=request.POST['pass']+user.password_salt
            md5.update(s.encode('utf-8'))
            if user.password_hash == md5.hexdigest():
                #当前登录成功的用户信息以webuser为key写入到session中
                request.session['webuser'] = user.toDict()#session中只可以存放字典
                #获取当前店铺信息
                shopob=Shop.objects.get(id=request.POST["shop_id"])
                request.session['shopinfo'] = shopob.toDict()
                #获取当前店铺中菜品类别和信息
                clist=Category.objects.filter(shop_id=shopob.id,status=1)
                categorylist=dict()
                productlist=dict()
                for vo in clist:
                    c = {'id':vo.id,'name':vo.name,'pids':[]}
                    plist=Product.objects.filter(category_id=vo.id,status=1)
                    for p in plist:
                        c['pids'].append(p.toDict())
                        productlist[p.id]=p.toDict()
                    categorylist[vo.id]=c
                #将上述结果存放到session
                request.session['categorylist']=categorylist
                request.session['productlist']=productlist

                #重定向到大堂点餐首页
                return redirect(reverse("web_index"))
            else:
                return redirect(reverse("web_login")+"?errinfo=5")
        else:
            return redirect(reverse("web_login") + "?errinfo=4")
    except Exception as err:
        print(err)
        return redirect(reverse("web_login") + "?errinfo=3")
    return render(request,"myadmin/index/login.html",context)


def logout(request):
    '''执行前台退出操作'''
    del request.session['webuser']
    return redirect(reverse('web_login'))


def webindex(request):
    # 取出购物车信息
    carlist = request.session.get('carlist', {})
    total_money=0 #初始化一个总金额
    #遍历购物车中的菜品并累加金额
    for vo in carlist.values():
        total_money+=vo['num']*vo['price']
    request.session['total_money'] = total_money  # 放进session
    #将session中的菜品和类别信息获取并items转换，可实现for in遍历
    context={'categorylist':request.session.get('categorylist',{}).items()}
    return render(request,"web/index.html",context)
#验证码
def verify(request):
    #引入随机函数模块
    import random
    from PIL import Image, ImageDraw, ImageFont
    #定义变量，用于画面的背景色、宽、高
    #bgcolor = (random.randrange(20, 100), random.randrange(
    #    20, 100),100)
    bgcolor = (242,164,247)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    #str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = '0123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('static/ARIAL.TTF', 21)
    #font = ImageFont.load_default().font
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, -3), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, -3), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, -3), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, -3), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

#购物车管理视图
def cart_add(request,pid):
    '''添加购物车操作'''
    #从session中获取当前店铺中所有菜品信息，并从中获取要放入购物车的菜品
    product=request.session['productlist'][pid]
    product['num']=1 #初始化当前菜品的购买量
    #尝试从session中获取购物车信息
    carlist=request.session.get('carlist',{})
    #判断当前购物车中是否存在要放进购物车的菜品
    if pid in carlist:
        carlist[pid]['num']+=1
    else:
        carlist[pid]=product #放进购物车
    #将cartlist放入购物车
    request.session['carlist']=carlist
    print(carlist)
    return redirect(reverse('web_index'))

def cart_delete(request,pid):
    #取出购物车信息
    carlist=request.session.get('carlist',{})
    del carlist[pid]
    #将carlist购物车信息放入到session中
    request.session['carlist']=carlist
    return redirect(reverse('web_index'))

def cart_clear(request):
    request.session['carlist'] = {}
    return redirect(reverse('web_index'))

def cart_change(request):
    pid = request.GET.get('pid',0)#获取要修改的菜品id
    m=int(request.GET.get('num',1))#要修改的数量
    carlist=request.session.get('carlist',{})
    if m<1:
        m=1
    carlist[pid]['num']=m;#修改购物车中的数量
    request.session['carlist'] = carlist
    return redirect(reverse('web_index'))

#订单信息管理视图文件
from django.views.decorators.cache import cache_page
@cache_page(15) #整体缓存
def order_index(request,pIndex=1):
    '''浏览订单信息'''
    #获取当前店铺的id号，因为你只能是这个店里的
    sid=request.session['shopinfo']['id']
    ulist = Orders.objects.filter(shop_id=sid)  # 过滤查询
    mywhere = []
    # 获取并判断搜索条件
    kw = request.GET.get("keyword", None)
    if kw:
        ulist = ulist.filter(Q(username__contains=kw) | Q(nickname__contains=kw))  # Q对象
        mywhere.append('keyword=' + kw)
    # 获取，判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append("status=" + status)

    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(ulist, 10)  # 以每页5条数据分页，
    maxpages = page.num_pages
    # 判断当前页是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息

    for vo in list2:
        if vo.member_id == 0:
            vo.membername = "大堂顾客"
        else:
            member=Member.objects.only("mobile").get(id=vo.member_id)
            vo.membername=member.mobile

    context = {"orderslist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, 'web/list.html', context)
    # return render(request,'web/list.html')


#三张表的填写
def order_insert(request,pIndex=1):
    '''执行订单添加'''
    try:
        #执行订单数据的添加
        od = Orders()
        od.shop_id = request.session['shopinfo']['id']
        od.member_id = 0
        od.user_id=request.session['webuser']['id']
        od.money=request.session['total_money']
        od.status = 1#订单状态:1过行中/2无效/3已完成
        od.payment_status=2#支付状态:1未支付/2已支付/3已退款
        od.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.save()

        #执行支付信息添加
        op=Payment()
        op.order_id=od.id#订单id号
        op.member_id=0
        op.type=2
        op.bank=request.GET.get("bank",3)#收款银行渠道：1微信/2余额/3现金/4支付宝
        op.money = request.session['total_money']
        op.status = 2  # 支付状态:1未支付/2已支付/3已退款
        od.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.save()

        #执行订单祥情的添加
        carlist=request.session.get("carlist",{})
        for item in carlist.values(): #循环购物车中的东西并添加到订单祥情中
            ov=OrderDetail()
            ov.order_id=od.id#订单id号
            ov.product_id=item['id']#菜品id
            ov.product_name=item['name']#菜品名称
            ov.price=item['price'] #单价
            ov.quantity=item['num'] #数量
            ov.status=1#状态：1正常/9删除
            ov.save()
        del request.session['carlist']
        del request.session['total_money']
        return HttpResponse("Y")
    except Exception as err:
        print(err)
        return HttpResponse("N")

def order_detail(request):
    '''加载订单详情'''
    oid=request.GET.get("oid",0)
    dlist=OrderDetail.objects.filter(order_id=oid)
    context={"detaillist":dlist}
    return render(request,"web/detail.html",context)


def order_status(request):
    '''修改订单状态'''
    try:
        oid =request.GET.get("oid",0)
        ob = Orders.objects.get(id=oid)  # 获取要修改的员工
        ob.status = request.GET['status']
        ob.save()
        return HttpResponse("Y")
    except Exception as err:
        print(err)
        return HttpResponse("N")

