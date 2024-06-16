import aiosqlite

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    async def setup(self):
        self.connection = await aiosqlite.connect(self.db_path)
        
    async def createTable(self,jsonData):
        tablename = str(jsonData['companyId'])+str(jsonData['frame'])
        query = f'''CREATE TABLE IF NOT EXISTS {tablename} ( ID INTEGER PRIMARY KEY AUTOINCREMENT, COMPANYID TEXT ,FRAME TEXT, OPEN NUMBER, HIGH NUMBER,LOW NUMBER, CLOSE NUMBER, VOLUME NUMBER )'''
        await self.connection.execute(query)
        await self.connection.commit()
        print(f'table {tablename} created successfully')
        

    async def insert(self, jsonData):
        tablename = str(jsonData['companyId'])+str(jsonData['frame'])
        query = f''' INSERT INTO {tablename}  (COMPANYID,FRAME,OPEN,HIGH,LOW,CLOSE,VOLUME) VALUES (?,?,?,?,?,?,?)'''
        await self.connection.execute(query,(jsonData['companyId'],jsonData['frame'],jsonData['open'],jsonData['high'],jsonData['low'],jsonData['close'],jsonData['volume']))
        await self.connection.commit()
        await self.printTable(tablename)
        
        
    async def printTable(self,tablename):
        query = 'SELECT * FROM '+tablename
        cursor = await self.connection.execute(query)
        rows = await cursor.fetchall()
        await cursor.close()
        for row in rows:
            print(row)
          
          
    async def delete_first_row(self,tablename):
        query = f'''DELETE FROM {tablename} WHERE ID = (SELECT ID FROM {tablename} ORDER BY ID LIMIT 1)'''
        await self.connection.execute(query)
        await self.connection.commit()
        
    async def fetch_table(self,tablename):
        query = f'''SELECT * FROM {tablename}'''
        cursor = await self.connection.execute(query)
        return cursor
        