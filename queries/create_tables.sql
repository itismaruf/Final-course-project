-- Удаляем таблицы, если они уже существуют
DROP TABLE IF EXISTS MedianHouseholdIncome2015;
DROP TABLE IF EXISTS PercentagePeopleBelowPovertyLevel;
DROP TABLE IF EXISTS PercentOver25CompletedHighSchool;
DROP TABLE IF EXISTS PoliceKillingsUS;
DROP TABLE IF EXISTS ShareRaceByCity;

-- Создаём таблицы (структура автоматически определяется при загрузке через Pandas)
CREATE TABLE MedianHouseholdIncome2015 AS SELECT * FROM df;
CREATE TABLE PercentagePeopleBelowPovertyLevel AS SELECT * FROM df;
CREATE TABLE PercentOver25CompletedHighSchool AS SELECT * FROM df;
CREATE TABLE PoliceKillingsUS AS SELECT * FROM df;
CREATE TABLE ShareRaceByCity AS SELECT * FROM df;

-- Данные загружаются и обрабатываются в Python через DuckDB
-- Подробнее см. в файле ddl.py