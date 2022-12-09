# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.utils.timezone import now
from django.core.exceptions import ValidationError

class Discountrate(models.Model):
    등급 = models.CharField(primary_key=True, max_length=10)
    할인율 = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'discountrate'

    def __str__(self):
        return self.등급


class Movies(models.Model):
    영화번호 = models.AutoField(primary_key=True, editable=False)
    영화제목 = models.CharField(max_length=30)
    영화감독 = models.CharField(max_length=20)
    주연배우 = models.CharField(max_length=20)
    포스터 = models.ImageField(blank=True, null=True, editable=True)
    줄거리 = models.TextField(null=True, blank=True)
    평점 = models.FloatField(default=5)

    class Meta:
        managed = True
        db_table = 'movies'

    def __str__(self):
        return self.영화제목


class Movieschedule(models.Model):
    영화번호 = models.ForeignKey('Movies', models.DO_NOTHING, db_column='영화제목')
    상영시간 = models.DateTimeField(default=now)
    상영관번호 = models.ForeignKey('Theater', models.DO_NOTHING, db_column='상영관번호')
    요금 = models.CharField(max_length=10)

    class Meta:
        managed = True
        db_table = 'movieschedule'
        constraints = [
            models.UniqueConstraint(
                fields=["상영시간", "상영관번호"],
                name="unique reservations",
            ),
        ]

    def __str__(self):
        return str(self.영화번호)+str(self.상영시간)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password, name, phone, card):
        user = self.model(
            username=username,
            등급=Discountrate.objects.get(할인율=10),
            회원이름=name,
            휴대전화=phone,
            카드번호=card
        )
        user.set_password(password)
        user.is_admin = False
        user.is_superuser = False
        user.is_staff = False
        user.save(using=self.db)
        return user

    def create_superuser(self, username, password):
        user = self.model(
            username=username,
            등급=Discountrate.objects.get(할인율=50)
        )
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)
        return user


class People(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(primary_key=True, max_length=20, unique=True)
    회원이름 = models.CharField(max_length=20)
    휴대전화 = models.CharField(max_length=15)
    등급 = models.ForeignKey(Discountrate, models.DO_NOTHING, db_column='등급')
    카드번호 = models.CharField(max_length=26)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    objects = UserManager()


    class Meta:
        managed = True
        db_table = 'people'

class Theater(models.Model):
    상영관번호 = models.CharField(primary_key=True, max_length=10)
    상영관형태 = models.CharField(max_length=10)

    class Meta:
        managed = True
        db_table = 'theater'

    def __str__(self):
        return self.상영관번호


class Theaterseat(models.Model):
    상영관번호 = models.OneToOneField(Theater, models.DO_NOTHING, db_column='상영관번호', primary_key=True)
    행번호 = models.CharField(max_length=5)
    총좌석수 = models.IntegerField()
    위치번호 = models.CharField(max_length=5)

    class Meta:
        managed = True
        db_table = 'theaterseat'
        unique_together = (('상영관번호', '행번호', '위치번호'),)

    def __str__(self):
        return str(self.상영관번호)


class Ticketing(models.Model):
    username = models.ForeignKey(People, models.DO_NOTHING)
    영화번호 = models.OneToOneField(Movieschedule, models.DO_NOTHING)
    상영관번호 = models.ForeignKey(Theaterseat, models.DO_NOTHING)
    예매일시 = models.DateTimeField(default=now, editable=False)
    예매좌석 = models.CharField(max_length=20)
    금액 = models.CharField(max_length=10)

    class Meta:
        managed = True
        db_table = 'ticketing'
        unique_together = (('영화번호', '상영관번호', '예매일시'),)

    def __str__(self):
        return str(self.영화번호.영화번호)+self.username.username+str(self.예매일시)

class Board(models.Model):
    id = models.AutoField(primary_key=True, editable=True)
    작성자 = models.ForeignKey(People, models.DO_NOTHING)
    영화 = models.ForeignKey(Movies, models.DO_NOTHING)
    평점 = models.IntegerField()
    후기 = models.CharField(max_length=200)
    작성일자 = models.DateTimeField(default=now, editable=False)

    class Meta:
        managed = True
        db_table = "board"

    def __str__(self):
        return str(self.id)
