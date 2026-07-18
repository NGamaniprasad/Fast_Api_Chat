# FastMail Portal

## Description

FastMail Portal is a web-based email sending application built using **FastAPI**. It provides a secure login system and allows users to send emails to multiple recipients with optional file attachments.

The application uses session-based authentication and environment variables for secure configuration.

## Features

- Password-based Login
- Secure User Session Management
- Send Emails from Web Interface
- Multiple Recipient Support
- File Attachment Support
- Email Status Response
- Logout Functionality
- Environment Variable Configuration

## Technologies Used

- Python
- FastAPI
- Jinja2 Templates
- HTML/CSS
- SMTP Email Service
- Python-dotenv

## Project Structure

```
FastMail-Portal/
│
├── main.py
├── email_utils.py
├── .env
├── requirements.txt
│
├── templates/
│   ├── home.html
│   ├── chat.html
│   └── response.html
│
└── README.md
```

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/fastmail-portal.git
```

### 2. Navigate to Project Folder

```bash
cd fastmail-portal
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux/Mac**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file in the project root:

```env
LOGIN_PASSWORD=your_password
SESSION_SECRET=your_secret_key

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_email_password
```

## Run the Application

Start FastAPI server:

```bash
uvicorn main:app --reload
```

or

```bash
python main.py
```

## Open Browser

Visit:

```
http://127.0.0.1:8000
```

## Application Flow

1. User opens the login page.
2. User enters the password.
3. After successful login, the user enters the email page.
4. User provides:
   - Sender email
   - Receiver email(s)
   - Subject
   - Message
   - Attachment (optional)
5. Email is sent successfully.
6. User receives a success or failure message.

## Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Login page |
| `/login` | POST | User authentication |
| `/chat` | GET | Email sending page |
| `/send` | POST | Send email |
| `/logout` | GET | Logout user |

## Security

- Login password stored using environment variables
- Session-based authentication
- Secret keys stored outside the code
- Configuration managed through `.env`

## Future Enhancements

- User registration
- Email history
- Multiple user accounts
- Email scheduling
- Email templates
- Dashboard analytics

## License

This project is developed for learning and educational purposes.

## Author
N Gamani 
