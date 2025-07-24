from django.shortcuts import render,redirect, get_object_or_404
from rest_framework.response import Response
from django.forms import inlineformset_factory
from rest_framework.views import APIView
from rest_framework import status
from .models import purchase,supplier,stock,issue,member,sales,saledt,subcateg,racks, catogories
import json
from django.contrib import messages
from datetime import date, datetime
from django.db.models import Q
from .serializers import supplier1
from rest_framework import viewsets
from .forms import supp_edt, memedt, stocedt, issuedt ,saleedt,saledtedt

# Create your views here.
def home(request):
    return render(request, 'home.html')
def base(request):
    return render(request, 'base.html')
def sto_book(request):
    data_search= stock.objects.all()
    sea_qt = request.GET.get('search1')
    if sea_qt:
       book_inf= stock.objects.filter(
            Q(booktitle__icontains=sea_qt) | Q(isbn__icontains=sea_qt)
        )
    else:
        book_inf = stock.objects.all().order_by("-purc_id__date")
    return render(request, 'stock/sto_book.html',{'book_inf': book_inf, 'data_search' : data_search})
def bookdt(request,acceno):
    book1=get_object_or_404(stock, acceno=acceno)
    purchasedt=book1.purc_id
    supplierdt=book1.suppl_id
    issu_dt=issue.objects.filter(book_id=book1)
    context={
        'a':book1,
        'b':purchasedt,
        'c':supplierdt,
        'd':issu_dt,
    }
    return render(request, "stock/bookdt.html", context)

def memdt(request,mem_id):
    mem=member.objects.get(member_id=mem_id)
    sto_iss=issue.objects.filter(mem_id=mem)
    return render(request, "member/memdt.html",locals())

def sto_entry(request):
    supp = supplier.objects.all()
    cat = catogories.objects.all()
    sub = subcateg.objects.all() 
    rac =racks.objects.all()
    context={
        'supp': supp,
        'sub' : sub, 
        'rac' : rac, 
        'a' : cat
    }
    if request.method == "POST":
        sup_id= request.POST.get("supp_id")
        suppdt=supplier.objects.get(supp_id=sup_id)
        bill_no= request.POST.get("billno")
        dat=request.POST.get("date")
        bill=request.FILES.get('bill')
        pur_inf=purchase.objects.create(
            supp_id= suppdt,
            billno=bill_no,
            date=dat,
            bill=bill
        )
        bkdt=request.POST.getlist("booktitle[]")
        autnme=request.POST.getlist("authorname[]")
        edt=request.POST.getlist("edition[]")
        year=request.POST.getlist("yearofpub[]")
        catogo_lst = request.POST.getlist("categ[]")
        clasfic=request.POST.getlist("classfic[]")
        qua=request.POST.getlist("qun[]")
        rte=request.POST.getlist("rate[]")
        rck=request.POST.getlist("rack[]")

        for booktitle,authorname, edition, yearofpub, rate,qun, catego_ries, classfic,rack in zip(bkdt, autnme, edt, year, rte, qua, catogo_lst, clasfic, rck):
            stock.objects.create(
                suppl_id = suppdt,
                purc_id = pur_inf,
                booktitle=booktitle,
                authorname= authorname,
                edition = edition,
                yearofpub = yearofpub,
                rate=rate,
                qun =qun,
                catego_ries= catego_ries,
                classfic=classfic,
                rack=rack,
                ava= "YES"
            )
        return redirect("sto_book.html")
        
    return render(request, 'stock/sto_entry.html', context)

def sup_entry(request):
    if request.method=="POST":
        supp_dt=supplier(
            sup_name=request.POST.get('sup_name'),
            email=request.POST.get('email'),
            mobile=request.POST.get('mobile'),
            doorno=request.POST.get('doorno'),
            street=request.POST.get('street'),
            dist=request.POST.get('dist'),
            stat=request.POST.get('stat'),
            pin=request.POST.get('pin'),
        )
        supp_dt.save()
        messages.success(request, "Supplier Entry has been saved Successfully !")
        return redirect('sup_list.html')
    return render(request, 'supplier/sup_entry.html')

def sup_list(request):
    sup_flt=request.GET.get('search_supp')
    if sup_flt:
        if sup_flt:
            suplist=supplier.objects.filter(
                Q(supp_id__icontains=sup_flt) | Q(sup_name__icontains=sup_flt)
            )
        else:
            messages.success(request, "NO Search Supplier are founded")
    else:
        suplist=supplier.objects.all()
    return render(request, "supplier/sup_list.html",locals())
