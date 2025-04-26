# 引入所需模块
from flask import Flask, request, jsonify
import requests
import random
import datetime
from flask_cors import CORS

# 初始化 Flask 应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求，解决前端浏览器的CORS限制

# Telegram Bot 信息
BOT_TOKEN = '7871596395:AAHs6vJ3GX-uJrMiq2vWt9taBFIaOyLam0U'  # <-- 请替换成你的真实 Bot Token
ADMIN_ID = '844368048'      # <-- 管理员Telegram用户ID

# 接收订单并发送到Telegram
@app.route('/receive_order', methods=['POST'])
def receive_order():
    data = request.json

    # 解析订单数据
    order_items = data.get('items', [])
    total_price = data.get('total_price', 0)

    # 生成订单编号（格式例子：ORDER-20250426-3812）
    order_id = generate_order_id()

    # 整理订单信息文本
    message = f"📦 新订单 - 编号: {order_id}\n\n"
    for item in order_items:
        message += f"- {item['name']} × {item['quantity']}（糖：{item['sugar_level']}）= ¥{item['subtotal']}\n"
    message += f"\n💵 总价：¥{total_price}"

    # 发送订单信息到管理员Telegram
    send_message_to_admin(message)

    return jsonify({
        "status": "success",
        "message": "订单接收并通知成功",
        "order_id": order_id  # 返回给前端订单编号
    })

# 发送文本消息到管理员
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

# 生成订单编号函数
def generate_order_id():
    today = datetime.datetime.now().strftime('%Y%m%d')
    rand = random.randint(1000, 9999)
    return f"ORDER-{today}-{rand}"

# 程序入口
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
