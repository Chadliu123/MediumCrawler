import LinkAzureDB

server = 'blogerler-db-server.database.windows.net'
database = 'BloglerDB'
username = 'blogerler'
password = 'TibameAI04'
driver = 'ODBC DRIVER 17 for SQL Server'
DB = LinkAzureDB.OpAzureSQL(server, database, username, password, driver)
# DB.TestDB()

TitleList = ["Name", "Age", "City"]
ContentList = ["小夫", "15", "TC"]
DB.Insert("People", TitleList, ContentList)
DB.Edit("People", TitleList, ContentList, "Name='Fred'" )
wher=str("Name='小夫'")
# DB.Delete("People", wher )
print(DB.GetAllData("People"))