from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
import time
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
import csv
# Create your views here.
#员工信息视图文件
#增删改查
from myadmin.models import User
from myadmin.models import Shop
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse

def index1(request):#后台首页
    return render(request,'myadmin/index/index.html')

def index(request,pIndex=1):
    '''浏览信息'''
    ulist=User.objects.filter(status__lt=9)#过滤查询
    mywhere=[]
    #获取并判断搜索条件
    kw = request.GET.get("keyword",None)
    if kw:
        ulist = ulist.filter(Q(username__contains=kw)|Q(nickname__contains=kw))#Q对象
        mywhere.append('keyword='+kw)
    #获取，判断并封装状态status搜索条件
    status=request.GET.get('status','')
    if status != '':
        ulist=ulist.filter(status=status)
        mywhere.append("status="+status)

    #执行分页处理
    pIndex=int(pIndex)
    page=Paginator(ulist,5)#以每页5条数据分页
    maxpages=page.num_pages
    #判断当前页是否越界
    if pIndex > maxpages :
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)#获取当前页数据
    plist = page.page_range#获取页码列表信息
    context={"userlist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,'myadmin/user/index.html',context)
    #return render(request,'myadmin/index/index.html')

def add(request):
    '''加载信息添加表单'''
    return render(request,"myadmin/user/add.html")

def insert(request):
    '''执行信息添加'''
    try:
        ob=User()
        ob.username=request.POST['username']
        ob.nickname=request.POST['nickname']

        #密码加密操作,做md5处理(直接从网上找就行了)
        import hashlib,random
        md5=hashlib.md5()
        n=random.randint(100000,999999)
        s=request.POST['password']+str(n)
        md5.update(s.encode('utf-8'))
        ob.password_hash=md5.hexdigest()
        ob.password_salt=n

        ob.status=1
        ob.create_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={'info':"添加成功"}
    except Exception as err:
        print(err)
        context={'info':"添加失败"}
    return render(request,"myadmin/info.html",context)


def delete(request,uid=0):
    '''执行信息删除'''
    try:
        ob=User.objects.get(id=uid)#获取要修改的员工
        ob.status=9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={'info':"删除成功"}
    except Exception as err:
        print(err)
        context={'info':"删除失败"}
    return render(request,"myadmin/info.html",context)

def edit(request,uid=0):
    '''加载信息编辑表单'''
    try:
        ob=User.objects.get(id=uid)#获取要编辑的员工
        context={'user':ob}
        return render(request, "myadmin/user/edit.html", context)
    except Exception as err:
        print(err)
        context={'info':"没有找到要修改的信息"}
        return render(request,"myadmin/info.html",context)


def update(request,uid=0):#说明路经中传了参数
    '''执行信息编辑'''
    try:
        ob = User.objects.get(id=uid)  # 获取要修改的员工
        ob.status = request.POST['status']
        ob.nickname=request.POST['nickname']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "修改成功"}
    except Exception as err:
        print(err)
        context = {'info': "修改失败"}
    return render(request, "myadmin/info.html", context)


#会员登录表单
def login(request):
    return render(request,'myadmin/index/login.html')

#执行会员登录
def dologin(request):
    try:
        #执行验证码的校验
        if request.POST['code'] != request.session['verifycode']:
            context={"info":"验证码错误"}
            return render(request,"myadmin/index/login.html",context)

        #根据登录帐号获取登录者信息
        user = User.objects.get(username=request.POST['username'])
        #判断当前用户是否是管理员
        if user.status == 6:
            #判断密码是否相同
            import hashlib
            md5=hashlib.md5()
            s=request.POST['pass']+user.password_salt
            md5.update(s.encode('utf-8'))
            if user.password_hash == md5.hexdigest():
                #当前登录成功的用户信息以adminuser为key写入到session中
                request.session['adminuser'] = user.toDict()#session中只可以存放字典
                #重定向到后台的管理首页
                return redirect(reverse("myadmin_index"))
            else:
                context={'info':"登录密码错误"}
        else:
            context={"info":"无效的登录账户"}
    except Exception as err:
        print(err)
        context={"info":"登录帐号不存在"}
    return render(request,"myadmin/index/login.html",context)
