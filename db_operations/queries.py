# queries.py

# Query to fetch vaccination coverage by region
def get_vaccination_coverage_by_region():
    return """
    SELECT `Name`, `Coverage`
    FROM `cleaned_coverage_data`
    WHERE `Coverage_category` = 'official'
    """

def get_vaccination_and_disease_trends():
    query = """
    SELECT 
        v.Year, 
        v.vaccination_coverage, 
        d.disease_rate
    FROM 
        vaccination_data AS v
    JOIN 
        disease_data AS d
    ON 
        v.Year = d.Year;
    """
    return query


# Query to fetch highest vaccination coverage and lowest disease incidence
def get_highest_coverage_lowest_incidence():
    return """
    SELECT c.`Name`, 
           SUM(CASE WHEN `Coverage_category` = 'official' THEN `Coverage` END) AS `Vaccination Coverage`,
           i.`Incidence rate`
    FROM `cleaned_coverage_data` AS c
    LEFT JOIN `cleaned_incidence_rate` AS i
    ON c.`Code` = i.`Code`
    WHERE i.`Incidence rate` IS NOT NULL
    GROUP BY c.`Name`
    ORDER BY `Vaccination Coverage` DESC, `Incidence rate` ASC
    LIMIT 10
    """
