# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
load_dotenv()


def send_mail(html_body, to_emails='kmercurino@dattek.com'):
    message = Mail(
        from_email='k.mercurino@duocuc.cl',
        to_emails=to_emails,
        subject='Restablecimiento de Contraseña "Vocational Insight"',
        html_content=html_body)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


def pull_html_body(token):
    reset_link = f"http://tu_dominio.com/reset_password_confirm?token={token}"

    html_content = f"""<html>
    <head>
        <meta charset="utf-8">
        <title>Restablecimiento de Contraseña</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                background-color: #ffffff;
                border-radius: 5px;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                max-width: 600px;
                margin: auto;
            }}
            h1 {{
                color: #333;
            }}
            p {{
                color: #555;
            }}
            a.button {{
                display: inline-block;
                background-color: #007BFF;
                color: #ffffff;
                padding: 10px 15px;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
            }}
            a.button:hover {{
                background-color: #0056b3;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 12px;
                color: #999;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Restablecimiento de Contraseña</h1>
            <p>Hola,</p>
            <p>Hemos recibido una solicitud para restablecer la contraseña de tu cuenta. Si no solicitaste este cambio, puedes ignorar este correo.</p>
            <p>Para restablecer tu contraseña, haz clic en el siguiente botón:</p>
            <a href='{reset_link}' class='button'>Restablecer Contraseña</a>
            <p>Este enlace es válido por 30 minutos.</p>
            <p>Gracias por usar nuestro servicio.</p>
            <p>Saludos,<br>El equipo de Vocational Insight</p>
        </div>
    </body>
    </html>"""
    return html_content


#html_body=pull_html_body(reset_link, token)
#send_mail(html_body, "kmercurino@dattek.com")