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
print "请选择需要编译的文档:"
i=0
titles=[]
for item in file_list:
    filePath=os.path.join(config_dir,item)
    config=json.load(file(filePath))
    title="[%d] %s %s"%(i,config["title"],config["ver"])
    titles.append(title)
    print title
    i=i+1

print "[%d] 全部"%i
while True:
    index_str=raw_input("请输入编号(输入q退出):")
    if index_str=="q":
        print "谢谢使用,再见!"
        exit()
    if not isNumber(index_str):
        print "输入编号有误!"
        continue
    index=int(index_str)
    if index<0 or index >i:
        print "输入编号有误!"
        continue
    if index==i:
        print "进行全部文档编译..."
        for item in file_list:
            filePath=os.path.join(config_dir,item)
            os.system("python  tools/ymdoc.py %s"%filePath)
    else:
        filePath=os.path.join(config_dir,file_list[index])
        os.system("python  tools/ymdoc.py %s"%filePath)
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print "已经编译完成!"
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print ""
    print "----------------------------------------------"
    for item in titles:
        print item
    print "[%d] 全部"%i 




    


