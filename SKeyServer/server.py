import socket
import random
import hashlib
import time

# 用户字典，用户名：[登陆次数, 密码]
user_dict = {}
max_cnt = 5
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999


def md5(s):
    """
    对s进行md5哈希

    :param s: 要进行md5加密的bytes字符串
    :return: md5加密后的字符串
    """
    m = hashlib.md5()
    m.update(s.encode('utf-8'))
    return m.hexdigest()


def get_seed():
    """
    生成要返回给客户端的种子

    :return: 种子
    """
    return str(random.randint(10000000, 99999999))


def send_seed():
    """
    生成种子，发送给客户端
    """
    _seed = get_seed()
    socket_client.send(_seed.encode('utf-8'))


def login_log(_username, _passed):
    """
    记录用户的登录操作日志
    """
    _time_login = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    plaintext = "%s: 用户%s尝试登录，登录" % (_time_login, _username)
    plaintext += "成功\n" if (_passed == 1) else "失败\n"
    with open("./log.txt", 'a') as f:
        f.write(plaintext)


def recv_first_pwd(_username):
    """
    接收客户端发送的第一个口令，并存储起来，初始化该用户的验证进程

    :param _username: 用户名
    """
    _pwd = (socket_client.recv(32)).decode('utf-8')
    # print(pwd)
    user_dict[_username] = [1, _pwd]


def recv_pwd(_username):
    """
    收到客户端发送的口令并验证，将验证结果返回给客户端

    :param _username: 用户名
    """
    _pwd_recv = socket_client.recv(32).decode('utf-8')
    _pwd = md5(_pwd_recv)
    # 口令正确，发送'1'
    if _pwd == user_dict[_username][1]:
        user_dict[_username][0] += 1
        user_dict[_username][1] = _pwd_recv
        socket_client.send('1'.encode('utf-8'))
        _passed = 1
    # 口令错误，发送'0'
    else:
        socket_client.send('0'.encode('utf-8'))
        _passed = 0
    login_log(_username, _passed)


if __name__ == '__main__':
    socket_server.bind((host, port))
    socket_server.listen(3)
    while True:
        socket_client, addr = socket_server.accept()
        username = (socket_client.recv(32)).decode('utf-8')
        # username存在，则查看口令是否用完
        if username in user_dict.keys():
            cnt = user_dict[username][0]
            pwd = user_dict[username][1]
            # 口令用完
            if cnt >= max_cnt:
                # 要进行初始化，发送0提示客户端
                socket_client.send('0'.encode('utf-8'))
                send_seed()
                recv_first_pwd(username)
                recv_pwd(username)
            # 口令没有用完
            elif cnt < max_cnt and pwd != '':
                socket_client.send('1'.encode('utf-8'))
                recv_pwd(username)
            else:
                exit(-1)

        else:
            # username不在，则注册
            socket_client.send('2'.encode('utf-8'))
            send_seed()
            # 接收第一个口令并存储
            recv_first_pwd(username)
            recv_pwd(username)
        socket_client.close()
