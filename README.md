# 项目使用
![image](https://github.com/umrcheng/SignIn/assets/55354489/d39e58e5-7ad7-4877-91e1-3fc6ce9e9ffc)

## 常见机场每日签到

### 如果你的代理商页面如下，相同或者极其相似，就可以使用本项目进行每日签到

![image](https://github.com/umrcheng/SignIn/assets/55354489/e0df8369-3151-4957-9d81-1d209f5e10b2)
![image](https://github.com/umrcheng/SignIn/assets/55354489/c851a51a-2724-49ff-8b82-9f14c4fed82a)
![image](https://github.com/umrcheng/SignIn/assets/55354489/a29342a3-d579-43ba-804f-ad6fad653352)
![image](https://github.com/umrcheng/SignIn/assets/55354489/f881c610-760f-4ed8-bc32-221867314639)

### 使用青龙面板

直接使用命令
```sh
ql repo https://github.com/umrcheng/SignIn.git "" "" "tools|config" "" "py|json"
```

手动配置
- 名称：签到领流量
- 类型：公开仓库
- 链接：[https://github.com/umrcheng/SignIn.get](https://github.com/umrcheng/SignIn.git)
- 定时类型：crontab
- 定时规则：30 10 27 * *
- 白名单：
- 黑名单：tools|config
- 依赖文件：tools|config
- 文件后缀：py|json

### 填写配置文件字段

- **url**: 代理商的域名
- **sign_in_type**: 登录的类型有两种 `password` `cookie`
- **username**, **password**: `sign_in_type`选择 `password` 时需要填写账户密码
- **cookies**: `sign_in_type`选择 `cookie` 时需要填写代理商页面获取到的 `cookie`
- 多用户就把这个对象配置项复制一份填到 sign 数组里, 要注意添加 `,` 号

```json
"sign": [
  {
    "url": "https://domain.com",
    "sign_in_type": "password",
    "username": "",
    "password": "",
    "cookies": ""
  }
]
```
