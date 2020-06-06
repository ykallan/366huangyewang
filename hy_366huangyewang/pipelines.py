# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
pymysql.install_as_MySQLdb()


class Hy366HuangyewangPipeline(object):

    def __init__(self):
        self.conn = pymysql.Connect(
            host='localhost',
            port=3306,
            database='scrapy',
            user='root',
            passwd='root',
            charset='utf8',
        )

        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        self.cursor.execute('''INSERT INTO hy336(com_name, cont_person, cont_phone, loc, address_detail) VALUES(%s, %s, %s, %s, %s)''',
                            (item['com_name'], item['cont_person'], item['cont_phone'], item['loc'], item['address_detail']))
        self.conn.commit()
        return item

        # item['com_name'] = com_name
        # item['cont_person'] = cont_person
        # item['cont_phone'] = cont_phone
        # item['loc'] = loc
        # item['address_detail'] = address_detail

    def close(self, spider):

        pass
