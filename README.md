
# 环境配置

## linux
* 1. python 2.7  安装命令是 sudo apt-get install python 
* 2. easy_install和pip   安装命令是 sudo apt-get install python-setuptools python-pip python-dev build-essential
* 3. sphinx  安装命令是 sudo easy_install sphinx
* 4. sphinx-bootstrap-theme 安装命令是 sudo pip install sphinx_bootstrap_theme

## windows

>
***务必按顺序进行配置，如果配置失败，请检查是否有按照教程指引.***

### 1)安装python

下载地址： 

32位windows : http://www.python.org/ftp/python/2.7.6/python-2.7.6.msi
64位windows : http://www.python.org/ftp/python/2.7.6/python-2.7.6.amd64.msi

### 2)设置环境变量:

```
    C:\Python27;C:\Python27\Scripts

```

###  一键安装windows环境的其他插件:
1.当前目录下有个windows目录，打开它，里面有个setups目录，在里面找到install.bat
2.双击install.bat 即可安装其余插件.

# 认识文档工具

## 目录说明


# 使用步骤



## 编写rst文档

### rst教程 

详见: 

### rst文件存留位置

source目录

*注意:source目录是多项目sdk文档共享目录，请不要改动他人的文档，创建或修改自己的文档,注意命名规范，支持中文命名。*

### source目录规

## 编写

1) 在source目录下编写rst文件
2) 双击build.bat
3) 在build目录查看生成结果，建议先用chrome查看效果，后续有专人优化样式模板。

3.如何写文档?
在source里面，注意conf.py和logo.png不能改，其他的都可以改。
rst即restructuredtext，类似于markdown，文档编写利器。需要大概学一下它的语法。

4.截图放哪?
source/_static目录下，可在里面建立子目录。

5.如何生成html文档?
双击build.bat即可。
