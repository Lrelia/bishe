.. Android 积分墙高级功能

:tocdepth: 2

积分墙高级功能
==============

`返回上一层 <javascript:history.back();>`_

一、刷新积分余额 UI 显示
------------------------

----

| 如果您在 UI 上显示用户的积分账户余额，用户的积分余额可能会因为各种可能的原因导致余额变动(增减)，
| 这时候您需要刷新 UI 上的显示值，可以通过以下方法实现积分余额在 UI 上的自动刷新。

1) 让 UI 相关的类（可以是 Activity 或 View 相关的类）implements net.youmi.android.offers.Ym_Class_PointsChangeNotify 这个接口。

   接口定义如下：

.. code-block:: java

    package net.youmi.android.offers;
    /**
     *  积分余额增减变动监听器
     *  @author youmi
     */
    public interface Ym_Class_PointsChangeNotify {
        /**
         *  积分余额增减变动通知,该回调在 UI 线程中进行，可直接与 UI 进行交互
         *  @param pointsBalance 当前积分余额
         */
        public void ym_method_onPointBalanceChange(int pointsBalance);
    }


2) 在 UI 初始化后调用：

.. code-block:: java

    import net.youmi.android.offers.Ym_Class_PointsManager;
    ...
    Ym_Class_PointsManager.getInstance(this).ym_method_registerNotify(notifyObject);


3) 在 UI 销毁前调用以下代码释放 Notify 引用，以防止造成内存漏洞：

.. code-block:: java

    import net.youmi.android.offers.Ym_Class_PointsManager;
    ...
    Ym_Class_PointsManager.getInstance(this).ym_method_unRegisterNotify(notifyObject);


二、通过 SDK 获取积分订单
-------------------------

----

用户完成了一次积分任务并在有米服务器成功结算后，可以通过以下方法让 SDK 回调通知应用用户所完成的订单：

1. 第一步，您需要定义一个 MyPointsReceiver 类（名字可以随意），它必须继承自 net.youmi.android.offers.Ym_Class_PointsReceiver：

*示例代码* ：

.. code-block:: java

    import android.content.Context;
    import net.youmi.android.offers.Ym_Class_EarnPointsOrderList;
    import net.youmi.android.offers.Ym_Class_PointsReceiver;

    public class MyPointsReceiver extends Ym_Class_PointsReceiver {
        @Override
        protected void ym_method_onEarnPoints(Context context, Ym_Class_EarnPointsOrderList list) {
            // 当 SDK 获取到用户赚取积分的订单时，会第一时间调用该方法通知您。
            // 参数 Ym_Class_EarnPointsOrderList 是一个积分订单列表，您可以在这里处理积分详细订单。
        }

        @Override
        protected void ym_method_onViewPoints(Context context) {
            // 这里是个有趣的小功能，当用户赚取积分之后，积分墙 SDK 会在通知栏上显示一条获取积分的提示，如果用户点击了这个通知，该函数会被调用。
            // 这时候您可以在这里实现一个跳转，让用户跳转到您设计好的一个积分账户余额页面（如"我的账户"之类的 Activity）。
            // 该操作是可选的，如果需要关闭通知栏积分提示，请调用 PointsManager.getInstance(context).setEnableEarnPointsNotification(false)
        }
    }


2. 第二步，您需要在 ``AndroidManifest.xml`` 上配置刚刚定义的 MyPointsReceiver：

*示例代码* ：

.. code-block:: xml

    <receiver
        android:name="MyPointsReceiver"
        android:exported="false" >
        <intent-filter>
            <action android:name="ep_请替换为您的AppID" />
            <action android:name="vp_请替换为您的AppID" />
        </intent-filter>
    </receiver>

.. Attention::

    这里有一个很关键的细节，您必须为 MyPointsReceiver 配置两个 Action，Action 的名字分别是以 **“ep\_”** 和 **“vp\_”** 开头，以您的应用的 AppID 结尾的字符串。（AppID 是从有米主站上申请的应用ID，16个字符，所以 Action 的总长度应该是19个字符）


附录：积分订单类定义
~~~~~~~~~~~~~~~~~~~~

