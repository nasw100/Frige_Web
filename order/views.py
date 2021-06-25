import logging
# from datetime import datetime
from django.shortcuts import render, get_object_or_404 #redirect,
# from django.template import loader
# from django.utils.dateformat import DateFormat
# from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *
from basket.basket import Basket
from django.views.generic.base import View
from django.http import JsonResponse
from member.models import Member
from product.models import Product

logger = logging.getLogger(__name__)


def order_create(request):
    basket = Basket(request)
    memid = request.session.get( "memid" )
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        order_name = request.POST.get("order_name")
        order_email = request.POST.get("order_email")
        order_postal_code = request.POST.get("postcode")
        order_address = request.POST.get("address")
        order_detail_address = request.POST.get("sample6_detailAddress")
        order_extra_address = request.POST.get("sample6_extraAddress")
        if form.is_valid():
            order = form.save(commit=True)
            c = ""
            # 주문내역 저장
            for item in basket :
                product = item['product']
                quantity = item['quantity']
                c = c + str(product) + "*" + str(quantity) + ";"
                # 재고 관리
                product_name = str(item['product'])
                purchased = Product.objects.get( name = product_name )

                past_orders = Order.objects.filter(member = memid)
                spicy_list = []
                for past_order in past_orders :
                    orderitems = OrderItem.objects.filter(order_id = past_order)
                    for orderitem in orderitems :
                        pro = Product.objects.get(id = orderitem.product_id)
                        for i in range( int(orderitem.quantity) ) :
                            spicy_list.append( pro.spicy )
                if len(spicy_list) >= 5 :
                    preference_update = round( sum(spicy_list) / len(spicy_list) )
                    member = Member.objects.get( user_id = memid )
                    member.preference = preference_update
                    member.save()
                try :
                    purchased.stock = int(purchased.stock) - int(item['quantity'] )
                    purchased.save()

                except :
                    message = "message"
                    return render(request, 'order/create.html', 
                    {'basket': basket, 
                    'form': form, 
                    'memid':memid, 
                    'order_name':order_name, 
                    'order_email':order_email, 
                    'order_postal_code':order_postal_code,
                    'order_address':order_address,
                    'order_detail_address':order_detail_address,
                    'order_extra_address':order_extra_address,
                    'message':message,})
            order.member = memid
            order.order_name = str(order_name)
            order.order_email = order_email
            order.order_postal_code = str(order_postal_code)
            order.order_address = str(order_address)
            order.order_detailAddress = str(order_detail_address)
            order.order_extraAddress = str(order_extra_address)
            order.save()
            for item in basket:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity']
                                         )
                # 로그
                logger.info(";checkout;(orderid_userid_productid_quantity_totalPrice);" + str(order.id) + ";" + str(memid) + ";" + str(purchased.id) + ";" + str(item['quantity']) + ";" + str(item['price']  * item['quantity']) )

            basket.clear()
            return render(request, 'order/complete.html', {'order': order, 'memid':memid})
    else:
        form = OrderCreateForm()
        member = Member.objects.get( user_id = memid)
        order_name = member.user_name
        order_email = member.email
        order_postal_code = member.postal_code
        order_address = member.address
        order_detail_address = member.detailAddress
        order_extra_address = member.extraAddress
        # for pro in basket :
        #     logger.info("basket_to_order:" + str(memid) + ":" + str(pro['product'].id) + ":" + str(pro['product'].name) + ":" + str(pro['quantity']) )
        return render(request, 'order/create.html', 
        {'basket': basket, 
        'form': form, 
        'memid':memid, 
        'order_name':order_name, 
        'order_email':order_email,
        'order_postal_code':order_postal_code,
        'order_address':order_address,
        'order_detail_address':order_detail_address,
        'order_extra_address':order_extra_address,
        })


def order_complete(request):
    order_id = request.GET.get('order_id')
    memid = request.session.get( "memid" )
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'order/complete.html', {'order': order, 'memid':memid})

class OrderCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        memid = request.session.get( "memid" )
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated": False}, status=403)

        basket = Basket(request)
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            for item in basket:
                OrderItem.objects.create(order=order,
                                         product=item['product_id'],
                                         price=item['price'],
                                         quantity=item['quantity']
                                         )
            basket.clear()
            data = {
                "order_id": order.id,
                "memid":memid
            }
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)


class OrderCheckoutAjaxView(View):
    def post(self, request, *args, **kwargs):
        memid = request.session.get( "memid" )
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated": False}, status=403)

        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        amount = request.POST.get('amount')
              

class OrderAjaxView(View):
    def post(self, request, *args, **kwargs):
        memid = request.session.get( "memid" )
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated": False}, status=403)

        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        amount = request.POST.get('amount')
        order

        try:
            trans = OrderTransaction.objects.get(
                order=order,            
                amount=amount
            )
        except:
            trans = None

        if trans is None:
            trans.save()
            order.save()
            data = {
                "works": True,
                "memid":memid
            }

            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)
