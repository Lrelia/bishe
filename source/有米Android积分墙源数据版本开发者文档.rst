有米Android积分墙源数据版本开发者文档
===========================

一、基本配置（重要）
--------------

1.导入SDK
~~~~~~~~~~~~~~~~~~~~~~~~
将sdk解压后的 **libs** 目录下的jar文件导入到工程指定的libs目录。 


2 权限配置
~~~~~~~~~~~~~~~~~~~~~~~~

**请将下面权限配置代码复制到 AndroidManifest.xml 文件中 :**::
	 

    <uses-permission android:name="android.permission.INTERNET"/> 
    <uses-permission android:name="android.permission.READ_PHONE_STATE"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" /> 
    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/> 
    <uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW"/>
    <uses-permission android:name="android.permission.GET_TASKS"/>
	
    <!--以下为可选权限-->
    <uses-permission android:name="com.android.launcher.permission.INSTALL_SHORTCUT"/>

3 广告组件配置
~~~~~~~~~~~~~~~~~~~~~~~~

**请将以下配置代码复制到 AndroidManifest.xml 文件中:**::

	<service
		android:name="net.youmi.android.Ym_Class_AdService"
		android:exported="false" >
	</service>
	<service
		android:name="net.youmi.android.Ym_Class_ExpService"
		android:exported="false" >
	</service>
	<receiver 
		android:name="net.youmi.android.Ym_Class_AdReceiver" >
		<intent-filter>
			<action android:name="android.intent.action.PACKAGE_ADDED" />
			<data android:scheme="package" />
		</intent-filter>
	</receiver> 
	<receiver
		android:name="net.youmi.android.offers.Ym_Class_OffersReceiver"
		android:exported="false" >
	</receiver>


4 混淆配置
~~~~~~~~~~~~~~~~~~~~~~~~
**如果您的项目使用了Proguard混淆打包，为了避免SDK被二次混淆导致无法正常获取广告，请务必在proguard-project.txt中添加以下代码:**::

    -dontwarn net.youmi.android.**
	-keep class net.youmi.android.** {
	*;  
	}  

二、初始化及相关工作（重要）
--------------
请务必在应用第一个Activity(启动的第一个类)的onCreate中调用以下代码::

	net.youmi.android.Ym_Class_AdManager.getInstance(context).init("AppId","AppSecret", false); 
	net.youmi.android.offers.diyoffer.Ym_Class_DiyOfferWallManager.getInstance(context).ym_method_onAppLaunch(); 

其中，AppId和AppSecret分别为应用的发布ID和密钥，这两个值通过有米后台自动生成，通过在有米后台-`应用详细信息 <http://www.youmi.net/apps/view>`_  可以获得。

然后在应用退出的地方（如：onDestroy）中调用下面方法以释放资源::

	net.youmi.android.offers.diyoffer.Ym_Class_DiyOfferWallManager.getInstance(context).ym_method_onAppExit(); 

三、获取广告列表（重要）
--------------

3.1 数据模型
~~~~~~~~~~~~~~~~~~~~~~~~

3.1.1 单个广告摘要信息的数据模型
~~~~~~~~~~~~~~~~~~~~~~~~
Ym_Class_AppSummaryObject中集成了一条广告的摘要信息，通过使用Ym_Class_AppSummaryObject，您可以获取广告的摘要信息，然后以列表形式展示出来::

	import net.youmi.android.offers.diyoffer.Ym_Class_AppSummaryObject;
	...

	Ym_Class_AppSummaryObject appSummaryObject;
	int id=appSummaryObject.ym_method_getAdId();		// 获取广告id
	String adName = appSummaryObject.ym_method_getAppName();		// 获取app的名称
	String pn = appSummaryObject.ym_method_getPackageName();		// 获取app的包名
	int versionCode =appSummaryObject.ym_method_getVersionCode();		// 获取app的版本号
	String adIconUrl = appSummaryObject.ym_method_getIconUrl();		// 获取app的图标地址
	String adSize = appSummaryObject.ym_method_getAppSize();		// 获取app的大小
	int adStatus = appSummaryObject.ym_method_getAdTaskStatus();		// 获取广告的完成状态
	int dlStatus = appSummaryObject.ym_method_getAdDownloadStatus();		// 获取广告的下载状态
	int points = appSummaryObject.ym_method_getPoints();		// 获取app的积分（已完成状态下的广告积分返回值为0）	
	String pointsUnit =appSummaryObject.ym_method_getPointsUnit();		// 获取广告的积分单位
	String adtext = appSummaryObject.ym_method_getAdSlogan();		// 获取广告标语
	int actionType=appSummaryObject.getActionType();		// 获取广告的类型
	String steps =appSummaryObject.ym_method_getTaskSteps();		// 任务步骤流程指

