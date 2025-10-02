```text
project-ner/
│
├── data/
│   ├── raw/
│   │   ├── train.csv
│   │   ├── submission.csv
│   │   └── close_submission.csv
│   └── processed/
│
├── docs/
│   └── ТЗ.pdf
│
├── models/
│   └── rubert_ner_v1/
│
├── notebooks/
│   └── rubert.ipynb
│
├── server/
│   ├── api/
│   │   ├── routes.py
│   │   └── __init__.py
│   ├── static/
│   │   └── index.html
│   ├── __init__.py
│   ├── main.py             # Основной файл для запуска сервера
│   ├── lifespan.py         # Управление жизненным циклом (загрузка модели)
│   ├── batcher.py          # Пакетная обработка запросов
│   └── schemas.py          # Схемы данных Pydantic для API
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── dataset.py
│   ├── model.py
│   └── train.py            # Код для ОБУЧЕНИЯ модели
│   
├── .gitignore
└── requirements.txt
```
