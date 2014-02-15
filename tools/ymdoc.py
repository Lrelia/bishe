# -*- coding:utf-8 -*- 
import os,sys,json,shutil


def copyIntoDir(srcPath,destDirPath):
    if not os.path.exists(destDirPath):
        os.makedirs(destDirPath)
    if os.path.isdir(srcPath):
        destTree=os.path.join(destDirPath,os.path.basename(srcPath))
        shutil.copytree(srcPath,destTree)
    else:
        shutil.copy2(srcPath,destDirPath)


if len(sys.argv)<2:
    print "请输入config.json!\n异常退出***"
    exit()

filePath=sys.argv[1]
print "配置文件:"+filePath

config=json.load(file(filePath))

#make html
os.environ["ympk_version"]=config["ver"]
os.environ["ympk_release"]=config["ver"]
os.system("make html")

#copy htmls
into=config["into"]
if os.path.exists(into):
    shutil.rmtree(into)
print into
os.makedirs(into)
src=config["from"]
for item in src:
    #print "copy "+item+" 到 "+into
    #print item
    copyIntoDir(item,into)

