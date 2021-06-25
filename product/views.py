# from django.db.models.query import QuerySet
from member.models import Member
from order.models import OrderItem, Review, ReviewReply
from django.views.decorators.csrf import csrf_exempt
from MealkitEx.settings import PAGE_BLOCK, PAGE_SIZE
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Sum

# Create your views here.
from .models import *
#basket에서 추가됨
from basket.forms import AddProductForm 
from basket.basket import Basket


def home(request) :
    memid = request.session.get( "memid" )
    basket = Basket( request)
    for product in basket:
        product['quantity_form'] = AddProductForm(initial={'quantity':product['quantity'], 'is_update':True})
    products = Product.objects.filter( available_display=True )        # 가능한 상품만 불러오기
    if memid :
        recommendations = Recommendation.objects.filter( user_id = memid )
        recommendedProductId = []
        for recommendation in recommendations :
            recommendedProductId.append(recommendation.product_id )
        if len( recommendedProductId ) == 0 :
            member = Member.objects.get( user_id = memid )
            recommendedProducts = Product.objects.filter( spicy = member.preference )
        else :
            recommendedProducts = Product.objects.filter( id__in=recommendedProductId )
        return render( request, 'shop/list.html', 
        {
            'products':products,
            "memid":memid,            
            "basket":basket,
            "recommendedProducts":recommendedProducts,
        } )
    return render( request, 'shop/list.html', 
    {
        'products':products,
        "memid":memid,            
        "basket":basket,
    } )

