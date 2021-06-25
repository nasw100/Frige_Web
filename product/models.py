from member.models import Member
from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model) :
    category = models.CharField(max_length=200, db_index=True)
    meta_description = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)

    class Meta :
        ordering = ['category']                     # 정렬기준
        verbose_name = 'category'               # 노출될 때 단수형 이름
        verbose_name_plural = 'categories'      # 노출될 때 복수형 이름

    def __str__(self) :
        return self.category

    def get_absolute_url(self):
        return reverse('product:product_in_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=200, db_index=True)
    slug  = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='products/%y/%m/%d', blank=True )
    description = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)
    spicy = models.DecimalField(max_digits=2, decimal_places=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available_display = models.BooleanField('Display', default=True)
    available_order = models.BooleanField('Order', default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta :
        ordering = ['-created', '-updated']
        index_together = [['id', 'slug']]     # 2개를 병합해서 인덱스 기준을 잡음

    def __str__(self) :
        return self.name

    def get_absolute_url(self) :
        return reverse('product:product_detail', args=[self.id, self.slug])


class Recommendation( models.Model ) :
    user_id = models.CharField( max_length=20, verbose_name="아이디" )
    product_id = models.CharField( max_length=30, verbose_name="상품아이디", null=False)
    # user_id = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='userId')
    # product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='productId')

    def get_absolute_url(self) :
        return reverse('product:product_detail', args=[self.id, self.slug])


