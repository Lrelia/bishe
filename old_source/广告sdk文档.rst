.. YoumiAndroidSdkDocumentation documentation master file, created by
   sphinx-quickstart on Thu Nov 28 23:10:38 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

欢迎使用有米广告Android Sdk开发者文档
========================================================
前言 
------
1.文档说明 
~~~~~~~~~~~

.. _doc_desc:

* `详情 <doc_desc.html>`_
2.SDK功能概览 
~~~~~~~~~~~

.. _features:

* 支持积分广告、无积分广告及在线参数等实用功能 `详情 <features.html>`_
3.更新日志
~~~~~~~~~~~

.. _changelog:

* 最新版本:v4.06 `详情 <changelog.html>`_



一、准备工作 
--------------
1.申请AppID 
~~~~~~~~~~~~~~
* . 点击[ 创建应用 ](https://www.youmi.net/apps/create) 进行新应用创建。  
* . 查看[ 应用详情 ](https://www.youmi.net/apps/view) ，获取发布ID和应用密钥，在后续[初始化](#section_ready_init)中使用。

2.导入SDK 
~~~~~~~~~~~~~~

3.配置AndroidManifest
~~~~~~~~~~~~~~~~~~~~~~~~
3.1 配置用户权限(重要)
'''''''''''''''''''''''
在AndroidManifest.xml文件中配置用户权限  

.. _permission:

* `查看详情 <permission.html>`_

3.2 添加必须组件(重要) 
'''''''''''''''''''''''
* `积分广告组件配置 <offers_config.html>`_
* `无积分广组件告配置 <offers_config.html>`_
* `积分+无积分广告组件配置 <offers_config.html>`_

