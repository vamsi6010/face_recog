from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn
# from face_dataset import *
# from trainer import *
from fastapi.middleware.cors import CORSMiddleware
import pyodbc
from datetime import datetime, date

server = "localhost"
database = "deep_vision"
username = "sa"
pwd = "G@krishna18"
# username = "rpos6"
# pwd = "t3m62uP@NZ"

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
from datetime import datetime

entrance_camera = "http://10.42.0.132:8080/video"
# 'Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.8.so.1.1};Server=' + server + ';Database=' + database + ';UID=' + username + ';PWD=' + pwd)}
# Driver={SQL SERVER}

def executeInsertQuery(query):
    conn = pyodbc.connect(
        'Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.8.so.1.1};Server=' + server + ';Database=' + database + ';UID=' + username + ';PWD=' + pwd)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()


def executeSelectQuery(query):
    conn = pyodbc.connect(
        'Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.8.so.1.1};Server=' + server + ';Database=' + database + ';UID=' + username + ';PWD=' + pwd)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result


@app.post("/login_start")
async def login_start(request: Request):
    customer_dtl = await request.json()
    # {"cid": "1","name": "Jeffrey"}
    print(datetime.now().strftime("%H:%M:%S"))
    customer_dtl["inStatus"] = "IN"  # {"cid": "1","name": "Jeffrey"}
    customer_dtl["inTime"] = datetime.now().strftime("%H:%M:%S")
    customer_dtl["tranDate"] = date.today()
    print(customer_dtl)
    # insert in sql table
    insert_q = "insert into customer_summary(trandate, cId, inTime, inStatus,custName) values('{}',{},'{}','{}','{}')".format(
        customer_dtl["tranDate"], customer_dtl["cid"], customer_dtl["inTime"], customer_dtl["inStatus"],
        customer_dtl["name"])

    print(insert_q)
    executeInsertQuery(insert_q)
    insert_q = "insert into customers(cId, cName) values('{}','{}')".format(customer_dtl["cid"],
                                                                            customer_dtl["name"])

    print(insert_q)
    executeInsertQuery(insert_q)
    # read_data(customer_dtl["cid"], entrance_camera)
    # faces, ids = getImagesAndLabels(path)
    # recognizer.train(faces, np.array(ids))
    # recognizer.write('trainer/trainer.yml')
    return "Success"


@app.post("/logout")
async def logout(request: Request):
    customer_dtl = await request.json()
    customer_dtl["outTime"] = datetime.now().strftime("%H:%M:%S")
    customer_dtl["inStatus"] = "OUT"
    customer_dtl["tranDate"] = date.today()
    # update in sql table
    update_q = "update customer_summary set outTime='{}',inStatus='OUT' where cId='{}' and trandate='{}'".format(
        customer_dtl["outTime"], customer_dtl["cid"], customer_dtl["tranDate"])
    print(update_q)
    executeInsertQuery(update_q)
    return "Success"


def extractResult(data):
    listval = data[0]
    tupleval = listval[0]
    return (tupleval)


@app.get("/fetch_name")
async def fetch_name():
    select_q = "select * from customers"
    print(select_q)
    cname = executeSelectQuery(select_q)
    print(cname)
    

    def extractValueFromQueryResult(data, fields):
        if fields == 0:
            listval = data[0]
            tupleval = listval[0]
            return (tupleval)
        else:
            json_query_result = []
            for rows in data:
                json_struct = {}
                for field, index in fields.items():
                    json_struct[field] = rows[index]
                json_query_result.append(json_struct)
            # print(json_query_result)
            return json_query_result

    return extractValueFromQueryResult(cname, {"cid": 0, "cName": 1})
    # custName=extractResult(cname)


@app.post("/cart_insert")
async def cart_insert(request: Request):
    customer_dtl = await request.json()
    insert_q = "insert into cart_values(cId, productId, qty, rate) values ('{}','{}','{}','{}')".format(
        customer_dtl["id"], customer_dtl["productId"], customer_dtl["qty"], customer_dtl["rate"])
    print(insert_q)
    executeInsertQuery(insert_q)
    return "success"


@app.post("/cart_update")
async def cart_update(request: Request):
    customer_dtl = await request.json()
    update_q = "update a set qty = {} from cart_Values a inner join customer_summary b on a.cId = b.cId where b.inStatus = 'IN' and b.cId = {} and a.productId = {}".format(
        customer_dtl["qty"], customer_dtl["id"], customer_dtl["productId"])
    executeInsertQuery(update_q)
    return "Success"


