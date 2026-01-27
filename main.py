

from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from email_utils import send_email
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

LOGIN_PASSWORD = "Gamani123-CBM"  # better to move this to env later

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, password: str = Form(...)):
    if password == LOGIN_PASSWORD:
        return RedirectResponse(url="/chat", status_code=302)
    return templates.TemplateResponse("data.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
def chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/send", response_class=HTMLResponse)
async def send_mail(
    request: Request,
    sender: str = Form(...),
    receivers: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    file: UploadFile = File(None),
):
    receiver_list = [r.strip() for r in receivers.split(",") if r.strip()][:25]

    try:
        await send_email(sender, receiver_list, subject, message, file)

        return templates.TemplateResponse(
            "response.html",
            {
                "request": request,
                "title": "✅ Success",
                "message": "Mail sent successfully!",
                "color": "green",
            },
        )

    except Exception as e:
        print("EMAIL ERROR:", e)
        return templates.TemplateResponse(
            "response.html",
            {
                "request": request,
                "title": "❌ Failed",
                "message": str(e),
                "color": "red",
            },
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
