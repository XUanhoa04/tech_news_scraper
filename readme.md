# Tech News Scraper

Du an thu thap va phan tich tin tuc cong nghe tu VnExpress va Tuoi Tre.

## Mo ta

Du an su dung Python de tu dong scrape bai viet tu cac bao dien tu Viet Nam, luu vao database SQLite va xuat CSV. Kem theo Jupyter Notebooks de phan tich du lieu (EDA, phan tich tu khoa, xu huong).

## Cong nghe su dung

- Python 3.10+
- requests, BeautifulSoup4 (web scraping)
- SQLite, Pandas (luu tru & xu ly du lieu)
- Matplotlib, Seaborn (truc quan hoa)
- pytest (unit test)

## Cau truc thu muc

```
tech_news_scraper/
├── config/
│   └── settings.py          # Cau hinh URL, paths
├── data/
│   ├── raw/                 # CSV files
│   └── tech_news.db         # SQLite database
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_text_analysis.ipynb
│   └── 03_trend_analysis.ipynb
├── src/
│   ├── scrapers/
│   │   ├── base.py          # Lop co so
│   │   ├── vnexpress.py     # Scraper VnExpress
│   │   └── tuoitre.py       # Scraper Tuoi Tre
│   ├── pipeline.py          # Dieu phoi scraping
│   ├── storage.py           # Luu CSV + SQLite
│   └── main.py              # CLI
├── tests/
│   ├── test_scrapers.py
│   └── test_storage.py
└── requirements.txt
```

## Cai dat

```bash
pip install -r requirements.txt
```

## Cach su dung

### Thu thap du lieu

```bash
# Scrape tat ca nguon, 20 bai/danh muc
python src/main.py scrape

# Chi scrape VnExpress, 10 bai/danh muc
python src/main.py scrape --sources vnexpress --max 10

# Xem thong ke
python src/main.py stats
```

### Phan tich du lieu

```bash
jupyter notebook notebooks/
```

Mo tung notebook va chay tuan tu:
1. `01_data_exploration.ipynb` - Kham pha du lieu tong quan
2. `02_text_analysis.ipynb` - Phan tich tu khoa, tan suat
3. `03_trend_analysis.ipynb` - Xu huong bai viet theo thoi gian

### Chay tests

```bash
python -m pytest tests/ -v
```

## Nguon du lieu

| Nguon | Danh muc |
|-------|----------|
| VnExpress | khoa-hoc, so-hoa, kinh-doanh, the-gioi |
| Tuoi Tre | cong-nghe, kinh-te, the-gioi, nhip-song-so |

## Ky nang thuc hanh

- Web scraping (requests, BeautifulSoup, CSS selectors)
- OOP (Base class, Factory pattern)
- Data pipeline (ETL)
- SQL (SQLite)
- Data analysis (Pandas)
- Data visualization (Matplotlib, Seaborn)
- Unit testing (pytest, mock)
