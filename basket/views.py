#장바구니에 담기 버튼을 눌렀을 때 동작할 뷰
#session으로 작용하게 할 예정 
#장바구니담기 -> back에서 일어날것들 ->button을 눌렀을때 
#이경우는 함수형 view로 만들고 있음

import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST # g함수형 view에 전처리를 담당 / post로 만 접근할수 있도록
# from django.template import loader
# from django.http.response import HttpResponse


from .forms import AddProductForm
from .basket import Basket
from product.models import Product 


logger = logging.getLogger(__name__)


#담기 기능
@require_POST #annotation: 먼저 실행하게 해둠
def add(request, product_id):
    memid = request.session.get( "memid" )
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id) #Api경우는 메세지를 띄우지는 않음 
    #클라이언드 -> 서버로 데이터를 전달 
    #유효성 검사 . injection에 대한 전처리 등등필요한데 
    #대신 처리를 해주는 것이 form => 노출하는 form 유효성검사form 둘다 쓰임 
    form = AddProductForm(request.POST) 
    
    if form.is_valid(): #필수데이터들이 다들어오면 
        cd = form.cleaned_data 
        basket.add( product = product, quantity=cd['quantity'], is_update=cd['is_update']) 
        # try :
        #     logger.info("basket_update:" + str(memid) + ":" + str(product.id) + ":" + str(product.name) + ":" + str(cd['quantity']) )
        # except :
        #     pass
        
    return redirect( 'basket:detail') #상세페이지로 돌아가서 결과를 확인할수 있도록

#
def remove( request, product_id):
    memid = request.session.get( "memid" )
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id)
    # for pro in basket :
    #     if pro['product'].id == product.id :
    #         try :
    #             logger.info("basket_remove:" + str(memid) + ":" + str(product.id) + ":" + str(product.name) + ":" + str(pro['quantity']) )
    #         except :
    #             pass
    basket.remove(product)
    
    return redirect( 'basket:detail')    

def detail(request):
    memid = request.session.get( "memid" )
    basket = Basket( request)
    hold = ""
    for product in basket:
        product['quantity_form'] = AddProductForm(initial={'quantity':product['quantity'], 'is_update':True})
        if product['quantity'] > product['product'].stock :
            hold = product['product'].name
    return render( request, 'basket/detail.html', {'basket':basket, 'memid':memid, 'hold':hold})


#view가 동작을 하려면 url이 필요하므로 url만들러 감 
























