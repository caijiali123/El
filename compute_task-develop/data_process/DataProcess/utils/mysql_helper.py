import pymysql
from sqlalchemy.dialects.mysql import insert


# 定义数据库连接类
class MysqlHelper(object):
    # 定义空连接
    conn = None

    # 初始化变量及类
    def __init__(self, host, username, password, db, charset='utf8', port=3306):
        self.cursor = None
        self.host = host  # 数据库地址
        self.username = username  # 数据库用户名
        self.password = password  # 数据库密码
        self.db = db  # 数据库名称
        self.charset = charset  # 数据库字符集
        self.port = port  # 数据库端口

    # 连接数据库
    def connect(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.username,
                                        password=self.password, db=self.db, charset=self.charset)
            # 初始化数据库游标, 这里返回的是字典对象, json
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            return True
        except Exception as e:
            print(e)
            return False

    # 释放数据库
    def close(self):
        # 释放数据游标
        self.cursor.close()
        # 关闭数据库
        self.conn.close()

    # 获取数据库返回集中第一条记录
    def get_one(self, sql):
        # 定义空数据集
        result = None
        try:
            if "SELECT" in str(sql).upper():  # 检测是否为查询语句
                self.cursor.execute(sql)  # 执行查询命令
                result = self.cursor.fetchone()  # 返回第一条记录
        except Exception as e:
            print(e)
        return result

    # 返回全部数据集合
    def get_all(self, sql):
        # 定义数据列表集合
        list_data = ()
        try:
            if "SELECT" in str(sql).upper():  # 检测是否为查询语句
                self.cursor.execute(sql)  # 执行查询命令
                list_data = self.cursor.fetchall()  # 返回全部记录
        except Exception as e:
            print(e)
        return list_data

    # 执行插入语句
    def insert(self, sql, params=()):
        if "INSERT" in str(sql).upper():  # 检测是否为插入语句
            return self.__edit(sql, params)
        else:
            return None

    # 执行数据库更新
    def update(self, sql, params=()):
        if "UPDATE" in str(sql).upper():  # 检测是否为更新语句
            return self.__edit(sql, params)
        else:
            return None

    # 执行数据删除
    def delete(self, sql, params=()):
        if "DELETE" in str(sql).upper():  # 检测是否为删除语句
            return self.__edit(sql, params)
        else:
            return None

    # 执行其他特殊命令 慎用
    def cmd_sql(self, sql, params=()):
        return self.__edit(sql, params)

    # 执行命令函数
    def __edit(self, sql, params):
        # 定义影响行数
        count = 0
        try:
            self.connect()  # 连接数据库
            count = self.cursor.execute(sql, params)  # 执行数据库命令语句
            self.conn.commit()  # 把命令推送到服务器
            self.close()  # 释放数据库
        except Exception as e:
            print(e)
        return count  # 返回受影响的行数

    def execute_custom_args(self, sql, params=None, exe_many=False):
        res = self.connect()
        if not res:
            return False
        cnt = 0
        try:
            if self.conn and self.cursor:
                if exe_many:
                    cnt = self.cursor.executemany(sql, params)
                else:
                    cnt = self.cursor.execute(sql, params)
                self.conn.commit()
        except Exception as e:
            print(e)
            return False
        self.close()
        return cnt

    def insert_custom_args(self, **kwargs):
        """
        table：必填，表名，如：table="test_table"
        data ：必填，更新数据，字典类型，如：data={"aaa": "666", "bbb": "888"}
        """
        table = kwargs["table"]
        data = kwargs["data"]
        sql = "insert into %s (" % table
        fields = ""
        values = []
        flag = ""
        for k, v in data.items():
            fields += "%s," % k
            values.append(str(v))
            flag += "%s,"
        fields = fields.rstrip(",")
        values = tuple(values)
        flag = flag.rstrip(",")
        sql += fields + ") values (" + flag + ");"

        try:
            self.execute(sql, values)
            # 获取自增id
            res = self.cursor.lastrowid
            return res
        except Exception as e:
            print(e)
            self.conn.rollback()

        return 0

    def delete_custom_args(self, **kwargs):
        """
        table：必填，表名，如：table="test_table"
        where：必填，删除条件，字典类型用于=，如：where={"aaa": 333, "bbb": 2}；字符串类型用于非等于判断，如：where="aaa>=333"
        """
        table = kwargs["table"]
        where = kwargs["where"]
        sql = "delete from %s where 1=1" % (table)
        values = []
        if type(where) == dict:
            for k, v in where.items():
                sql += " and {} in (%s)".format(k)
                values.append(str(v))
        elif type(where) == str:
            sql += " and %s" % where
        sql += ";"
        values = tuple(values)

        try:
            self.execute(sql, values)
            rowcount = self.cursor.rowcount
            return rowcount
        except Exception as e:
            print(e)
            self.conn.rollback()
        return 0

    def update_custom_args(self, **kwargs):
        """
        table：必填，表名，如：table="test_table"
        data ：必填，更新数据，字典类型，如：data={"aaa": "666'6", "bbb": "888"}
        where：必填，更新条件，字典类型用于=，如：where={"aaa": 333, "bbb": 2}；字符串类型用于非等于判断，如：where="aaa>=333"
        """
        table = kwargs["table"]
        data = kwargs["data"]
        where = kwargs["where"]
        sql = "update %s set " % table
        values = []
        for k, v in data.items():
            sql += "{}=%s,".format(k)
            values.append(str(v))
        sql = sql.rstrip(",")
        sql += " where 1=1 "
        if type(where) == dict:
            for k, v in where.items():
                sql += " and {} in (%s)".format(k)
                values.append(str(v))
        elif type(where) == str:
            sql += " and %s" % where
        sql += ";"
        values = tuple(values)

        try:
            self.execute(sql, values)
            rowcount = self.cursor.rowcount
            return rowcount
        except Exception as e:
            print(e)
            self.conn.rollback()

        return 0

    def get_one_custom_args(self, **kwargs):
        """
        table：必填，表名，如：table="test_table"
        where：必填，查询条件，字典类型用于=，如：where={"aaa": 333, "bbb": 2}；字符串类型用于非等于判断，如：where="aaa>=333"
        field： 非必填，查询列名，字符串类型，如：field="aaa, bbb"，不填默认*
        order： 非必填，排序字段，字符串类型，如：order="ccc"
        sort：  非必填，排序方式，字符串类型，如：sort="asc"或者"desc"，不填默认asc
        """
        table = kwargs["table"]
        field = "field" in kwargs and kwargs["field"] or "*"
        where = kwargs["where"]
        order = "order" in kwargs and "order by " + kwargs["order"] or ""
        sort = kwargs.get("sort", "asc")
        if order == "":
            sort = ""
        sql = "select %s from %s where 1=1 " % (field, table)
        values = []
        if type(where) == dict:
            for k, v in where.items():
                sql += " and {} in (%s)".format(k)
                values.append(str(v))
        elif type(where) == str:
            sql += " and %s" % where
        sql += " %s %s limit 1;" % (order, sort)
        values = tuple(values)

        try:
            self.execute(sql, values)
            data = self.cursor.fetchone()
            return data
        except Exception as e:
            print(e)
            self.conn.rollback()

        return ()

    def get_all_custom_args(self, **kwargs):
        """
        table：必填，表名，如：table="test_table"
        where：必填，查询条件，字典类型用于=，如：where={"aaa": 333, "bbb": 2}；字符串类型用于非等于判断，如：where="aaa>=333"
        field： 非必填，查询列名，字符串类型，如：field="aaa, bbb"，不填默认*
        order： 非必填，排序字段，字符串类型，如：order="ccc"
        sort：  非必填，排序方式，字符串类型，如：sort="asc"或者"desc"，不填默认asc
        offset：非必填，偏移量，如翻页，不填默认0
        limit： 非必填，条数，不填默认100
        """
        table = kwargs["table"]
        field = "field" in kwargs and kwargs["field"] or "*"
        order = "order" in kwargs and "order by " + kwargs["order"] or ""
        sort = kwargs.get("sort", "asc")
        if order == "":
            sort = ""
        where = kwargs["where"]
        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 100)
        sql = "select %s from %s where 1=1 " % (field, table)
        values = []
        if type(where) == dict:
            for k, v in where.items():
                sql += " and {} in (%s)".format(k)
                values.append(str(v))
        elif type(where) == str:
            sql += " and %s" % where
        values = tuple(values)
        sql += " %s %s limit %s, %s;" % (order, sort, offset, limit)

        try:
            self.execute(sql, values)
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            print(e)
            self.conn.rollback()

        return ()

    def get_count_custom_args(self, **kwargs):
        """
        table：必填，表名，如：table="test_table"
        where：必填，查询条件，字典类型用于=，如：where={"aaa": 333, "bbb": 2}；字符串类型用于非等于判断，如：where="aaa>=333"
        """
        table = kwargs["table"]
        where = kwargs["where"]
        sql = "select count(1) as count from %s where 1=1 " % (table)
        values = []
        if type(where) == dict:
            for k, v in where.items():
                sql += " and {} in (%s)".format(k)
                values.append(str(v))
        elif type(where) == str:
            sql += " and %s;" % where
        values = tuple(values)

        try:
            self.execute(sql, values)
            data = self.cursor.fetchone()
            return data[0]
        except Exception as e:
            print(e)
            self.conn.rollback()

        return 0

    # see
    # https://www.appsloveworld.com/mysql/100/10/pandas-to-sql-fails-on-duplicate-primary-key#:~:text=Pandas%20to_sql%20fails%20on%20duplicate%20primary%20key-mysql%20score%3A0,a%20table%20that%20has%20a%20primary%20key%20constraint.
    def insert_on_duplicate(self, table, conn, keys, data_iter):
        insert_stmt = insert(table.table).values(list(data_iter))
        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(insert_stmt.inserted)
        print(on_duplicate_key_stmt)
        conn.execute(on_duplicate_key_stmt)
