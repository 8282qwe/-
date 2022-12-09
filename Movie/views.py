import re

from django.shortcuts import render, redirect
from .serializers import PeopleSerializer
from .models import People, Movies, Movieschedule, Discountrate, Ticketing, Theaterseat, Board
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import auth
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib import messages


# Create your views here.
def movie_view(request):
    schedule_all = Movieschedule.objects.values('영화번호')
    movie_all = Movies.objects.filter(영화번호__in=schedule_all)
    movie_all_not = Movies.objects.all().exclude(영화번호__in=schedule_all)
    return render(request, 'mainpage.html', {"movie_list": movie_all,
                                             "movie_list_not": movie_all_not})


def board_view(request):
    if request.method == 'POST':
        if request.POST['board'] == "게시판":
            movie_id = request.POST['영화번호']
            movie = Movies.objects.get(영화번호=movie_id)
            board = Board.objects.all().filter(영화=movie)
            return render(request, 'board.html', {"movie": movie,
                                                  "boards": board})
        if request.POST['board'] == "저장":
            board = Board()
            movie_id = int(request.POST['movie_id'])
            score = int(request.POST['select'])
            movie = Movies.objects.get(영화번호=movie_id)
            movie.평점 = float((movie.평점 + score) / 2)
            if movie.평점 > 5.0:
                movie.평점 = 5.0
            board.작성자 = request.user
            board.영화 = movie
            board.평점 = score
            board.후기 = request.POST['review']
            board.save()
            board = Board.objects.all().filter(영화=movie)
            movie.save()
            return render(request, 'board.html', {'movie': movie,
                                                  'boards': board})
        if request.POST['board'] == "delete":
            movie_id = request.POST['movie_id']
            movie = Movies.objects.get(영화번호=movie_id)
            board_id = int(request.POST['board_id'])
            board = Board.objects.get(id=board_id)
            movie.평점 = movie.평점 * 2 - board.평점
            if movie.평점 > 5.0:
                movie.평점 = 5.0
            elif movie.평점 < 0.0:
                movie.평점 = 0.0
            board.delete()
            movie.save()
            boarder = Board.objects.all().filter(영화=movie)
            return render(request, 'board.html', {'movie': movie,
                                                  'boards': boarder})

    return render(request, "board.html")


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        if request.POST['check'] == '회원가입':
            return redirect('signup')

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if user.is_staff:
                return redirect('/admin/')
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'ID or Password is incorrect.'})
    else:
        return render(request, 'login.html')


def delete_view(request):
    if request.method == 'POST':
        pw = request.POST['password']
        user = request.user
        if check_password(pw, user.password):
            user.delete()
            auth.logout(request)
            messages.warning(request, "회원탈퇴가 완료되었습니다.")
            return redirect('home')
        else:
            return render(request, 'delete.html', {"error": "패스워드가 틀립니다."})
    else:
        return render(request, 'delete.html')


def signup_view(request):
    if request.method == "POST":
        if People.objects.all().filter(username=request.POST['username']):
            return render(request, 'signup.html', {'ID_error': '중복되는 ID가 있습니다.'})
        if People.objects.all().filter(휴대전화=request.POST['phone']):
            return render(request, 'signup.html', {'Phone_error': '중복되는 핸드폰 번호가 있습니다.'})
        if People.objects.all().filter(카드번호=request.POST['card']):
            return render(request, 'signup.html', {'Card_error': '중복되는 카드번호가 있습니다.'})
        if request.POST["password1"] == request.POST["password2"]:
            user = People.objects.create_user(
                username=request.POST["username"], password=request.POST["password1"],
                name=request.POST['name'], phone=request.POST['phone'],
                card=request.POST['card'],
            )
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'signup.html', {'PW_error': 'Password 와 Password Check가 일치하지 않습니다.'})
    return render(request, 'signup.html')


def logout_view(request):
    auth.logout(request)
    return redirect('home')


def schedule_view(request):
    schedule_all = Movieschedule.objects.values('영화번호')
    movie_all = Movies.objects.filter(영화번호__in=schedule_all)
    schedule_all = Movieschedule.objects.all()
    return render(request, 'movieschedule.html', {'schedules': schedule_all,
                                                  'movies': movie_all})


def account_view(request):
    user = request.user
    return render(request, 'account.html', {'username': user.username,
                                            '회원이름': user.회원이름,
                                            '휴대전화': user.휴대전화,
                                            '카드번호': user.카드번호})


