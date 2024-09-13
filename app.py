import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 从环境变量中获取 corpid, corpsecret
CORP_ID = os.getenv("CORP_ID", "")
if not CORP_ID:
    raise ValueError("CORP_ID environment variables must be set")

# 通用函数：获取 access_token
def get_access_token(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise ValueError("No access_token found in the response")
        return access_token
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to get access_token: {str(e)}")
    except ValueError as e:
        raise RuntimeError(f"Invalid response: {str(e)}")

# 通用函数：调用企业微信 API
def call_wechat_api(url, payload):
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to call WeChat API: {str(e)}")

# 发送图文消息的接口
@app.route('/api/sendMsg', methods=['POST'])
def send_message():
    try:
        # 获取查询参数
        app_id = request.args.get('appId')
        app_secret = request.args.get('appSecret')
        if not app_id or not app_secret:
            return jsonify({"error": "Missing appId or appSecret"}), 400
        
        # 获取 access_token 的 URL
        get_access_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={CORP_ID}&corpsecret={app_secret}"
        access_token = get_access_token(get_access_token_url)
        
        payload = request.json
        if not payload:
            return jsonify({"error": "Invalid input"}), 400
        
        # 调用企业微信 API
        send_msg_url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
        response_data = call_wechat_api(send_msg_url, payload)
        return jsonify(response_data)
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8300)