# from fastapi import FastAPI, Request, Form, UploadFile, File # BackgroundTasks
# from fastapi.responses import HTMLResponse, RedirectResponse
# #from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# import time

# from email_utils import send_email

# app = FastAPI()

# templates = Jinja2Templates(directory="templates")
# #app.mount("/static", StaticFiles(directory="static"), name="static")

# PASSWORD = "Gamani123-CBM"


# @app.get("/", response_class=HTMLResponse)
# def home(request: Request):
#     return templates.TemplateResponse("home.html", {"request": request})




# @app.post("/login", response_class=HTMLResponse)
# def login(request: Request, password: str = Form(...)):
#     if password == PASSWORD:
#         return RedirectResponse(url="/chat", status_code=302)

#     return templates.TemplateResponse(
#         "data.html",
#         {
#             "request": request
#         }
#     )

# @app.get("/chat", response_class=HTMLResponse)
# def chat(request: Request):
#     return templates.TemplateResponse("chat.html", {"request": request})


# #WOrking
# # async def delayed_send(delay, *args):
# #     time.sleep(delay)
# #     await send_email(*args)

# # @app.post("/send", response_class=HTMLResponse)
# # async def send_mail(
# #     request: Request,
# #     background_tasks: BackgroundTasks,
# #     sender: str = Form(...),
# #     receivers: str = Form(...),
# #     subject: str = Form(...),
# #     message: str = Form(...),
# #     schedule: int = Form(0),
# #     file: UploadFile = File(None),
# # ):
# #     receiver_list = [r.strip() for r in receivers.split(",") if r.strip()][:25]

# #     try:
# #         background_tasks.add_task(
# #             delayed_send,
# #             max(schedule, 0),
# #             sender,
# #             receiver_list,
# #             subject,
# #             message,
# #             file,
# #         )

# #         return templates.TemplateResponse(
# #             "response.html",
# #             {
# #                 "request": request,
# #                 "title": "✅ Success",
# #                 "message": "Mail sent successfully to recipients.",
# #                 "color": "green",
# #             },
# #         )

# #     except Exception as e:
# #         return templates.TemplateResponse(
# #             "response.html",
# #             {
# #                 "request": request,
# #                 "title": "❌ Failed",
# #                 "message": "Mail sending failed. Please try again.",
# #                 "color": "red",
# #             },
# #         )


# @app.post("/send", response_class=HTMLResponse)
# async def send_mail(
#     request: Request,
#     sender: str = Form(...),
#     receivers: str = Form(...),
#     subject: str = Form(...),
#     message: str = Form(...),
#     file: UploadFile = File(None),
# ):
#     receiver_list = [r.strip() for r in receivers.split(",") if r.strip()][:25]

#     try:
#         await send_email(
#             sender,
#             receiver_list,
#             subject,
#             message,
#             file,
#         )

#         return templates.TemplateResponse(
#             "response.html",
#             {
#                 "request": request,
#                 "title": "✅ Success",
#                 "message": "Mail sent successfully.",
#                 "color": "green",
#             },
#         )

#     except Exception as e:
#         print("EMAIL ERROR:", e)
#         return templates.TemplateResponse(
#             "response.html",
#             {
#                 "request": request,
#                 "title": "❌ Failed",
#                 "message": "Mail sending failed.",
#                 "color": "red",
#             },
#         )

# import os

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         "main:app",
#         host="0.0.0.0",
#         port=int(os.environ.get("PORT", 8000))
#     )


from fastapi import FastAPI, Request, Form, UploadFile, File, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from email_utils import send_email  # Your existing send_email function

app = FastAPI()

templates = Jinja2Templates(directory="templates")

PASSWORD = "Gamani123-CBM"


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


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


# ---------------------------
# Fixed /send route
# ---------------------------
@app.post("/send", response_class=HTMLResponse)
def send_mail(
    request: Request,
    background_tasks: BackgroundTasks,
    sender: str = Form(...),
    receivers: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    file: UploadFile = File(None),
):
    # Limit to 25 recipients max
    receiver_list = [r.strip() for r in receivers.split(",") if r.strip()][:25]

    try:
        # Add the email sending function to the background
        background_tasks.add_task(send_email, sender, receiver_list, subject, message, file)

        return templates.TemplateResponse(
            "response.html",
            {
                "request": request,
                "title": "✅ Success",
                "message": "Mail is being sent in the background.",
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
                "message": "Mail sending failed. Please try again.",
                "color": "red",
            },
        )


# ---------------------------
# Run server
# ---------------------------
import os

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )

