from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn
#from face_dataset import *
#from trainer import *
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




if name == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000, debug=True)