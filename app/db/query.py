set_debugged_devices = """
    WITH debugged_devices AS (
        SELECT DISTINCT BD.id_brand, BD.mcc, BD.androidid
        FROM clean_brand_data BD
        INNER JOIN drone.devicedata2 DR
        ON (BD.androidid = DR.androidid 
            AND BD.id_brand= DR.brand_id)
        LEFT JOIN (
         SELECT B.id_brand, B.androidid
            FROM clean_brand_data B
            WHERE B.id_brand IN (99900120,
                99900119,
                9990082)
        ) cte
        ON(BD.androidid = cte.androidid)
        WHERE BD.updatedat is not null
            AND cte.androidid is  null
            AND (DR.is_archived is null OR not DR.is_archived)
            AND CASE WHEN BD.report -> :str_report_id @> :new_status
            THEN FALSE ELSE TRUE END
    )
    UPDATE clean_brand_data CBD
    SET report = CASE
            WHEN CBD.report IS NULL THEN :new_report_payload
            WHEN NOT CBD.report ? :str_report_id
            THEN CBD.report || :new_report_payload
            ELSE jsonb_insert(CBD.report, {report_id}, :new_status, true) END
    FROM debugged_devices devices
    WHERE CBD.androidid=devices.androidid
    AND CBD.id_brand=devices.id_brand
    AND CBD.mcc=devices.mcc
"""

# Update Debugged devices to sent a new partition
debbuged_devices = """
    WITH pre_data as (
        SELECT c.id_brand, d.androidid as androidid
        FROM drone.devicedata2 as d
            INNER JOIN clean_brand_data as c 
            ON (c.id_brand = d.brand_id and c.androidid = d.androidid)
        WHERE (not d.is_archived or d.is_archived is null)
        AND c.report -> :str_report_id @> :new_status
    )
    UPDATE clean_brand_data BD
    SET id_brand=(select pruned_id from oem where id=BD.id_brand limit 1)
    FROM pre_data as p
    where BD.id_brand = p.id_brand
    AND BD.androidid = p.androidid
    AND BD.updatedat is not null
    AND BD.report -> :str_report_id @> :new_status;
"""

count_debugged_devices = """
SELECT (SELECT oem_role FROM public.oem WHERE id=T.id_brand) AS brand,total
FROM (
    SELECT DISTINCT BD.id_brand, count(BD.androidid) as total
    FROM clean_brand_data BD
        INNER JOIN drone.devicedata2 DR
        ON (BD.androidid = DR.androidid 
            AND BD.id_brand= DR.brand_id)
    WHERE (DR.is_archived is null OR not DR.is_archived)
        AND BD.updatedat is not null
        AND NOT EXISTS (SELECT 1 FROM public.oem WHERE pruned_id=BD.id_brand)
        AND BD.report -> :str_report_id @> :new_status
    GROUP BY BD.id_brand
) T
"""

check_devices_archived = """
    WITH pre_data as (
        SELECT d.brand_id as id_brand, d.androidid as androidid
        FROM drone.devicedata2 as d
            INNER JOIN clean_brand_data as c
            ON (substr(cast(c.id_brand as text), 6, 3)::int = d.brand_id
            AND c.androidid = d.androidid)
        WHERE c.id_brand in (99900120, 99900119, 9990082)
        AND (not d.is_archived or d.is_archived is null)
        AND c.report -> :str_report_id @> :new_status
    )
    update drone.devicedata2 as d
    SET is_archived = true
    FROM pre_data as p
    WHERE p.id_brand = d.brand_id
    AND p.androidid = d.androidid;
"""