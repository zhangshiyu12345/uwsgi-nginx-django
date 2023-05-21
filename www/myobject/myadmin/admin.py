from django.contrib import admin

# Register your models here.
from .models import User,Product,Payment,Shop,OrderDetail,Orders,Category
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Payment)
admin.site.register(Shop)
admin.site.register(Orders)
admin.site.register(OrderDetail)
admin.site.register(Category)