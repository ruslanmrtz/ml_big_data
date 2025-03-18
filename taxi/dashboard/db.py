import sqlite3
import pandas as pd


def get_mean_passenger_count():
    con = sqlite3.connect('data/taxi.db')
    sql = '''select strftime('%Y-%m-%d', year || '-' || month || '-' || day)  as date, avg(passenger_count) as mean_passengers
    from taxi2019
    group by date
    union all
    select strftime('%Y-%m-%d', year || '-' || month || '-' || day)  as date, avg(passenger_count) as mean_passengers
    from taxi20
    group by date
    union all
    select strftime('%Y-%m-%d', year || '-' || month || '-' || day)  as date, avg(passenger_count) as mean_passengers
    from taxi2021
    group by date
    '''
    result = pd.read_sql(sql, con)
    con.close()
    return result


def get_mean_tip():
    con = sqlite3.connect('data/taxi.db')
    sql = ("select strftime('%m.%Y', date) as month_tip, avg(sum_amount) as mean_tip "
           "from "
           "(select strftime('%Y-%m-%d', year || '-' || month || '-' || day) as date,"
           "sum(tip_amount) sum_amount "
           'from taxi2019 '
           'order by date) '
           "group by month_tip "
           "union all "
            "select strftime('%m.%Y', date) as month_tip, avg(sum_amount) as mean_tip "
           "from "
           "(select strftime('%Y-%m-%d', year || '-' || month || '-' || day) as date,"
           "sum(tip_amount) sum_amount "
           'from taxi20 '
           'order by date) '
           "group by month_tip "
           "union all "
           "select strftime('%m.%Y', date) as month_tip, avg(sum_amount) as mean_tip "
           "from "
           "(select strftime('%Y-%m-%d', year || '-' || month || '-' || day) as date,"
           "sum(tip_amount) sum_amount "
           'from taxi2021 '
           'order by date) '
           "group by month_tip"
           )
    result = pd.read_sql(sql, con)
    con.close()
    return result


def get_week_amount(week):
    con = sqlite3.connect('data/taxi.db')
    sql = f"""SELECT PULocationID, SUM(total_amount)
                FROM taxi2021
                WHERE strftime('%W', year || '-' || printf('%02d', month) || '-' || printf('%02d', day)) = '{str(week).zfill(2)}'
                GROUP BY PULocationID
                    """
    result = pd.read_sql(sql, con)
    con.close()
    return result


def get_sum_passenger_count():
    con = sqlite3.connect('data/taxi.db')
    sql = '''select strftime('%Y-%m-%d', year || '-' || month || '-' || day)  as date, sum(passenger_count) as sum_passengers
    from taxi2019
    group by date
    union all
    select strftime('%Y-%m-%d', year || '-' || month || '-' || day)  as date, sum(passenger_count) as sum_passengers
    from taxi20
    group by date
    union all
    select strftime('%Y-%m-%d', year || '-' || month || '-' || day)  as date, sum(passenger_count) as sum_passengers
    from taxi2021
    group by date
    '''
    result = pd.read_sql(sql, con)
    result = result[result['sum_passengers'] < 1_000_000]
    con.close()
    return result


def get_week_count_by_type(week):
    con = sqlite3.connect('data/taxi.db')
    sql = f""" SELECT count(*) as all_count
    FROM taxi2019
    WHERE strftime('%W', year || '-' || printf('%02d', month) || '-' || printf('%02d', day)) = '{str(week).zfill(2)}'"""
    result = pd.read_sql(sql, con)
    all_week = result.values[0][0]

    sql = f"""
    select t.payment_type, round(count(1) * 100 / {all_week}, 3) 
            FROM taxi2019 t
                WHERE strftime('%W', t.year || '-' || printf('%02d', t.month) || '-' || printf('%02d', t.day)) = '{str(week).zfill(2)}'
            group by t.payment_type
                """

    result = pd.read_sql(sql, con)
    con.close()
    return result