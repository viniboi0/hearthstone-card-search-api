
Built by https://www.blackbox.ai

---

# Hearthstone Card Search by API

## Project Overview
Hearthstone Card Search is a web application built using Flask that allows users to search for Hearthstone cards using the Hearthstone JSON API. Users can input card names or IDs, and the application will retrieve relevant card details including their attack, health, mana cost, and text description.

## Installation
To run this application, you need to have Python and Flask installed on your machine.

1. **Clone the repository:**
   ```bash
   git clone [REPO_URL]
   cd [REPO_NAME]
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   Make sure you have `requests` and `flask` installed. You can install them using pip:
   ```bash
   pip install flask requests
   ```

## Usage
To run the application, execute the following command:
```bash
python web_app.py
```
This will start a local web server at `http://0.0.0.0:8000`. Open this URL in your web browser to access the Hearthstone Card Search application.

### Input Instructions
- Paste Hearthstone card names or IDs into the provided text area, one per line.
- Click the "Search Cards" button to view the card information.

## Features
- Search for Hearthstone cards by name or ID.
- Displays card details including attack, health, mana cost, and card text.
- User-friendly interface styled with Tailwind CSS.
- Error handling for failed API requests and empty responses.

## Dependencies
The project depends on the following libraries:
- Flask
- Requests

You can find these listed in the `requirements.txt` file if created or install them directly.

## Project Structure
```
/[PROJECT_ROOT]
├── web_app.py           # Main application file
```

## Acknowledgments
This application uses the Hearthstone JSON API for retrieving card data. You can find more information about the API [here](https://api.hearthstonejson.com/).

```
Feel free to customize the repository URL and other relevant information according to your project's specifics.