import json
import os
from datetime import datetime, timedelta
import requests
import re
import time

def send_dingding_msg(msg):
    timestamp = str(round(time.time() * 1000))
    secret = os.environ.get('DING_SECRET')
    access_token = os.environ.get('DING_TOKEN')
    
    if not secret or not access_token:
        print("未配置钉钉密钥，跳过通知")
        return
        
    url = f'https://oapi.dingtalk.com/robot/send?access_token={access_token}'
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = {
        "msgtype": "text",
        "text": {
            "content": f"VPS到期提醒：\n{msg}"
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print("钉钉通知发送成功")
        else:
            print(f"钉钉通知发送失败: {response.text}")
    except Exception as e:
        print(f"发送钉钉通知异常: {str(e)}")

def check_expiration(vps_list):
    today = datetime.now()
    notification_msg = []
    
    for vps in vps_list:
        if "expireDate" in vps:
            expire_date = datetime.strptime(vps["expireDate"], "%Y-%m-%d")
            days_left = (expire_date - today).days
            
            if days_left <= 3:  # 提前3天提醒
                notification_msg.append(f"{vps['name']} 将在 {days_left} 天后到期")
        
        elif "monthlyExpireDay" in vps:
            monthly_day = vps["monthlyExpireDay"]
            if today.day == monthly_day - 1:  # 提前1天提醒
                notification_msg.append(f"{vps['name']} 将在明天进行续费")
    
    if notification_msg:
        send_dingding_msg("\n".join(notification_msg))

def get_vps_data():
    """获取VPS数据"""
    vps_services = [
        {
            "name": "斯巴达VPS",
            "cost": 8,
            "currency": "USD",
            "monthlyExpireDay": 3,
            "color": "primary",
            "url": "https://billing.spartanhost.net/login"
        },
        {
            "name": "阿里云轻量香港",
            "cost": 34,
            "currency": "CNY",
            "monthlyExpireDay": 29,
            "color": "danger",
            "url": "https://swasnext.console.aliyun.com/servers/cn-hongkong"
        },
        {
            "name": "v.ps圣何塞",
            "cost": 2.75,
            "currency": "EUR",
            "expireDate": "2025-2-7",
            "color": "primary",
            "url": "https://vps.hosting/clientarea/"
        },
        {
            "name": "OVH加拿大0.97",
            "cost": 0.97,
            "currency": "USD",
            "expireDate": "2025-2-9",
            "color": "danger",
            "url": "https://ca.ovh.com/manager/#/hub"
        },
        {
            "name": "raksmart-hk",
            "cost": 0,
            "currency": "USD",
            "expireDate": "2025-11-9",
            "color": "success",
            "url": "https://billing.raksmart.com/whmcs/clientarea.php?action=products"
        },
        {
            "name": "OVH美西",
            "cost": 5.5,
            "currency": "EUR",
            "monthlyExpireDay": 18,
            "color": "success",
            "url": "https://us.ovhcloud.com/vps/"
        },
        {
            "name": "卢森堡2G",
            "cost": 7,
            "currency": "USD",
            "monthlyExpireDay": 19,
            "color": "warning",
            "url": "https://my.frantech.ca/cart.php?gid=39"
        },
        {
            "name": "Netcup4c8G",
            "cost": 5.75,
            "currency": "EUR",
            "monthlyExpireDay": 29,
            "color": "info",
            "url": "https://www.customercontrolpanel.de/index.php?action=se"
        }
    ]
    
    # 计算北京时间
    utc_time = datetime.utcnow()
    beijing_time = utc_time + timedelta(hours=8)
    update_time = beijing_time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"生成更新时间 (北京时间): {update_time}")
    
    # 添加到期检查
    check_expiration(vps_services)
    
    return {
        "services": vps_services,
        "lastUpdate": update_time
    }

def update_html_file():
    """更新HTML文件中的数据"""
    try:
        data = get_vps_data()
        
        print("正在读取 index.html...")
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        print("原始文件大小:", len(html_content))
        
        # 更新VPS数据
        vps_data_str = json.dumps(data['services'], ensure_ascii=False, indent=4)
        
        # 使用正则表达式替换 vpsServices 数组内容
        pattern = r'const\s+vpsServices\s*=\s*\[([\s\S]*?)\]\s*;'
        new_content = re.sub(pattern, f'const vpsServices = {vps_data_str};', html_content)
        
        # 更新最后更新时间
        if '<div class="last-update text-center mb-3">' in html_content:
            # 如果已存在更新时间，则替换它
            new_content = re.sub(
                r'<div class="last-update text-center mb-3">.*?</div>',
                f'<div class="last-update text-center mb-3">最后更新时间: {data["lastUpdate"]}</div>',
                new_content
            )
        else:
            # 如果不存在，则在标题后添加
            new_content = new_content.replace(
                '</h1>',
                f'</h1>\n        <div class="last-update text-center mb-3">最后更新时间: {data["lastUpdate"]}</div>'
            )
        
        print("新文件大小:", len(new_content))
        
        print("正在写入更新后的文件...")
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print("文件更新完成")
        
    except Exception as e:
        print(f"更新失败: {str(e)}")
        raise

def main():
    update_html_file()

if __name__ == "__main__":
    main() 