注：

1、广告的完成状态有2种，对应的值分别为：
	
	<已完成>：net.youmi.android.offers.diyoffer.Ym_Class_AdTaskStatus.ALREADY_COMPLETE;
	
	<未完成>：net.youmi.android.offers.diyoffer.Ym_Class_AdTaskStatus.NOT_COMPLETE;
	
*其中：只有<未完成>状态下的广告才可以获取积分；<已完成>状态下的广告是不能获取积分的，同时，<已完成>状态下方法Ym_Class_AppSummaryObject.ym_method_getPoints()的返回值也为0*
	
2、广告的下载状态有3种，对应的值分别为：
	
	<未下载>：net.youmi.android.offers.diyoffer.Ym_Class_AdDownloadStatus.NOT_DOWNLOAD;
	
	<正在下载>：net.youmi.android.offers.diyoffer.Ym_Class_AdDownloadStatus.DOWNLOADING;
	
	<已经下载>：net.youmi.android.offers.diyoffer.Ym_Class_AdDownloadStatus.ALERADY_DOWNLOAN;
	
3、广告的类型有2种，对应的值分别为：
	
	<体验类型>：net.youmi.android.offers.diyoffer.Ym_Class_AdType.EXPERIENCE;

	<注册类型>：net.youmi.android.offers.diyoffer.Ym_Class_AdType.REGISTER;
	

3.1.2 广告列表数据模型
~~~~~~~~~~~~~~~~~~~~~~~~

Ym_Class_AppSummaryObjectList中包含了每个广告的摘要信息Ym_Class_AppSummaryObject，每次请求广告的时候都会返回这个列表数据模型，我们为这个列表数据模型提供以下几个方法::

	public class Ym_Class_AppSummaryObjectList {
		/**
		 * 获取指定索引的广告的摘要信息
		 */
		public Ym_Class_AppSummaryObject get(int index);
		/**
		 * 判断广告列表是否为空
		 */
		public boolean isEmpty();
		/**
		 * 获取广告列表的长度
		 */
		public int size();
		}

3.2 获取方式
~~~~~~~~~~~~~~~~~~~~~~~~

**获取积分墙列表数据有两种方式，一种为同步加载，一种为异步加载**  

1、同步加载方式(请注意在非UI线程中使用)::

	/**
	 * 获取积分墙列表数据
	 * @param pageIndex		请求页码(正整数，从1开始)
	 * @param requestType	 	请求类型
	 *      Ym_Class_DiyOfferWallManager.ym_param_REQUEST_ALL:	所有（默认值）
	 *      Ym_Class_DiyOfferWallManager.ym_param_REQUEST_GAME: 	只请求游戏广告
	 *      Ym_Class_DiyOfferWallManager.ym_param_REQUEST_APP: 	只请求应用广告
	 *      Ym_Class_DiyOfferWallManager.ym_param_REQUEST_SPECIAL_SORT: 	请求列表特殊排序，应用先于游戏显示
	 * @param withAdDownloadUrl 	 广告是否携带url下载地址（可用于实现广告列表页实现下载功能）
	 *      false:	不携带（默认值）
	 *      true:	携带
	 * @return
	 * 	Ym_Class_AppSummaryObjectList		广告摘要信息列表
	 */
	Ym_Class_DiyOfferWallManager.getInstance(Context context).ym_method_getOfferWallAdList(int pageIndex, int requestType, boolean withAdDownloadUrl);

