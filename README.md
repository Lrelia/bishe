
# 一、环境配置

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

# 二、认识文档工具

## 目录说明

1.source目录

该目录用于存放文档的rst文件，一个产品所需要的rst文件可能是多个，在创建你的rst文件(支持中文命名)，最终将会生成.html文件，该目录同时存放多个产品的文档，请勿改动其他项目的rst文件。

2.configs目录

该目录用于存放产品文档的配置文件,产品文档配置文件主要说明产品名称、版本号以及最终生成的html文件需要存放到的目标路径。

配置用的json文件定义:

```
    {
    "title":"这里写产品标题",
    "ver":"这里写产品文档版本号",
    "from":[
            "build/html/有米Android积分墙开发者文档.html", //比如这个
            "build/html/_static" //这个是必须的
        ],
    "into":"out/android/您的产品的英文名目录" //参考其他配置
    }

```
##　文档管理规则

在该项目中保存所有产品文档，生成统一样式的html文档，保存在out目录下，其他的打包工具可以直接引用out下面的文档存档。


# 三、使用步骤

编写rst文档->在configs下面新建产品文档配置->运行html.sh或html.bat


## 编写rst文档

rst教程详见: https://github.com/buke/openerp-doc/wiki/reStructuredText%E7%AE%80%E6%98%8E%E6%95%99%E7%A8%8B

或搜索 "reStructuredText教程"

*注意:source目录是多项目sdk文档共享目录，请不要改动他人的文档，创建或修改自己的文档,注意命名规范，支持中文命名。*
**注意，支持中文命名哦，自己规范命名，另外千万不要覆盖已有的文档！**

## 建立configs配置文件

这是一次性工作，比如安卓插播广告的sdk文档的配置文件，可以在configs目录下建立一个spot.json，参考目录里面已有的配置文件。注意最后要写入的into目录需要明确指定保存的路径，比如安卓插播广告的是out/android/spot，而ios的是out/ios/spot。

## 生成html文档

在命令行下运行以下命令:
linux :
```
    sh html.sh
```
windows:
```
    html.bat
```

然后选择操作编号，即可生成文档，最终产品的文档将保存到配置文件指定的into目录中，一般是out目录下。
