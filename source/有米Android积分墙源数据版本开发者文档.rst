有米Android积分墙源数据版本开发者文档
===========================

一、基本配置 
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

	<activity
		android:name="net.youmi.android.Ym_Class_AdBrowser"
		android:configChanges="keyboard|keyboardHidden|orientation"            
		android:theme="@android:style/Theme.Light.NoTitleBar" >
	</activity>
	<service
		android:name="net.youmi.android.Ym_Class_AdService"
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

二、初始化及相关工作
--------------
请务必在应用第一个Activity(启动的第一个类)的onCreate中调用以下代码::

	net.youmi.android.Ym_Class_AdManager.getInstance(this).init("AppId","AppSecret", false); 
	net.youmi.android.offers.Ym_Class_OffersManager.getInstance(this).ym_method_onAppLaunch(); 

其中，AppId和AppSecret分别为应用的发布ID和密钥，这两个值通过有米后台自动生成，通过在有米后台-`应用详细信息 <http://www.youmi.net/apps/view>`_  可以获得。

然后在应用退出的地方（如：onDestroy）中调用下面方法以释放资源::

	net.youmi.android.offers.Ym_Class_OffersManager.getInstance(this).ym_method_onAppExit(); 

三、获取广告列表
--------------

3.1 数据模型
~~~~~~~~~~~~~~~~~~~~~~~~

Ym_Class_AppSummaryObject中集成了一条广告的摘要信息，通过使用Ym_Class_AppSummaryObject，您可以获取广告的摘要信息，然后以列表形式展示出来::

	import net.youmi.android.offers.diyoffer.Ym_Class_AppSummaryObject;
	...

	Ym_Class_AppSummaryObject appSummaryObject;
	int id=appSummaryObject.getId();		// 获取id
	String adName = appSummaryObject.ym_method_getAppName();		// 获取app的名称
	String pn = appSummaryObject.ym_method_getPackageName();		// 获取app的包名
	String adIconUrl = appSummaryObject.ym_method_getIconUrl();		// 获取app的图标地址
	String adSize = appSummaryObject.ym_method_getAppSize();		// 获取app的大小
	int is = appSummaryObject.ym_method_getInstallStatus();		// 获取app的安装状态
	int points = appSummaryObject.ym_method_getPoints();		// 获取app的积分	
	int versionCode =appSummaryObject.ym_method_getVersionCode();		// 获取app的版本号(可用于升级)
	String adtext = appSummaryObject.ym_method_getAdSlogan();		// 获取广告语
	int actionType=appSummaryObject.getActionType();		// 获取广告的类型，其中，3为安装试用类广告，5为注册类广告，其他值请忽略。
	int exp = appSummaryObject.ym_method_getExpirySecond();		// 广告有效期，超过多少秒该广告会失效
	String brief = appSummaryObject.ym_method_getTaskBrief();		// 任务提示语（可用于在列表展示页中说明）
	String steps =appSummaryObject.ym_method_getTaskSteps();		// 任务步骤流程指引（可用于在广告详情页中说明）

注：

1、因为某些字段的数据还在录入中，所以可能暂时无法获取到数据，暂受影响的数据有：app的大小、任务提示语、任务步骤流程（当没有获取到数据的时候返回""）。

2、app的状态有4种，对应的值分别为：

	<已完成>：ym_param_ALREADY_DONE；
	
	<未安装>：ym_param_NOT_INSTALL；
	
	<正在下载>：ym_param_DOWNLOADING；
	
	<已经下载>：ym_param_ALERADY_DOWNLOAN。

其中：<已完成>、<未安装>状态下对应的积分关系如下：

	<已完成>状态下获取到的积分为0。
	
	<未安装>状态下获取到的积分为该应用所提供的积分。
	
app的状态定义于net.youmi.android.offers.diyoffer.Ym_Class_AppStatus类中：::

    public class Ym_Class_AppStatus{

	/**
	 * 安装任务可进行，此时该任务可获得的积分数大于0。可提示:"未安装"
	 */
	public final static int ym_param_NOT_INSTALL = 1;
	
	
	/**
	 * 安装任务已结束，此时该任务可获得的积分数为0 。可提示:"已完成"
	 */
	public final static int ym_param_ALREADY_DONE = 3;
	
	/**
	 * 正在下载，该任务为可安装任务，并且正在下载中。可提示:"正在下载"
	 */
	public final static int ym_param_DOWNLOADING=4;
	
	/**
	 * 已经下载，待安装：该任务为可安装任务，已经完成安装包的下载。可提示:"已经下载成功，请安装!"
	 */
	public final static int ym_param_ALREADY_DOWNLOAD=5;

   }