*示例代码*::

	import net.youmi.android.offers.diyoffer.Ym_Class_AppSummaryObjectList;
	import net.youmi.android.offers.diyoffer.Ym_Class_DiyOfferWallManager;
	...

	// 请求第一页广告，广告类型不限，广告附带url下载地址
	new Thread(new Runnable() {
		 @Override
		 public void run() {
			 Ym_Class_AppSummaryObjectList data =
					 Ym_Class_DiyOfferWallManager.getInstance(this).ym_method_getOfferWallAdList(1, Ym_Class_DiyOfferWallManager.ym_param_REQUEST_ALL, true);
		 }
	}).start();

2、异步加载方式::

	/**
	 * 异步加载积分墙数据列表
	 * @param pageIndex	请求页码(正整数，从1开始)
	 * @param requestType	请求类型
	 *      Ym_Class_DiyOfferWallManager.ym_param_REQUEST_ALL:	所有（默认值）
	 *      Ym_Class_DiyOfferWallManager.ym_param_REQUEST_GAME:	只请求游戏广告
	 *      Ym_Class_DiyOfferWallManager.ym_param_REQUEST_APP:	只请求应用广告
	 *      Ym_Class_DiyOfferWallManager.ym_param_REQUEST_SPECIAL_SORT:	请求列表特殊排序，应用先于游戏显示
	 * @param withAdDownloadUrl 	 广告是否携带url下载地址（可用于实现广告列表页实现下载功能）
	 *      false:	不携带（默认值）
	 *      true:	携带
	 */
	Ym_Class_DiyOfferWallManager.getInstance(context).ym_method_loadOfferWallAdList(int pageIndex, int requestType, boolean withAdDownloadUrl,
			Ym_Class_AppSummaryDataInterface appSummaryDataInterface);

*示例代码*::

	import net.youmi.android.offers.diyoffer.Ym_Class_AppSummaryDataInterface;
	import net.youmi.android.offers.diyoffer.Ym_Class_AppSummaryObject;
	import net.youmi.android.offers.diyoffer.Ym_Class_AppSummaryObjectList;
	import net.youmi.android.offers.diyoffer.Ym_Class_DiyOfferWallManager;
	...

	/**
	 * 请求第一页广告，广告类型不限，广告不附带下载地址
	 */
	 
	 Ym_Class_DiyOfferWallManager.getInstance(this).ym_method_loadOfferWallAdList(1, Ym_Class_DiyOfferWallManager.ym_param_REQUEST_ALL, false,
			new Ym_Class_AppSummaryDataInterface() {

				/**
				 * 当成功获取积分墙列表数据的时候会回调这个方法（注意:本回调方法不在UI线程中执行，所以请不要在本接口中进行UI线程方面的操作）
				 */
				@Override
				public void ym_method_onLoadAppSumDataSuccess(Context context, Ym_Class_AppSummaryObjectList adList) {
					// TODO Auto-generated method stub
					for(int i=0; i<adList.size(); ++i){
						Log.d("test",adList.get(i).toString());
					}
				}

				/**
				 * 当获取积分墙数据失败的时候会回调这个方法（注意:本回调方法不在UI线程中执行，所以请不要在本接口中进行UI线程方面的操作）
				 */
				@Override
				public void ym_method_onLoadAppSumDataFailed() {
					// TODO Auto-generated method stub
					Log.d("test","没有获取到数据");
				}
			}
		);


四、获取广告的详细数据（重要）
--------------

4.1 数据模型
~~~~~~~~~~~~~~~~~~~~~~~~