#会员退出
def logout(request):
    del request.session['adminuser']
    return redirect(reverse("myadmin_login"))

#输出验证码
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


#店铺信息管理
def shop_index(request,pIndex=1):
    '''浏览信息'''
    slist=Shop.objects.filter(status__lt=9)#过滤查询
    mywhere=[]
    #获取并判断搜索条件
    kw = request.GET.get("keyword",None)
    if kw:
        slist = slist.filter(name__contains=kw)#Q对象
        mywhere.append('keyword='+kw)
    #获取，判断并封装状态status搜索条件
    status=request.GET.get('status','')
    if status != '':
        slist=slist.filter(status=status)
        mywhere.append("status="+status)

    slist=slist.order_by("id")#对id排序

    #执行分页处理
    pIndex=int(pIndex)
    page=Paginator(slist,5)#以每页5条数据分页
    maxpages=page.num_pages
    #判断当前页是否越界
    if pIndex > maxpages :
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)#获取当前页数据
    plist = page.page_range#获取页码列表信息
    context={"shoplist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,'myadmin/shop/index.html',context)
    #return render(request,'myadmin/index/index.html')


def shop_add(request):
    return render(request,"myadmin/shop/add.html")

def shop_insert(request):
    '''执行信息添加'''
    try:
        #店铺封面图片的上传处理
        myfile=request.FILES.get("cover_pic",None)
        if not myfile:
            return HttpResponse("没有店铺上传文件信息")
        cover_pic=str(time.time())+"."+myfile.name.split('.').pop()
        destination=open("./static/uploads/shop/"+cover_pic,"wb+")
        for chunk in myfile.chunks():
            destination.write(chunk)
        destination.close()

        #店铺logo图片的上传处理
        myfile = request.FILES.get("banner_pic", None)
        if not myfile:
            return HttpResponse("没有店铺logo上传文件信息")
        banner_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/" + banner_pic, "wb+")
        for chunk in myfile.chunks():
            destination.write(chunk)
        destination.close()

        ob = Shop()
        ob.name = request.POST['name']
        ob.address = request.POST['address']
        ob.phone=request.POST['phone']
        ob.cover_pic=cover_pic
        ob.banner_pic=banner_pic
        ob.status=1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "添加成功"}
    except Exception as err:
        print(err)
        context = {'info': "添加失败"}
    return render(request, "myadmin/info.html", context)

def shop_delete(request,sid=0):
    '''执行信息删除'''
    try:
        ob=Shop.objects.get(id=sid)#获取要修改的员工
        ob.status=9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={'info':"删除成功"}
    except Exception as err:
        print(err)
        context={'info':"删除失败"}
    return render(request,"myadmin/info.html",context)

def shop_edit(request,sid=0):
    '''加载信息编辑表单'''
    try:
        ob=Shop.objects.get(id=sid)#获取要编辑的员工
        context={'shop':ob}
        return render(request, "myadmin/shop/edit.html", context)
    except Exception as err:
        print(err)
        context={'info':"没有找到要修改的信息"}
        return render(request,"myadmin/info.html",context)


def shop_update(request,sid=0):#说明路经中传了参数
    '''执行信息编辑'''
    try:
        ob = Shop.objects.get(id=sid)  # 获取要修改的员工
        ob.status = request.POST['status']
        ob.name=request.POST['name']
        ob.address=request.POST['address']
        ob.phone=request.POST['phone']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "修改成功"}
    except Exception as err:
        print(err)
        context = {'info': "修改失败"}
    return render(request, "myadmin/info.html", context)

