## 演示


```
https://woniu336.github.io/vps-date/
```

- 北京时间每天8点和晚上8点自动更新
- 首次使用，可以手动触发运行测试


## 添加监控

拷贝仓库，修改 update_vps_data.py

添加小鸡信息，例如：

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

## 手动触发运行

图1：

![Image](https://img.meituan.net/video/a1dd1235b55426848b809904ca47fcd1136540.png)

图2：

![Image](https://img.meituan.net/video/bfaac2b0278fc258c8b9adbe6a9339b965243.png)


## 开启GitHub Pages


![Image](https://img.meituan.net/video/41151f0258dcd0e8dde99c9538fe0e8184301.png)




## 通知

> 本项目没有整合通知，需要下载 vps_monitor.py 脚本到机子上运行
> 记得把小鸡ip加入到钉钉ip段

![Image](https://img.meituan.net/video/b873c041a39d51ba8a26632bfaebde6722621.png)

通知测试

![Image](https://img.meituan.net/video/38ec1feedfcfae28dc36cc3251820ff817647.png)


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



