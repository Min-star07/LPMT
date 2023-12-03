# -*- coding: utf-8 -*-

"""
@author: Min
@email: limin93@ihep.ac.cn
@file: read_database_to_csv.py
@time: 2022/11/7 14:26
"""

import pandas as pd
import numpy as np
import pymysql as ms
from pandas import DataFrame
from sqlalchemy import create_engine


def connect_database():
    #con = create_engine('mysql+pymysql://root:@localhost:3306/qualifiedlpmt')
    con = create_engine('mysql+pymysql://root:@localhost:3306/junopmt')
    try:
        sql = """show tables"""
        #sql = """select * from lpmt_veto_list where classification ='pole'""";
        #sql = """select SN, Mass_ID, Container_ID, Channel_ID,  DCR from lpmt_all where SN = "PA1706-419C" """;
        df = pd.read_sql_query(sql, con)
        print(df)
        #df.to_csv("test_juno.csv")

    except:
        print("Connect database failed")

    #con.close()
if __name__ == '__main__':
    connect_database()

