# monitor
Monitor devices
将设备如空调，温湿度等通过串口接入PC，在PC端有软件与设备进行通讯，获取设备当前模拟量和状态信息，并将数据传输到网页展示。

环境要求：
操作系统: windows
编程语言：python 2.7
python库：serial
第三方软件：vspd(绑定串口)


文件说明：
check_sum.py 计算校验，目前只实现了modbus的crc16校验
serial_communication.py 串口通讯的简单示例，通过serial创建串口连接，进行发包，并收取回包
simulate_modbus.py 模拟modbus回包，由于目前没有接入实际设备，因此使用此脚本模拟设备通讯
utility.py 一些常用的方法集合
