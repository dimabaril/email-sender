import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")
TO_EMAIL = os.getenv("TO_EMAIL")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS")


# origins = [
#     "http://127.0.0.1:5500",  # from where the request will be made
# ]

ORIGINS = os.getenv("ALLOWED_HOSTS", "").split(",")

if SENDGRID_API_KEY is None:
    raise ValueError("SENDGRID_API_KEY is not set")
if FROM_EMAIL is None:
    raise ValueError("FROM_EMAIL is not set")
if TO_EMAIL is None:
    raise ValueError("TO_EMAIL is not set")
if ORIGINS is None:
    raise ValueError("ORIGINS is not set")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EmailMessage(BaseModel):
    name: str
    email: EmailStr
    message: str


@app.post("/send-email")
async def send_email(data: EmailMessage):
    message = Mail(
        from_email=FROM_EMAIL,  # should be verified in SendGrid
        to_emails=TO_EMAIL,  # where the email will be sent, google does not work don't know why
        subject="Some subject",
        plain_text_content=f"От {data.name} ({data.email}):\n\n{data.message}",
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return {"status": "success", "response": response.status_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
