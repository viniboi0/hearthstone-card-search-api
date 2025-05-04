# Hearthstone Card Search Web App

This is a Flask web application that allows users to search Hearthstone card data using the Hearthstone JSON API. It includes user authentication, saved searches, pagination, and error handling.

## Features

- User registration and login
- Search Hearthstone cards by name or ID
- Save previous searches for logged-in users
- Pagination of search results
- Custom error pages for 404 and 500 errors
- Responsive design with Tailwind CSS
- Deployment ready with Gunicorn and Procfile

## Setup

1. Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app locally:

```bash
python3 web_app.py
```

4. Access the app at `http://localhost:8000`

## Deployment

This app is ready to be deployed on platforms like Heroku using the provided `Procfile`.

Run the following command to start the app with Gunicorn:

```bash
gunicorn web_app:app
```

## Notes

- Replace the `app.secret_key` in `web_app.py` with a secure secret key for production.
- The user data and saved searches are stored in-memory for demo purposes. For production, integrate a database.
- Customize the static assets and templates as needed.

## License

MIT License
