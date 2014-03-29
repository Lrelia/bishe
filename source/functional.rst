.. Android SDK 使用工具

:tocdepth: 3


SDK 实用工具
============

`返回上一层 <javascript:history.back();>`_


    SDK 实用功能提供了检查更新和在线配置等功能，可以为您提供便捷的实用工具。


一、检查更新接口
----------------

----

| 有米广告 SDK 提供应用版本检查更新接口，您可以在应用中调用提示用户升级。
| 通过在 `「有米主站」 <https://www.youmi.net>`_ 上传应用的新版本通过审核后，使用有米广告 SDK 的应用版本检查更新接口就可以获得更新信息，
| 它包括更新提示和下载地址，这样您可以进行下一步的操作，如向用户提示更新以及下载安装新版本。

*接口：*

.. code-block:: java

    import net.youmi.android.Ym_Class_AdManager
    import net.youmi.android.dev.Ym_Class_AppUpdateInfo
    import net.youmi.android.dev.Ym_Class_CheckAppUpdateCallBack;

    // 通过调用 Ym_Class_AdManager 的 ym_method_syncCheckAppUpdate 或 ym_method_asyncCheckAppUpdate 接口即可检查更新。
    // 返回值 AppUpdateInfo 包含了更新提示以及下载地址，如果结果为 null 则表示当前已经是最新版本，无需下一步操作

    // 1. 同步调用方法：
    Ym_Class_AppUpdateInfo updateInfo=Ym_Class_AdManager.getInstance(this).ym_method_syncCheckAppUpdate();
    // 注意，此方法务必在非 UI 线程调用，否则有可能不成功。

    // 2. 异步调用方法：
    Ym_Class_AdManager.getInstance(this).ym_method_asyncCheckAppUpdate(callback);
    // 注意，此方法可以在任意线程中调用。

    //当 updateInfo 不为 null 时，请自行处理提示及下载安装流程。


*示例：* （同步接口，必须在非 UI 线程中调用，示例使用了 AsyncTask）

.. code-block:: java

    import net.youmi.android.Ym_Class_AdManager;
    import net.youmi.android.dev.Ym_Class_AppUpdateInfo;
    import android.app.AlertDialog;
    import android.content.Context;
    import android.content.DialogInterface;
    import android.content.Intent;
    import android.net.Uri;
    import android.os.AsyncTask;

    /**
     *  这里示例一个调用更新应用接口的工具类，由开发者自定义，继承自 AsyncTask
     */
    public class UpdateHelper extends AsyncTask<Void, Void, AppUpdateInfo> {
        private Context mContext;
        public UpdateHelper(Context context) {
            mContext = context;
        }

        @Override
        protected AppUpdateInfo doInBackground(Void... params) {
            try {
                // 在 doInBackground 中调用 Ym_Class_AdManager 的 ym_method_checkAppUpdate 即可从有米服务器获得应用更新信息。
                return Ym_Class_AdManager.getInstance(mContext).ym_method_syncCheckAppUpdate();
                // 此方法务必在非 UI 线程调用，否则有可能不成功。
            }
            catch (Throwable e) {
                // TODO: handle exception
                e.printStackTrace();
            }
            return null;
        }

        @Override
        protected void onPostExecute(Ym_Class_AppUpdateInfo result) {
            super.onPostExecute(result);
            try {
                if (result == null || result.getUrl() == null) {
                    // 如果 Ym_Class_AppUpdateInfo 为 null 或它的 url 属性为 null，则可以判断为没有新版本。
                    Toast.makeText(this, "当前版本已经是最新版", Toast.LENGTH_SHORT).show();
                    return;
                }

                // 这里简单示例使用一个对话框来显示更新信息
                new AlertDialog.Builder(mContext)
                    .setTitle("发现新版本")
                    .setMessage(result.getUpdateTips()) // 这里是版本更新信息
                    .setNegativeButton("马上升级",
                        new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                Intent intent = new Intent( Intent.ACTION_VIEW, Uri.parse(result.getUrl()) );
                                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                                mContext.startActivity(intent);
                                // ps：这里示例点击“马上升级”按钮之后简单地调用系统浏览器进行新版本的下载，
                                // 但强烈建议开发者实现自己的下载管理流程，这样可以获得更好的用户体验。
                            }
                    })
                    .setPositiveButton("下次再说",
                        new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                dialog.cancel();
                            }
                    }).create().show();
            }
            catch (Throwable e) {
                e.printStackTrace();
            }
        }
    }


