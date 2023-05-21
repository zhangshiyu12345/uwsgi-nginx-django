from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import time
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
import csv
from django.urls import reverse
from django.shortcuts import redirect
from myadmin.models import Member,Shop,Category,Product,Orders,Payment,OrderDetail
from datetime import datetime


# Create your views here.
def index(request):
    '''移动端首页'''
    #获取并判断当前的店铺信息
    shopinfo=request.session.get("shopinfo",None)
    if shopinfo is None:
        return redirect(reverse('mobile_shop'))#从定向到店铺选择页
    #获取当前店铺下的菜品类别和菜品信息
    clist=Category.objects.filter(shop_id=shopinfo['id'],status=1)
    productlist=dict()
    for vo in clist:
        plist=Product.objects.filter(category_id=vo.id,status=1)
        productlist[vo.id]=plist
    context={'categorylist':clist,'productlist':productlist.items(),'cid':clist[0]}

    return render(request,"mobile/index.html",context)



    return render(request,"mobile/index.html")

def register(request):
    '''移动端会员注册/登录表单'''
    return render(request,"mobile/register.html")

def doRegister(request):
    ''' 执行会员注册/登录 '''
    # 模拟短信验证
    verifycode = "1234"  # reuqest.session['verifycode']
    if verifycode != request.POST['code']:
        context = {"info": '短信验证码错误'}
        return render(request, "mobile/register.html", context)

    try:
        # 根据手机号码获取当前会员信息
        member = Member.objects.get(mobile=request.POST['mobile'])
    except Exception as err:
        # print(err)
        # 此处可以执行当前会员注册（添加）
        ob = Member()
        ob.nickname = "顾客"  # 默认会员名称
        ob.avatar = "moren.png"  # 默认头像
        ob.mobile = request.POST['mobile']  # 手机号码
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        member = ob
    # 检验当前会员状态
    if member.status == 1:
        # 将当前会员信息转成字典格式并存放到session中
        request.session['mobileuser'] = member.toDict()
        # 重定向到登录页
        return redirect(reverse("mobile_index"))
    else:
        context = {"info": '此账户信息禁用！'}
        return render(request, "mobile/register.html", context)


def shop(request):
    '''移动端选择店铺页面'''
    context={"shoplist":Shop.objects.filter(status=1)}
    return render(request,'mobile/shop.html',context)

def selectShop(request):
    '''执行移动端店铺选择'''
    #获取选择的店铺信息并放置到session中
    sid=request.GET['sid']
    ob=Shop.objects.get(id=sid)
    request.session['carlist']={}#清空购物车
    request.session['shopinfo']=ob.toDict()

    #跳转到首页
    return redirect(reverse("mobile_index"))

def addOrders(request):
    '''移动端下单表单页'''
    # 尝试从session中获取名字为cartlist的购物车信息，若没有返回{}
    carlist = request.session.get('carlist', {})
    total_money = 0  # 初始化一个总金额
    # 遍历购物车中的菜品并累加总金额
    for vo in carlist.values():
        total_money += vo['num'] * vo['price']
    request.session['total_money'] = total_money  # 放进session
    return render(request, "mobile/addOrders.html")

def doAddOrders(request):
    ''' 执行订单添加操作 '''
    try:
        #执行订单信息的添加
        od = Orders()
        od.shop_id = request.session['shopinfo']['id']
        od.member_id = request.session['mobileuser']['id']
        od.user_id = 0
        od.money = request.session['total_money']
        od.status = 1 #订单状态:1过行中/2无效/3已完成
        od.payment_status = 2 #支付状态:1未支付/2已支付/3已退款
        od.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.save()

        #执行支付信息添加
        op = Payment()
        op.order_id = od.id #订单id号
        op.member_id = request.session['mobileuser']['id']
        op.type = 2
        op.bank = request.GET.get("bank",3) #收款银行渠道:1微信/2余额/3现金/4支付宝
        op.money = request.session['total_money']
        op.status = 2 #支付状态:1未支付/2已支付/3已退款
        op.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.save()

        #执行订单详情的添加
        cartlist = request.session.get("cartlist",{}) #获取购物车中的菜品信息
        #遍历购物车中的菜品并添加到订单详情中
        for item in cartlist.values():
            ov = OrderDetail()
            ov.order_id = od.id  #订单id
            ov.product_id = item['id']  #菜品id
            ov.product_name = item['name'] #菜品名称
            ov.price = item['price']     #单价
            ov.quantity = item['num']  #数量
            ov.status = 1 #状态:1正常/9删除
            ov.save()

        del request.session["cartlist"]
        del request.session['total_money']
    except Exception as err:
        print(err)
    return render(request,"mobile/orderinfo.html",{"order":od})

def member_index(request):
    '''个人中心首页'''
    return render(request,"mobile/member.html")

def member_orders(request):
    '''个人中心浏览订单'''
    mod = Orders.objects
    mid = request.session['mobileuser']['id']  # 获取当前会员id号
    olist = mod.filter(member_id=mid)
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        olist = olist.filter(status=status)

    list2 = olist.order_by("-id")  # 对id排序
    #遍历当前订单，封装订单详情信息
    orders_status=['无','排队中','已撤销','已完成']
    for vo in list2:
        plist=OrderDetail.objects.filter(order_id=vo.id)[:4]
        vo.plist=plist
        vo.statusinfo=orders_status[vo.status]

    context = {"orderslist": list2}
    return render(request,"mobile/member_orders.html",context)

def member_detail(request):
    '''个人中心的订单祥情'''
    orders_status = ['无', '排队中', '已撤销', '已完成']
    pid=request.GET.get('pid',0)
    #获取当前订单
    order=Orders.objects.get(id=pid)
    #获取当前订单详情
    plist=OrderDetail.objects.filter(order_id=order.id)
    order.plist=plist
    shop=Shop.objects.only("name").get(id=order.shop_id)
    order.shopname=shop.name
    order.statusinfo=orders_status[order.status]
    return render(request,"mobile/member_detail.html",{'order':order})

def member_logout(request):
    '''执行会员退出'''
    del request.session['mobileuser']
    return render(request,"mobile/register.html")

#购物车管理视图
def cart_add(request):
    '''添加购物车操作'''
    #获取要购买的菜品信息
    carlist=request.session.get('carlist',{})
    pid = request.GET.get("pid",None)
    if pid is not None:
        product=Product.objects.get(id=pid).toDict()
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
        #print(carlist)
    #响应:购物车转成json格式的数据

    return JsonResponse({'carlist':carlist})

def cart_delete(request):
    #取出购物车信息
    carlist=request.session.get('carlist',{})
    del carlist[pid]
    #将carlist购物车信息放入到session中
    request.session['carlist']=carlist
    return JsonResponse({'carlist': carlist})

def cart_clear(request):
    request.session['carlist'] = {}
    return JsonResponse({'carlist': {}})

def cart_change(request):
    pid = request.GET.get('pid',0)#获取要修改的菜品id
    m=int(request.GET.get('num',1))#要修改的数量
    carlist=request.session.get('carlist',{})
    if m<1:
        m=1
    carlist[pid]['num']=m;#修改购物车中的数量
    request.session['carlist'] = carlist
    return JsonResponse({'cartlist': carlist})
