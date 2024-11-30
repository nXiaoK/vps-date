import json
import os
from datetime import datetime
import requests

def get_vps_data():
    """获取VPS数据"""
    vps_services = [
        {
            "name": "斯巴达VPS",
            "cost": 8,
            "currency": "USD",
            "monthlyExpireDay": 15,
            "color": "primary"
        },
        {
            "name": "阿里云轻量香港",
            "cost": 34,
            "currency": "CNY",
            "monthlyExpireDay": 29,
            "color": "danger"
        },
        {
            "name": "v.ps圣何塞",
            "cost": 2.75,
            "currency": "EUR",
            "expireDate": "2025-2-7",
            "color": "primary"
        },
        {
            "name": "OVH加拿大0.97",
            "cost": 0.97,
            "currency": "USD",
            "expireDate": "2025-2-9",
            "color": "danger"
        },
        {
            "name": "raksmart-hk",
            "cost": 0,
            "currency": "USD",
            "expireDate": "2025-11-9",
            "color": "success"
        },
        {
            "name": "OVH美西",
            "cost": 5.5,
            "currency": "EUR",
            "monthlyExpireDay": 18,
            "color": "success"
        },
        {
            "name": "卢森堡2G",
            "cost": 7,
            "currency": "USD",
            "monthlyExpireDay": 19,
            "color": "warning"
        },
        {
            "name": "Netcup4c8G",
            "cost": 5.75,
            "currency": "EUR",
            "monthlyExpireDay": 29,
            "color": "info"
        }
    ]
    
    # 计算最后更新时间
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "services": vps_services,
        "lastUpdate": update_time
    }

def update_html_file():
    """更新HTML文件中的数据"""
    data = get_vps_data()
    
    # 读取原始HTML文件
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 更新VPS数据
    vps_data_str = json.dumps(data['services'], ensure_ascii=False, indent=4)
    
    # 在</h1>标签后添加最后更新时间
    new_content = html_content.replace(
        '</h1>',
        f'</h1>\n        <div class="last-update text-center mb-3">最后更新时间: {data["lastUpdate"]}</div>'
    )
    
    # 更新VPS服务数据
    new_content = new_content.replace(
        'const vpsServices = [',
        f'const vpsServices = {vps_data_str}'
    )
    
    # 写入更新后的文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    update_html_file() 