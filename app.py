import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

app = FastAPI()


origins = [
    "http://127.0.0.1:5500",  # from where the request will be made
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EmailMessage(BaseModel):
    name: str
    email: EmailStr
    message: str


SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

if SENDGRID_API_KEY is None:
    raise ValueError("SENDGRID_API_KEY is not set")


@app.post("/send-email")
async def send_email(data: EmailMessage):
    message = Mail(
        from_email="dimabaril@gmail.com",  # should be verified in SendGrid
        to_emails="dimabaril@yandex.ru",  # where the email will be sent, google does not work don't know why
        subject="Some subject",
        plain_text_content=f"От {data.name} ({data.email}):\n\n{data.message}",
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return {"status": "success", "response": response.status_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
