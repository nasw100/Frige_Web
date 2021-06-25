#session을 이용한 장바구니 사용 
from decimal import Decimal
from django.conf import settings
from product.models import Product

class Basket(object ):
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_ID)
        if not basket:
            basket = self.session[settings.BASKET_ID] = {}
        self.basket = basket    
        
    def __len__(self): #장바구니에 담겨있는 수량 
        return sum(item['quantity'] for item in self.basket.values())
    
    def __iter__(self):
        product_ids = self.basket.keys()
        
        products = Product.objects.filter(id__in=product_ids)
        for product in products :
            self.basket[str(product.id)]['product'] = product
            
        for item in self.basket.values():# 장바구니에 있는 것을 하나씩 꺼냄
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            
            yield item 
                       
    def add(self, product, quantity=1, is_update=False):#장바구니에 담을떄는 add
        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {'quantity':0, 'price':str(product.price)}
        if is_update: #장바구니에 제품이 있는경우
            self.basket[product_id]['quantity'] = quantity
        else :
            self.basket[product_id]['quantity'] += quantity
            
        self.save() #update된 정보를 저장하기 

    def save(self):  
        self.session[settings.BASKET_ID] = self.basket
        self.session.modified = True #변동사항이 있을때 변경한것을 저장     
        
    def remove(self, product):
        product_id = str(product.id )
        if product_id in self.basket:     
            del(self.basket[product_id])
            self.save()   
            
    def clear(self):     #장바구니 비우기 
        self.session[settings.BASKET_ID] = {}
        self.session.modified = True
    
    def get_product_total(self): #장바구니에 들어있는 총수량과 가격의 합 
        return sum(Decimal(item['price'])*item['quantity']for item in self.basket.values())  
            

            
            
            
            
            
