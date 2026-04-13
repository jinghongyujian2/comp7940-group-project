FROM python:3.12-slim

WORKDIR /comp7940-lab

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码文件（不包含 config.ini）
COPY chatbot.py ChatGPT_HKBU.py README.md . 

# 启动程序
CMD ["python", "chatbot.py"]