#菜品类别的信息管理
from myadmin.models import Category
def category_index(request,pIndex=1):
    '''浏览信息'''
    slist=Category.objects.filter(status__lt=9)#过滤查询
    mywhere=[]
    #获取并判断搜索条件
    kw = request.GET.get("keyword",None)
    if kw:
        slist = slist.filter(name__contains=kw)#Q对象
        mywhere.append('keyword='+kw)
    #获取，判断并封装状态status搜索条件
    status=request.GET.get('status','')
    if status != '':
        slist=slist.filter(status=status)
        mywhere.append("status="+status)

    slist=slist.order_by("id")#对id排序

    #执行分页处理
    pIndex=int(pIndex)
    page=Paginator(slist,10)#以每页10条数据分页
    maxpages=page.num_pages
    #判断当前页是否越界
    if pIndex > maxpages :
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)#获取当前页数据
    plist = page.page_range#获取页码列表信息
    #遍历当前菜品分类信息并封装对应的店铺信息(跨表查询)
    for vo in list2:
        sob=Shop.objects.get(id=vo.shop_id)
        vo.shopname=sob.name
    context={"categorylist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,'myadmin/category/index.html',context)
    #return render(request,'myadmin/index/index.html')

def category_loadCategory(request,sid):
    clist = Category.objects.filter(status__lt=9,shop_id=sid).values("id","name")
    #返回QuerySet对象，使用list强转成对应的菜品分类列表信息
    return JsonResponse({'data':list(clist)})

def category_add(request):
    #获取所有店铺
    slist=Shop.objects.values("id","name")
    context={"shoplist":slist}
    return render(request,"myadmin/category/add.html",context)

def category_insert(request):
    '''执行信息添加'''
    try:
        ob = Category()
        ob.shop_id = request.POST['shop_id']
        ob.name = request.POST['name']
        ob.status=1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "添加成功"}
    except Exception as err:
        print(err)
        context = {'info': "添加失败"}
    return render(request, "myadmin/info.html", context)

def category_delete(request,cid=0):
    '''执行信息删除'''
    try:
        ob=Category.objects.get(id=cid)#获取要修改的员工
        ob.status=9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={'info':"删除成功"}
    except Exception as err:
        print(err)
        context={'info':"删除失败"}
    return render(request,"myadmin/info.html",context)

def category_edit(request,cid=0):
    '''加载信息编辑表单'''
    try:
        slist = Shop.objects.values("id", "name")
        context = {"shoplist": slist}
        ob=Category.objects.get(id=cid)#获取要编辑的员工
        context["category"] = ob
        return render(request, "myadmin/category/edit.html", context)
    except Exception as err:
        print(err)
        context={'info':"没有找到要修改的信息"}
        return render(request,"myadmin/info.html",context)


def category_update(request,cid=0):#说明路经中传了参数
    '''执行信息编辑'''
    try:
        ob = Category.objects.get(id=cid)  # 获取要修改的员工
        ob.shop_id = request.POST['shop_id']
        ob.name = request.POST['name']
        ob.status=request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "修改成功"}
    except Exception as err:
        print(err)
        context = {'info': "修改失败"}
    return render(request, "myadmin/info.html", context)


#菜品信息管理
from myadmin.models import Product
import time,os #图片上传
def product_index(request,pIndex=1):
    '''浏览信息'''
    slist=Product.objects.filter(status__lt=9)#过滤查询
    mywhere=[]
    #获取并判断搜索条件
    kw = request.GET.get("keyword",None)
    if kw:
        slist = slist.filter(name__contains=kw)#Q对象
        mywhere.append('keyword='+kw)
    #获取并判断搜素菜品类别条件
    cid = request.GET.get("category_id", None)
    if cid:
        slist = slist.filter(category_id__contains=cid)  # Q对象
        mywhere.append('category_id=' + cid)
    #获取，判断并封装状态status搜索条件
    status=request.GET.get('status','')
    if status != '':
        slist=slist.filter(status=status)
        mywhere.append("status="+status)

    slist=slist.order_by("id")#对id排序

    #执行分页处理
    pIndex=int(pIndex)
    page=Paginator(slist,10)#以每页10条数据分页
    maxpages=page.num_pages
    #判断当前页是否越界
    if pIndex > maxpages :
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)#获取当前页数据
    plist = page.page_range#获取页码列表信息
    #遍历当前菜品分类信息并封装对应的店铺和菜品类别信息信息(跨表查询)
    for vo in list2:
        sob=Shop.objects.get(id=vo.shop_id)
        vo.shopname=sob.name
        cob=Category.objects.get(id=vo.category_id)
        vo.categoryname=cob.name
    context={"productlist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,'myadmin/product/index.html',context)
    #return render(request,'myadmin/index/index.html')

def product_add(request):
    #获取所有店铺
    slist=Shop.objects.values("id","name")
    context={"shoplist":slist}
    return render(request,"myadmin/product/add.html",context)

def product_insert(request):
    '''执行信息添加'''
    try:
        myfile = request.FILES.get("cover_pic", None)
        if not myfile:
            return HttpResponse("没有封面上传文件信息")
        cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/product/" + cover_pic, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        ob = Product()
        ob.shop_id = request.POST['shop_id']
        ob.category_id=request.POST['category_id']
        ob.name = request.POST['name']
        ob.price=request.POST['price']
        ob.status=1
        ob.cover_pic=cover_pic
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "添加成功"}
    except Exception as err:
        print(err)
        context = {'info': "添加失败"}
    return render(request, "myadmin/info.html", context)