def sup_dt(request,supp_id):
    supp=get_object_or_404(supplier,supp_id=supp_id)
    purdt=stock.objects.filter(suppl_id=supp)
    context={
        'supp':supp,
        'purdt':purdt
    }
    return render(request, "supplier/sup_dt.html",context)

def mem_entry(request):
    if request.method=="POST":
        mement=member(
            memname=request.POST.get('memname'),
            dob=request.POST.get('dob'),
            gender=request.POST.get('gender'),
            doorno=request.POST.get('doorno'),
            strnme=request.POST.get('strnme'),
            dist=request.POST.get('dist'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode'),
            memtype=request.POST.get('memtype')
        )
        mement.save()
        messages.success(request, "Member Entry has been saved Successfully !")
        return redirect('mem_list.html')
    return render(request, "member/mem_entry.html")
def mem_list(request):
    memlist = member.objects.all()
    mem_flt=request.GET.get("search_mem")
    no_res=False
    if mem_flt:
        memlist=member.objects.filter(
            Q(member_id__icontains=mem_flt) | Q(memname__icontains=mem_flt)
        )
        if not memlist.exists():
            no_res=True

    context={
        'memlist':memlist,
        'non':no_res
    }
    return render(request,"member/mem_list.html",context)

def issu_lt(request):
    isslist=issue.objects.all()
    iss_flt=request.GET.get("search_issu")
    no_rec=False
    if iss_flt:
        isslist= issue.objects.filter(
            Q(book_id__booktitle__icontains=iss_flt) | Q(mem_id__member_id=iss_flt) | Q(mem_id__memname=iss_flt)
        )
        if not isslist.exists():
            no_rec=True

    context={
         'isslist':isslist,
         'no_rec':no_rec
    }
    return render(request, "issue/issu_lt.html",context)
def issu_dt(request, issu_id):
    issdt=issue.objects.filter(issu_id=issu_id)
    context={
        'a': issdt,
    }
    return render(request, "issue/issu_dt.html", context)

def issu_entry(request):
    sto=stock.objects.all()
    mem=member.objects.all()
    sto_finish = False
    saved = False
    if request.method=="POST":
        sel_book=stock.objects.get(acceno=request.POST.get('book_id'))
        sel_mem=get_object_or_404(member, member_id=request.POST.get('mem_id'))
        if sel_book.ava.lower() == "yes" and sel_book.qun >=1 :
            issnew = issue(
                book_id=sel_book,
                mem_id=sel_mem,
                iss_date= request.POST.get('iss_date'),
                ret_date= request.POST.get('ret_date')
            )
            issnew.save()
            messages.success(request, "Issue has been successfully saved!")
            return redirect('issu_lt.html')
        else:
            messages.error(request, "Book is not available to issue.")
            return redirect('issu_lt.html')

    context = {
            'BK_LST': sto,
            'MEM_LST': mem,
    }
    return render(request, "issue/issu_entry.html",context)

def issu_ret(request, issu_id):
    iss_obj1 = issue.objects.filter(issu_id=issu_id, actual_date__isnull=True)
    if request.method == "POST":
        iss_obj = issue.objects.get(issu_id= issu_id, actual_date__isnull=True)
        actual_date = request.POST.get('actual_date')
        if iss_obj and actual_date:
            actual_date1 = datetime.strptime(actual_date, "%Y-%m-%d").date()
            iss_obj.actual_date = actual_date1
            iss_obj.save()
            if iss_obj.fine >=1:
                return redirect("issu_fine.html", issu_id=iss_obj.issu_id )
            else:
                return redirect("issu_lt.html")
    return render(request, "issue/issu_ret.html",locals())

def issu_fine(request,issu_id):
    iss_obj2 = issue.objects.filter(issu_id=issu_id, paymth__isnull=True)
    if request.method == "POST":
        iss_obj = issue.objects.get(issu_id=issu_id, paymth__isnull=True)
        paymth1 = request.POST.get('paymth')
        if iss_obj and paymth1:
            iss_obj.paymth = paymth1
            iss_obj.save()
            messages.success(request, "Payment method saved successfully.")
            return redirect("issu_lt.html")
    return render(request, "issue/issu_fine.html", {"iss_obj2":iss_obj2})

def tot_sup(request):
    amount=0
    quan1=0
    sup_en=0
    count_mem=0
    tot_fine=0
    tot_sales=0
    book_obj=stock.objects.all()
    for i in book_obj:
        amu=i.rate
        quan=i.qun
        res=amu*quan
        quan1=quan1 + quan
        amount=amount+res

    sup_obj= supplier.objects.all()
    for j in sup_obj:
        supp=j.supp_id
        sup_en=sup_en+1

    mem_dt=member.objects.all()
    for a in mem_dt:
        mem=a.member_id
        count_mem=count_mem+1

    iss_tot=issue.objects.all()
    for b in iss_tot:
        fines=b.fine
        tot_fine=tot_fine+fines

    sale_tot= sales.objects.all()
    for c in sale_tot:
        ech=c.tot
        tot_sales=tot_sales+ech


    return render(request, 'more/tot_sup.html',locals())

def issu_retdt(request):
    isslist=issue.objects.filter(actual_date__isnull=True)
    return render(request, 'issue/issu_retdt.html',locals())
def sale_nw(request):
    mem_lst=member.objects.all()
    sto_lst=stock.objects.filter(qun__gt= 0)
    total = 0 
    noti = False
    if request.method== "POST":
        if sto_lst: 
            memid=request.POST.get("memdt")
            tot=request.POST.get("total")
            invo_inf= sales.objects.create(
                mem_dt=member.objects.get(member_id=memid),
                dat = request.POST.get("dat"),
                tot =0,
            )
            isbn_list=request.POST.getlist("isbn_dt[]")
            book_list = request.POST.getlist("book_dt[]")
            rate_list=request.POST.getlist("perunt[]")
            qun_list=request.POST.getlist("qunt[]")
            amt_list=request.POST.getlist("amount[]")
            for bkisbn_dt, bktit_dt, perunt, qunt, amount in zip(isbn_list, book_list, rate_list, qun_list, amt_list):
                saledt.objects.create(
                    invoice = invo_inf,
                    bkisbn_dt=stock.objects.get(isbn=bkisbn_dt),
                    bktit_dt=bktit_dt,
                    perunt=perunt,
                    qunt=qunt,
                    amount=amount,
                )
                total += float(amount)     
                invo_inf.tot = total 
                invo_inf.save()  
            return redirect("sale_list.html")
        else: 
            messages.error(request, "CHECK BOOK AVALIBILITY")
    return render(request,'sales/sale_nw.html',locals())


def sale_list(request):
    inv_id= sales.objects.all()
    return render(request, "sales/sale_list.html",locals())
def vw_bill(request,invcno):
    inv_dt= get_object_or_404(sales, invcno=invcno)
    memdt= inv_dt.mem_dt
    memdt_obj = member.objects.get(member_id = memdt)
    saled = saledt.objects.filter(invoice = inv_dt)
    context = {
            'a': inv_dt,
            'b': memdt_obj,
            'c': saled,
    }

    return render(request, "sales/vw_bill.html", context)

def pur_lst(request):
    pur=purchase.objects.all()
    return render(request, 'purchase/pur_lst.html', locals())
def pur_dt(request, purch_id):
    pur_dt= get_object_or_404(purchase, purch_id=purch_id)
    sto_dt=stock.objects.filter(purc_id=pur_dt)
    final=0
    for i in sto_dt:
        rate= i.rate
        qua = i.qun
        fin=qua * rate
        final=final+fin
    context={
        'a': pur_dt,
        'b' : sto_dt,
        'c' : final,
    }
    return render(request, 'purchase/pur_dt.html', context)

## API Update
class supplier_edt(APIView):
    def get(self, request, supp_id):
        try:
            supplier_obj = supplier.objects.get(supp_id=supp_id)
            serializer = supplier1(supplier_obj)
            return Response(serializer.data)
        except supplier.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

    def put(self, request, supp_id):
        try:
            supplier_obj = supplier.objects.get(supp_id=supp_id)
        except supplier.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        serializer = supplier1(supplier_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


def edit_supplier(request, supp_id):
    sup_obj= get_object_or_404(supplier, supp_id=supp_id)
    sup_form =supp_edt(request.POST or None, instance=sup_obj)
    if sup_form.is_valid():
        sup_form.save()
        return redirect("sup_dt.html", supp_id= sup_obj.supp_id)
    context= {
        'a':sup_form,
        'b': sup_obj
    }
    return render(request, "supplier/edit_supplier.html",context)

def sup_det(request, supp_id):
    sup_obj= get_object_or_404(supplier, supp_id=supp_id)
    pur_inf = purchase.objects.filter(supp_id= sup_obj)
    sto_inf = stock.objects.filter(suppl_id= sup_obj)
    iss_inf = issue.objects.filter(book_id__in=sto_inf)
    if request.method == "POST":
        sup_obj.delete()
        return redirect('sup_list.html')
    con={
        'a': sup_obj,
        'b': pur_inf,
        'c': sto_inf,
        'd': iss_inf,

    }
    return render(request, "supplier/sup_det.html",con)

def mem_edt(request, member_id):
    mem_obj = get_object_or_404(member, member_id=member_id)
    mem_form = memedt(request.POST or None, instance=mem_obj)
    if mem_form.is_valid():
        mem_form.save()
        return redirect("memdt.html", mem_id= mem_obj.member_id)
    con={
        'a': mem_form,
        'b': mem_obj
    }

    return render(request,"member/mem_edt.html", con)

def memdel(request, member_id):
    mem_obj = get_object_or_404(member, member_id=member_id)
    issu_obj =issue.objects.filter(mem_id= mem_obj)
    if request.method== "POST":
        mem_obj.delete()
        return redirect('mem_list.html')
    con={
        'a':mem_obj,
        'b':issu_obj,
    }
    return render(request, "member/memdel.html", con)

def sto_edt(request, acceno):
    sto_obj = get_object_or_404(stock, acceno=acceno)
    stock_form = stocedt(request.POST or None, instance=sto_obj)
    if stock_form.is_valid():
        stock_form.save()
        messages.success(request, "STOCK Data Saved Successfully")
        return redirect("bookdt.html", acceno=sto_obj.acceno) 
    context = {
        'a': sto_obj,
        'b': stock_form,                

    }
    return render(request, "stock/sto_edt.html", context)

def sto_del(request,acceno): 
    sto_obj = get_object_or_404(stock, acceno=acceno)   
    if request.method == "POST": 
        sto_obj.delete() 
        messages.warning(request, f"STOCK {{sto_obj.booktitle}} Have been Deleted.")
        return redirect("sto_book.html") 
    return render(request, "stock/sto_del.html", {'a': sto_obj})

def iss_edt(request, issu_id): 
    iss_obj = get_object_or_404(issue, issu_id = issu_id)
    is_form= issuedt(request.POST or None, instance=iss_obj)
    if is_form.is_valid(): 
        is_form.save()  
        return redirect("issu_dt.html", issu_id = iss_obj.issu_id)

    con={
        "a":is_form,
        "b" : iss_obj,
    }    
    return render(request, "issue/iss_edt.html", con)

def iss_del(request, issu_id): 
    iss_obj = get_object_or_404(issue, issu_id = issu_id) 
    stoc_obj = iss_obj.book_id
    iss_ret =iss_obj.actual_date 
    if request.method == "POST": 
        if iss_ret: 
            stoc_obj.qun= stoc_obj.qun 
        else:
            stoc_obj.qun= stoc_obj.qun+1 
            stoc_obj.save()
        iss_obj.delete()
        return redirect("issu_lt.html") 
    con={
        'a' : iss_obj
    }
    return render(request, "issue/iss_del.html", con)

def sale_edt(request, invcno): 
    sales_obj = get_object_or_404(sales, invcno = invcno) 
    saledt_obj = saledt.objects.filter(invoice = sales_obj).order_by("id")
    stck_dt =stock.objects.all()
    mem_dt = member.objects.all()

    if request.method == "POST": 
        memdt = request.POST.get("mem_dt")
        sales_obj.mem_dt =  member.objects.get(member_id= memdt)
        date_str = request.POST.get("dat") 
        sales_obj.dat =datetime.strptime(date_str, "%B %d, %Y").date()
        sales_obj.tot= request.POST.get("tot_see")
        sales_obj.save()

        bkisbn_dtlt = request.POST.getlist("bkisbn_dt[]")
        bktit_dtlt = request.POST.getlist("bktit_dt[]")
        peruntlt = request.POST.getlist("perunt[]")
        quntlt = request.POST.getlist("qunt[]")
        amountlt = request.POST.getlist("amount[]")

        for i, (bkisbn_dt, bktit_dt, per, qty, amt) in  enumerate(zip(bkisbn_dtlt, bktit_dtlt, peruntlt, quntlt, amountlt)): 
            obj = saledt_obj[i] 
            obj.bktit_dt = bktit_dt
            obj.perunt = float(per)
            print(obj.perunt) 
            obj.qunt = int(qty)
            print(obj.qunt)
            obj.amount = float(amt)
            obj.save()
            try: 
                obj.bkisbn_dt= stock.objects.get(isbn = bkisbn_dt)  
                obj.save() 
            except stock.DoesNotExist: 
                continue    
            
        return redirect("sale_list.html") 

    con={
        'a': sales_obj, 
        'b': saledt_obj,
        'stck_dt' : stck_dt,
        'mem_dt' : mem_dt
    }
    return render(request, "sales/sale_edt.html", con)

def sale_del(request, invcno):  
    sales_obj = get_object_or_404(sales, invcno= invcno) 
    saledt_obj = saledt.objects.filter(invoice = sales_obj) 

    if request.method == "POST": 
        sales_obj.delete() 
        return redirect("sale_list.html") 
    
    return render(request, "sales/sale_del.html", locals())