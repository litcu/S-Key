import socket
import hashlib

max_cnt = 5
pwd_list = []
socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999


def str2hex(s):
    """
    将字符串转换为对应的16进制整数\n
    :param s: 16进制字符串
    :return: 整数
    """
    return int(s, 16)


def md5(s):
    """
    对字符串进行md5哈希\n
    :param s: 要进行md5加密的字符串
    :return: md5加密后的字符串
    """
    m = hashlib.md5()
    m.update(s.encode('utf-8'))
    return m.hexdigest()


def preprocess(s):
    """
    对要生成口令的字符串进行预处理\n
    :param s: 经过md5加密后的32位字符串
    :return: S
    :rtype: str
    """
    first_s = str2hex(s[:16])
    last_s = str2hex(s[16:])
    s1 = hex(first_s ^ last_s)
    return s1[2:]


def generate_keys(s):
    """
    生成max_cnt个口令\n
    :param s: S
    """
    global pwd_list
    for _i in range(max_cnt):
        s1 = md5(s)
        pwd_list.append(s1)
        s = s1
    pwd_list.reverse()
    # print(pwd_list)
    socket_client.send(pwd_list[0].encode('utf-8'))
    print("为您生成了%d个口令，请顺序使用：" % (max_cnt - 1))
    for i in range(1, max_cnt):
        print("第%d个口令：%s" % (i, pwd_list[i]))


def send_pwd():
    """
    输入并发送口令到服务器\n
    :return:
    """
    pwd = str(input("请输入口令："))
    socket_client.send(pwd.encode('utf-8'))
    verified = socket_client.recv(1).decode('utf-8')
    print(verified)
    if verified == '1':
        print("口令正确！\n")
    else:
        print("口令错误！\n")
    socket_client.close()


if __name__ == '__main__':
    username = str(input("请输入用户名："))
    password = ''
    socket_client.connect((host, port))
    socket_client.send(username.encode('utf-8'))
    flag = socket_client.recv(1).decode('utf-8')
    # 初始化口令
    if flag == '0':
        print("口令已用完，将自动初始化...\n")
        seed = socket_client.recv(8).decode('utf-8')
        s_init = username + seed
        S = preprocess(md5(s_init))
        generate_keys(S)
        send_pwd()

    elif flag == '1':
        send_pwd()

    elif flag == '2':  # 新注册用户
        seed = socket_client.recv(32).decode('utf-8')
        print("当前用户名不存在，将进行注册...")
        s_init = username + seed
        S = preprocess(md5(s_init))
        generate_keys(S)
        # 将口令发送给服务器
        send_pwd()