Ym_Class_AppDetailObject中集成了一条广告的详细信息，通过Ym_Class_AppDetailObject，您可以获取广告的详细信息，然后展示广告的详情页::
	
	import net.youmi.android.offers.diyoffer.Ym_Class_AppDetailObject;
	...
	
	Ym_Class_AppDetailObject appDetailObject;
	int id=appDetailObject.ym_method_getAdId();	// 获取广告id
	String adName = appDetailObject.ym_method_getAppName();	// 获取app的名称
	String pn = appDetailObject.ym_method_getPackageName();	// 获取app的包名
	String adIconUrl = appDetailObject.ym_method_getIconUrl();	// 获取app的图标地址
	String [] ssUrls = appDetailObject.ym_method_getScreenShotUrls();	// 获取app的截图地址列表
	String size = appDetailObject.ym_method_getAppSize();	// 获取app的大小
	int adStatus = appDetailObject.ym_method_getAdTaskStatus();		// 获取广告的完成状态
	int dlStatus = appDetailObject.ym_method_getAdDownloadStatus();		// 获取广告的下载状态
	String appCat = appDetailObject.ym_method_getAppCategory();	// 获取app的类别
	int points = appDetailObject.ym_method_getPoints();	// 获取app的积分
	String versionName = appDetailObject.ym_method_getVersionName();	// 获取app的版本名
	int versionCode = appDetailObject.ym_method_getVersionCode();	// 获取app的版本号
	String adSlogan = appDetailObject.ym_method_getAdSlogan();	// 获取广告标语
	int actionType=appDetailObject.getActionType();	// 获取广告的类型
	String desc = appDetailObject.ym_method_getDescription();	// 获取app的详细描述
	String author = appDetailObject.ym_method_getAuthor();	// 获取该app的作者名
	String steps = appDetailObject.ym_method_getTaskSteps();	// 任务步骤流程指引

注：

1、广告的完成状态、下载状态以及广告的类型值请参考上述第三点：获取广告列表中的描述


4.2 获取方式
~~~~~~~~~~~~~~~~~~~~~~~~

**获取积分墙某个广告的详细数据有两种方式，一种为同步加载，一种为异步加载**

1、同步加载方式(请注意在非UI线程中使用)::

	import net.youmi.android.offers.diyoffer.Ym_Class_AppDetailObject;
	import net.youmi.android.offers.diyoffer.Ym_Class_DiyOfferWallManager;
	...

	/**
	 * 获取广告的详细信息（请注意不要在UI线程中直接使用）
	 * @param Ym_Class_AppSummaryObject				
	 * 		广告的摘要信息对象，广告的摘要信息对象请参考3.1节的描述
	 */
	Ym_Class_DiyOfferWallManager.getInstance(Context context).ym_method_getAppDetailData(Ym_Class_AppSummaryObject appSummaryObject);


*示例代码*::

	import net.youmi.android.offers.diyoffer.Ym_Class_AppDetailObject;
	import net.youmi.android.offers.diyoffer.Ym_Class_DiyOfferWallManager;
	...

	new Thread(new Runnable() {
			@Override
			public void run() {
				// 这里传入广告的摘要信息数据模型对象，以获取广告的详细数据
				Ym_Class_AppDetailObject data  = Ym_Class_DiyOfferWallManager.getInstance(this).ym_method_getAppDetailData(appSummaryObject);
		 }
	}).start();
	
2、异步加载方式::

	/**
	 * 获取广告的详细信息
	 * @param appSumObject				
	 * 		要加载的广告的摘要信息对象
	 * @param appDetailDataInterface
	 * 		回调接口，当返回数据结果时回调本接口
	 */
	Ym_Class_DiyOfferWallManager.getInstance(Context context).ym_method_loadAppDetailData(Ym_Class_AppSummaryObject appSummaryObject, 
			Ym_Class_AppDetailDataInterface appDetailDataInterface);

*示例代码*::

	import net.youmi.android.offers.diyoffer.Ym_Class_AppSummaryObject;
	import net.youmi.android.offers.diyoffer.Ym_Class_AppDetailObject;
	import net.youmi.android.offers.diyoffer.Ym_Class_DiyOfferWallManager;
	import net.youmi.android.offers.diyoffer.Ym_Class_AppDetailDataInterface;
	...
	/**
	 * 异步加载积分墙某个广告的详细数据
	 */
	Ym_Class_DiyOfferWallManager.getInstance(this).ym_method_loadAppDetailData(appSummaryObject, 
			new Ym_Class_AppDetailDataInterface() {
		/**
		 * 当成功加载到数据的时候，会回调本方法（注意:本回调方法不在UI线程中执行，所以请不要在本接口中进行UI线程方面的操作）
		 */
		@Override
		public void ym_method_onLoadAppDetailDataSuccess(Context context, Ym_Class_AppDetailObject appDetailObject) {
			Log.d("test",appDetailObject.toString());
		}
		/**
		 * 当加载数据失败的时候，会回调本方法（注意:本回调方法不在UI线程中执行，所以请不要在本接口中进行UI线程方面的操作）
		 */
		@Override
		public void ym_method_onLoadAppDetailDataFailed() {
			Log.d("test","没有获取到数据");
		}
	});

	
