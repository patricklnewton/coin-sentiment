from typing import Union
from fastapi import FastAPI
import psycopg2
from config import DB, USER, PW, HOST, PORT

app = FastAPI()

@app.get("/coins/{coin}")
def read_item(coin: str):
    res = get_records_by_coin(coin)
    return {"coins": res}



def get_records_by_coin(coin):
    json_response = []
    try:
        conn = psycopg2.connect(
            database = DB, 
            user = USER, 
            password = PW, 
            host = HOST, 
            port = PORT
        )
        cur = conn.cursor()
        cur.execute('SELECT date_created, positive, negative, neutral, compound, coin FROM sentiment WHERE coin=%s', (coin,))
        row = cur.fetchone()
        while row is not None:
            row = {
                'date_created': row[0],
                'positive': row[1],
                'negative': row[2],
                'neutral': row[3],
                'compound': row[4], 
                'coin': row[5]
            }
            json_response.append(row)
            row = cur.fetchone()
        conn.close()
        cur.close()
        return json_response
    except Exception as e: 
        print('error with database...', e)