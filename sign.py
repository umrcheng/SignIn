from time import sleep
import requests
import tools

session = requests.session()
sign_subpaths = ["/user/checkin"]
auth_subpaths = ["/auth/login"]
headers = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41",
}


def cookie_latest(i, conf):
    """
    携带 cookie 请求登录页面，获取最新的 cookie，并保存下来
    :param i:
    :param conf:
    :return:
    """
    cookie = config.get_cookie(i)
    url = tools.Format.domain_format(conf["url"])
    for item in auth_subpaths:
        try:
            session.cookies.update(cookie.get_cookie())
            req = session.post(url + item, headers=headers, timeout=10)
        except requests.exceptions.ConnectionError:
            print("更新 cookie 失败")
            return False
        if req.status_code == 200:
            cookie.save_cookie(session.cookies)
            return True


def sign_cookie(conf):
    """
    携带 cookie 请求签到地址，获取流量，输出流量信息
    :param conf:
    :return:
    """
    url = tools.Format.domain_format(conf["url"])
    for item in sign_subpaths:
        try:
            req = session.post(url + item, headers=headers, timeout=10)
            if req.status_code == 200:
                session.cookies.clear()
                try:
                    obj = req.json()
                    if obj.get('msg'):
                        if "失败" in obj['msg']:
                            print("今天已经签到过了")
                            return False
                        else:
                            print(obj['msg'])
                    if obj.get('traffic'):
                        print("流量：", obj['traffic'])
                    if obj.get('trafficInfo'):
                        if obj['trafficInfo'].get('unUsedTraffic'):
                            print("未使用的流量：", obj['trafficInfo']['unUsedTraffic'])
                        if obj['trafficInfo'].get('lastUsedTraffic'):
                            print("最近使用的流量：", obj['trafficInfo']['lastUsedTraffic'])
                        if obj['trafficInfo'].get('todayUsedTraffic'):
                            print("今天使用的流量：", obj['trafficInfo']['todayUsedTraffic'])
                    return True
                except requests.exceptions.JSONDecodeError:
                    print("签到失败，cookie 失效。")
                    return False
        except requests.exceptions.ConnectionError:
            print("请求错误，签到失败")
            continue


def sign_password(i, conf):
    """
    使用 用户名密码 登录，获取登录状态的 cookie
    :param i:
    :param conf:
    :return:
    """
    url = tools.Format.domain_format(conf["url"])
    user_info = {
        "code": "",
        "email": conf["username"],
        "passwd": conf["password"],
        "remember_me": "true"
    }
    for item in auth_subpaths:
        try:
            req = session.post(url + item, data=user_info, headers=headers, timeout=10)
            if req.status_code == 200:
                try:
                    obj = req.json()
                    if obj['ret'] == 1:
                        print(" 登录成功 ".center(40, "="))
                        config.save_cookie(i, session.cookies)
                        sign_cookie(conf)
                    else:
                        print("登录失败, 账户或密码错误")
                except requests.exceptions.JSONDecodeError:
                    print("未知错误。")
                    return False
            else:
                print("请求错误，登录失败".center(40, "="))
        except requests.exceptions.ConnectionError:
            print(f"登录失败跳过用户 {conf['username']}")
            return False


def main():
    """
    根据参数选择不同的签到方式
    :return:
    """
    for index, user in enumerate(config.get_sub_conf()):
        if user["sign_in_type"] == "cookie":
            # 使用 cookie 进行签到
            if user["cookies"] == "":
                print("登录类型为 cookie 那么配置文件的 cookies 就不能为空！")
                return False
            cookie_latest(index, user)
            sign_cookie(user)
        elif user["sign_in_type"] == "password":
            # 使用 账户，密码 进行签到
            if user["username"] == "" or user["password"] == "":
                print("登录类型为 password 那么配置文件的 username, password 就不能为空！")
                return False
            sign_password(index, user)
        sleep(5)


if __name__ == '__main__':
    """
    fn: 配置文件路径
    ln: 配置文件该文档的列表项名字
    """
    config = tools.Config("config.json", "sign")
    main()
