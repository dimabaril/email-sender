clone project:

`git clone https://github.com/dimabaril/email-sender.git`

fill in .env according example.env:
go to the https://app.sendgrid.com/guide/integrate/langs/python and create SENDGRID_API_KEY dont forget
verification
FROM_EMAIL should be verified in SendGrid
TO_EMAIL where the email will be sent, google does not work don't know why

```
SENDGRID_API_KEY=your_api_key_from_sendgrid
FROM_EMAIL=some-email@gmail.com
TO_EMAIL=some-email@yandex.ru
ALLOWED_HOSTS=http://127.0.0.1:5500,localhost,example.com
```

go in:
`cd email-sender`

make venv (python required):
`python -m venv venv`

go in:
`source venv/bin/activate`

instal requirements:
`pip install -r requirements.txt`

run app:
`uvicorn app:app --reload`

open index.html in liveserver (if we change request side we need to modify or add origins)
