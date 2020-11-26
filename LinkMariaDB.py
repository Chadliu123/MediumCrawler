import pymysql
import csv
import codecs


class OpMariaSQL:
    DataBase = None
    Link = None

    def __init__(self, hostName: str, portNum: str, username: str, password: str, DBName: str, CharSet: str):
        """
        與資料庫建立連線
        :param hostName: hostName(IP)
        :param portNum: portNum(3306)
        :param username: 使用者名稱
        :param password: 使用者密碼
        :param DBName: DB名稱
        :param CharSet: "utf8"
        """

        self.Link = pymysql.connect(
            host=hostName,
            port=portNum,
            user=username,
            password=password,
            db=DBName,
            charset=CharSet
        )
        self.DataBase = self.Link.cursor()

    def Insert(self, DataTableName, TitleList, ValueList):
        # "INSERT INTO `news` (`title`,`source`,`create_time`,`description`,`web_url`)"+
        # "VALUES('aaa','aaa','2020-09-08','aaa','http://google.com/')"
        # try:
        TitleCmd = ""
        times = 0
        for Title in TitleList:
            if times == 0:
                TitleCmd = Title
            else:
                TitleCmd += "," + Title + ""
            times += 1

        ValuesCMD = ""
        times = 0
        for Value in ValueList:
            if times == 0:
                ValuesCMD = "'" + Value + "'"
            else:
                ValuesCMD += ",'" + Value + "'"
            times += 1

        Commend = "INSERT INTO " + DataTableName + " (" + TitleCmd + ")" + " VALUES(" + ValuesCMD + ")"

        print("InsertCommend:" + Commend)
        self.DataBase.execute(Commend)

        self.Link.commit()

    # except:
    # 	pass

    def Edit(self, DataTableName, TitleList, ValueList, where):
        """
        編輯資料內容，以where指定編輯位址
        :param DataTableName: DataTable名稱
        :param TitleList: DataTable欄位(column)名稱List
        :param ValueList: 欲編輯資料每個欄位(column)的List
        :param where: 更新條件(SQL指令:WHERE之後)
        :return:
        """
        # try:
        EditCmd = ""
        times = 0
        while times < len(TitleList):
            if times == 0:
                EditCmd += TitleList[times] + "='" + ValueList[times] + "'"
            else:
                EditCmd += "," + TitleList[times] + "='" + ValueList[times] + "'"
            times += 1

        Cmd = "UPDATE " + DataTableName + " SET " + EditCmd + " WHERE " + where
        print("EditCmd:", Cmd)
        self.DataBase.execute(Cmd)
        self.Link.commit()

    # UPDATE `test` SET `value1`='bb', `value2`='cc', `value3`='dd' WHERE `number`>'5'
    # except:
    # 	pass
    def Delete(self, DataTableName, where):
        """
        刪除資料內容，以where指定刪除輯位址
        :param DataTableName: DataTable名稱
        :param where: 刪除條件(SQL指令:WHERE之後)
        :return:
        """
        # DELETE FROM 資料表名稱 WHERE 篩選條件
        # DELETE FROM `test` WHERE `name` ='aa' AND (`month` >'5' OR `day` <'7')
        # try:
        Cmd = "DELETE FROM " + DataTableName + " WHERE " + where
        print("DeleteCmd:", Cmd)
        self.DataBase.execute(Cmd)
        self.Link.commit()

    # except:
    # 	pass
    def Find(self):
        """
        目前未使用
        :return:
        """
        # SELECT 欄位名1,欄位名2… FROM 資料表名稱 WHERE 篩選條件
        # "SELECT * FROM `news`"
        # SELECT `value1`, `value2`, `value3` FROM `test` WHERE `value3`>'5'
        # SELECT * FROM `test` WHERE `value3`>'5'

        # SELECT 欄位名1,欄位名2… FROM 資料表名稱 WHERE 篩選條件 ORDER BY 排序欄位 排序方式

        # SELECT * FROM `test` WHERE `number`>'5' ORDER BY `value` ASC
        # SELECT * FROM `test` WHERE `number`>'5' ORDER BY `value` DESC

        pass

    def GetAllData(self, DataTableName):
        """
        回傳DataTable內所有資料
        :param DataTableName:
        :return: 所有資料List
        """
        Cmd = "SELECT * FROM " + DataTableName
        # print("GetAllDataCmd:"+Cmd)
        self.DataBase.execute(Cmd)

        data = self.DataBase.fetchall()  # 取全部，或取fetchone剩下的資料
        return data

    def IntputFindCmd(self, Cmd):
        """
        輸入SQL指令，輸出符合條件的資料
        :rtype: object
        :param Cmd: SQL指令
        :return: 資料List
        """
        print("IntputFindCmd:\n", Cmd)
        self.DataBase.execute(Cmd)
        data = self.DataBase.fetchall()  # 取全部，或取fetchone剩下的資料
        return data

    def IntputFindCmdToCSV(self, Cmd, FilePath):
        """
        輸入SQL指令，輸出符合條件的資料
        :param Cmd: SQL指令
        :return: 資料List
        """
        print("IntputFindCmdToCSV:\n", Cmd)
        self.DataBase.execute(Cmd)
        data = self.DataBase.fetchall()  # 取全部，或取fetchone剩下的資料

        with open(FilePath, "w", encoding="utf-16", newline="") as f:
            writer = csv.writer(f)
            for a in data:
                writer.writerow(a)

        return data

    def TestDB(self):
        """
        測試是否連線成功，成功Print版本號
        :return:
        """
        # Sample select query
        self.DataBase.execute("SELECT @@version;")
        row = self.DataBase.fetchone()
        while row:
            print(row[0])
            row = self.DataBase.fetchone()

    def CreateNewDatabale(self):
        self.DataBase.execute('''

                       CREATE TABLE People
                       (
                       Name nvarchar(50),
                       Age int,
                       City nvarchar(50)
                       )

                       ''')
        self.Link.commit()
        return 0

    def CloseDB(self):
        self.DataBase.close()
        self.Link.close()

    def __LoadCSV(self, CSVPath):
        with open(CSVPath, encoding="utf-8") as csvfile:
            # 讀取 CSV 檔案內容
            rows = csv.reader(csvfile)
            # 以迴圈輸出每一列
            times = 0
            for row in rows:
                if row[0] == "id":
                    Title = row
                    continue
                times += 1
                print(row[10])
                print(times)
                cmd = f"SELECT [id],[article_type] FROM main WHERE id = '{str(row[0])}'"
                DBdata = self.IntputFindCmd(cmd)
                print(DBdata)

                if str(DBdata[0][1]) != str(row[10]):
                    WHERE = f"id='{row[0]}'"
                    self.Edit("main", Title[10:11], ["-1"], WHERE)
                    cmd = f"SELECT [id],[article_type] FROM main WHERE id = '{str(row[0])}'"
                    DBdata = self.IntputFindCmd(cmd)
                    print("Edit:", DBdata)

        pass

# server = 'blogerler-db-server.database.windows.net'
# database = 'BloglerDB'
# username = 'blogerler'
# password = 'TibameAI04'
# driver = 'SQL Server'
# # DB = OpAzureSQL(server, database, username, password, driver)
# pyodbc.connect('driver={%s};server=%s;database=%s;uid=%s;pwd=%s' % (driver, server, database, username, password))
# DB.TestDB()

# cursor.execute("SELECT @@version;")
# row = cursor.fetchone()
# while row:
#     print(row[0])
#     row = cursor.fetchone()
