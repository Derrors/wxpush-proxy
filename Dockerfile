# 使用 Python 官方基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 将当前目录的文件复制到 Docker 容器中的工作目录
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 设置环境变量（可以用 ENV 指令设置默认值）
ENV CORP_ID=
ENV SECRET=
ENV PORT=

# 启动 Flask 应用
CMD ["python", "app.py"]