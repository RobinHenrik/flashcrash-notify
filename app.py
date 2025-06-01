from contextlib import asynccontextmanager

from fastapi import FastAPI

import main_notify

main_notify.start()
app = FastAPI()

LOG_FILE_PATH = "flashcrash_logs.log"

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
            return lines
    except Exception as e:
        return f"Error reading log {e}"

@app.get("/log")
def read_log():
    log_lines = tail_log(LOG_FILE_PATH)
    return log_lines