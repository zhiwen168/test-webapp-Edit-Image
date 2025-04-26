from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
# 允许跨域请求，解决浏览器CORS限制
from flask_cors import CORS
CORS(app)


# Telegram Bot 信息
BOT_TOKEN = '你的bot_token'  # <-- 替换为你的实际 bot token
ADMIN_ID = '844368048'

# 接收订单、联系方式、位置
@app.route('/receive_order', methods=['POST'])
def receive_order():
    data = request.json

    # 解析数据
    order_items = data.get('items', [])
    total_price = data.get('total_price', 0)
    user_contact = data.get('contact', {})
    user_location = data.get('location', {})

    # 整理订单信息
    message = "📦 新订单\n\n"
    for item in order_items:
        message += f"- {item['name']} × {item['quantity']}（糖：{item['sugar_level']}）= ¥{item['subtotal']}\n"
    message += f"\n💵 总价：¥{total_price}\n\n"

    if user_contact:
        message += f"📱 电话: {user_contact.get('phone_number', '无')}\n"
        message += f"👤 姓名: {user_contact.get('first_name', '')} {user_contact.get('last_name', '')}\n"

    # 先发文字订单
    send_message_to_admin(message)

    # 再发位置
    if user_location:
        send_location_to_admin(
            user_location.get('latitude'),
            user_location.get('longitude')
        )

    return jsonify({"status": "success", "message": "订单接收并通知成功"})

def send_message_to_admin(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": ADMIN_ID,
        "text": text
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print("发送订单消息失败:", e)

def send_location_to_admin(lat, lon):
    if lat is None or lon is None:
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendLocation"
    payload = {
        "chat_id": ADMIN_ID,
        "latitude": lat,
        "longitude": lon
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print("发送位置失败:", e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
