# WPS Word转PDF服务 (ARM64)

基于 WPS Office 的 Word 转 PDF HTTP 服务，适用于 ARM64 架构。

## 目录结构

```
my-arm64/
├── Dockerfile.base          # 基础镜像：Ubuntu + WPS + pywpsrpc + Xvfb
├── Dockerfile               # 服务镜像：基础镜像 + Flask + gunicorn
├── docker-compose.yml       # 编排配置
├── app.py                   # Flask 服务代码
├── docker-entrypoint.sh     # 容器入口（启动 Xvfb + D-Bus）
├── Office.conf              # WPS 配置
├── test_convert.py          # WPS 转换脚本（基础镜像依赖）
└── pywpsrpc-*.whl           # pywpsrpc 预编译包
```

## 构建

> 一定要在ARM系统打包docker镜像，它是基于你系统架构拉镜像的。    

```bash
# 1. 构建基础镜像
docker build -f Dockerfile.base -t wps-base .

# 2. 构建服务镜像（二选一）
docker compose build
# 或
docker build -t wps-convert .
```

## 运行

```bash
docker compose up -d
```

服务监听 `http://localhost:5001`。

## API

### 健康检查

```bash
curl http://localhost:5001/health
# {"status":"ok"}
```

### Word 转 PDF

```bash
curl -F "file=@test.docx" http://localhost:5001/convert -o output.pdf
```

支持格式：`.doc` `.docx` `.wps` `.txt` `.rtf`

## 测试

```bash
# 准备一个测试文件
echo "Hello World" > /tmp/test.txt

# 转换
curl -f -F "file=@/tmp/test.txt" http://localhost:5001/convert -o /tmp/output.pdf

# 验证输出
file /tmp/output.pdf
# 应显示: /tmp/output.pdf: PDF document

# 测试错误情况
curl -F "file=@image.png" http://localhost:5001/convert
# {"error":"不支持的格式: .png，支持: ..."}
```

## 配置说明

- **gunicorn workers**：默认 2 个进程，在 Dockerfile CMD 中通过 `-w` 调整
- **超时时间**：默认 120 秒（`-t 120`），大文件可酌情增加
- **端口**：默认 5000，在 docker-compose.yml 中修改

