query = """
    SELECT
        *
    FROM
      stg_vex_schema.stg_vex_table1
    UNION ALL
    SELECT
      *
    FROM
      stg_vex_schema.stg_vex_table2
    """