@app.post("/cartFetch")
async def cart(request: Request):
    customer_dtl = await request.json()
    select_q = "select a.cId, inStatus, productId from cart_values a inner join customer_summary b on a.cId = b.cId where a.cId = '{}' and inStatus = 'in'".format(
        customer_dtl["cid"])
    print(select_q)
    cname = executeSelectQuery(select_q)
    print(cname)
    fields = {"cid": 0, "status": 1, "itemid": 2}
    json_query_result = []
    for rows in cname:
        json_struct = {}
        for field, index in fields.items():
            json_struct[field] = rows[index]
        json_query_result.append(json_struct)
    print(json_query_result)
    return json_query_result

@app.post("/cartFetchAll")
async def cartFetchall(request: Request):
    # customer_dtl = await request.json()
    select_q="select a.cId, inStatus, productId from cart_values a inner join customer_summary b on a.cId = b.cId where inStatus = 'in'"
    cname = executeSelectQuery(select_q)
    print(cname)
    fields = {"cid": 0, "status": 1, "itemid": 2}
    json_query_result = []
    for rows in cname:
        json_struct = {}
        for field, index in fields.items():
            json_struct[field] = rows[index]
        json_query_result.append(json_struct)
    print(json_query_result)
    return json_query_result

@app.get("/metrics")
async def metrics(request: Request):
    conn = pyodbc.connect(
        'Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.8.so.1.1};Server=' + server + ';Database=' + database + ';UID=' + username + ';PWD=' + pwd)
    cursor = conn.cursor()
    stats = {}

    getCustInStore = "select distinct(count(cId))custInStore from customer_summary "
    getCustInStore += "where inStatus='IN'and trandate=convert(varchar,getdate(),23)"

    getUniqueCustomers = "select distinct(count(cId))custVisited from customer_summary "
    getUniqueCustomers += "where trandate=convert(varchar,getdate(),23) and inStatus='OUT'"

    getAverageTimeSpent = "select cast(cast(sum(datediff(minute,inTime,outTime))as numeric(18,2))/count(cId) as numeric(18,2)) avgTimeSpent from customer_summary"

    getOppurtunityLost = "select abs(sum(qty*rate)) oppurtunityLost from cart_values where qty<0"

    getProductReturnedtoShelf = "select top 3 productName,cart_values.productId,"
    getProductReturnedtoShelf += "count(cart_values.productId) occurrences,productUrl from cart_values "
    getProductReturnedtoShelf += "inner join products on cart_values.productId=products.productId where qty<0 "
    getProductReturnedtoShelf += "group by productName,cart_values.productId,rate,productUrl order by occurrences desc"

    getAttentionSeeks = "select top 3 productName,cart_values.productId, "
    getAttentionSeeks += "count(cart_values.productId) occurrences,productUrl "
    getAttentionSeeks += "from cart_values inner join products on cart_values.productId=products.productId "
    getAttentionSeeks += "group by productName,cart_values.productId,rate,productUrl order by occurrences desc"

    def executeQuery(query):
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def extractValueFromQueryResult(data, fields):
        if fields == 0:
            listval = data[0]
            tupleval = listval[0]
            return (tupleval)
        else:
            json_query_result = []
            for rows in data:
                json_struct = {}
                for field, index in fields.items():
                    json_struct[field] = rows[index]
                json_query_result.append(json_struct)
            # print(json_query_result)
            return json_query_result

    def genDictionary(keystr, value):
        stats[keystr] = value

    fields = {"itemName": 0, "itemCode": 1, "count": 2 , "imageSrc": 3,
"expiryDate": 4,"price": 5,"categoryName":6 , "Biscuits":7}
    fields1 = {"itemName": 0, "itemCode": 1, "count": 2,"imageUrl":3}
    keyVal = {'liveCount': (getCustInStore, 0), 'uniqueCustomers': (getUniqueCustomers, 0),
              "avgTimerPerCustomer": (getAverageTimeSpent, 0), "opportunityLost": (getOppurtunityLost, 0),
              "attentionSeekingProducts": (getProductReturnedtoShelf, fields1),
              "mostViewedProducts": (getAttentionSeeks, fields1)}
    for key, value in keyVal.items():
        query_result = executeQuery(value[0])
        extracted_value = extractValueFromQueryResult(query_result, value[1])
        genDictionary(key, extracted_value)
    print(stats)
    return  stats


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000, debug=True)