def product_delete(request,pid=0):
    '''执行信息删除'''
    try:
        ob=Product.objects.get(id=pid)#获取要修改的员工
        ob.status=9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={'info':"删除成功"}
    except Exception as err:
        print(err)
        context={'info':"删除失败"}
    return render(request,"myadmin/info.html",context)

def product_edit(request,pid=0):
    '''加载信息编辑表单'''
    try:
        ob= Product.objects.get(id=pid)
        context = {"product": ob}
        slist=Shop.objects.values("id","name")#获取要编辑的员工
        context["shoplist"] = slist
        return render(request, "myadmin/product/edit.html", context)
    except Exception as err:
        print(err)
        context={'info':"没有找到要修改的信息"}
        return render(request,"myadmin/info.html",context)


def product_update(request,pid=0):#说明路经中传了参数
    '''执行信息编辑'''
    try:
        #获取原图片
        oldpicname=request.POST['oldpicname']

        #图片的的上传
        myfile = request.FILES.get("cover_pic", None)
        if not myfile:
            cover_pic=oldpicname
        else:
            cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
            destination = open("./static/uploads/product/" + cover_pic, "wb+")
            for chunk in myfile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()

        ob = Product.objects.get(id=pid)  # 获取要修改的员工
        ob.shop_id = request.POST['shop_id']
        ob.category_id=request.POST["category_id"]
        ob.name = request.POST['name']
        ob.price=request.POST['price']
        ob.cover_pic=cover_pic
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "修改成功"}

        #判断并删除老图片
        if myfile:
            os.remove("./static/uploads/product/" + oldpicname)
    except Exception as err:
        print(err)
        context = {'info': "修改失败"}
        if myfile:
            os.remove("./static/uploads/product/" + cover_pic)
    return render(request, "myadmin/info.html", context)

#会员信息管理
from myadmin.models import Member
def member_index(request,pIndex=1):
    '''浏览信息'''
    ulist=Member.objects.filter(status__lt=9)#过滤查询
    mywhere=[]
    #获取，判断并封装状态status搜索条件
    status=request.GET.get('status','')
    if status != '':
        ulist=ulist.filter(status=status)
        mywhere.append("status="+status)

    #执行分页处理
    pIndex=int(pIndex)
    page=Paginator(ulist,5)#以每页5条数据分页
    maxpages=page.num_pages
    #判断当前页是否越界
    if pIndex > maxpages :
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)#获取当前页数据
    plist = page.page_range#获取页码列表信息
    context={"memberlist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,'myadmin/member/index.html',context)
    #return render(request,'myadmin/member/index.html')

def member_delete(request,uid=0):
    '''执行信息删除'''
    try:
        ob=Member.objects.get(id=uid)#获取要修改的员工
        ob.status=9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={'info':"删除成功"}
    except Exception as err:
        print(err)
        context={'info':"删除失败"}
    return render(request,"myadmin/info.html",context)

