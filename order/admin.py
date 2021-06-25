from django.contrib import admin
from django.http import HttpRequest
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import OrderItem, Order, Review, ReviewReply
import csv
import datetime



# def export_to_csv(modeladmin, request, queryset):
#     opts = modeladmin.model._meta
#     response = HttpRequest(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment;filename={}.csv.format(opts.verbose_name)'
#     writer = csv.writer(response)

#     fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
#     writer.writerow([field.verbose_name for field in fields])

#     for obj in queryset:
#         data_row = []
#         for field in fields:
#             value = getattr(obj, field.name)
#             if isinstance(value, datetime.datetime):
#                 value = value.strftime("%Y-%m-%d")
#             data_row.append(value)
#         writer.writerow(data_row)
#     return response
# export_to_csv.short_description = 'Export to CSV'


class OrderAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'member', 'order_name', 'order_email', 'order_address', 'order_detailAddress', 'order_extraAddress', 'order_postal_code',  'created', 'updated']
    list_filter = [ 'created', 'updated']
    # inlines = [OrderItemInline] # 다른 모델과 연결되어있는 경우 한페이지 표시하고 싶을 때
    # actions = [export_to_csv]


admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'price', 'quantity']

admin.site.register(OrderItem, OrderItemAdmin)

class ReviewAdmin( admin.ModelAdmin) :
    list_display = ['id', 'orderitem_id', 'writer', 'content', 'ratings', 'created']
    list_filter = ['orderitem_id', 'writer', 'created']
    list_editable = ['content', 'ratings']

admin.site.register(Review, ReviewAdmin)

class ReviewReplyAdmin( admin.ModelAdmin ) :
    list_display = ['id', 'review', 'replier', 'reply', 'created']
    list_filter = ['review', 'replier', 'created']
    list_editable = ['reply']

admin.site.register( ReviewReply, ReviewReplyAdmin )