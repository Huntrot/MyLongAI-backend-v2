# MyLongAI Backend (FastAPI - Production Template)

## 📌 Overview

Backend template được thiết kế theo tư duy **Spring Boot**, giúp:

* Cấu trúc rõ ràng (Controller - Service - Config)
* Dễ scale team
* Dễ tích hợp AI (YOLO, Roboflow,...)

---

## Project Structure

```
app/
│
├── main.py                # Entry của FastAPI app (giống Application.java)
│
├── api/                   # Controller layer (handle request)
│   └── routes/
│       ├── ai_detect.py   # API AI detect
│       └── health.py      # API check server
│
├── services/              # Business logic (giống Service)
│   └── ai_service.py
│
├── models/                # Database models (optional)
│
├── schemas/               # DTO (request/response)
│
├── core/                  # Config (giống application.yml)
│   └── config.py
│
├── dependencies/          # Dependency injection (optional)
│
└── utils/                 # Helper functions

root/
│
├── run.py                 # Entry point để chạy server
├── requirements.txt       # Dependencies
├── .env                   # Environment variables
├── Dockerfile             # Container config (production)
└── .gitignore
```

---

# 🧠 Team Workflow (QUAN TRỌNG)

## 🚧 Khi làm việc hằng ngày (DEV)

👉 Mỗi thành viên:

1. Pull code từ GitHub
2. Chạy bằng `.venv`
3. Code feature riêng (API / service)

❗ **KHÔNG dùng Docker ở bước này**

---

## 🔀 Khi làm việc nhóm

Ví dụ:

* Dev A làm `/ai/detect`
* Dev B làm `/user/login`

👉 Cả 2:

* Dùng `.venv`
* Không cần Docker

---

## 🔄 Khi merge code

* Merge vào `main`
* Đảm bảo:

  * Code chạy OK
  * Update `requirements.txt` nếu có lib mới

👉 Người khác chỉ cần:

```
pip install -r requirements.txt
```

---

## 🚀 Khi deploy (QUAN TRỌNG)

### 🔥 Với project hiện tại (dùng Render)

👉 Flow đúng:

1. Merge code vào `main`
2. Push lên GitHub
3. Render tự:

   * pull code
   * cài dependencies
   * chạy server

❗ **KHÔNG cần Docker**

---

### 🐳 Khi nào mới dùng Docker?

👉 Chỉ dùng khi:

* Deploy server riêng (VPS, AWS, GCP)
* Cần kiểm soát môi trường (GPU, CUDA, YOLO nặng)
* Muốn đảm bảo chạy giống nhau 100%

---

# How to Run (Local - DEV)

## 1. Setup (chỉ chạy lần đầu)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## 2. Run project (mỗi lần làm việc)

```bash
.venv\Scripts\activate
python run.py
```

---

## 3. Khi thêm thư viện mới

```bash
pip install <package-name>
pip freeze > requirements.txt
```

---

## API Docs

Sau khi chạy:

```
http://localhost:8000/docs
```

---

## Architecture Flow

```
Client → API (routes) → Service → Response
```

---

# 🐳 Docker (Production / Advanced)

## 🧠 Docker là gì?

👉 Docker = đóng gói project thành “một môi trường chạy hoàn chỉnh”

* Có Python
* Có thư viện
* Có code

👉 Chạy ở đâu cũng giống nhau

---

## ❗ Khi nào dùng Docker?

✔ Khi:

* Deploy production thật
* Dùng AI nặng (YOLO, GPU)
* Cần môi trường chuẩn

❌ Không dùng khi:

* Đang code
* Đang test API
* Làm việc nhóm hằng ngày

---

## Dockerfile

```dockerfile
FROM python:3.10
WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

CMD ["python", "run.py"]
```

---

## Cách chạy bằng Docker

### 1. Build image

```bash
docker build -t mylongai-backend .
```

---

### 2. Run container

```bash
docker run -p 8000:8000 mylongai-backend
```

---

👉 Truy cập:

```
http://localhost:8000/docs
```

---

# 📌 Tóm tắt cực quan trọng

| Giai đoạn             | Dùng gì            |
| --------------------- | ------------------ |
| Dev hằng ngày         | `.venv`            |
| Làm việc nhóm         | `.venv`            |
| Merge code            | `.venv`            |
| Deploy Render         | ❌ Không cần Docker |
| Deploy production xịn | ✅ Docker           |

---

## Notes

* Không commit:

  * .venv/
  * **pycache**/
  * .env

* Luôn tách:

  * Controller (routes)
  * Business logic (services)

* Chỉ cần tạo `.venv` **1 lần duy nhất**

* Luôn activate trước khi chạy server

* `requirements.txt` là danh sách thư viện để team đồng bộ môi trường

---