*示例代码*::

	import net.youmi.android.offers.diyoffer.Ym_Class_AppStatus;
	import net.youmi.android.offers.diyoffer.Ym_Class_AppSummaryObject;
	...
	
	Ym_Class_AppSummaryObject appSummaryObject;
	int points = appSummaryObject.ym_method_getPoints();		// 获取app的积分	
	int appStatus = appSummaryObject.ym_method_getInstallStatus();		// 获取app的安装状态

3.2 获取方式
~~~~~~~~~~~~~~~~~~~~~~~~

**获取积分墙列表数据有两种方式，一种为同步加载，一种为异步加载**  

1、同步加载方式(注意在非UI线程中使用)::

	import net.youmi.android.offers.diyoffer.Ym_Class_AppSummaryObject;
	import net.youmi.android.offers.diyoffer.Ym_Class_DiyOfferWallManager;
	...
	/**
	 * 同步加载积分墙数据列表（请注意不要在UI线程中直接使用）
	 * @param pageIndex	请求页码(正整数，从1开始)
	 * @param adNumPerPage	每页的广告数量（正整数，从1开始）
	 * @param requestType	请求类型
	 *      Ym_Class_DiyOfferWallManager.ym_param_REQUEST_ALL: 所有（默认值）
	 *      Ym_Class_DiyOfferWallManager.ym_param_REQUEST_GAME: 只请求游戏广告
	 *      Ym_Class_DiyOfferWallManager.ym_param_REQUEST_APP: 只请求应用广告
	 *      Ym_Class_DiyOfferWallManager.ym_param_REQUEST_SPECIAL_SORT: 请求列表特殊排序，应用先于游戏显示
	 * @param Ym_Class_AppSummaryDataInterface	回调接口，当返回数据结果时回调本接口
	 */
	Ym_Class_AppSummaryObjectList data = Ym_Class_DiyOfferWallManager.getInstance(this).ym_method_getOfferWallAdList(int pageIndex, int adNumPerPage, int requestType);

2、异步加载方式::

	/**
	 * 异步加载积分墙数据列表
	 * @param pageIndex	请求页码(正整数，从1开始)
	 * @param adNumPerPage	每页的广告数量（正整数，从1开始）
	 * @param requestType	请求类型
	 *      Ym_Class_DiyOfferWallManager.ym_param_REQUEST_ALL: 所有（默认值）
	 *      Ym_Class_DiyOfferWallManager.ym_param_REQUEST_GAME: 只请求游戏广告
	 *      Ym_Class_DiyOfferWallManager.ym_param_REQUEST_APP: 只请求应用广告
	 *      Ym_Class_DiyOfferWallManager.ym_param_REQUEST_SPECIAL_SORT: 请求列表特殊排序，应用先于游戏显示
	 * @param Ym_Class_AppSummaryDataInterface	回调接口，当返回数据结果时回调本接口
	 */
	Ym_Class_DiyOfferWallManager.getInstance(context).ym_method_loadOfferWallAdList(int pageIndex, int adNumPerPage, 
			int requestType, Ym_Class_AppSummaryDataInterface appSummaryDataInterface); 

*示例代码*::

	import net.youmi.android.offers.diyoffer.Ym_Class_AppSummaryDataInterface;
	import net.youmi.android.offers.diyoffer.Ym_Class_AppSummaryObject;
	import net.youmi.android.offers.diyoffer.Ym_Class_AppSummaryObjectList;
	import net.youmi.android.offers.diyoffer.Ym_Class_DiyOfferWallManager;
	...

	/**
	 * 获取第一页10条类型不限的广告
	 */
	Ym_Class_DiyOfferWallManager.getInstance(this).ym_method_loadOfferWallAdList(1, 10, 
			Ym_Class_DiyOfferWallManager.ym_param_REQUEST_ALL, new Ym_Class_AppSummaryDataInterface() {
		
		/**
		 * 当成功获取到积分墙列表数据的时候会回调这个方法（注意:本接口不在UI线程中执行，所以请不要在本接口中进行UI线程方面的操作）
		 */
		@Override
		public void ym_method_onLoadAppSumDataSuccess(Context context, Ym_Class_AppSummaryObjectList adList) {
			for(int i=0; i<adList.size(); i++){
				Log.d("test",adList.get(i).toString());
			}
		}

		/**
		 * 当获取到积分墙数据失败的时候会回调这个接口（注意:本接口不在UI线程中执行，所以请不要在本接口中进行UI线程方面的操作）
		 */
		@Override
		public void ym_method_onLoadAppSumDataFailed() { 
			Log.d("test","没有获取到数据");
		}
	});


四、获取广告的详细数据
--------------

4.1 数据模型
~~~~~~~~~~~~~~~~~~~~~~~~

