from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

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
        sender_email = os.getenv('EMAIL_USER')
        sender_password = os.getenv('EMAIL_PASS')
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = sender_email
        msg['Subject'] = f'Portfolio Contact from {name}'
        
        body = f'Name: {name}\nEmail: {email}\nMessage: {message}'
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        return jsonify({'message': 'Email sent successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to send email', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
