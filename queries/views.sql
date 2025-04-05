-- View 1: Числовые данные для корреляции, распределений и статистики

DROP VIEW IF EXISTS city_demographics_view;

CREATE VIEW city_demographics_view AS
SELECT
    CASE 
        WHEN a.poverty_rate ~ '^[0-9.]+$' THEN CAST(a.poverty_rate AS DOUBLE)
        ELSE NULL
    END AS poverty_rate,

    CASE 
        WHEN b.median_income ~ '^[0-9]+$' THEN CAST(b.median_income AS INTEGER)
        ELSE NULL
    END AS median_income,

    CASE 
        WHEN c.percent_completed_hs ~ '^[0-9.]+$' THEN CAST(c.percent_completed_hs AS DOUBLE)
        ELSE NULL
    END AS percent_completed_hs,

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
    END AS share_asian

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


-- View 2
DROP VIEW IF EXISTS city_education_police_view;

CREATE VIEW city_education_police_view AS
SELECT
    a.city,
    a.geographic_area,

    CASE 
        WHEN a.percent_completed_hs ~ '^[0-9.]+$' THEN CAST(a.percent_completed_hs AS DOUBLE)
        ELSE NULL
    END AS percent_completed_hs,

    CASE 
        WHEN b.share_white ~ '^[0-9.]+$' THEN CAST(b.share_white AS DOUBLE)
        ELSE NULL
    END AS share_white,

    CASE 
        WHEN b.share_black ~ '^[0-9.]+$' THEN CAST(b.share_black AS DOUBLE)
        ELSE NULL
    END AS share_black,

    CASE 
        WHEN b.share_asian ~ '^[0-9.]+$' THEN CAST(b.share_asian AS DOUBLE)
        ELSE NULL
    END AS share_asian,

    CASE 
        WHEN b.share_hispanic ~ '^[0-9.]+$' THEN CAST(b.share_hispanic AS DOUBLE)
        ELSE NULL
    END AS share_hispanic,

    CAST(c.age AS DOUBLE) AS age,
    c.armed,
    c.race,
    c.gender,
    c.signs_of_mental_illness

FROM
    ShareRaceByCity a
JOIN
    PoliceKillingsUS b ON a.city = b.city AND a.geographic_area = b.geographic_area
JOIN
    PercentOver25CompletedHighSchool c ON a.city = c.city AND a.geographic_area = c.state;