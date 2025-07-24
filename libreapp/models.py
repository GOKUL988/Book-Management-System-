import string
import random
from email.policy import default
from django.db import models
import uuid
from datetime import date
from decimal import Decimal
# Create your models here.
def default_id_gen():
    return str(random.randint(100000, 999999))
class supplier(models.Model):
    supp_id=models.CharField(primary_key=True, max_length=20,editable=False)
    sup_name=models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    mobile = models.CharField(max_length=15)
    doorno = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    dist = models.CharField(max_length=50)
    stat = models.CharField(max_length=50)
    pin = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        if not self.supp_id:
            max_retries=10
            for _ in range(max_retries):
                ran_id = ''.join(random.sample(string.digits, 6))
                if not self.__class__.objects.filter(supp_id=ran_id).exists():
                    self.supp_id = ran_id
                    break
            else:
                raise ValueError("purchase id generated failure")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sup_name}-{self.supp_id}"

class purchase(models.Model):
    purch_id=models.CharField(primary_key=True, editable=False, max_length=20)
    supp_id=models.ForeignKey(supplier,on_delete=models.CASCADE)
    billno=models.CharField(max_length=20)
    date=models.DateField()
    bill=models.FileField()

    def save(self, *args, **kwargs):
        if not self.purch_id:
            max_retries=10
            for _ in range(max_retries):
                ran_id = ''.join(random.sample(string.digits, 6))
                if not self.__class__.objects.filter(purch_id=ran_id).exists():
                    self.purch_id = ran_id
                    break
            else:
                raise ValueError("purchase id generated failure")
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.purch_id}-{self.billno}"

class stock(models.Model):
    suppl_id= models.ForeignKey(supplier, on_delete=models.CASCADE)
    purc_id= models.ForeignKey(purchase, on_delete=models.CASCADE)
    acceno=  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    isbn=models.CharField(unique=True, editable=False, max_length=20)
    booktitle= models.CharField(max_length=100)
    authorname=models.CharField(max_length=50)
    edition=models.CharField(max_length=50)
    yearofpub=models.CharField(max_length=50)
    rate=models.FloatField(max_length=40)
    qun=models.IntegerField(default=0)
    catego_ries = models.CharField(max_length=50, null=True, blank=True)
    classfic=models.CharField(max_length=50,  null=True, blank=True)
    rack=models.CharField(max_length=50)
    ava=models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.isbn:
            max_retries = 10
            for _ in range(max_retries):
                ran_id = ''.join(random.choices(string.digits, k=13))  # ALLOWS REPEATS
                if not self.__class__.objects.filter(isbn=ran_id).exists():
                    self.isbn = ran_id
                    break
            else:
                raise ValueError("ISBN number generation failed")
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.acceno}-{self.booktitle}-{self.isbn}"
class member(models.Model):
    member_id = models.CharField(max_length=15, unique=True, editable=False)
    memname = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=50)
    doorno = models.CharField(max_length=50)
    strnme = models.CharField(max_length=50)
    dist = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=50)
    memtype = models.CharField(max_length=50)
    def save(self, *args, **kwargs):
        if not self.member_id:
            while True:
                random_id = ''.join(random.choices(string.digits, k=6))  # five digit unique number
                if not member.objects.filter(member_id=random_id).exists():  # helps to identity unique
                    self.member_id = random_id
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.member_id}"

class issue(models.Model):
    book_id=models.ForeignKey(stock, on_delete=models.CASCADE)
    mem_id=models.ForeignKey(member, on_delete=models.PROTECT)
    issu_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    iss_date=models.DateField()
    ret_date=models.DateField()
    actual_date = models.DateField(null=True, blank=True)
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    issued=models.CharField(max_length=10 ,editable=False, default="No")
    paymth=models.CharField(max_length=20,blank=True,null=True)
    def calc(self, perdaystu=5, perdaypub=10):
        if self.actual_date and self.actual_date > self.ret_date:
            delay = (self.actual_date - self.ret_date).days
            mem_type = self.mem_id.memtype.lower()
            if mem_type == "public" and "PUBLIC":
                self.fine = delay * perdaypub

            elif mem_type == "student" and "STUDENT":
                self.fine = delay * perdaystu

            else:
                self.fine = 0
        else:
            self.fine = 0

    def save(self, *args, **kwargs):
        # 1. saving a book issued or not
        if self.iss_date and not self.actual_date:
            self.issued = "Yes"
        else:
            self.issued = "No"

        # 2. Calling fine
        if self.actual_date and self.ret_date:
            self.calc()

        # 3. Update qun and ava
        stock_obj = self.book_id

        if self.actual_date:  # Book returned
            stock_obj.qun += 1
            stock_obj.ava = "YES" if stock_obj.qun > 0 else "NO"
            if self.paymth:
                stock_obj.qun=stock_obj.qun -1
            stock_obj.save()

        else:  # Book issued now
            if stock_obj.qun > 0:
                stock_obj.qun -= 1
                stock_obj.ava = "YES" if stock_obj.qun > 0 else "NO"
                stock_obj.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.issu_id}-{self.book_id.booktitle}"   

class sales(models.Model):
    mem_dt=models.ForeignKey(member, on_delete=models.PROTECT)
    invcno = models.IntegerField(unique=True, editable=False)
    dat=models.DateField()
    tot = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.invcno:
            max_retries = 10
            for _ in range(max_retries):
                ran_id = ''.join(random.choices(string.digits, k=6))  # ALLOWS REPEATS
                if not self.__class__.objects.filter(invcno=ran_id).exists():
                    self.invcno = ran_id
                    break
            else:
                raise ValueError("INVOICE NO generation failed")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invcno}"

class saledt(models.Model):
    invoice=models.ForeignKey(sales, on_delete=models.CASCADE)
    bkisbn_dt = models.ForeignKey(stock,on_delete=models.CASCADE)
    bktit_dt = models.CharField(max_length=100)
    perunt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    qunt = models.IntegerField()                               
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self,*args,**kwargs):
        sto_obj = self.bkisbn_dt
        sale_qun = int(self.qunt)
        if sto_obj:
            sto_obj.qun= sto_obj.qun - sale_qun
            if sto_obj.qun == 0:
                sto_obj.ava ="NO"
            else:
                sto_obj.ava = "YES"
            sto_obj.save()

        self.amount= float(self.perunt) * float(self.qunt)

        super().save(*args,**kwargs)

    def __str__(self):
        return  f"{self.invoice.invcno}- {self.bktit_dt}"
    
class catogories(models.Model): 
    cato1 = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.cato1}'
class subcateg(models.Model): 
    cate_it = models.CharField(max_length=50) 
    sub = models.CharField(max_length=50) 
    def __str__(self):
        return f'{self.sub}- {self.cate_it}' 
class racks(models.Model): 
    rack_sh = models.CharField(max_length=50) 
    def __str__(self):
        return f'{self.rack_sh}'

