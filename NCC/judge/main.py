import sys, os
from sandy import sandy_func
from comparator import compare

base_dir = os.path.dirname(os.path.abspath(__file__))
user_dir = base_dir + "/USERS"
description_dir = base_dir + "/standard/description"
input_dir = base_dir + "/standard/input"
output_dir = base_dir + "/standard/output"


def run_testcase(i, exec_file, uid, qid):
    in_file = input_dir + "/" + str(qid) + "/" + str(i) + ".in"  # standard input for running

    in_file_fd = open(in_file, "r")
    user_out = user_dir + "/" + str(uid) + "/" + str(qid) + "/" + str(i) + ".uout"

    user_out_fd = os.open(user_out, os.O_RDWR | os.O_CREAT)  # user output after running
    des_file = description_dir + "/" + str(qid) + "/" + str(i) + ".txt"  # description file

    des_fd = open(des_file, "r")
    lines = des_fd.readlines()
    time = lines[0].strip()
    mem = lines[1].strip()
    des_fd.close()

    res = sandy_func(exec_file, in_file_fd, user_out_fd, time, mem)

    in_file_fd.close()

    os.close(user_out_fd)
    actual_out = output_dir + "/" + qid + "/" + str(i) + ".out"

    if (res == 1):
        res = compare(user_out, actual_out)

    # print res
    os.remove(user_out)  # removing user output
    return res


def compile(src_userfile, exec_file, ext):
    a = 1
    if (ext == 'c'):
        a = os.system("gcc " + src_userfile + " -o " + exec_file + " -lm")
    elif (ext == "cpp"):
        a = os.system("g++ " + src_userfile + " -o " + exec_file + " -lm")
    return a


def main():
    filename = sys.argv[1]
    ext = sys.argv[1].split(".")[-1]  # Assuming filename with format uid_qid.ext is passed on command line
    # print ext
    uid = sys.argv[2]
    qid = sys.argv[3]
    # print uid,qid,sid

    src_userfile = user_dir + "/" + uid + "/" + qid + "/" + filename
    exec_file = user_dir + "/" + uid + "/" + qid + "/" + filename.split(".")[0]
    # error_file=error_dir+"/"+uid+"/"+filename.split(".")[0]		#need to check existence before using
    res = []
    # if(os.path.isfile(error_file)==False):
    # error_fd=os.open(error_file, os.O_RDONLY|os.O_CREAT)
    # os.close(error_fd)
    a = compile(src_userfile, exec_file, ext)  # exec_file created after compilation

    if (a == 0):
        # os.remove(error_file)			#removes files only not directory removedirs to remove dir
        for i in range(0,5):
            r = run_testcase(i, exec_file, uid, qid)
            res.append(r)
            #print(r)
        os.remove(exec_file)
        #print(res)
    else:
        res = -89
        #print(res)

    return res


a = main()
ans = 0
if(a != -89):
    for i in range(0,5):
        if(a[i] < 0):
            a[i] = -a[i]
        if(a[i] < 10):
            a[i] = a[i] * 10
        ans = ans *100 + a[i]
else:
    ans = 8989898989
print(ans)
sys.exit(0)
# 10 = right answer
# 99 = wrong anwer
# 89 = compile tile error
# 50  = TLE
# 70 = Abnormal termination
# 10 = Standard input
# 20 = custom
