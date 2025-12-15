import os
from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from pathlib import Path

app = FastAPI()

DATA_FOLDER = "datas"
os.makedirs(DATA_FOLDER, exist_ok=True)

API_KEY = ""  # Set your API key

def get_next_filename():
    existing_files = list(Path(DATA_FOLDER).glob("fatedata*.txt"))
    if not existing_files:
        return "fatedata1.txt"
    max_num = max(int(f.stem.replace("fatedata", "")) for f in existing_files)
    return f"fatedata{max_num + 1}.txt"

@app.get("/stats")
async def stats(apikey: str = Query(...)):
    if apikey != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    files = list(Path(DATA_FOLDER).glob("*.txt"))
    total_files = len(files)
    total_lines = 0
    for f in files:
        with open(f, 'rb') as fd:
            total_lines += sum(1 for _ in fd)
    return {"files": total_files, "lines": total_lines}

@app.get("/count")
async def count(apikey: str = Query(...), query: str = Query(...), type: str = Query(...), max: int = Query(100000)):
    if apikey != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    count = 0
    files = list(Path(DATA_FOLDER).glob("*.txt"))
    for f in files:
        with open(f, 'r', encoding='utf-8', errors='ignore') as fd:
            for line in fd:
                if query in line:
                    count += 1
                if count >= max:
                    return {"count": count}
    return {"count": count}

@app.get("/query")
async def query(apikey: str = Query(...), query: str = Query(...), type: str = Query(...), mode: str = Query("full"), max: int = Query(100000)):
    if apikey != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    results = []
    files = list(Path(DATA_FOLDER).glob("*.txt"))
    for f in files:
        with open(f, 'r', encoding='utf-8', errors='ignore') as fd:
            for line in fd:
                line = line.strip()
                if query in line:
                    if mode == "combo":
                        parts = line.split(':')
                        if len(parts) >= 2:
                            results.append(f"{parts[-2]}:{parts[-1]}")
                        else:
                            results.append(line)
                    else:
                        results.append(line)
                if len(results) >= max:
                    return {"results": results}
    return {"results": results}

@app.post("/upload")
async def upload(apikey: str = Query(...), file: UploadFile = File(...)):
    if apikey != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    filename = get_next_filename()
    path = Path(DATA_FOLDER) / filename
    contents = await file.read()
    with open(path, 'wb') as fd:
        fd.write(contents)
    lines = len(contents.splitlines())
    return {"filename": filename, "lines": lines}