Ym_Class_EarnPointsOrderList
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: java

    package net.youmi.android.offers;

    /**
     *  积分订单列表
     *
     */
    public class Ym_Class_EarnPointsOrderList {
        /**
         *  获取服务器上设置积分单位名称
         */
        public String getCurrencyName();

        /**
         *  根据 index 获取订单详情（EarnPointsOrderInfo）
         */
        public Ym_Class_EarnPointsOrderInfo get(int index);

        /**
         *  判断列表是否为空
         */
        public boolean isEmpty();

        /**
         * 获取列表项数量
         */
        public int size();
    }

Ym_Class_EarnPointsOrderInfo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: java

    package net.youmi.android.offers;

    /**
     *  赚取积分的订单
     */
    public final class Ym_Class_EarnPointsOrderInfo {
        /**
         *  获取订单号(具有唯一性)
         */
        public String getOrderID();

        /**
         *  获取渠道号，这里指在 AndroidManifest.xml 上配置的有米渠道号，详见文档
         */
        public int getChannelId();

        /**
         *  获取开发者自定义用户唯一标识，该值通过 OffersManager 设置
         */
        public String getCustomUserID();

        /**
         *  获取积分订单的状态：
         *      1. 表示开发者获得了收入并且用户获得了积分。
         *      2. 表示开发者没有获得收入但用户获得了积分（未通过审核以及测试模式下结算无效等情况）。
         */
        public int getStatus()

        /**
         *  本次获取积分的描述语，如“成功安装《--》获取了100金币”
         */
        public String getMessage();

        /**
         *  本次获得的积分
         */
        public int getPoints();

        /**
         *  本次获得积分的结算时间
         */
        public long getSettlingTime();
    }


三、通过服务器获取积分订单
--------------------------

----

.. caution::

    **注意：** 如果您使用服务器回调，请登录有米后台，进入到 `广告设置 <https://www.youmi.net/apps/setting>`_ - 积分广告基本设置 - 余额显示设置，关闭该功能！

务必在调用积分墙的任意接口之前调用以下接口设置用户的标识，该标识最终通过订单回调到您的服务器：

.. code-block:: java

    import net.youmi.android.offers.Ym_Class_OffersManager;
    ...
    Ym_Class_OffersManager.getInstance(context).ym_method_setCustomUserId("your_userid");

| 用户完成了一次积分任务并在有米服务器成功结算后，也可以通过服务器通讯的方式，由有米服务器向您的服务器回调用户完成的订单，
| 详情请查看 `有米 Android 积分墙积分订单服务器回调协议 <http://wiki.youmi.net/Youmi_android_offers_order_callback_protocol>`_ 。

.. error::

    如果使用了服务器订单回调，则上文所述的“通过 SDK 获取积分订单”将不可用，即 SDK 将不会通知应用订单到账。同时 SDK 原有的积分管理功能也将被禁用，所有积分流程只能通过服务器实现，可以极大地提高积分 **安全性** 。


四、验证积分墙配置是否正确
--------------------------

----

嵌入 SDK 时如果配置有误有可能会导致没有收入或者获取不到积分，在完成文档中的配置之后可以通过调用以下接口查看配置是否正确：

.. code-block:: java

    import net.youmi.android.offers.Ym_Class_OffersManager;
    ...	

    // 积分墙配置检查（没有使用“通过 SDK 获取积分订单”功能）：
    boolean isSuccess = Ym_Class_OffersManager.getInstance(context).ym_method_checkOffersAdConfig();

    // 积分墙配置检查（使用“通过 SDK 获取积分订单”功能）：
    boolean isSuccess = Ym_Class_OffersManager.getInstance(context).ym_method_checkOffersAdConfig(true);

.. Attention::

    该接口调用的结果如果返回 true，则说明配置正确，可以删掉该调用。如果返回 false，则需要查看 logcat 的相关输出，里面有指出哪些相关的配置错误内容。


五、关闭有米的 Debug Log
------------------------

----

如果需要关闭有米广告 SDK 的 debug log，请调用以下代码来关闭 SDK 的 log 输出。

*代码示例：*

.. code-block:: java

    import net.youmi.android.Ym_Class_AdManager;
    ...
    Ym_Class_AdManager.getInstance(this).ym_method_setEnableDebugLog(false);

.. tip::

    **注意：** 上传到有米主站进行审核时务必开启 debug log，这样才能保证通过审核。
