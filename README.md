# DATATHON2026 - ITE1Go

Repository làm bài cho **VINTELLIGENCE DATATHON 2026 - Vòng 1**.

## Team: ITE1Go
- Đào Thị Mai Chi (Leader)
- Huỳnh Thị Nha Sinh
- Nguyễn Thị Hằng
- Nguyễn Đăng Hậu

## Mục tiêu repo
Repo này dùng để thực hiện các phần chính của bài thi:

- Xử lý và kiểm tra chất lượng dữ liệu
- Trả lời 10 câu hỏi trắc nghiệm MCQ
- Làm EDA, visualization và business insights
- Xây dựng mô hình forecasting
- Tạo file `submission.csv` theo đúng format của `sample_submission.csv`

## Cấu trúc thư mục
```text
DATATHON2026/
├── artifacts/
│   └── cleaned_data/
│       ├── customers.csv
│       ├── geography.csv
│       ├── inventory.csv
│       ├── order_items.csv
│       ├── orders.csv
│       ├── payments.csv
│       ├── products.csv
│       ├── promotions.csv
│       ├── returns.csv
│       ├── reviews.csv
│       ├── sales.csv
│       ├── sample_submission.csv
│       ├── shipments.csv
│       └── web_traffic.csv
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
│       └── submission.csv
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_mcq_answers.ipynb
│   └── baseline.ipynb
├── reports/
│   ├── data_audit/
│   │   ├── business_rule_summary.csv
│   │   ├── cleaning_actions.csv
│   │   ├── cleaning_overview.csv
│   │   ├── duplicate_summary.csv
│   │   ├── erd_overview.png
│   │   ├── erd_relationships.csv
│   │   ├── inventory_summary.csv
│   │   ├── join_check_summary.csv
│   │   ├── null_summary.csv
│   │   └── schema_summary.csv
│   ├── figures/
│   └── final/
│       └── mcq_answers.csv
├── src/
│   ├── __init__.py
│   ├── cleaning.py
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

Copy phần này thay cho mục **4. Chạy project** trong README:

## 3. Chạy project

Chạy các lệnh bên dưới tại thư mục gốc `DATATHON2026/`.

### 3.1. Chạy cleaning

```bash
python -m src.cleaning
````

### 3.2. Chạy MCQ

```bash
python -m src.mcq
```

### 3.3. Mở notebook

```bash
jupyter lab
```

Hoặc:

```bash
jupyter notebook
```

Các notebook hiện có:

* `notebooks/01_data_audit.ipynb`
* `notebooks/02_mcq_answers.ipynb`
* `notebooks/baseline.ipynb`

### 3.4. Chạy lại trước khi nộp hoặc push GitHub

```bash
python -m src.cleaning
python -m src.mcq
```

## 4. Lưu ý
- Không chỉnh sửa dữ liệu gốc trong `data/raw/`
- Không dùng dữ liệu ngoài bài thi
- Với forecasting, tránh data leakage và dùng validation theo thời gian
- Giữ `submission.csv` đúng format mẫu và đúng thứ tự dòng

---
**Status:** in progress  
**Competition:** DATATHON 2026 - Round 1
