from fastapi import FastAPI

app = FastAPI(title="sample")


@app.get("/")
async def root() -> dict:
    return {"message": "OK"}
