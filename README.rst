monitor: 对设备进行监控采集
========================

总览
----

将设备如空调，温湿度等通过串口接入PC，在PC端有软件与设备进行通讯，获取设备当前模拟量和状态信息，并将数据传输到网页展示。

环境要求
--------

操作系统: windows

编程语言：python 2.7

python库：serial

第三方软件：vspd(绑定串口)


文件说明
--------

check_sum.py 计算校验，目前只实现了modbus的crc16校验

serial_communication.py 串口通讯的简单示例，通过serial创建串口连接，进行发包，并收取回包

simulate_modbus.py 模拟modbus回包，由于目前没有接入实际设备，因此使用此脚本模拟设备通讯

utility.py 一些常用的方法集合

准备
----

使用前需要做一些配置工作.
1 创建数据库::

    >>> python manage.py db upgrade

2 设置邮件相关配置::

    >>> export MAIL_USERNAME=<Gmail username>
    >>> export MAIL_PASSWORD=<Gmail password>
    >>> export FLASKY_ADMIN=<your-email-address>

使用方法
--------

导入库monitor: ::

    >>> import monitor

开启模拟modbus回包工具:
首先使用vspd绑定串口com3与com103,
然后导入模块
::
    
    >>> from monitor import simulate_modbus

    >>> sm = simulate_modbus.SimulateModbus('com103')

    >>> sm.start()

接下来使用commix软件打开串口com3,组包命令如：**01 03 00 00 00 01** 选择modbusRTU校验，点击发送，
即可看到回包数据。

使用**ctrl + C**结束。

安装
----

最简单的安装方式: ::
    
    $ pip install monitor


贡献
----

如果你想加入我们，请fork此代码库，并提交改变到 **dev** 分支，并且发送一个 **pull request**。
