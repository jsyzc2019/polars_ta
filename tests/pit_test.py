import polars as pl

from polars_ta.utils.pit import ts_pit
from polars_ta.wq.time_series import ts_mean

PATH_STEP0_INPUT1 = r'M:\data\jqresearch\get_fundamentals_balance'
# PATH_STEP0_INPUT1 = r'M:\data\jqresearch\get_fundamentals_cash_flow'
# PATH_STEP0_INPUT1 = r'M:\data\jqresearch\get_fundamentals_income'
# PATH_STEP0_INPUT1 = r'M:\data\jqresearch\get_fundamentals_indicator'

df1 = pl.read_parquet(PATH_STEP0_INPUT1, use_pyarrow=True)

# 格式处理
df1 = df1.with_columns([pl.col('pubDate').str.strptime(pl.Date, "%Y-%m-%d"),
                        pl.col('statDate').str.strptime(pl.Date, "%Y-%m-%d")]).drop('statDate.1')


def func(df: pl.DataFrame):
    df = df.with_columns(
        ts_mean(pl.col('id')).alias('test1')
    )
    return df


if __name__ == '__main__':
    d = df1.group_by('code').map_groups(lambda x: ts_pit(x, funcs=(func,), date='statDate', update_time='pubDate'))
    print(d.tail())