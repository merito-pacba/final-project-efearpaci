[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=22745001)

# Digital Postcard App Walkthrough

## Overview
The Digital Postcard App is a simple gallery application built with Flask. It allows users to upload photos with greetings, which are displayed in a grid layout.

## Features
- **Gallery View**: Displays all postcards in a responsive grid.
- **Create Postcard**: Form to upload an image and add a message.
- **Azure Storage**: Integration for storing images (configurable via `.env`).
- **Database**: Uses SQLAlchemy (SQLite locally, adaptable for Azure SQL).

## How to Run Locally

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Environment**:
    - Rename `.env.example` to `.env`.
    - Set `AZURE_STORAGE_CONNECTION_STRING` if you have one.
    - If no Azure string is provided, the app will upload to a placeholder URL (for testing logic).
    
    > [!NOTE]
    > To test actual image upload, you need a valid Azure Storage Connection String.

3.  **Run the App**:
    ```bash
    python app.py
    ```

4.  **Access**:
    - Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Project Structure
- `app.py`: Main application logic, database model, and routes.
- `templates/`: HTML templates using Bootstrap 5.
    - `base.html`: Common layout.
    - `index.html`: Gallery display.
    - `create.html`: Upload form.
- `requirements.txt`: Python dependencies.

## Deployment
The application can be deployed to Azure App Service!

- **App Service**: Create a Linux Python Web App.
- **GitHub Integration**: Connect via Deployment Center.
- **Configuration**: Add environment variables (`DATABASE_URL`, `AZURE_STORAGE_CONNECTION_STRING`) in Azure Portal.
