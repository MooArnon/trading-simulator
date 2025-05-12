WITH scope AS (
    select 
        position
    from read_parquet(
        's3://<S3_BUCKET>/<S3_PREFIX>/<PREDICTION_TABLE>/asset=<ASSET>/predicted_date=<PREDICTED_DATE>/*.parquet'
    )
    order by predicted_time desc
)
select
    position
    , count(1) as count
from scope
group by 1
;