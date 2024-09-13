## 企业微信推送代理
企业微信使用应用推送消息需要配置信任 IP，这要求调用方 IP 是固定的，否则需要频繁配置 IP 要应用的信任 IP 列表
为解决这个问题，采用代理服务来调用企业微信消息推送 API，代理服务需要部署在固定公网 IP 的机器或 VPS 上；

### 1. 部署方式
docker run -d -p 8300:8300 \
  -e CORP_ID=your_corpid \
  --name wxpush-proxy wxpush-proxy

- CORP_ID: 企业微信的企业 ID


### 2. 使用指南
docker 部署完成后，提供调用接口：
* url: POST http://ip:port/api/sendMsg?appId={应用agentId}&appSecret={应用secret}
* 请求体格式与 [发送应用消息](https://developer.work.weixin.qq.com/document/path/90236) 一致。