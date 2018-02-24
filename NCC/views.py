from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import *
import datetime
import os

upath = ""
totalquestion = 6
endtime = 0
startTime = 0


def addsTime():
    global startTime
    now = datetime.datetime.now()
    print("Call")
    time = now.second + now.minute * 60 + now.hour * 60 * 60
    startTime = time + 1 * 30
    print(startTime)


def start(request):
    if checkTimeslot(request) == 1:
        context = {
            'rt': rtime(request)
        }
        return render(request, 'instructions.html', context)
    else:
        print(checkTimeslot(request))
        return render(request, 'signup.html')


def setEndtime(request):
    global endtime
    addtime = request.GET["time"]
    now = datetime.datetime.now()
    time = now.second + now.minute * 60 + now.hour * 60 * 60
    endtime = time + addtime


def checkTimeslot(request):
    now = datetime.datetime.now()
    time = now.second + now.minute * 60 + now.hour * 60 * 60
    addt = 0
    if logincheck(request) == 1:
        addt = request.user.player.time
    print(startTime)
    if time < startTime:
        return 1
    elif time > (endtime + addt):
        return 2
    else:
        return 0


def logincheck(request):
    if request.user.is_authenticated:
        print("1")
        return 1
    else:
        print("0")
        return 0


def pagecheck(request):
    t = checkTimeslot(request)
    if t == 0 and logincheck(request) == 1:
        return 0
    else:
        if t == 1:
            return 1
        elif t == 2:
            return 2
        else:
            return 3


def rtime(request):
    now = datetime.datetime.now()
    time = now.second + now.minute * 60 + now.hour * 60 * 60
    if checkTimeslot(request) == 0:
        return (endtime + request.user.player.time) - time
    else:
        return startTime - time


def sendpage(request, exitcode):
    if exitcode == 1:
        return render("waiting Page")
    elif exitcode == 2:
        return HttpResponse("Leaderboard")
    else:
        return start(request)


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
        # now = datetime.datetime.now()
        # time = now.second + now.minute * 60 + now.hour * 60 * 60
        time = 0
        user = User.objects.create_user(username=uname, email=p1email, password=password)
        user_object = Player.objects.create(pid=user, p1name=p1name, p2name=p2name, p1email=p1email,
                                            p2email=p2email,
                                            p1mno=p1mno, p2mno=p2mno, score=0, time=time,
                                            q1_score=0, q2_score=0, q3_score=0, q4_score=0,
                                            q5_score=0, q6_score=0, subtime=0,level=level,rank=0)
        user_object.save()
        u2 = authenticate(request, username=uname, password=password)

        print(uname)

        login(request, u2)

        userFolderCreate(request)
        return render(request, 'QuestionPage.html', )
    else:
        return start(request)


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
        'score': request.user.player.score
    }
    return render(request, "codingPage.html", context)

def setRank(request):
    p = Player.objects.all().filter(leve =request.user.player.level).order_by("-score", "subtime","id")
    count = 0
    for i in p:
        count = count + 1
        if i.pid == request.user:
            i.rank = count
            return


def loadbuff(request):
    response_data = {}
    x = request.get_full_path().split('/')
    x = x[-1]
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
        'score': score,
        'rank': 1,
        'rt': rtime(request)

    }

    return render(request, "codingPage.html", context)


def coding(request):
    return render(request, "codingPage.html")


def leaderboard(request):
    p = Player.objects.all().order_by("-score","subtime")
    context = {
        'p': p
    }
    return render(request, "leaderboard.html", context)


def questionhub(request):
    return render(request, 'QuestionPage.html', )


def log_out(request):
    u = request.user
    score = u.player.score
    context = {
        'score': score,
        'rank': 1,

    }
    logout(request)
    return render(request, 'result.html', context)


def CodeSave(request):
    if request.method != "POST":
        return questionhub(request)
    if logincheck(request) == 0:
        return start(request)
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
    time = now.second + now.minute * 60 + now.hour * 60 * 60
    x = request.get_full_path().split('/')
    x = x[-1]
    qscore = {
        1: q1_score,
        2: q2_score,
        3: q3_score,
        4: q4_score,
        5: q5_score,
        6: q6_score
    }
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
    ans = os.popen("python NCC/judge/main.py " + str(time) + "." + str(code) + " " + u + " " + x).read()
    # ans = ans[::-1]
    ans = int(ans)
    print(ans)
    tcOut = [0, 1, 2, 3, 4]
    switch = {
        10: 0,
        99: 1,
        50: 2,
        89: 3,
        70: 4

    }
    score = 0
    for i in range(0, 5):
        data[i] = ans % 100
        ans = int(ans / 100)
        tcOut[i] = switch[data[i]]
        if tcOut[i] == 0:
            score = score + 20
    print(tcOut)

    # score = (tc1 + tc2 + tc3 + tc4 + tc5) * 20
    context = {
        'tc10': tcOut[4],
        'tc20': tcOut[3],
        'tc30': tcOut[2],
        'tc40': tcOut[1],
        'tc50': tcOut[0],
        'score': score
    }
    u = request.user
    s = u.player
    if s.qscore[x] < score:
        s.score = s.score + score - qscore[x]
        s.qscore[x] = score
        s.subtime = time
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
    u = request.user.username
    file = upath + "/" + str(u) + "/" + str(x) + "/" + filename + "." + ext
    print(file)
    f = open(file, "r")
    data = f.read()
    response_data["file"] = data
    return JsonResponse(response_data)