五、下载和打开应用（重要）
--------------
通过调用下面方法即可下载（或打开）广告，如果该广告的完成状态为<未完成>，则可获取积分结算

**请注意：打开广告务必调用本方法，否则可能无法获取积分和结算**::

	// 1、传入Ym_Class_AppSummaryObject对象
	Ym_Class_DiyOfferWallManager.getInstance(Context context).ym_method_openOrDownloadApp(Ym_Class_AppSummaryObject appSummaryObject);
	// 2、传入Ym_Class_AppDetailObject对象
	Ym_Class_DiyOfferWallManager.getInstance(Context context).ym_method_openOrDownloadApp(Ym_Class_AppDetailObject appDetailObject);

	
六、监听应用的下载和安装（可选）
--------------
app下载安装监听器适用于当app下载安装状态改变时通知UI界面进行更新显示，比如下载进度的更新时UI界面应该显示进度条，当下载成功时隐藏进度条并提示用户安装等等，这些一般都只适用于UI交互。

通过实现net.youmi.android.offers.diyoffer.DiyAppNotify这个接口，并且在界面初始化后向net.youmi.android.offers.diyoffer.Ym_Class_DiyOfferWallManager的``registerListener方法注册监听即可让界面随时获得app的下载安装状态，在界面销毁时，请务必调用removeListener方法注销监听。

DiyAppNotify的定义::

    /**
     * app下载安装监听器 
     *
     */
    public interface DiyAppNotify {
    /**
      * 下载进度变更通知，在UI线程中执行。
      * @param id
      * @param contentLength
      * @param completeLength
      * @param percent
      * @param speedBytesPerS
      */
    public void onDownloadProgressUpdate(int id,long contentLength, long completeLength, int percent,long speedBytesPerS); 
    
    /**
      * 下载成功通知，在UI线程中执行。
      * @param id
      */
    public void onDownloadSuccess(int id);
    
    /**
      * 下载失败通知，在UI线程中执行。
      * @param id
      */
    public void onDownloadFailed(int id);
    
    /**
      * 安装成功通知，在UI线程中执行。
      * @param appObject
      */
    public void onInstallSuccess(int id);
    }

如果需要判断两个app是否为同一个，则可以通过获取它的广告id进行比较即可。

Ym_Class_DiyOfferWallManager关于下载安装监听器的调用::

    /**
     *注册监听器
     */
    public void registerListener(DiyAppNotify listener);

    /**
      *注释监听器
      */
    public void removeListener(DiyAppNotify listener);


七、其他功能（可选）
--------------

7.1 设置请求广告的数量
~~~~~~~~~~~~~~~~~~~~~~~~
通过调用下面方法即可设置每次请求广告列表的长度，如果需要使用本方法，请在调用获取广告列表的方法之前调用本方法::

	Ym_Class_DiyOfferWallManager.getInstance(Context context).ym_method_setRequestCount(int count);

7.2 签到功能
~~~~~~~~~~~~~~~~~~~~~~~~
通过调用下面方法可以为<已完成>状态的广告进行签到::

	// 1、传入Ym_Class_AppSummaryObject对象
	Ym_Class_DiyOfferWallManager.getInstance(Context context).ym_method_sendSignInActionType(Ym_Class_AppSummaryObject appSummaryObject);
	// 2、传入Ym_Class_AppDetailObject对象
	Ym_Class_DiyOfferWallManager.getInstance(Context context).ym_method_sendSignInActionType(Ym_Class_AppDetailObject appDetailObject);
	
