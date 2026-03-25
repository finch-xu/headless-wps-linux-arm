FROM wps-base:latest

RUN pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple && \
    pip3 install --no-cache-dir flask gunicorn

COPY app.py /app/app.py

WORKDIR /app
EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "2", "-t", "120", "app:app"]
