WITH prediction_scope AS (
    select 
        predicted_time
        , position
    from read_parquet(
        's3://<S3_BUCKET>/<S3_PREFIX>/<PREDICTION_TABLE>/asset=<ASSET>/predicted_date=<PREDICTED_DATE>/*.parquet'
    )
),
raw_scope AS (
    select 
        TO_TIMESTAMP(open_time/1000) AT TIME ZONE 'UTC' as open_time
        , CAST(open AS FLOAT) as open
    from read_parquet(
        's3://<S3_BUCKET>/<S3_PREFIX>/<RAW_TABLE>/asset=<TICKER>/open_date=<PREDICTED_DATE>/*.parquet'
    )
    order by open_time
),
labeled AS (
    select 
        open_time
        , open
        , lead(open) over (order by open_time) as next_open
        , case 
            when LEAD(open) over (order by open_time) > open then 'LONG'
            when LEAD(open) over (order by open_time) < open then 'SHORT'
            else 'NEUTRAL'
        end as position_label
    from raw_scope
),
prediction_and_actual AS(
    select
        labeled.open_time
        , labeled.open
        , labeled.next_open - labeled.open as diff
        , position_label as actual_position
        , prediction_scope.predicted_time
        , prediction_scope.position as predicted_position
        , case
                when position_label:: varchar = predicted_position:: varchar then 'correct'
                when position_label:: varchar <> predicted_position:: varchar then 'wrong'
            end as result
    from labeled
        join prediction_scope
            on prediction_scope.predicted_time = labeled.open_time:: timestamp
),
pnl as (
    select
        open_time
        , open
        , diff
        , case
                when result = 'correct' and diff > 0 then diff
                when result = 'correct' and diff < 0 then abs(diff)
                when result = 'wrong' and diff > 0 then -1*diff
                when result = 'wrong' and diff < 0 then diff
            end as pnl
        , actual_position
        , predicted_position
        , result
    from prediction_and_actual
    order by open_time
),
summary AS (
    SELECT
        COUNT(*) AS total,
        COUNT(*) FILTER (WHERE result = 'correct') AS correct,
        ROUND(100.0 * COUNT(*) FILTER (WHERE result = 'correct') / COUNT(*), 2) AS accuracy_percent,
        SUM(pnl) AS total_pnl
    FROM pnl
)
SELECT * FROM summary
;