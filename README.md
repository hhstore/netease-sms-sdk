# netease-sms-sdk
网易云信-短信验证码服务 API 对接. Python3版本.



## 功能说明:

- 基于 python3 + requests 实现.
- 网易官方未提供Python 版本的 SDK 包, 只提供接口和参数说明.
- 且官方文档给出的示例, 有错误.(校验有坑, 传入参数有坑)
- 全部接口都已测试, 如果使用异常, 仔细对照一下传参示例.



### 使用说明:

- 网易云信官网, 注册一个测试帐号, 默认送几十条免费测试短信.
- 拿到 APP_KEY 和 APP_SECRET, 传入模块.
- 云信上, 需要配置一下 模板短信的模板, 需人工审核.
- 对应的 ID.
- 代码里的 KEY, ID, 都作了错误处理, 非真实有效值, 请注意替换.




## 官方文档:

- [官方文档](http://dev.netease.im/docs?doc=server_sms)
- [接口校验](http://dev.netease.im/docs?doc=server&#接口概述)




