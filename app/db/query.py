set_debugged_devices = """
    WITH debugged_devices AS (
        SELECT DISTINCT BD.id_brand, BD.mcc, BD.androidid
        FROM clean_brand_data BD
        INNER JOIN cota_mcc_mnc cmm ON
                    BD.mcc = cmm.mcc
                    AND BD.mnc = cmm.mnc
        LEFT JOIN (
         SELECT B.id_brand, B.androidid
            FROM clean_brand_data B
            WHERE B.id_brand IN (99900120,
                99900119,
                9990082)
        ) cte
        ON(BD.androidid = cte.androidid)
        WHERE BD.updatedat is not null
            AND NOT EXISTS (SELECT 1 FROM public.oem WHERE pruned_id=BD.id_brand)
            AND cte.androidid is  null
            AND CASE WHEN BD.report -> :str_report_id @> :new_status
            THEN FALSE ELSE TRUE END
    )
    UPDATE clean_brand_data CBD
    SET report = CASE
            WHEN CBD.report IS NULL THEN :new_report_payload
            WHEN NOT CBD.report ? :str_report_id
            THEN CBD.report || :new_report_payload
            ELSE jsonb_insert(CBD.report, {report_id}, :new_status, true) END
    FROM (
            SELECT DD.*
            FROM debugged_devices DD
            INNER JOIN drone.devicedata DR
            ON (DD.androidid = DR.androidid 
            AND DD.id_brand= DR.brand_id)
    ) devices
    WHERE CBD.androidid=devices.androidid
    AND CBD.id_brand=devices.id_brand
    AND CBD.mcc=devices.mcc
    AND CASE WHEN CBD.report -> :str_report_id @> :new_status
    THEN FALSE ELSE TRUE END
"""

# Update Debugged devices to sent a new partition
debbuged_devices = """
    UPDATE clean_brand_data BD
    SET id_brand=(select pruned_id from oem where id=BD.id_brand limit 1)
    WHERE BD.updatedat is not null
    AND BD.report -> :str_report_id @> :new_status
    AND NOT EXISTS (SELECT 1 FROM public.oem WHERE pruned_id=BD.id_brand)
"""

count_debugged_devices = """
SELECT (SELECT oem_role FROM public.oem WHERE id=T.id_brand) AS brand,total
FROM (
    SELECT DISTINCT id_brand, count(androidid) as total
    FROM clean_brand_data BD
    INNER JOIN cota_mcc_mnc cmm ON
                BD.mcc = cmm.mcc
                AND BD.mnc = cmm.mnc
    WHERE BD.updatedat is not null
        AND NOT EXISTS (SELECT 1 FROM public.oem WHERE pruned_id=BD.id_brand)
        AND BD.report -> :str_report_id @> :new_status
    GROUP BY id_brand
) T
"""