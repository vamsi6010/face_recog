from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn
from face_dataset import *

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)  # for our testing / replaced by order easy in future




@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        customerId = await websocket.receive_text()
        read_data(customerId)
        await websocket.send_text(f"Message text was: {customerId}")


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8005, debug=True)



"""
. order easy app  - train and work
. frame - start session - qr code - customerid+dt+start/stop
. post api - will get a post call
. 8 members -  customers
"""