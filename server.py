import asyncio
import json
import pandas as pd
from Database import Database


class Server:
    def __init__(self, host, port, database):
        self.host = host
        self.port = port
        self.database = database
        
    async def fetch_table_as_dataframe(self,tablename):
        cursor = await self.database.fetch_table(tablename)
        rows = await cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        await cursor.close()
        df = pd.DataFrame(rows, columns=column_names)
        if(len(df)>5):
            await self.database.delete_first_row(tablename)
        return df
        
    
    async def handle_request(self, reader, writer):
        while True:
            try:
                # Read data from client
                message = await reader.read(1024)
                data = message.decode()
                print(data)

                # Parse JSON data
                data = json.loads(data)
                if data['protocol'] == 1:
                    await self.database.createTable(data)
                else:
                    await self.database.insert(data)

                # Send response to client
                response = await self.fetch_table_as_dataframe('AAPL1Min')
                response = response.iloc[-1]
                writer.write(str(response.to_json()).encode())
                await writer.drain()

            except Exception as e:
                response = f"Error: {str(e)}"
                writer.write(response.encode())
                await writer.drain()

    async def start_server(self):
        server = await asyncio.start_server(self.handle_request, self.host, self.port)
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Server is running .... {addrs}')

        async with server:
            await server.serve_forever()

async def main():
    db = Database(':memory:')
    await db.setup()

    server = Server('localhost', 8888, db)
    await server.start_server()

if __name__ == '__main__':
    asyncio.run(main())
