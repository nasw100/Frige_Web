from product.models import Product
from django.db import models
# from django.core.validators import MinValueValidator, MaxValueValidator

from member.models import Member
# import hashlib
from django.db.models.signals import post_save



# order_id       주문번호 PK
# user_id        사용자 로그인 ID FK
# order_name     주문자
# product_id     상품번호 FK
# product_name   상품명
# email          이메일
# quantity       수량
# order_address  배송주소
# postal_code    우편번호 ~
# created      
# updated
# paid

class Order( models.Model ) :   
    member = models.CharField( max_length=20, verbose_name="유저아이디" )
    order_name = models.CharField( max_length=20, verbose_name="주문자명" )
    order_email = models.EmailField(max_length=100, verbose_name="이메일주소")
    order_postal_code = models.CharField( max_length=10, verbose_name="우편번호")
    order_address = models.CharField( max_length=100, verbose_name="주소")
    order_detailAddress = models.CharField( max_length=100, verbose_name="상세주소")
    order_extraAddress = models.CharField( max_length=100, verbose_name="참고주소")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    
    class Meta:
        ordering = ['-created']
        db_table = "order_order"
        verbose_name = "order"
        verbose_name_plural = "order"
    
    def __str__(self):
        return f'Order{self.id}'
        
    def get_total_product(self):
        return sum(item.get_item_price() for item in self.items.all())
        
    def get_total_price(self):
        total_product = self.get_total_product()
        return total_product
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items' )
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_product")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return '{}'.format(self.id)

    
    def get_item_price(self):
        return self.price * self.quantity
    

class OrderTransaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)    
    amount = models.PositiveIntegerField(default=0)
    # type = models.CharField(max_length=120, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    def __str__(self):
        return str(self.order.id)

    class Meta:
        ordering = ['-created']

class Review( models.Model ) :
    orderitem_id = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True, related_name='orderitem')
    writer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='writer' )
    content = models.TextField(blank=True)
    ratings = models.PositiveIntegerField()

    created = models.DateTimeField(auto_now_add=True)

    class Meta :
        ordering = ['-created']
        index_together = [['id']]
    
    def __str__(self) :
        return str(self.id)

class ReviewReply( models.Model ) :
    review = models.ForeignKey( Review, on_delete=models.CASCADE, null=True, related_name="reviews")
    replier = models.ForeignKey( Member, on_delete=models.SET_NULL, null=True, related_name='replier')
    reply = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta :
        ordering = ['created']
        index_together = [['id']]
    
    def __str__(self) :
        return str(self.id)


