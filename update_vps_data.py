import json
import os
from datetime import datetime, timedelta
import requests
import re

def get_vps_data():
    """获取VPS数据"""
    vps_services = [
        {
            "name": "Netcup-VPS1000",
            "cost": 5.75,
            "currency": "EUR",
            "monthlyExpireDay": 26,
            "color": "primary",
            "url": "https://www.customercontrolpanel.de/produkte.php"
        },
        {
            "name": "OVH-KS-LE-1",
            "cost": 11.1,
            "currency": "USD",
            "monthlyExpireDay": 21,
            "color": "primary",
            "url": "https://ca.ovh.com/manager/#/hub/"
        },
        {
            "name": "Claw-HK",
            "cost": 4,
            "currency": "USD",
            "expireDate": "2024-12-29",
            "color": "primary",
            "url": "https://claw.cloud/clientarea.php"
        },
        {
            "name": "OVH-0.97",
            "cost": 0.97,
            "currency": "USD",
            "monthlyExpireDay": 26,
            "color": "primary",
            "url": "https://ca.ovh.com/manager/#/hub/"
        },
        {
            "name": "OVH-0.81",
            "cost": 0.81,
            "currency": "EUR",
            "monthlyExpireDay": 26,
            "color": "primary",
            "url": "https://ovh.ie"
        },
        {
            "name": "V.PS-San Jose Mini Pro",
            "cost": 19.98,
            "currency": "EUR",
            "expireDate": "2025-2-24",
            "color": "primary",
            "url": "https://v.ps"
        },
        {
            "name": "V.PS-San Jose Starter",
            "cost": 29.98,
            "currency": "EUR",
            "expireDate": "2025-3-1",
            "color": "primary",
            "url": "https://v.ps"
        },
        {
            "name": "Bagevm-Hong Kong - BFTINY",
            "cost": 2.59,
            "currency": "USD",
            "monthlyExpireDay": 28,
            "color": "primary",
            "url": "https://bagevm.com/clientarea.php"
        }

    ]
    
    # 计算北京时间
    utc_time = datetime.utcnow()
    beijing_time = utc_time + timedelta(hours=8)
    update_time = beijing_time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"生成更新时间 (北京时间): {update_time}")
    
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

if __name__ == "__main__":
    update_html_file() 
