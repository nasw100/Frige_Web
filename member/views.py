from basket.basket import Basket
from product.models import Product
from order.models import Order, OrderItem, Review
from django.template import loader
from django.http.response import HttpResponse, JsonResponse




from member.models import Member
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateformat import DateFormat
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import auth

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from .token import account_activation_token
from django.utils.encoding import force_bytes, force_text

import logging
logger = logging.getLogger(__name__)

@csrf_exempt
def register( request ) :
    memid = request.session.get('memid')
    if memid :
        return redirect ("/")
    else :
        if request.method == "POST" :   
            dto = Member(
                user_id = request.POST["user_id"],
                password = request.POST["password1"],
                email = request.POST["email"],
                hp = request.POST["hp"],
                birth = request.POST["birth"],
                postal_code = request.POST["sample6_postcode"],
                address = request.POST.get("sample6_address"),
                detailAddress = request.POST.get("sample6_detailAddress"),
                extraAddress = request.POST.get("sample6_extraAddress"),
                gender = request.POST["gender"],
                preference = request.POST["preference"],
                user_name = request.POST["user_name"],
                level = 0,
                date_joined = DateFormat(datetime.now()).format('Y-m-d')
            )
            user = User.objects.create_user(
                username = request.POST["user_id"],
                password = request.POST["password1"],
                email = request.POST["email"]
            )
            user.is_active = False
            user.save()
            dto.save()
            current_site = get_current_site(request) 
            # localhost:8000
            message = render_to_string('user_active_mail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = "[SOT] 회원가입 인증 메일입니다."
            user_email = user.email
            email = EmailMessage(mail_subject, message, to=[user_email])
            email.send()
            return HttpResponse(
                '<div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center; '
                'justify-content: center; align-items: center;">'
                '입력하신 이메일<span>로 인증 링크가 전송되었습니다.</span>5초 후 자동으로 홈으로 돌아갑니다.'
                '<meta http-equiv="refresh" content="5; url=http://192.168.10.9:8000/">'
                '</div>'
            )
            #return redirect( "login" )
        else :
            template = loader.get_template( "register.html" )
            context = {}
            return HttpResponse( template.render( context, request ) )

def activate(request, uid64, token):
    
    uid = force_text(urlsafe_base64_decode(uid64))
    user = User.objects.get(pk=uid)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect("login")
    else:
        return HttpResponse('비정상적인 접근입니다.')

def checkid(request):
    user_id = request.GET["user_id"]
    try:
        user = Member.objects.get(user_id=user_id)
    except Exception as e:
        user = None
    result = {
        'result':'success',
        # 'data' : model_to_dict(user)  # console에서 확인
        'data' : "not exist" if user is None else "exist"
    }    
    return JsonResponse(result)

def checkemail(request):
    email = request.GET["email"]
    try:
        user=Member.objects.get(email=email)
    except Exception as e:
        user = None
    result = {
        'result':'success',
        # 'data' : model_to_dict(user)  # console에서 확인
        'data' : "not exist" if user is None else "exist"
    }
    return JsonResponse(result)      

from django.core.exceptions import ObjectDoesNotExist

def login( request ) :
    if request.method == "POST" : 
        user_id = request.POST["user_id"]
        password = request.POST["password"]      
        template = loader.get_template( "login.html" )   
        next = request.POST["next"] 
        try :
            dto = Member.objects.get( user_id=user_id )
            # 아이디가 있는 경우     
            if password == dto.password :
                # 비밀번호가 같다 - 로그인 처리
                user = auth.authenticate(request, username=user_id, password=password)
                # 성공
                if user is not None:
                    auth.login(request, user)
                    request.session["memid"] = user_id  # 쿠키     
                    if next == "" :
                        return redirect( '../') 
                    else :
                        return redirect( next )
                # 실패
                else:        
                    # 이메일인증 무효
                    user = User.objects.get(username = user_id)
                    user.is_active = True
                    user.save()            
                    auth.login(request, user)
                    request.session["memid"] = user_id
                    return redirect( '/' )
                    # 이메일인증
                    # return HttpResponse(
                    #     # '<div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center; '
                    #     # 'justify-content: center; align-items: center;">'
                    #     # '이메일 인증<span>을 완료한 후 다시 로그인해주세요. </span>5초 후 자동으로 홈으로 돌아갑니다.'
                    #     # '<meta http-equiv="refresh" content="5; url=http://localhost:8000/">'
                    #     # '</div>'
                    # )              
            else :  
                message = "입력한 비밀번호가 다릅니다"  
                context = {
                "message1": message
                }       
        except ObjectDoesNotExist :
            # 아이디가 없는 경우
            message = "등록된 아이디가 없습니다"
            context = {
                "message2": message
            }
        return HttpResponse( template.render( context, request ) )
    else :
        template = loader.get_template( "login.html" )
        try :
            next = request.GET['next']
            context = {"next":next}
        except : 
            context = {}
        return HttpResponse( template.render( context, request ) )
 
def profile( request ) :
    template = loader.get_template( "profile.html" )
    memid = request.session.get( "memid" )
    context = {
        "memid":memid,
        }
    return HttpResponse( template.render( context, request ) )
    
def logout( request ) :
    del( request.session["memid"] )
    basket = Basket(request)
    basket.clear()
    return redirect( "/" )

def delete( request ) :
    if request.method == "POST" : 
        user_id = request.session.get( "memid" )
        password = request.POST["password"]
        dto = Member.objects.get( user_id=user_id )
        user = User.objects.get(username=user_id)
        if password == dto.password :
            user.delete()
            dto.delete()  # delete 호출
            del( request.session["memid"] )
            return redirect( "/" )
        else :
            template = loader.get_template( "delete.html" )
            context = { 
               "message" : "비밀번호가 다릅니다",
               "memid" : user_id
               }
            return HttpResponse( template.render( context, request ) ) 
    else :
        memid = request.session.get( "memid" )        
        template = loader.get_template( "delete.html" )
        context = {
            "memid" : memid
        }
        return HttpResponse( template.render( context, request ) )

def modify( request ) :
    if request.method == "POST" : 
        user_id = request.session.get( "memid" )
        password = request.POST["password"]
        dto = Member.objects.get( user_id=user_id )    
        if password == dto.password :
            template = loader.get_template( "modifyview.html" )
            context = {
                "dto":dto,
                "memid" : user_id
                }        
        else :
            template = loader.get_template( "modify.html" )
            context = { 
               "message" : "비밀번호가 다릅니다",
               "memid" : user_id
               }
        return HttpResponse( template.render( context, request ) ) 
    else :
        memid = request.session.get( "memid" )
        template = loader.get_template( "modify.html" )
        context = {
            "memid" : memid
        }
        return HttpResponse( template.render( context, request ) )

def modifypro( request ) :
    user_id = request.session.get( "memid" )
    dto = Member.objects.get( user_id = user_id )
    dto.password = request.POST["password1"]
    dto.user_name = request.POST["user_name"]  
    dto.email = request.POST["email"]
    dto.hp = request.POST["hp"]
    dto.postal_code = request.POST["sample6_postcode"]
    dto.address = request.POST["sample6_address"]
    dto.detailAddress = request.POST["sample6_detailAddress"]
    dto.extraAddress = request.POST["sample6_extraAddress"]
    dto.save()    
    return redirect( "profile" )
      
def order_detail(request) :
    user_id = request.session.get( "memid" )
    orders = Order.objects.filter( member = user_id )
    orderitem_list = []
    for order in orders :
        orderitem_list.append( OrderItem.objects.filter( order = order.id ) )
    template = loader.get_template( "detail.html" )
    context = {
        "orders":orders,
        "memid":user_id,
        "orderitem_list":orderitem_list,
        }
    return HttpResponse( template.render( context, request ) )

def orderitem(request) :
    memid = request.session.get( 'memid' )
    if request.method == "POST" :
        order_in = request.POST.get('order')
        order = Order.objects.get( id = int(order_in[5:]) )
        orderitems = OrderItem.objects.filter( order = order)
        template = loader.get_template( "orderitem.html" )
        reviewed = []
        for orderitem in orderitems :
            try :
                reviewed.append( (orderitem, Review.objects.get(orderitem_id = orderitem)) ) 
            except :
                reviewed.append( (orderitem, -1))
        context = {
            "orderitems":orderitems,
            "memid":memid,
            "order":order,
            "reviewed":reviewed,
        }
        return HttpResponse( template.render( context, request ))
    else :
        return redirect( './orderdetail' )

def review_write(request) :
    memid = request.session.get('memid')
    if request.method == "POST" :
        template = loader.get_template( "write.html" )
        orderitem = request.POST.get("orderitem")
        orderitem = OrderItem.objects.get(id = orderitem)
        order = request.POST.get("order")
        context = {
            "memid":memid,
            "order":order,
            "orderitem":orderitem,
        }
    return HttpResponse( template.render( context, request ))

def review_write_pro(request) :
    if request.method == "POST" :
        orderitem = request.POST.get('orderitem')
        orderitem = OrderItem.objects.get(id = orderitem)
        memid = request.session.get('memid')
        ratings = request.POST.getlist('ratings')
        ratings = max(ratings)
        product = Product.objects.get(id = orderitem.product_id)
        review = Review(
            orderitem_id = orderitem,
            writer = Member.objects.get(user_id = memid),
            ratings = ratings,
            content = request.POST.get('content'),
            )
        review.save()

        logger.info(";Review;(userid_category_productid_orderitemid_ratings);" + str(memid) + ";" + str(product.category) + ";" + str(orderitem.product_id) + ";" + str(orderitem.id) + ";" + str(ratings) )
    return redirect("./orderitem")

def review_modify(request) :
    memid = request.session.get('memid')
    if request.method == "POST" :
        template = loader.get_template( "review_modify.html" )
        orderitem = request.POST.get("orderitem")
        review = Review.objects.get(orderitem_id = orderitem)
        orderitem = OrderItem.objects.get(id = orderitem)
        order = request.POST.get("order")
        context = {
            "memid":memid,
            "order":order,
            "orderitem":orderitem,
            "review":review
        }
    return HttpResponse( template.render( context, request ))

def review_modify_pro(request) :
    if request.method == "POST" :
        orderitem = request.POST.get('orderitem')
        orderitem = OrderItem.objects.get(id = orderitem)
        review = request.POST['review']
        rev = Review.objects.get( id = review )
        rev.content = request.POST['content']
        rev.save()
    return redirect("./orderitem")
