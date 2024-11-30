import time
import logging
import json
import hmac
import hashlib
import base64
import urllib.parse
from datetime import datetime
import requests
import re
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='vps_monitor.log'
)

# 从环境变量获取钉钉配置
DINGTALK_TOKEN = os.getenv('DINGTALK_TOKEN')
DINGTALK_SECRET = os.getenv('DINGTALK_SECRET')
DINGTALK_WEBHOOK = f"https://oapi.dingtalk.com/robot/send?access_token={DINGTALK_TOKEN}"

def calculate_days_until_expire(service):
    """计算距离到期还有多少天"""
    today = datetime.now()
    
    if 'expireDate' in service:
        # 处理具体到期日期
        expire_date = datetime.strptime(service['expireDate'], '%Y-%m-%d')
        days_left = (expire_date - today).days
    elif 'monthlyExpireDay' in service:
        # 处理每月重复日期
        expire_day = service['monthlyExpireDay']
        next_expire = datetime(today.year, today.month, expire_day)
        
        if today.day > expire_day:
            if today.month == 12:
                next_expire = datetime(today.year + 1, 1, expire_day)
            else:
                next_expire = datetime(today.year, today.month + 1, expire_day)
        
        days_left = (next_expire - today).days
    else:
        return None
    
    return days_left

def sign_dingtalk_webhook():
    """为钉钉消息签名"""
    timestamp = str(round(time.time() * 1000))
    secret_enc = DINGTALK_SECRET.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, DINGTALK_SECRET)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return f"{DINGTALK_WEBHOOK}&timestamp={timestamp}&sign={sign}"

def send_dingtalk_alert(expiring_services):
    """发送钉钉警报"""
    if not expiring_services:
        return
    
    message = "# 🚨 VPS服务即将到期警报 🚨\n\n"
    message += "以下服务即将到期：\n\n"
    
    for service in expiring_services:
        days_left = service['days_left']
        urgency = "❗️❗️❗️" if days_left <= 1 else "⚠️"
        
        message += f"## {urgency} {service['name']}\n"
        message += f"- 月付费用: {service['cost']} {service['currency']}\n"
        message += f"- 剩余天数: {days_left}天\n"
        if 'expireDate' in service:
            message += f"- 到期日期: {service['expireDate']}\n"
        elif 'monthlyExpireDay' in service:
            message += f"- 每月续费日: {service['monthlyExpireDay']}号\n"
        message += "\n"
    
    message += "\n> [查看详情](http://vps.smtv.us.kg/index.html)"
    
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "VPS到期警报",
            "text": message
        },
        "at": {
            "isAtAll": True  # 添加@所有人
        }
    }
    
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json'
    }
    webhook_url = sign_dingtalk_webhook()
    
    try:
        json_data = json.dumps(data, ensure_ascii=False)
        response = requests.post(webhook_url, headers=headers, data=json_data.encode('utf-8'))
        if response.status_code == 200:
            logging.info("钉钉警报发送成功")
            print("钉钉警报发送成功")
        else:
            error_msg = f"钉钉警报发送失败: {response.text}"
            logging.error(error_msg)
            print(error_msg)
    except Exception as e:
        error_msg = f"发送钉钉警报时发生错误: {str(e)}"
        logging.error(error_msg)
        print(error_msg)

def get_html_content():
    """获取HTML内容"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Charset': 'UTF-8'
        }
        response = requests.get(VPS_PAGE_URL, headers=headers)
        response.encoding = 'utf-8'
        content = response.text
        print("✓ 成功获取页面内容")
        return content
    except requests.exceptions.RequestException as e:
        error_msg = f"获取页面内容失败: {str(e)}"
        logging.error(error_msg)
        print(f"✗ {error_msg}")
        return None

def extract_vps_services(html_content):
    """从HTML文件中提取VPS服务配置"""
    try:
        pattern = r'const\s+vpsServices\s*=\s*(\[\s*{[\s\S]*?\}\s*\]);'
        match = re.search(pattern, html_content)
        
        if not match:
            raise ValueError("未找到VPS服务配置")
        
        js_array = match.group(1)
        
        # 1. 移除注释行
        py_array = re.sub(r'//.*?\n', '\n', js_array)
        
        # 2. 处理单引号为双引号
        py_array = py_array.replace("'", '"')
        
        # 3. 处理没有引号的属性名
        py_array = re.sub(r'(\w+):', r'"\1":', py_array)
        
        # 4. 移除可能的尾随逗号
        py_array = re.sub(r',(\s*[}\]])', r'\1', py_array)
        
        # 5. 移除多余的空行和空格
        py_array = re.sub(r'\n\s*\n', '\n', py_array)
        py_array = re.sub(r'^\s+', '', py_array, flags=re.MULTILINE)
        
        # 6. 打印转换后的内容以便调试
        print("转换后的JSON字符串:", py_array)
        
        services = json.loads(py_array)
        print(f"✓ 成功读取 {len(services)} 个VPS配置")
        return services
    except Exception as e:
        error_msg = f"配置读取失败: {str(e)}\n转换前的内容: {js_array}"
        logging.error(error_msg)
        print(f"✗ {error_msg}")
        return []

def check_vps_expiration():
    """检查VPS到期情况"""
    try:
        html_content = get_html_content()
        if not html_content:
            return
        
        services = extract_vps_services(html_content)
        expiring_services = []
        
        current_time = datetime.now()
        
        for service in services:
            days_left = calculate_days_until_expire(service)
            if days_left is not None and days_left <= 2:  # 保持2天的提醒阈值
                service['days_left'] = days_left
                expiring_services.append(service)
                logging.info(f"服务 {service['name']} 将在 {days_left} 天后到期")
                print(f"⚠️ {service['name']} 将在 {days_left} 天后到期")
        
        if expiring_services:
            send_dingtalk_alert(expiring_services)
            logging.info(f"发送了 {len(expiring_services)} 个服务的到期提醒")
        else:
            msg = "✓ 所有服务运行正常，无即将到期服务"
            logging.info(msg)
            print(msg)
            
    except Exception as e:
        error_msg = f"检查失败: {str(e)}"
        logging.error(error_msg)
        print(f"✗ {error_msg}")

def main():
    """主函数"""
    print("VPS监控服务已启动")
    logging.info("VPS监控服务启动")
    
    while True:
        try:
            check_vps_expiration()
            print("\n>>> 等待6小时后进行下一次检查...\n")
            time.sleep(6 * 60 * 60)
        except Exception as e:
            error_msg = f"运行时错误: {str(e)}"
            logging.error(error_msg)
            print(f"✗ {error_msg}")
            print(">>> 5分钟后重试...")
            time.sleep(300)

if __name__ == "__main__":
    main() 