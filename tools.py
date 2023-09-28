from requests.cookies import RequestsCookieJar
from requests.utils import dict_from_cookiejar
from json import loads, dumps


class Config:
    __config_path = ""
    __list_name = ""
    __config = ""
    __config_obj = None
    __cookie = ""
    __jar = RequestsCookieJar()

    def __init__(self, fn, ln):
        """

        :param fn: 配置文件路径
        :param ln: 该项目配置信息名字
        """
        self.__config_path = fn
        self.__list_name = ln
        self.__load_config()

    def __load_config(self):
        with open(self.__config_path, 'r', encoding='utf8') as c:
            read = c.read()
            self.__config = read
            self.__config_obj = loads(read)

    def get_sub_conf(self):
        return self.__config_obj[self.__list_name]

    def get_cookie(self, index: int):
        """

        :param index:
        :return:
        """

        """遍历cookie字符串去除配置文件中的空格"""
        temp = ""
        for i in self.__config_obj[self.__list_name][index]["cookies"]:
            if i == " ":
                continue
            temp += i
        if not temp:
            return
        self.__config = temp

        """把cookie格式的字符串转换为 dict 对象"""
        cookie = {}
        cookie_list = temp.split(";")
        for i in cookie_list:
            key, value = i.split("=")
            cookie[key] = value

        """cookie对象保存到 requests.cookies.RequestsCookieJar """
        for key in cookie:
            self.__jar.set(key, cookie[key])

    def set_cookie(self, obj: dict):
        if obj["key"] is not None and obj["value"] is not None:
            self.__jar.set_cookie(obj["key"], obj["value"])
        return self.__jar

    def save_cookie(self, index: int, jar: RequestsCookieJar):
        cookie = dict_from_cookiejar(jar)
        cookie_string = ""
        for key, val in cookie.items():
            cookie_string += f"{key}={val};"
        cookie_string = cookie_string[:-1]

        with open(self.__config_path, "w", encoding="utf8") as f:
            self.__config_obj[self.__list_name][index]["cookies"] = cookie_string
            f.write(dumps(self.__config_obj, indent=2, ensure_ascii=False, sort_keys=False))
        return self


class Format:
    @staticmethod
    def domain_format(domain):
        if domain[-1] == "/":
            return domain[0:-1]
        return domain
