from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    
    try:
        sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
        recipient_email = os.getenv('RECIPIENT_EMAIL')
        
        mail_message = Mail(
            from_email=recipient_email,
            to_emails=recipient_email,
            subject=f'Portfolio Contact from {name}',
            html_content=f'<strong>Name:</strong> {name}<br><strong>Email:</strong> {email}<br><strong>Message:</strong> {message}'
        )
        
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(mail_message)
        
        return jsonify({'message': 'Email sent successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to send email', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
