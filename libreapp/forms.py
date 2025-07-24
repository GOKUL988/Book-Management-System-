from django import forms
from .models import supplier, member, stock, issue, sales, saledt

class supp_edt(forms.ModelForm):
    class Meta:
        model= supplier
        fields=[
            "sup_name",
            "email",
            "mobile",
            "doorno",
            "street",
            "dist",
            "stat",
            "pin"
            ]

class memedt(forms.ModelForm):
    class Meta:
        model = member
        fields= '__all__'

class stocedt(forms.ModelForm):
    class Meta:
        model= stock
        fields =[
            "booktitle", 
            "authorname", 
            "edition",
            "yearofpub",
            "rate",
            "qun",
            "classfic",
            "rack",
            "ava"
        ]

class issuedt(forms.ModelForm): 
    class Meta: 
        model= issue       
        fields=[
            "book_id", 
            "mem_id", 
            "iss_date", 
            "actual_date",
            "fine", 
            "paymth"

        ] 

class saleedt(forms.ModelForm): 
    class Meta: 
        model= sales 
        fields= [
            "mem_dt", 
            "dat", 
        ]    

class saledtedt(forms.ModelForm): 
    class Meta: 
        model = saledt 
        fields= [
            "bkisbn_dt", 
            "qunt",
            "amount",
        ]