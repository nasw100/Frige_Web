from django.contrib import admin
from .models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin) :
    list_display = ['id', 'category', 'slug']
    prepopulated_fields = {'slug':('category',)}        # tuple, list 가능

admin.site.register(Category, CategoryAdmin)

@admin.register(Product)        # 어노테이션 기법, 아래를 실행하기 전에 이것을 하겠다
class ProductAdmin(admin.ModelAdmin) :
    list_display = ['id', 'name', 'slug', 'category', 'spicy', 'price', 'stock', 'available_display', 'available_order', 'created', 'updated']
    list_filter = ['available_display', 'created', 'updated', 'category']
    prepopulated_fields = {'slug':('name',)}    # slug하고 name 섞어서 쓰겠다
    list_editable = ['price', 'stock', 'available_display', 'available_order']

class RecommendationAdmin(admin.ModelAdmin) :
    list_display = ['id','user_id', 'product_id']
    list_editable = ['user_id', 'product_id']

admin.site.register(Recommendation, RecommendationAdmin)

search_fields = ('category__name',)

# class ReviewAdmin(admin.ModelAdmin) :
#     list_display = ['num', 'writer', 'product_id', 'subject', 'ratings', 'passwd', 'content', 'readcount', 'ref', 'restep', 'relevel', 'regdate', 'ip']