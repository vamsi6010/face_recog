from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn
from face_dataset import *
from trainer import *
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
import datetime
import time
from fastapi import Request

entrance_camera = "http://10.42.0.109:8080/video"


@app.post("/login_start")
async def login_start(request: Request):
    customer_dtl = await request.json()
    # {"cid": "1","name": "Jeffrey"}
    customer_dtl["inStatus"] = "in",    # {"cid": "1","name": "Jeffrey"}

    customer_dtl["inTime"] = time.time(),
    customer_dtl["tranDate"]: datetime.date()
    # insert in sql table
    read_data(customer_dtl["cid"], entrance_camera)
    faces, ids = getImagesAndLabels(path)
    recognizer.train(faces, np.array(ids))
    recognizer.write('trainer/trainer.yml')
    return "Success"


@app.post("/logout")
async def logout(request:Request):
    customer_dtl = await request.json()
    customer_dtl["outTime"] = time.time()
    customer_dtl["inStatus"] = "out"
    # update in sql table
    return "Success"

@app.get("/fetch_name")
async def logout(request:Request):
    customer_dtl = await request.json()

@app.get("/cart")
async def cart(request: Request):
    response = [
{
"customerId": "1",
"status": "in",
"cart": [
{
"itemId": "2"
}
]
}
]
    return response


@app.get("/metrics")
async def metrics(request: Request):
    response = {
        "liveCount": 2,
        "uniqueCustomers": 12,
        "avgTimePerCustomer": 30,
        "oppurtunityLost": 17350,
        "attentionSeekingProducts": [
            {
                "itemCode": 10007,
                "itemName": "Unibic Choco Cookies",
                "count": 12
            },
            {
                "itemCode": 10107,
                "itemName": "Little Hearts",
                "count": 7
            },
            {
                "itemCode": 10117,
                "itemName": "Knorr Sweet and Corn Soup",
                "count": 5
            }
        ],
        "mostViewedProduct": "Kit Kat 250GM",
        "mostViewedProductCount": 23
    }

    return response




if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000, debug=True)
