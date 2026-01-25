



from fastapi import FastAPI, Request, Form, UploadFile, File, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
#from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import time

from email_utils import send_email

app = FastAPI()

templates = Jinja2Templates(directory="templates")
#app.mount("/static", StaticFiles(directory="static"), name="static")

PASSWORD = "Gamani123-CBM"


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# @app.post("/login")
# def login(password: str = Form(...)):
#     if password == PASSWORD:
#         return RedirectResponse(url="/chat", status_code=302)
#     return {"error": "Wrong password"}


@app.post("/login", response_class=HTMLResponse)
def login(request: Request, password: str = Form(...)):
    if password == PASSWORD:
        return RedirectResponse(url="/chat", status_code=302)

    return templates.TemplateResponse(
        "data.html",
        {
            "request": request
        }
    )

@app.get("/chat", response_class=HTMLResponse)
def chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

#
# @app.post("/send")
# async def send_mail(
#     background_tasks: BackgroundTasks,
#     sender: str = Form(...),
#     receivers: str = Form(...),
#     subject: str = Form(...),
#     message: str = Form(...),
#     schedule: int = Form(0),
#     file: UploadFile = File(None),
# ):
#     receiver_list = [r.strip() for r in receivers.split(",") if r.strip()]
#
#     if len(receiver_list) > 25:
#         return {"error": "Maximum 25 recipients allowed at one time"}
#
#     if schedule > 0:
#         background_tasks.add_task(
#             delayed_send,
#             schedule,
#             sender,
#             receiver_list,
#             subject,
#             message,
#             file,
#         )
#     else:
#         await send_email(sender, receiver_list, subject, message, file)
#
#     return {"status": f"Mail sent to {len(receiver_list)} recipients"}


async def delayed_send(delay, *args):
    time.sleep(delay)
    await send_email(*args)

@app.post("/send", response_class=HTMLResponse)
async def send_mail(
    request: Request,
    background_tasks: BackgroundTasks,
    sender: str = Form(...),
    receivers: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    schedule: int = Form(0),
    file: UploadFile = File(None),
):
    receiver_list = [r.strip() for r in receivers.split(",") if r.strip()][:25]

    try:
        background_tasks.add_task(
            delayed_send,
            max(schedule, 0),
            sender,
            receiver_list,
            subject,
            message,
            file,
        )

        return templates.TemplateResponse(
            "response.html",
            {
                "request": request,
                "title": "✅ Success",
                "message": "Mail sent successfully to recipients.",
                "color": "green",
            },
        )

    except Exception as e:
        return templates.TemplateResponse(
            "response.html",
            {
                "request": request,
                "title": "❌ Failed",
                "message": "Mail sending failed. Please try again.",
                "color": "red",
            },
        )

import os

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )
