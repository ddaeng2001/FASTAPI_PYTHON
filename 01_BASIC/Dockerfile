FROM python:3.11-slim
WORKDIR /app

# 의존성 먼저 설치
COPY requirements.txt .
# 현재 보고 있는 requirements.txt를 linux docker안에 있는 .(앱)안에 복사를 하겠다!

RUN pip install --no-cache-dir -r requirements.txt

# 앱 파일 복사
COPY main.py .
# docker container내 최상위 폴더 안에 main.py를 복사하겠다!

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