@csrf_exempt
def product_in_category(request, category_slug=None) :
    current_category = None             # category가 없다 >> 전체 제품 보여주기
    categories = Category.objects.all()
    memid = request.session.get( "memid" )
    basket = Basket( request)
    for product in basket:
        product['quantity_form'] = AddProductForm(initial={'quantity':product['quantity'], 'is_update':True})
    products = Product.objects.filter( available_display=True )        # 가능한 상품만 불러오기
    if category_slug :
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)           # 실제로 전달하기 전까지는 실행되지 않음
    # 페이징
    products_all = products
    count = products.count()
    
    pagenum = request.GET.get("pagenum")
    if not pagenum :
        pagenum = "1"
    pagenum = int( pagenum )    
        
    start = ( pagenum -1 ) * int(PAGE_SIZE)    # ( 3 - 1 ) * 10     20
    end = start + int( PAGE_SIZE )                  # 20 + 10            30
    if end > count : 
        end = count    
    products = products[start:end]
    number = count - ( pagenum - 1 ) * int(PAGE_SIZE)
    
    startpage = pagenum // PAGE_BLOCK * PAGE_BLOCK + 1
                # 9 // 10 * 10 + 1     1
                # 19 // 10 * 10 + 1    11
    if pagenum % PAGE_BLOCK == 0 :
        startpage -= PAGE_BLOCK            
                
    endpage = startpage + PAGE_BLOCK - 1
                # 1 + 10 - 1           10                
    pagecount = ( count // PAGE_SIZE ) 
    if count % PAGE_SIZE > 0 :
        pagecount += 1  
    if endpage > pagecount :
        endpage = pagecount    
    
    pages = range( startpage, endpage+1 ) 

    if current_category == None :
        if memid :
            recommendations = Recommendation.objects.filter( user_id = memid )
            recommendedProductId = []
            for recommendation in recommendations :
                recommendedProductId.append(recommendation.product_id )
            recommendedProducts = Product.objects.filter( id__in=recommendedProductId )
            return render( request, 'shop/shop.html', 
            {
                'current_category':current_category,
                'categories':categories,
                'products':products,
                "memid":memid,            
                "basket":basket,
                "recommendedProducts":recommendedProducts,
                "count":count,
                "number":number,
                "pages":pages,
                "pagenum" : pagenum,
                "number" : number,
                "pages" : pages,
                "startpage" : startpage,
                "endpage" : endpage,
                "pageblock" : PAGE_BLOCK,
                "pagecount" : pagecount,
                "products_all" : products_all,
            } )
    return render( request, 'shop/shop.html', 
        {
            'current_category':current_category,
            'categories':categories,
            'products':products,
            "memid":memid,            
            "basket":basket,
            "count":count,
            "number":number,
            "pages":pages,
            "pagenum" : pagenum,
            "number" : number,
            "pages" : pages,
            "startpage" : startpage,
            "endpage" : endpage,
            "pageblock" : PAGE_BLOCK,
            "pagecount" : pagecount,
            "products_all" : products_all,
        } )

def product_detail(request, id, product_slug=None) :
    product = get_object_or_404(Product, id=id, slug=product_slug)
    memid = request.session.get( "memid" )

    #Basket추가
    add_to_basket = AddProductForm( initial={'quantity':1})
    basket = Basket( request)

    # Review
    orderitems = OrderItem.objects.filter(product = product.id )
    review_list = []
    sum_list = []
    for orderitem in orderitems :
        if Review.objects.filter( orderitem_id = orderitem.id ).exists() :
            review_list.append( Review.objects.filter( orderitem_id = orderitem.id ) )
            sum = Review.objects.filter(orderitem_id = orderitem.id).aggregate(Sum('ratings'))
            sum_list.append( sum )
    sum_val = 0
    for dic in sum_list :
        sum_val += dic['ratings__sum']
    try :
        ratings_avg_int = range(sum_val // len( sum_list ))
        ratings_avg_mod = [sum_val / len( sum_list ) - sum_val // len( sum_list )]
    except :
        ratings_avg_int = [0]
        ratings_avg_mod = [float(0)]
    
    review_list = sorted( review_list, key=lambda x:x[0].created, reverse=True )
    reply_list = []
    for reviews in review_list :
        for review in reviews :
            if ReviewReply.objects.filter( review = review.id ).exists() :
                reply_list.append(ReviewReply.objects.filter( review = review.id ))

    count = len( review_list )
    
    pagenum = request.GET.get("pagenum")
    if not pagenum :
        pagenum = "1"
    pagenum = int( pagenum )    
        
    start = ( pagenum -1 ) * int(PAGE_SIZE)    # ( 3 - 1 ) * 10     20
    end = start + int( PAGE_SIZE )                  # 20 + 10            30
    if end > count : 
        end = count    
    review_list_on_pages = review_list[start:end]
    number = count - ( pagenum - 1 ) * int(PAGE_SIZE)
    
    startpage = pagenum // PAGE_BLOCK * PAGE_BLOCK + 1
                # 9 // 10 * 10 + 1     1
                # 19 // 10 * 10 + 1    11
    if pagenum % PAGE_BLOCK == 0 :
        startpage -= PAGE_BLOCK            
                
    endpage = startpage + PAGE_BLOCK - 1
                # 1 + 10 - 1           10                
    pagecount = ( count // PAGE_SIZE ) 
    if count % PAGE_SIZE > 0 :
        pagecount += 1  
    if endpage > pagecount :
        endpage = pagecount    
    
    pages = range( startpage, endpage+1 )

    for pro in basket:
        pro['quantity_form'] = AddProductForm(initial={'quantity':pro['quantity'], 'is_update':True})
    return render(request, 'shop/detail.html', 
        {
        'product':product,
        'add_to_basket': add_to_basket,
        "memid":memid,
        "basket":basket,
        "orderitems":orderitems,
        "review_list":review_list,
        "review_list_on_pages":review_list_on_pages,
        "reply_list":reply_list,
        "number":number,
        "pages":pages,
        "pagenum" : pagenum,
        "number" : number,
        "pages" : pages,
        "startpage" : startpage,
        "endpage" : endpage,
        "pageblock" : PAGE_BLOCK,
        "pagecount" : pagecount,
        "ratings_avg_int" : ratings_avg_int,
        "ratings_avg_mod" : ratings_avg_mod,
        } )

def reply_write( request ) :
    memid = request.session.get('memid')
    geturl = request.POST.get('get_url')
    if memid :
        review = request.POST.get('reply_review')
        if request.method=="POST":
            reply_write = ReviewReply(
                review = Review.objects.get( id = review ),
                replier = Member.objects.get(user_id=memid),
                reply = request.POST.get('reply_write'),
            )
            reply_write.save()
            return redirect(str(geturl))
        else :
            return redirect(str(geturl))
    else :
        return redirect(str(geturl))