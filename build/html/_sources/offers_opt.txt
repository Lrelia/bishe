积分墙高级功能
==============

`返回上一层 <javascript:history.back();>`_

1.刷新积分余额UI显示
--------------------

如果您在UI上显示用户的积分账户余额，用户的积分余额可能会因为各种可能的原因导致余额变动(增减)，这时候您需要刷新UI上的显示值，可以通过以下方法实现积分余额在UI上的自动刷新。

(1)让UI相关的类(可以是Activity或View相关的类) implements net.youmi.android.offers.Ym_Class_PointsChangeNotify这个接口。

接口定义如下: ::

	package net.youmi.android.offers;
	
	/**  
	* 积分余额增减变动监听器   
        * @author youmi       
        */  	
	public interface Ym_Class_PointsChangeNotify {	
	
	/**
	 * 积分余额增减变动通知,该回调在UI线程中进行，可直接与UI进行交互
	 * @param pointsBalance 当前积分余额
	 */
	public void ym_method_onPointBalanceChange(int pointsBalance);
	
	}


(2)在UI初始化后调用: ::

	net.youmi.android.offers.Ym_Class_PointsManager.getInstance(this).ym_method_registerNotify(notifyObject);
	
(3)在UI销毁前调用以下代码释放Notify引用，以防止造成内存漏洞: ::

	net.youmi.android.offers.Ym_Class_PointsManager.getInstance(this).ym_method_unRegisterNotify(notifyObject);
	

2.通过SDK获取积分订单
---------------------

用户完成了一次积分任务并在有米服务器成功结算后，可以通过以下方法让SDK回调通知应用用户所完成的订单: 

 
第一步，您需要定义一个MyPointsReceiver类(名字可以随意)，它必须继承自net.youmi.android.offers.Ym_Class_PointsReceiver:  

*示例代码*: ::
 
	package com.test;  
	import android.content.Context;    
	import net.youmi.android.offers.Ym_Class_EarnPointsOrderList;  
	import net.youmi.android.offers.Ym_Class_PointsReceiver;	
	public class MyPointsReceiver extends Ym_Class_PointsReceiver{		
		@Override
		protected void ym_method_onEarnPoints(Context context, Ym_Class_EarnPointsOrderList list) {
  			//当SDK获取到用户赚取积分的订单时，会第一时间调用该方法通知您。
			//参数Ym_Class_EarnPointsOrderList是一个积分订单列表，您可以在这里处理积分详细订单。
		}		
		@Override
		protected void ym_method_onViewPoints(Context context) {
			//这里是个有趣的小功能，当用户赚取积分之后，积分墙SDK会在通知栏上显示一条获取积分的提示，如果用户点击了这个通知，该函数会被调用。  
			//这时候您可以在这里实现一个跳转，让用户跳转到您设计好的一个积分账户余额页面(如"我的账户"之类的Activity)。
			//该操作是可选的，如果需要关闭通知栏积分提示，请调用PointsManager.getInstance(context).setEnableEarnPointsNotification(false) 
		}	
	}
	

第二步，您需要在AndroidManifest.xml上配置刚刚定义的 MyPointsReceiver:  

*示例代码*:  ::
	
	<receiver
		android:name="MyPointsReceiver"
		android:exported="false" >
		<intent-filter>
			<action android:name="ep_请替换为您的AppID" />
			<action android:name="vp_请替换为您的AppID" />
		</intent-filter>
	</receiver>
  
注意:这里有一个很关键的细节，您必须为MyPointsReceiver配置两个Action，Action的名字分别是**以"ep\_"和"vp\_"开头**，以您的应用的AppID结尾的字符串。（AppID是从有米主站上申请的应用ID，16个字符，所以Action的总长度应该是19个字符）
 
 
附录:积分订单类定义
 

Ym_Class_EarnPointsOrderList: ::
 
	package net.youmi.android.offers;
	...
	/**
	 * 积分订单列表
	 * 
	 */
	public class Ym_Class_EarnPointsOrderList {
		/**
		 * 获取服务器上设置积分单位名称
		 */
		public String getCurrencyName();
		/**
		 * 根据index获取订单详情(EarnPointsOrderInfo)
		 */
		public Ym_Class_EarnPointsOrderInfo get(int index);
		/**
		 * 判断列表是否为空
		 */
		public boolean isEmpty();
		/**
		 * 获取列表项数量
		 */
		public int size(); 
	} 
 

Ym_Class_EarnPointsOrderInfo: ::


	package net.youmi.android.offers; 
	/**
	 * 赚取积分的订单
	 */
	public final class Ym_Class_EarnPointsOrderInfo {
		/**
		 * 获取订单号(具有唯一性)
		 */
		public String getOrderID();
		/**
		 * 获取渠道号，这里指在AndroidManifest.xml上配置的有米渠道号，详见文档 
		 */
		public int getChannelId();
		/**
		 * 获取开发者自定义用户唯一标识，该值通过OffersManager设置
		 */
		public String getCustomUserID();
		/**
		 * 获取积分订单的状态: 1.表示开发者获得了收入并且用户获得了积分。 2.表示开发者没有获得收入但用户获得了积分(未通过审核以及测试模式下结算无效等情况)。
		 */
		public int getStatus()
		/**
		 * 本次获取积分的描述语，如"成功安装《--》获取了100金币" 
		 */
		public String getMessage();
		/**
		 * 本次获得的积分 
		 */
		public int getPoints();
		/**
		 * 本次获得积分的结算时间
		 */
		public long getSettlingTime();
	}


3.通过服务器获取积分订单
------------------------
用户完成了一次积分任务并在有米服务器成功结算后，也可以通过服务器通讯的方式，由有米服务器向您的服务器回调用户完成的订单，详情请查看 `有米Android积分墙积分订单服务器回调协议 <http://wiki.youmi.net/Youmi_android_offers_order_callback_protocol>`_ 。

**注意:如果使用了服务器订单回调，则上文所述的"通过SDK获取积分订单"将不可用，即SDK将不会通知应用订单到账，同时SDK原有的积分管理功能也将被禁用，所有积分流程只能通过服务器实现，可以极大地提高积分安全性。**


4.验证积分墙配置是否正确
------------------------

嵌入SDK时如果配置有误有可能会导致没有收入或者获取不到积分，在完成文档中的配置之后可以通过调用以下接口查看配置是否正确: ::

    //积分墙配置检查(没有使用"通过SDK获取积分订单"功能):
    bool isSuccess = net.youmi.android.offers.Ym_Class_OffersManager.getInstance(context).ym_method_checkOffersAdConfig();	
    //积分墙配置检查(使用"通过SDK获取积分订单"功能):
    bool isSuccess = net.youmi.android.offers.Ym_Class_OffersManager.getInstance(context).ym_method_checkOffersAdConfig(true);

**注意,该接口调用的结果如果返回true，则说明配置正确，可以删掉该调用。如果返回false，则需要查看logcat的相关输出，里面有指出哪些相关的配置错误内容。**


5.关闭有米的 debug log 
---------------------

如果需要关闭有米广告SDK的 debug log，请调用以下代码来关闭sdk的log输出。

*代码示例:* ::
	 
	net.youmi.android.Ym_Class_AdManager.getInstance(this).ym_method_setEnableDebugLog(false);

注意:上传到有米主站进行审核时务必开启debug log,这样才能保证通过审核。
