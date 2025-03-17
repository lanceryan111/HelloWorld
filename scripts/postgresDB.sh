SELECT start_time, build_duration_ms
FROM build
WHERE build_result = 'SUCCESS'
  AND job_name = 'td-ca-android-banking'
  AND LOWER(branch_type) = 'master'
  AND start_time >= '2024-03-06'
ORDER BY start_time DESC;