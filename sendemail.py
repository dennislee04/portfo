import oauth
from email.mime.text import MIMEText
import base64


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def send_message(sender, to, subject, message_text, user_id='me'):
    msg = create_message(sender, to, subject, message_text)
    try:
        service = oauth.get_g_service()
        message = (service.users().messages().send(userId=user_id, body=msg)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except ValueError as e:
        print('An error occurred: %s' % e)


send_message("leedennis04@gmail.com", "leedennis04@gmail.com", "test", "this is a tesst",
             user_id='leedennis04@gmail.com')
