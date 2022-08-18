import webbrowser
import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
from starlette.responses import FileResponse
from calculations import df_creator
from calculations import switcher
from calculations import yuzde_DF
from calculations import matrix_summation
from calculations import average_puan
endeks = 0
UzmanDF = {}
from models import uzman_list as Model_uzman_list

import os
from dotenv import load_dotenv

load_dotenv('environment.env')

app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

@app.on_event("startup")
async def startup_event():
    webbrowser.open("http://localhost:8000/matrixstartup/")

@app.get('/uzman_list/')
async def uzman_list():
    item = db.session.query(Model_uzman_list).all()
    return item

@app.get("/matrixstartup/")
async def matrixstartup():
    global endeks
    global UzmanDF
    uzmanList = await uzman_list()
    UzmanDF = df_creator(uzmanList)
    # matrix = yuzde_DF(df)
    # endeks = matrix_summation(matrix)
    return "API başlatıldı. Bu pencereyi kapatabilirsiniz."

@app.get("/switch_request/")
async def switch_request_handler(uzman_ids):
    global UzmanDF
    uzman_ids_list = uzman_ids.split(" ", 1)
    uzmanList = await uzman_list()
    UzmanDF = df_creator(uzmanList)
    SwitchedUzmanDF = switcher(UzmanDF, uzman_ids_list)
    average = average_puan(SwitchedUzmanDF)
    return average

@app.get("/ortalamaStart/")
async def ortalamaStart():
    global UzmanDF
    average = average_puan(UzmanDF)
    return average

@app.get("/UyumsuzlukEndeksi")
async def UyumsuzlukEndeksi(uzman_ids_list):
    uzmanList = await uzman_list()
    df = df_creator(uzmanList)
    average = average_puan(df)
    return average

@app.get('/favicon.ico')
async def favicon():
    return FileResponse("venv/Lib/favicon/favicon.ico")

# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)