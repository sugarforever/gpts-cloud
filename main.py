from fastapi import FastAPI, Depends
from starlette.responses import HTMLResponse, RedirectResponse
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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/login/google", include_in_schema=False)
async def login_google():
    GOOGLE_CLIENT_ID=os.environ["GOOGLE_CLIENT_ID"]
    GOOGLE_REDIRECT_URI=os.environ["GOOGLE_REDIRECT_URI"]
    auth_url = "https://accounts.google.com/o/oauth2/auth"
    redirect_url = f"f{auth_url}?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    return RedirectResponse(url=redirect_url, status_code=301)


@app.get("/auth/google", include_in_schema=False)
async def auth_google(code: str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": os.environ["GOOGLE_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
        "redirect_uri": os.environ["GOOGLE_REDIRECT_URI"],
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
                             headers={"Authorization": f"Bearer {access_token}"})
    return user_info.json()


@app.get("/token")
async def get_token(token: str = Depends(oauth2_scheme)):
    # return jwt.decode(token, os.environ["GOOGLE_CLIENT_SECRET"], algorithms=["HS256"])
    return { "token": token }


@app.get("/privacy", response_class=HTMLResponse, include_in_schema=False)
async def serve_privacy_policy():
    with open("web/privacy_policy.html", "r", encoding="utf-8") as privacy_policy_file:
        privacy_policy_content = privacy_policy_file.read()
        return privacy_policy_content


@app.get("/openapi.json", response_model=OpenAPI, include_in_schema=False)
async def get_openapi_schema():
    openapi_schema = app.openapi()
    return openapi_schema

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
