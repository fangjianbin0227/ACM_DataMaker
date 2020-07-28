import argparse
import os
import data

parser = argparse.ArgumentParser()
parser.add_argument('--file1',default="bat/tmp1.cpp")
parser.add_argument('--file2',default="bat/tmp2.cpp")
parser.add_argument('--out1',default="bat/tmp1.out")
parser.add_argument('--out2',default="bat/tmp2.out")
parser.add_argument('--dataout',default="bat/data.out")
parser.add_argument('--repeat',type=int,default=1)
parser.add_argument('--bigdata',type=bool,default=False)
args = parser.parse_args()
file1 = args.file1
file2 = args.file2
out1 = args.out1
out2 = args.out2
dataout = args.dataout
t = args.repeat
bigdata = args.bigdata

print("compling...")
os.system("g++ " + file1 + " -o bat/tmp1")
os.system("g++ " + file2 + " -o bat/tmp2")
for i in range(t):
    print("generating...")
    data = data.get_data()
    if data == None:
        print("get no input data,please check out data.py")
        exit(0)

    print("comparing...")
    if not bigdata:
        p1 = os.popen("echo " + data + " | bat/tmp1")
        p2 = os.popen("echo " + data + " | bat/tmp2")
        r1 = p1.read()
        r2 = p2.read()
        if(r1 != r2):
            with open(dataout,"w") as f:
                f.write(data)
            os.system("cat " + dataout + " | bat/tmp1 > " + out1)
            os.system("cat " + dataout + " | bat/tmp2 > " + out2)
            cmd = "diff " + out1 + " " + out2
            p = os.popen(cmd)
            print(cmd)
            print(p.read())
            exit(0)
    else:
        with open(dataout,"w") as f:
            f.write(data)
        os.system("cat " + dataout + " | bat/tmp1 > " + out1)
        os.system("cat " + dataout + " | bat/tmp2 > " + out2)
        cmd = "diff " + out1 + " " + out2
        p = os.popen(cmd)
        r = p.read()
        if r:
            print(cmd)
            print(r)
            exit(0)

print("no diff")