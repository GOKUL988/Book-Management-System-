from django.contrib import admin
from.models import supplier,purchase,stock,member,issue,sales, saledt, subcateg, racks, catogories
# Register your models here.
admin.site.register(supplier)
admin.site.register(purchase)
admin.site.register(stock)
admin.site.register(member)
admin.site.register(issue)
admin.site.register(sales)
admin.site.register(saledt)
admin.site.register(subcateg)
admin.site.register(racks)
admin.site.register(catogories)
