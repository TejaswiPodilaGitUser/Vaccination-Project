def get_vaccination_coverage_top_bottom():
    return """
    (SELECT `NAME`, 
            ROUND(AVG(CAST(`COVERAGE` AS FLOAT)), 2) AS `Average Coverage`
     FROM `cleaned_coverage_data`
     WHERE `COVERAGE_CATEGORY` = 'official'
     GROUP BY `NAME`
     ORDER BY `Average Coverage` DESC
     LIMIT 10)
    UNION ALL
    (SELECT `NAME`, 
            ROUND(AVG(CAST(`COVERAGE` AS FLOAT)), 2) AS `Average Coverage`
     FROM `cleaned_coverage_data`
     WHERE `COVERAGE_CATEGORY` = 'official'
     GROUP BY `NAME`
     ORDER BY `Average Coverage` ASC
     LIMIT 10);
    """


def get_vaccination_and_disease_trends_grouped_by_area():
    return """
    SELECT 
        v.`NAME` AS `Area`,
        v.`YEAR`,
        COUNT(v.`COVERAGE`) AS `Record Count`,
        ROUND(AVG(CAST(v.`COVERAGE` AS FLOAT)), 2) AS `Average Vaccination Coverage`,
        ROUND(AVG(CAST(d.`INCIDENCE_RATE` AS FLOAT)), 2) AS `Average Disease Incidence`
    FROM 
        cleaned_coverage_data AS v
    JOIN 
        cleaned_incidence_rate AS d
    ON 
        v.YEAR = d.YEAR AND v.CODE = d.CODE
    WHERE 
        v.`COVERAGE_CATEGORY` = 'official'
    GROUP BY 
        v.`NAME`, v.`YEAR`
    HAVING 
        `Average Vaccination Coverage` IS NOT NULL AND `Average Disease Incidence` IS NOT NULL
    ORDER BY 
        v.`NAME`, v.`YEAR` ASC
    LIMIT 40;
    """


def get_highest_coverage_lowest_incidence_grouped_by_area():
    return """
    SELECT 
        v.`NAME` AS `Area`,
        ROUND(AVG(CAST(v.`COVERAGE` AS FLOAT)), 2) AS `Average Vaccination Coverage`,
        ROUND(AVG(CAST(d.`INCIDENCE_RATE` AS FLOAT)), 2) AS `Average Disease Incidence`
    FROM 
        cleaned_coverage_data AS v
    JOIN 
        cleaned_incidence_rate AS d
    ON 
        v.CODE = d.CODE
    WHERE 
        v.`COVERAGE_CATEGORY` = 'official'
    GROUP BY 
        v.`NAME`
    HAVING 
        `Average Vaccination Coverage` > 75 AND `Average Disease Incidence` < 10
    ORDER BY 
        `Average Disease Incidence` ASC
    LIMIT 10;
    """


def get_top_and_bottom_10_vaccination_coverage():
    return """
SELECT *
FROM (
    (SELECT `CODE`,
            ROUND(AVG(CAST(`COVERAGE` AS FLOAT)), 2) AS `Average_Coverage`, 
            'Top 10' AS `Category`
     FROM `cleaned_coverage_data`
     WHERE `COVERAGE_CATEGORY` = 'official'
     GROUP BY `CODE`
     LIMIT 10)
    UNION ALL
    (SELECT `CODE`,
            ROUND(AVG(CAST(`COVERAGE` AS FLOAT)), 2) AS `Average_Coverage`, 
            'Bottom 10' AS `Category`
     FROM `cleaned_coverage_data`
     WHERE `COVERAGE_CATEGORY` = 'official'
     GROUP BY `CODE`
     LIMIT 10)
) AS combined_results
ORDER BY `Category`, `Average_Coverage` DESC;
    """
