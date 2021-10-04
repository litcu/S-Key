具体内容可前往我的[个人博客](https://littlecu.cn/archives/123)访问。

# S/Key身份认证

本项目为课程实验内容，简单模拟了通过S/Key协议进行身份认证的过程。

## 运行环境

系统：Arch Linux

语言：Python 3.9

IDE：Pycharm

## 实现的功能

1. S/Key协议身份认证
2. 用户登录日志记录

## 本项目中S/Key协议认证过程

1. 客户端连接服务器，提示用户输入用户名，将输入的用户名发送到服务器
2. 服务器在用户信息字典中查询，根据用户名是否存在，向客户端发送不同的反馈信息
3. 客户端收到反馈信息，根据内容判断：
   - 用户名不存在，接受服务器发送的Seed，与用户名首尾相连后进行一次MD5哈希，然后前8位与后8位进行异或运算，得到S。对S进行MD5运算1次，得到第n个密码；2次得到第n-1个密码;…;n次得到第1个密码。将第一个密码发送到服务器保存在用户信息字典中，依次使用第2到n个口令进行登录。
   - 用户名存在，但是生成的n个口令已使用完，则进行初始化，过程和用户名不存在的情况一样。
   - 用户名存在，且n个口令未使用完，则直接提示用户输入口令。
4. 用户输入口令，发送到服务器，服务器接收到客户端发送的口令之后，对其进行一次MD5哈希运算，将所得结果与用户信息字典中的上一个口令进行比较，根据是否一致发送不同的反馈信息给客户端。
5. 客户端收到反馈，若两者一致，则允许登录；否则不允许登录。
6. 对于每一次登录，无论是否成功，都需要记录日志，保存在path/to/SKeyServer/log.txt文件中。保存信息包括时间、用户名、登录是否成功。

