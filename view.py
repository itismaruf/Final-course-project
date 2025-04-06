import duckdb

# Подключение к базе
conn = duckdb.connect("final_project.duckdb")

# Обновлённый SQL-запрос
query = """
DROP VIEW IF EXISTS city_demographics_view;

CREATE VIEW city_demographics_view AS
SELECT
    -- Уникальный ID для каждого города
    ROW_NUMBER() OVER () AS city_id,

    a.geographic_area AS state,
    a.city AS city,

    -- Чистка и преобразование poverty_rate
    CASE 
        WHEN a.poverty_rate ~ '^[0-9.]+$' THEN CAST(a.poverty_rate AS DOUBLE)
        ELSE NULL
    END AS poverty_rate,

    -- Категория уровня бедности
    CASE 
        WHEN a.poverty_rate ~ '^[0-9.]+$' AND CAST(a.poverty_rate AS DOUBLE) < 20 THEN 'low'
        WHEN a.poverty_rate ~ '^[0-9.]+$' AND CAST(a.poverty_rate AS DOUBLE) < 40 THEN 'medium'
        WHEN a.poverty_rate ~ '^[0-9.]+$' THEN 'high'
        ELSE NULL
    END AS poverty_level_category,

    -- Median Income
    CASE 
        WHEN b.median_income ~ '^[0-9]+$' THEN CAST(b.median_income AS INTEGER)
        ELSE NULL
    END AS median_income,

    -- Percent Completed HS
    CASE 
        WHEN c.percent_completed_hs ~ '^[0-9.]+$' THEN CAST(c.percent_completed_hs AS DOUBLE)
        ELSE NULL
    END AS percent_completed_hs,

    -- Расовая структура
    CASE 
        WHEN d.share_white ~ '^[0-9.]+$' THEN CAST(d.share_white AS DOUBLE)
        ELSE NULL
    END AS share_white,

    CASE 
        WHEN d.share_black ~ '^[0-9.]+$' THEN CAST(d.share_black AS DOUBLE)
        ELSE NULL
    END AS share_black,

    CASE 
        WHEN d.share_hispanic ~ '^[0-9.]+$' THEN CAST(d.share_hispanic AS DOUBLE)
        ELSE NULL
    END AS share_hispanic,

    CASE 
        WHEN d.share_asian ~ '^[0-9.]+$' THEN CAST(d.share_asian AS DOUBLE)
        ELSE NULL
    END AS share_asian,

    CASE 
        WHEN d.share_native_american ~ '^[0-9.]+$' THEN CAST(d.share_native_american AS DOUBLE)
        ELSE NULL
    END AS share_native_american

FROM
    MedianHouseholdIncome2015 a
JOIN
    PercentagePeopleBelowPovertyLevel b 
    ON a.city = b.city AND a.geographic_area = b.geographic_area
JOIN
    ShareRaceByCity c 
    ON a.city = c.city AND a.geographic_area = c.geographic_area
JOIN
    PoliceKillingsUS d
    ON a.city = d.city AND a.geographic_area = d.geographic_area;
"""

# Выполняем запрос
conn.execute(query)

print("✅ Вьюшка city_demographics_view обновлена с city_id и категорией бедности.")