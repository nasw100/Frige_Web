'''Created on 2021. 6. 1.@author: 30403'''
from product.models import Product
from django import forms
#클라이언트 화면에 입력 폼을 만들어주고 
#클라이언트가 입력한(validation/ escape) 데이터에 대한 전처리

class AddProductForm(forms.Form):
    quantity = forms.IntegerField(label="", min_value=1, widget=forms.TextInput ) #장바구니의 수량
    is_update = forms.BooleanField(required=False, initial=False, widget= forms.HiddenInput ) 
    #required=False로 해둬어야 값이 없다라고 여기는 경우가 있어서 #(위widget= #클라이언트에게 노출될떄 어떤 html형태로 보여줄것인지)










