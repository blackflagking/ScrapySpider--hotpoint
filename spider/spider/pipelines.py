# -*- coding: utf-8 -*-
import pymysql, settings

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SpiderPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host = settings.MYSQL_HOST,
            db = settings.MYSQL_DBNAME,
            user = settings.MYSQL_USER,
            passwd = settings.MYSQL_PASSWD,
            charset = 'utf8',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into hotbaidu(name, url) values (%s, %s)""", (item['bdname'], item['bdurl'])
            )
            self.cursor.execute(
            """insert into hot360(name, url) values (%s, %s)""",(item['name360'], item['url360'])
            )
            self.cursor.execute(
            """insert into hotweibo(name, url) values (%s, %s)""",(item['weiboname'], item['weibourl'])
            )

        except Exception as error:
            print error
            self.connect.rollback()
        else:
            self.connect.commit()

        return item