*示例：* （异步接口，可在任意线程使用）

.. code-block:: java

    import net.youmi.android.Ym_Class_AdManager;
    import net.youmi.android.dev.Ym_Class_AppUpdateInfo;
    import net.youmi.android.dev.Ym_Class_CheckAppUpdateCallBack;
    import android.content.Context;
    import android.app.Activity;
    import android.content.Intent;
    import android.net.Uri;

    /**
     *  这里示例一个Activity调用
     *
     */
    public class UpdateActivity extends Activity implements CheckAppUpdateCallBack {
        @Override
        protected void onCreate(Bundle savedInstanceState) {
            // 调用检查更新接口，这里可以在 UI 线程调用，也可以在非 UI 线程调用。
            Ym_Class_AdManager.getInstance(this).ym_method_asyncCheckAppUpdate(this);
        }

        @Override
        public void onCheckAppUpdateFinish(Ym_Class_AppUpdateInfo updateInfo) {
            // 检查更新回调，注意，这里是在 UI 线程回调的，因此您可以直接与 UI 交互，但不可以进行长时间的操作（如在这里访问网络是不允许的）
            if (updateInfo == null) {
                // 当前已经是最新版本
            }
            else {
                // 有更新信息
            }
        }
    }



二、在线参数
------------

----

1) 在线参数介绍
~~~~~~~~~~~~~~~

在线参数是有米平台推出的新服务，可以让开发者动态修改应用中的配置项，如欢迎语、道具价格、广告开关等等。它以 Key-Value 的形式使用。


2) 使用在线参数
~~~~~~~~~~~~~~~

开发者可以在 `「有米主站」 <https://www.youmi.net>`_  开发者面板的应用详情里面设置指定应用的在线参数，然后在代码中调用它。

*示例代码：*

.. code-block:: java

    import net.youmi.android.Ym_Class_AdManager;
    import net.youmi.android.dev.Ym_Class_OnlineConfigCallBack; // 异步回调
    ...

    String mykey = "mycustomkey";  // key
    String defaultValue = null;    // 默认的 value，当获取不到在线参数时，会返回该值

    // 1. 同步调用方法，务必在非 UI 线程中调用，否则可能会失败。
    String value = Ym_Class_AdManager.getInstance(context).ym_method_syncGetOnlineConfig(key, defaultValue);

    // 2. 异步调用（可在任意线程中调用）
    Ym_Class_AdManager.getInstance(this).ym_method_asyncGetOnlineConfig(mykey, new Ym_Class_OnlineConfigCallBack() {
        @Override
        public void ym_method_onGetOnlineConfigSuccessful(String key, String value) {
            // TODO Auto-generated method stub
            // 获取在线参数成功
        }

        @Override
        public void ym_method_onGetOnlineConfigFailed(String key) {
            // TODO Auto-generated method stub
            // 获取在线参数失败，可能原因有：键值未设置或为空、网络异常、服务器异常
        }
    });
    ...

.. Attention::

    在线配置服务缓存具有一定的延时，因此在开发者控制面板上更改的配置项客户端可能需要一定的时间才能响应更新。



三、用户数据统计功能
--------------------

----

1) 用户数据统计功能介绍
~~~~~~~~~~~~~~~~~~~~~~~

用户数据统计功能是有米平台 **Android SDK v4.08** 之后推出的一个新功能。

开启这个功能，开发者可以在后台查看开发者应用的启动用户数、新增用户数、活跃用户数。


2) 使用方式
~~~~~~~~~~~

通过调用下面方法可以开启用户数据统计服务，本方法会统计应用的启动用户数，新增用户数，活跃用户数，开发者可以通过开发者后台查看数据

.. code-block:: java

    // 开启用户数据统计服务,默认不开启，传入 false 值也不开启，只有传入 true 才会调用
    Ym_Class_AdManager.getInstance(Context context).ym_method_setUserDataCollect(true);
