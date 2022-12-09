from rest_framework import serializers
from .models import People


class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ['회원번호', '회원이름', '휴대전화', '등급', '카드번호']
