from django.db import models
from member.choice import  LEVEL_CHOICE, GENDER_CHOICE, PREFERENCE_CHOICE

# user_id        사용자 로그인 ID
# password       사용자 계정 비밀번호
# email          메일주소
# hp             핸드폰번호
# name           이름
# student_id     학번
# grade          학년, 졸업생 구분
# level          사이트 사용권한
# date_joined    가입일

class Member( models.Model ) :   
    user_id = models.CharField( max_length=20, verbose_name="아이디" )
    password = models.CharField( max_length=50, verbose_name="비밀번호" )
    user_name =  models.CharField( max_length=30, verbose_name="회원이름", null=False )
    birth =  models.DateField( max_length=30, verbose_name="생년월일", null=True )
    gender = models.CharField( choices=GENDER_CHOICE, max_length=10, verbose_name="성별", null = False )
    email = models.EmailField( max_length=100, verbose_name="이메일", null=True, unique=True )
    hp = models.CharField( max_length=15, verbose_name="핸드폰", null=True, unique=True)
    postal_code = models.CharField( max_length=10, verbose_name="우편번호")
    address = models.CharField( max_length=100, verbose_name="주소")
    detailAddress = models.CharField( max_length=100, verbose_name="상세주소")
    extraAddress = models.CharField( max_length=100, verbose_name="참고주소")
    preference = models.CharField( choices=PREFERENCE_CHOICE, max_length=30, verbose_name="매운맛선호도", null = False )
    level = models.CharField( choices=LEVEL_CHOICE, max_length=30, verbose_name="등급", default=3 )
    date_joined = models.DateTimeField( auto_now_add=True, verbose_name="가입일", null=True, blank=True )






