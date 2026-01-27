# from fastapi import FastAPI, Request, Form, UploadFile, File
# from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.templating import Jinja2Templates
# from starlette.middleware.sessions import SessionMiddleware
# from starlette.middleware.base import BaseHTTPMiddleware
# from email_utils import send_email
# import os

# app = FastAPI()

# # Session
# app.add_middleware(SessionMiddleware, secret_key="SUPER_SECRET_KEY_123")

# # ---------- AUTH MIDDLEWARE ----------
# class AuthMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         protected = ["/chat", "/send"]

#         if any(request.url.path.startswith(p) for p in protected):
#             if not request.session.get("user"):
#                 return RedirectResponse("/", status_code=303)

#         return await call_next(request)

# app.add_middleware(AuthMiddleware)

# templates = Jinja2Templates(directory="templates")
# LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD", "Gamani123-CBM")


# # ---------- HOME ----------
# @app.get("/", response_class=HTMLResponse)
# def home(request: Request):
#     return templates.TemplateResponse("home.html", {"request": request})


# # ---------- LOGIN ----------
# @app.post("/login", response_class=HTMLResponse)
# def login(request: Request, password: str = Form(...)):
#     request.session.clear()

#     if password == LOGIN_PASSWORD:
#         request.session["user"] = "logged"
#         return RedirectResponse("/chat", status_code=303)

#     return templates.TemplateResponse(
#         "home.html",
#         {"request": request, "error": "❌ Invalid password!"}
#     )


# # ---------- CHAT ----------
# @app.get("/chat", response_class=HTMLResponse)
# def chat(request: Request):
#     return templates.TemplateResponse("chat.html", {"request": request})


# # ---------- SEND MAIL ----------
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
#         await send_email(sender, receiver_list, subject, message, file)
#         return templates.TemplateResponse(
#             "response.html",
#             {
#                 "request": request,
#                 "title": "✅ Success",
#                 "message": "Mail sent successfully!",
#                 "color": "green",
#             },
#         )
#     except Exception as e:
#         return templates.TemplateResponse(
#             "response.html",
#             {
#                 "request": request,
#                 "title": "❌ Failed",
#                 "message": str(e),
#                 "color": "red",
#             },
#         )


# # ---------- LOGOUT ----------
# @app.get("/logout")
# def logout(request: Request):
#     request.session.clear()
#     return RedirectResponse("/", status_code=303)


from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from email_utils import send_email
import os

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="SUPER_SECRET_KEY_123")

templates = Jinja2Templates(directory="templates")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD", "Gamani123-CBM")


def require_login(request: Request):
    if request.session.get("user") != "logged":
        return RedirectResponse("/", status_code=303)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/login", response_class=HTMLResponse)
def login(request: Request, password: str = Form(...)):
    request.session.clear()

    if password == LOGIN_PASSWORD:
        request.session["user"] = "logged"
        return RedirectResponse("/chat", status_code=303)

    return templates.TemplateResponse(
        "home.html",
        {"request": request, "error": "❌ Invalid password!"}
    )


@app.get("/chat", response_class=HTMLResponse)
def chat(request: Request):
    guard = require_login(request)
    if guard:
        return guard
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
    guard = require_login(request)
    if guard:
        return guard

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
        return templates.TemplateResponse(
            "response.html",
            {
                "request": request,
                "title": "❌ Failed",
                "message": str(e),
                "color": "red",
            },
        )


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)

# ---------- RUN ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
