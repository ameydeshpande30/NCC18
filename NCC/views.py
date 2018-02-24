from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import *
import datetime
import os

upath = ""
totalquestion = 6


def start(request):
    return render(request, 'signup.html')


def signup(request):
    print(request.method)
    if request.method == 'POST':
        uname = request.POST.get('uname')
        password = request.POST.get("password")
        p1name = request.POST.get("p1name")
        p2name = request.POST.get("p2name")
        p1email = request.POST.get("p1email")
        p2email = request.POST.get("p2email")
        p1mno = request.POST.get("p1mno")
        p2mno = request.POST.get("p2mno")
        level = request.POST.get("optradio")
        now = datetime.datetime.now()
        time = now.second + now.minute * 60 + now.hour * 60 * 60
        user = User.objects.create_user(username=uname, email=p1email, password=password)
        user_object = Player.objects.create(pid=user, p1name=p1name, p2name=p2name, p1email=p1email, p2email=p2email,
                                            p1mno=p1mno, p2mno=p2mno, score=0, time=time)
        user_object.save()
        u2 = authenticate(request, username=uname, password=password)

        print(uname)

        login(request, u2)

        userFolderCreate(request)
        return render(request, 'QuestionPage.html', )
    else:
        return render(request, 'signup.html', )


def userFolderCreate(request):
    global upath
    global totalquestion
    path = upath
    path = path + "/" + str(request.user.username)
    print(path)
    if not os.path.exists(path):
        os.mkdir(path)
        for i in range(1, totalquestion + 1):
            os.mkdir(path + "/" + str(i))


def set():
    path = os.path.dirname(os.path.abspath(__file__))
    path = path + "/judge/USERS"
    print("***User Folder Created***")
    if not os.path.exists(path):
        os.mkdir(path)
    global upath
    upath = path


def testp(request):
    context = {
        'tc10': 1,
        'tc20': 1,
        'tc30': 0,
        'tc40': 0,
        'tc50': 1,
        'tc60': 1,
        'score': 100
    }
    return render(request, "codingPage.html", context)


def mysubmission(request):
    return HttpResponse("hello")


def loadbuff(request):
    response_data = {}
    x = request.get_full_path().split('/')
    x = x[-1]
    q = x
    u = request.user.username
    file = upath + "/" + str(u) + "/" + str(x) + "/" + str("lbf")
    f = open(file, "r")
    text = f.read()
    if not text:
        data = ""
    response_data["text"] = text
    return JsonResponse(response_data)


def checkuser(request):
    response_data = {}
    uname = request.POST.get("username")
    check1 = User.objects.filter(username=uname)
    if not check1:
        response_data["is_success"] = True
    else:
        response_data["is_success"] = False
    return JsonResponse(response_data)


def test(request):
    x = request.get_full_path().split('/')
    x = x[-1]
    x = str(x)
    q = Attempt.objects.all().filter(user=request.user, qid=x)
    score = request.user.player.score
    context = {
        'x': x,
        'q': q,
        'score':score,
        'rank':1

    }

    return render(request, "codingPage.html", context)


def coding(request):
    return render(request, "codingPage.html")


def questionhub(request):
    return render(request, 'QuestionPage.html', )


def log_out(request):
    u = request.user
    score = u.player.score
    context = {
        'score': score,
        'rank': 1

    }
    logout(request)
    return render(request, 'result.html', context)


def CodeSave(request):
    codeValue = request.POST.get("optradioc")
    print(codeValue)
    text = request.POST.get("editorta")
    code = "c"
    cv = int(codeValue)
    if cv == 2:
        code = "cpp"
    print(text)
    u = request.user.username
    print(u)
    now = datetime.datetime.now()
    time = now.second + now.minute * 60
    x = request.get_full_path().split('/')
    x = x[-1]
    q = x
    data = [1, 2, 3, 4, 5]
    print(upath)
    file = upath + "/" + str(u) + "/" + str(x) + "/" + str(time) + "." + str(code)
    lfile = upath + "/" + str(u) + "/" + str(x) + "/" + str("lbf")
    mysub = Attempt.objects.create(user=request.user, qid=str(x), time=time, ext=str(code), status="Testing")
    mysub.save()
    with open(file, 'w') as f:
        f.write(str(text) + '\n')
    with open(lfile, 'w') as f:
        f.write(str(text) + '\n')
    ans = os.popen("python NCC/judge/main.py " + str(time) + "." + str(code) + " " + u + " " + q).read()
    #ans = ans[::-1]
    ans = int(ans)

    tc1 = 0
    tc2 = 0
    tc3 = 0
    tc4 = 0
    tc5 = 0
    tc6 = 0
    print(ans)
    tcOut = [0,1,2,3,4]
    switch = {
        10:0,
        99:1,
        50:2,
        89:3,
        70:4

    }
    for i in range(0, 5):
        data[i] = ans % 100
        ans = int(ans / 100)
        tcOut[i] = switch[data[i]]
    print(tcOut)

    score = (tc1 + tc2 + tc3 + tc4 + tc5) * 20
    context = {
        'tc10': tcOut[0],
        'tc20': tcOut[1],
        'tc30': tcOut[2],
        'tc40': tcOut[3],
        'tc50': tcOut[4],
        'tc60': tcOut[4],
        'score': score
    }
    u = request.user
    s = u.player
    s.score = s.score + score
    s.save()
    return render(request, "testcase.html", context)


def leaderboard(request):
    count = Player.objects.all().count()
    p = Player.objects.all().order_by('-score', 'time', 'p1name')

    context = {
        'pl': p,
        'count': count
    }
    return render(request, 'leaderboard.html', context)


def MySubmissions(request):
    response_data = {}
    filename = request.POST["filename"]
    ext = request.POST["ext"]
    x = request.get_full_path().split('/')
    x = x[-1]
    q = x
    u = request.user.username
    file = upath + "/" + str(u) + "/" + str(x) + "/" + filename + "." + ext
    print(file)
    f = open(file, "r")
    data = f.read()
    response_data["file"] = data
    return JsonResponse(response_data)
