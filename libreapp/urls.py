from django.urls import path, include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import supplier_edt

##router=DefaultRouter()
##router.register('supplier', supplier_edt)

urlpatterns=[
    path("",views.home, name='home.html'),
    path("base",views.base, name='base.html'),
    path("sto_entry", views.sto_entry, name='sto_entry.html'),
    path("bookdt/<uuid:acceno>", views.bookdt, name='bookdt.html'),
    path("memdt/<mem_id>",views.memdt, name="memdt.html"),
    path("sto_book", views.sto_book, name='sto_book.html'),
    path("sup_entry", views.sup_entry, name='sup_entry.html'),
    path("sup_list", views.sup_list, name='sup_list.html'),
    path("sup_dt/<supp_id>", views.sup_dt, name='sup_dt.html'),
    path("mem_entry", views.mem_entry, name='mem_entry.html'),
    path("mem_list", views.mem_list, name='mem_list.html'),
    path("issu_lt", views.issu_lt , name='issu_lt.html'),
    path("issu_dt/<issu_id>", views.issu_dt, name='issu_dt.html'),
    path('issu_entry',views.issu_entry, name='issu_entry.html'),
    path("issu_ret/<issu_id>", views.issu_ret, name='issu_ret.html'),
    path("tot_sup", views.tot_sup, name= 'tot_sup.html'),
    path("issu_retdt", views.issu_retdt, name='issu_retdt.html'),
    path("sale_nw", views.sale_nw, name='sale_nw.html'),
    path("sale_list", views.sale_list, name="sale_list.html"),
    path("vw_bill/<invcno>", views.vw_bill, name="vw_bill.html"),
    path("issu_fine/<uuid:issu_id>", views.issu_fine, name="issu_fine.html"),
    path("pur_lst", views.pur_lst, name="pur_lst.html"),
    path("pur_dt/<purch_id>", views.pur_dt, name="pur_dt.html"),
    ## This for REST API
    path("supplier/<supp_id>", supplier_edt.as_view(),name="supplier_edt"),
    ##path('', include(router.urls)),
    path("edit_supplier/<supp_id>", views.edit_supplier, name="edit_supplier.html"),
    path("sup_det/<supp_id>", views.sup_det, name="sup_det.html"),
    path("mem_edt/<member_id>", views.mem_edt, name="mem_edt.html"),
    path("memdel/<member_id>", views.memdel, name="memdel.html"),
    path("sto_edt/<acceno>", views.sto_edt, name="sto_edt.html"), 
    path("sto_del/<acceno>", views.sto_del, name="sto_del.html"),
    path("iss_edt/<issu_id>", views.iss_edt, name="iss_edt.html"), 
    path("iss_del/<issu_id>", views.iss_del, name="iss_del.html"), 
    path("sale_edt/<invcno>", views.sale_edt, name="sale_edt.html"),
    path("sale_del/<invcno>", views.sale_del, name= "sale_del.html"),
]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)