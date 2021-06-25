from django.db import models

# Create your models here.

class Basket( models.Model ):
    basket_id = models.CharField( max_length=20, verbose_name = "장바구니번호", null=False, unique = True )
    user_id = models.CharField( max_length=20, verbose_name = "아이디", null=False, unique = True )
    product_id = models.CharField( max_length=20, verbose_name = "제품번호", null=False, unique = True )
    product_name = models.CharField(max_length=100, verbose_name="제품이름", null=False )
    quantity = models.CharField(max_length=100, verbose_name="개수", null=False )
    
    
    
    