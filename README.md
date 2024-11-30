
## MJJ订阅追踪



监控页面

```
https://woniu336.github.io/vps-date/
```

添加机子信息，格式：

例如：

```
        {
            "name": "OVH加拿大",
            "cost": 0.97,
            "currency": "USD",
            "expireDate": "2025-2-9",
            "color": "danger",
            "url": "https://ca.ovh.com/manager/#/hub"
        },
```

- cost 是费用
- currency 是币种，USD、EUR、CNY 三种币种
- expireDate 到期时间
- monthlyExpireDay 每月续费的日期，例如：3，就是每月3号续费，注意：expireDate和monthlyExpireDay只能二选一
- color 颜色
- url 链接


## 通知

> 本项目没有整合通知，需要下载 vps_monitor.py 脚本到机子上运行


1. 安装依赖

```
pip install requests
```

修改脚本，添加钉钉通知


2. 测试

```
python3 vps_monitor.py
```


3. 后台运行

```
nohup python3 vps_monitor.py > vps_monitor.out 2>&1 &
```



4. 停止监控

```
ps aux | grep vps_monitor.py
```

停止进程

```
kill <进程ID>
```




