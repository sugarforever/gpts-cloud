from fastapi import FastAPI, Depends
from starlette.responses import HTMLResponse
from fastapi.openapi.models import OpenAPI
from fastapi.security import OAuth2PasswordBearer
import os
import requests
from jose import jwt
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(servers=[
    {
        "url": "https://gpts-cloud.vercel.app",
        "description": "GPTs Cloud - Staging"
    },
])

@app.get("/token")
async def get_token(token: str):
    return jwt.decode(token, os.environ["GOOGLE_CLIENT_SECRET"], algorithms=["HS256"])


@app.get("/privacy", response_class=HTMLResponse)
async def serve_privacy_policy():
    with open("web/privacy_policy.html", "r", encoding="utf-8") as privacy_policy_file:
        privacy_policy_content = privacy_policy_file.read()
        return privacy_policy_content


@app.get("/openapi.json", response_model=OpenAPI)
async def get_openapi_schema():
    openapi_schema = app.openapi()
    return openapi_schema

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
