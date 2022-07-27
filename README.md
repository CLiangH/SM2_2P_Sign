项目目标
=

implement sm2 2P sign with real network communication

项目原理
=

![image](https://github.com/CLiangH/Picture/blob/main/SM22PS1.png)

代码解析
=

本项目为模仿真实世界通讯，创建了两个文件以模仿两位用户，两文件之间通过socket模块进行通信。

__用户A__
________________

__Sign1__

计算
`P1=$D^{-1}$G`

__Sign3__

计算
`M'=Za||M`
`e-Hash(M')`
`Q1=kG`

__Sign5__

求解最终签名，具体算法为：

`s=(d*k)*s2+d*s3-r mod n`

下面进行主函数介绍：

用户A首先调用Sign1、Sign2函数求得P1、Q1、e，之后通过socket发送给用户B，等待用户B计算完成后从它那里
接收r、s2、s3，并将这三个数据作为参数传到Sign5函数中，得到最终签名值。

__用户B__
________________

__Sign__

传入参数P1、Q1、e，求得r、s2、s3。

用户B从用户A处接收P1、Q1、e，并将其传入Sign函数中，得到r、s2、s3，最后将其传回用户A即可。

运行指导
=

此作品需先打开用户A进程，之后打开用户B进程连接，即可成功。

运行截图
=

![image](https://github.com/CLiangH/Picture/blob/main/SM22PS2.png)
















