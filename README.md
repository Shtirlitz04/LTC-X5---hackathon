# Структура ML-проекта
project/
│
├── data/                # Данные
│   ├── raw/             # Сырые данные (неизменные)
│   ├── processed/       # Обработанные данные
│   └── external/        # Внешние источники (если есть)
│
├── notebooks/           # Jupyter ноутбуки для экспериментов
│   ├── EDA.ipynb        # разведочный анализ данных
│   └── experiments.ipynb
│
├── src/                 # Основной код проекта
│   ├── data/            # загрузка и предобработка данных
│   │   └── make_dataset.py
│   ├── features/        # создание признаков
│   │   └── build_features.py
│   ├── models/          # обучение и инференс
│   │   ├── train_model.py
│   │   └── predict_model.py
│   └── utils/           # вспомогательные функции
│
├── models/              # сохранённые модели (pickle, joblib, h5)
│
├── reports/             # Отчёты и визуализации
│   ├── figures/
│   └── metrics.json
│
├── tests/               # Тесты (юнит и интеграционные)
│
├── configs/             # Конфигурации (YAML/JSON)
│   ├── train_config.yaml
│   └── model_config.yaml
│
├── requirements.txt     # зависимости
├── pyproject.toml       # или setup.py (если библиотека)
├── README.md            # описание проекта
└── .gitignore



# Описание для LTC-X5---hackathon

Файл submission.csv - пример для файла, который можно отправить в offline-оценку. Файл содержит предсказания базовой модели из инструкции.

Чтобы оценить модель команды необходимо составить такой же файл с предсказаниями модели.

> Важно: offline-оценка не попадает на лидерборд.
