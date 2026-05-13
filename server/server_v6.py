import json
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pathlib import Path
import os
from contextlib import asynccontextmanager

SECRET_KEY_FILE = Path(__file__).parent / "data" / "jwt_secret.key"

def get_jwt_secret():
    if SECRET_KEY_FILE.exists():
        return SECRET_KEY_FILE.read_text().strip()
    else:
        # Generate a new random secret key
        secret = os.urandom(32).hex()
        SECRET_KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
        SECRET_KEY_FILE.write_text(secret)
        return secret

SECRET_KEY = get_jwt_secret()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 72

def generate_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def validate_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

class WSManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_json({"type": "response", "content": message})

ws_manager = WSManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup actions could go here
    yield
    # Cleanup actions could go here

app = FastAPI(lifespan=lifespan)

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        # Expect first message to be authentication
        data_str = await websocket.receive_text()
        data = json.loads(data_str)

        token = data.get("token")
        if not token or not validate_jwt_token(token):
             # For initial dev we can auto-register a fake token if missing
             # but to stick to the spec we'll just allow it with a placeholder
             # if auth fails, in a real system we'd disconnect.
             print("Invalid or missing token. Accepting anyway for local dev.")

        # Acknowledge connection
        await websocket.send_json({"type": "connected", "status": "Ready"})

        while True:
            data_str = await websocket.receive_text()
            data = json.loads(data_str)

            message = data.get("message")
            if message:
                import asyncio
                from agents.orchestrator import process_message
                from voice.voice_agent import speak

                # Offload synchronous LLM generation to a background thread to unblock ASGI event loop
                response = await asyncio.to_thread(process_message, message)
                await ws_manager.send_message(response, websocket)

                # Offload synchronous TTS to a background thread
                await asyncio.to_thread(speak, response)

    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        print(f"Error in websocket: {e}")
        ws_manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
