import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from azure.storage.blob import BlobServiceClient
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key' # Change in production
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Azure Storage Config
AZURE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
AZURE_CONTAINER_NAME = os.getenv('AZURE_CONTAINER_NAME', 'postcards')

class Postcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(100), nullable=False)
    sender_name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Postcard {self.city_name}>'

def upload_to_azure(file):
    if not AZURE_CONNECTION_STRING:
        # Fallback for local testing without Azure keys if needed, 
        # but requirements say "Application must use database stored in Azure to read data".
        # For images, "Application should serve files (eg. pictures) from Azure storage".
        # We'll assume keys are provided or return a placeholder if strictly local dev without net.
        # For now, let's just return a placeholder or fail if no key.
        print("Azure Connection String not set. Returning placeholder.")
        return "https://via.placeholder.com/300"

    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
        
        # Create container if it doesn't exist
        try:
            container_client.create_container(public_access='blob')
        except Exception:
            pass # Container likely already exists

        filename = secure_filename(file.filename)
        # Append timestamp to filename to avoid collisions
        unique_filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{filename}"
        
        blob_client = container_client.get_blob_client(unique_filename)
        blob_client.upload_blob(file)
        
        return blob_client.url
    except Exception as e:
        print(f"Error uploading to Azure: {e}")
        return None

@app.route('/')
def index():
    postcards = Postcard.query.order_by(Postcard.date_created.desc()).all()
    return render_template('index.html', postcards=postcards)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        city = request.form.get('city_name')
        sender = request.form.get('sender_name')
        message = request.form.get('message')
        file = request.files.get('image')
        
        if file:
            image_url = upload_to_azure(file)
            if image_url:
                new_postcard = Postcard(
                    city_name=city,
                    sender_name=sender,
                    message=message,
                    image_url=image_url
                )
                db.session.add(new_postcard)
                db.session.commit()
                return redirect(url_for('index'))
            else:
                flash('Error uploading image. Please try again.')
        else:
            flash('Image is required.')
            
    return render_template('create.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
