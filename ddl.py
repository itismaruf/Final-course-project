import pandas as pd
import glob
import re
import duckdb

# Путь к файлам CSV
files = glob.glob('/Users/mac/Desktop/Папки/Final Project (Zypl)/source/*.csv')

# Список имён для DataFrame
dataframe_names = [
    "MedianHouseholdIncome2015",
    "PercentagePeopleBelowPovertyLevel",
    "PercentOver25CompletedHighSchool",
    "PoliceKillingsUS",
    "ShareRaceByCity"
]

# Читаем CSV в DataFrame
dataframes_dict = {name: pd.read_csv(file, encoding='latin1') for name, file in zip(dataframe_names, files)}

# Функция нормализации имен колонок
def normalize_column_names(df):
    df.columns = [re.sub(r'[^a-zA-Z0-9]', '_', col.strip()).lower() for col in df.columns]
    return df

# Применяем нормализацию имен столбцов
normalized_dataframes = {name: normalize_column_names(df) for name, df in dataframes_dict.items()}

# Создаём базу данных DuckDB и загружаем данные
db_path = "final_project.duckdb"

with duckdb.connect(db_path) as con:
    for name, df in normalized_dataframes.items():
        con.execute(f"DROP TABLE IF EXISTS {name}")  # Удаляем таблицу, если она уже есть
        con.execute(f"CREATE TABLE {name} AS SELECT * FROM df")

print("✅ Загружены таблицы с нормализованными именами столбцов.")