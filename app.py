from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://pornokuningad.pro",
]

# ✅ Correct way to add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOG_FILE_PATH = "flashcrash_logs.log"
ALERT_FILE_PATH = "alerts.log"

def tail_log(path, n_lines=50):
    try:
        with open(path, 'rb') as f:
            f.seek(0, 2) # Moves to the end of the file
            size = f.tell() # File size
            block = 1024 # How many bytes to read at a time
            data = b'' # Byte sequence
            while size > 0 and data.count(b'\n') <= n_lines:
                seek_size = min(block, size)
                f.seek(-seek_size, 1)
                data = f.read(seek_size) + data
                f.seek(-seek_size, 1)
                size -= seek_size
            lines = b'\n'.join(data.splitlines()[-n_lines:]).decode(errors="replace").split('\n')
            return lines[::-1]
    except Exception as e:
        return f"Error reading log {e}"

@app.get("/log")
def read_log():
    log_lines = tail_log(LOG_FILE_PATH)
    return log_lines

@app.get("/alerts")
def read_log():
    log_lines = tail_log(ALERT_FILE_PATH)
    return log_lines