Ym_Class_AppDetailObject中集成了一条广告的详细信息，通过Ym_Class_AppDetailObject，您可以获取广告的详细信息，然后展示广告的详情页::
	
	import net.youmi.android.offers.diyoffer.Ym_Class_AppDetailObject;
	...
	
	Ym_Class_AppDetailObject appDetailObject;
	int id=appDetailObject.getId();		// 获取id
	String adName = appDetailObject.ym_method_getAppName();		// 获取app的名称
	String pn = appDetailObject.ym_method_getPackageName();		// 获取app的包名
	String adIconUrl = appDetailObject.ym_method_getIconUrl();		// 获取app的图标地址
	String size = appDetailObject.ym_method_getAppSize();		// 获取app的大小
	int is = appDetailObject.ym_method_getInstallStatus();		// 获取app的安装状态
	int points = appDetailObject.ym_method_getPoints();		// 获取app的积分
	String appCat = appDetailObject.ym_method_getAppCategory();		// 获取app的类别
	String versionName = appDetailObject.ym_method_getVersionName();		// 获取app的版本名(可用于展示)
	int versionCode = appDetailObject.ym_method_getVersionCode();		// 获取app的版本号(可用于升级)
	String adSlogan = appDetailObject.ym_method_getAdSlogan();		// 获取广告语
	int actionType=appDetailObject.getActionType();		// 获取广告的类型，其中，3为安装试用类广告，5为注册类广告，其他值请忽略。
	String desc = appDetailObject.ym_method_getDescription();		// 获取app的详细描述
	String [] ssUrls = appDetailObject.ym_method_getScreenShotUrls();		// 获取app的截图地址列表
	String author = appDetailObject.ym_method_getAuthor();		// 获取该app的作者名
	String brief = appDetailObject.ym_method_getTaskBrief();		// 任务提示语
	String steps = appDetailObject.ym_method_getTaskSteps();		// 任务步骤流程指引

注：

1、因为某些字段的数据还在录入中，所以可能暂时无法获取到数据，暂受影响的数据有：任务提示语、任务步骤流程（当没有获取到数据的时候返回""）。  

2、应用状态和积分的关系请参考上述第三点：获取广告列表


4.2 获取方式
~~~~~~~~~~~~~~~~~~~~~~~~

**获取积分墙某个广告的详细数据有两种方式，一种为同步加载，一种为异步加载**

1、同步加载方式(注意在非UI线程中使用)::

	import net.youmi.android.offers.diyoffer.Ym_Class_AppDetailObject;
	import net.youmi.android.offers.diyoffer.Ym_Class_DiyOfferWallManager;
	...

	/**
	 * 同步加载积分墙某个广告的详细数据（请注意不要在UI线程中直接使用）
	 * @param Ym_Class_AppSummaryObject				
	 * 		要加载的app摘要信息对象
	 */
	Ym_Class_AppDetailObject data = Ym_Class_DiyOfferWallManager.getInstance(this).ym_method_getAppDetailData(Ym_Class_AppSummaryObject appSumObject);

2、异步加载方式::

	/**
	 * 获取app的详细数据
	 * @param appSumObject				
	 * 		要加载的app摘要信息对象
	 * @param appDetailDataInterface
	 * 		回调接口，当返回数据结果时回调本接口
	 */
	Ym_Class_DiyOfferWallManager.getInstance(context).ym_method_loadAppDetailData(Ym_Class_AppSummaryObject appSumObject, 
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
	Ym_Class_DiyOfferWallManager.getInstance(this).ym_method_loadAppDetailData(Ym_Class_AppSummaryObject appSumObject, 
			new Ym_Class_AppDetailDataInterface() {
		/**
		 * 当成功加载到数据的时候，会回调本接口（注意:本接口不在UI线程中执行，所以请不要在本接口中进行UI线程方面的操作）
		 */
		@Override
		public void ym_method_onLoadAppDetailDataSuccess(Context context, Ym_Class_AppDetailObject appDetailObject) {
			Log.d("test",appDetailObject.toString());
		}
		/**
		 * 当加载数据失败的时候，会回调本接口（注意:本接口不在UI线程中执行，所以请不要在本接口中进行UI线程方面的操作）
		 */
		@Override
		public void ym_method_onLoadAppDetailDataFailed() {
			Log.d("test","没有获取到数据");
		}
	});


五、下载应用
--------------
通过调用下面方法即可下载app，如果app的安装状态为<未安装>，则可获取积分结算::

	// 传入Ym_Class_AppDetailObject对象即可
	Ym_Class_DiyOfferWallManager.getInstance(this).ym_method_downloadApp(appDetailObject);

六、监听应用的下载和安装
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

Ym_Class_DiyOfferWallManager关于下载安装监听器的调用::

    /**
     *注册监听器
     */
    public void registerListener(DiyAppNotify listener);

    /**
      *注释监听器
      */
    public void removeListener(DiyAppNotify listener);

如果需要判断两个app是否为同一个，则可以通过获取它的id进行比较即可。

