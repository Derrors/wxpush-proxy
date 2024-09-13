import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 从环境变量中获取 corpid, corpsecret
CORP_ID = os.getenv("CORP_ID", "")
SECRET = os.getenv("SECRET", "")

# 验证环境变量是否存在
if not CORP_ID or not SECRET:
    raise ValueError("CORP_ID and SECRET environment variables must be set")

# 获取 access_token 的 URL
GET_ACCESS_TOKEN_URL = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={CORP_ID}&corpsecret={SECRET}"

# 发送消息的 URL
SEND_URL = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}"

# 通用函数：获取 access_token
def get_access_token():
    try:
        response = requests.get(GET_ACCESS_TOKEN_URL)
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
        access_token = get_access_token()
        payload = request.json
        if not payload:
            return jsonify({"error": "Invalid input"}), 400
        
        # 构建 API URL
        c_url = SEND_URL.format(access_token)
        
        # 调用企业微信 API
        response_data = call_wechat_api(c_url, payload)
        return jsonify(response_data)
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8300)