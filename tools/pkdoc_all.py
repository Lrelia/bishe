# -*- coding:utf-8 -*- 
import os,sys,json,shutil,re

def isNumber(str):
    pattern=re.compile(r'[0-9]+')
    match=pattern.match(str)
    if match:
        return True
    return False


if len(sys.argv)<2:
    print "请输入configs目录路径!\n异常退出***"
    exit()

config_dir=sys.argv[1]
if not os.path.exists(config_dir):
    print "configs目录不存在!\n异常退出***"
    exit()
file_list=os.listdir(config_dir)

for item in file_list:
    filePath=os.path.join(config_dir,item)
    os.system("python  tools/ymdoc.py %s"%filePath)
print ""
print "已经编译完成!"
print ""
print ""
print "----------------------------------------------"
