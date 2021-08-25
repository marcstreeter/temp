from fastapi import FastAPI

serve = FastAPI()


@serve.get("/")
def status():
    return {
        "running": True,
        "message": "ok",
    }
