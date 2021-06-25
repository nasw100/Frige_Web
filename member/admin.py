from django.contrib import admin
from member.models import Member
from django.contrib.auth.models import User

class MemberAdmin( admin.ModelAdmin ) :
    list_display = (
        "user_id",
        "password",
        "user_name",
        "birth",
        "gender",
        "email",
        "hp",
        "postal_code",        
        "address",
        "detailAddress",
        "extraAddress",
        "preference",
        "level",
        "date_joined"        
        )    
admin.site.register( Member, MemberAdmin )

# class UserAdmin( admin.ModelAdmin ) :
#     list_display = [ 'username', 'is_active']
#     list_filter = [ 'username', ]
#     list_editable = ['username', 'is_active']
# admin.site.register( User, UserAdmin)