def modify_view(request):
    user = request.user

    if request.method == "POST":
        if People.objects.all().filter(휴대전화=request.POST['phone']):
            return render(request, 'login.html', {'Phone_error': '중복되는 핸드폰 번호가 있습니다.'})
        if People.objects.all().filter(카드번호=request.POST['card']):
            return render(request, 'login.html', {'Card_error': '중복되는 카드번호가 있습니다.'})
        if request.POST["password1"] == request.POST["password2"]:
            user.set_password(request.POST["password1"])
            user.카드번호 = request.POST['card']
            user.휴대전화 = request.POST['phone']
            user.save()
        else:
            return render(request, 'modify.html', {'PW_error': 'Password 와 Password Check가 일치하지 않습니다.'})
        auth.login(request, user)
        return redirect('/')
    else:
        return render(request, 'modify.html')


@csrf_exempt
def ticketing_view(request):
    movie_sch = Movieschedule.objects.all()
    user = request.user
    if request.method == 'POST':
        ticketing = Ticketing()
        buffer = ''
        jsonObject = json.loads(request.body)
        buffer = jsonObject['seat'][1:-1]
        split = jsonObject['movie'].split('/')
        people = People.objects.get(username=user.username)
        movie = Movieschedule.objects.get(id=int(split[0]))
        theater = Theaterseat.objects.get(상영관번호=str(split[3][0]))
        cost = str(int(jsonObject['cost']))
        print(buffer)
        ticketing.username = people
        ticketing.영화번호 = movie
        ticketing.상영관번호 = theater
        ticketing.금액 = cost
        ticketing.예매좌석 = buffer
        ticketing.save()
        return redirect('/')
    elif request.method == 'GET':
        id = request.GET['id']
        movie_sch_one = Movieschedule.objects.get(id=id)
        theaterseat = []
        movie_sch_all = movie_sch.filter(id=id).values("상영관번호")[0]["상영관번호"]
        ticketing_all = Theaterseat.objects.get(상영관번호=movie_sch_all)
        for i in range(0, ticketing_all.총좌석수):
            theaterseat.append(i)
        if Ticketing.objects.filter(영화번호=id).count() != 0:
            seat_selected = []
            ticketings = Ticketing.objects.all().filter(영화번호=id).values("예매좌석")
            for ticketing in ticketings:
                seat_selected = seat_selected + (ticketing['예매좌석'].split(','))
            seat_selected = list(set(seat_selected))
            seat_selected.sort()
            for x in seat_selected:
                theaterseat[int(x)] = 400
        theater = ticketing_all.행번호.split(',')
        theater_width = int(ticketing_all.위치번호) * int(theater[0])
        theater_height = int(theater[1])
        discount = Discountrate.objects.filter(등급=user.등급).values('할인율')
        discount = list(discount)
        buffer = discount[0]['할인율']
        return render(request, 'ticketing.html', {'movie_sch': movie_sch_one,
                                                  'id': id,
                                                  'users': buffer,
                                                  'theaterseat': theaterseat,
                                                  'theater_width': str(theater_width),
                                                  'theater_height': str(theater_height),
                                                  'theater_row': int(theater[0])})


@csrf_exempt
def ticketing_search_view(request):
    if request.method == 'POST':
        ticket_id = int(request.POST['영화번호'])
        ticket = Ticketing.objects.get(id=ticket_id)
        ticket.delete()

    user = request.user
    ticketing = Ticketing.objects.all().filter(username=user.username)
    return render(request, 'ticketing_search.html', {"ticketings": ticketing})


def search_view(request):
    if request.method == 'POST':
        if request.POST['select'] == '영화제목':
            movie = Movies.objects.all().filter(영화제목__contains=request.POST['content'])
        elif request.POST['select'] == '영화감독':
            movie = Movies.objects.all().filter(영화감독__contains=request.POST['content'])
        elif request.POST['select'] == '주연배우':
            movie = Movies.objects.all().filter(주연배우__contains=request.POST['content'])
        elif request.POST['select'] == '평점(이상)':
            score = float(request.POST['content'])
            movie = Movies.objects.all().filter(평점__gte=score)
        elif request.POST['select'] == '평점(이하)':
            score = float(request.POST['content'])
            movie = Movies.objects.all().filter(평점__lte=score)
        else:
            movie = Movies.objects.all()
        return render(request, 'search.html', {"movies":movie})
    return render(request, 'search.html')
