# DATATHON2026 - ITE1Go

Repository làm bài cho **VINTELLIGENCE DATATHON 2026 - Vòng 1**.

## Team: ITE1Go
- Đào Thị Mai Chi (Leader)
- Huỳnh Thị Nha Sinh
- Nguyễn Thị Hằng
- Nguyễn Đăng Hậu

## Mục tiêu repo
Repo này dùng để:
- xử lý **MCQ**
- làm **EDA / visualization / business insights**
- xây dựng mô hình **forecasting** và tạo `submission.csv`

## Cấu trúc thư mục
```text
DATATHON2026/
├── data/
│   ├── raw/
│   │   ├── analytical/
│   │   │   ├── sales.csv
│   │   │   └── sample_submission.csv
│   │   ├── master/
│   │   │   ├── customers.csv
│   │   │   ├── geography.csv
│   │   │   ├── products.csv
│   │   │   └── promotions.csv
│   │   ├── operational/
│   │   │   ├── inventory.csv
│   │   │   └── web_traffic.csv
│   │   └── transaction/
│   │       ├── order_items.csv
│   │       ├── orders.csv
│   │       ├── payments.csv
│   │       ├── returns.csv
│   │       ├── reviews.csv
│   │       └── shipments.csv
│   ├── processed/
│   └── submissions/
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_mcq_answers.ipynb
│   └── baseline.ipynb
├── reports/
│   ├── data_audit/
│   │   ├── business_rule_summary.csv
│   │   ├── duplicate_summary.csv
│   │   ├── erd_overview.png
│   │   ├── erd_relationships.csv
│   │   ├── inventory_summary.csv
│   │   ├── join_check_summary.csv
│   │   ├── null_summary.csv
│   │   └── schema_summary.csv
│   └── final/
│       └── mcq_answers.csv
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── data_prep.py
│   └── mcq.py
├── .gitignore
├── README.md
└── requirements.txt
```

## 1. Clone repo
```bash
git clone https://github.com/ndhau1706/DATATHON2026.git
cd DATATHON2026
```

## 2. Tạo môi trường và cài thư viện
### macOS / Linux
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 3. Chạy project
Chạy các lệnh bên dưới tại thư mục gốc `DATATHON2026/`.

### Cách 1: Mở notebook
```bash
jupyter lab
```

Hoặc:

```bash
jupyter notebook
```

Các notebook hiện có:
- `notebooks/01_data_audit.ipynb`
- `notebooks/02_mcq_answers.ipynb`
- `notebooks/baseline.ipynb`

### Cách 2: Chạy script sinh đáp án MCQ
```bash
python -m src.mcq
```

Kết quả sẽ được lưu tại:

```text
reports/final/mcq_answers.csv
```

## 4. Lưu ý
- Không chỉnh sửa dữ liệu gốc trong `data/raw/`
- Không dùng dữ liệu ngoài bài thi
- Với forecasting, tránh data leakage và dùng validation theo thời gian
- Giữ `submission.csv` đúng format mẫu và đúng thứ tự dòng

---
**Status:** in progress  
**Competition:** DATATHON 2026 - Round 1
