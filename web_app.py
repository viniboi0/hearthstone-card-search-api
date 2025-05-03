from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Hearthstone Card Search by API</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 p-6">
    <div class="max-w-4xl mx-auto bg-white p-6 rounded shadow">
        <h1 class="text-2xl font-bold mb-4">Hearthstone Card Search by API</h1>
        <form method="POST" class="mb-4">
            <textarea name="card_queries" rows="10" placeholder="Paste Hearthstone card names or IDs here, one per line" required class="w-full p-2 border rounded mb-2 font-mono"></textarea>
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Search Cards</button>
        </form>
        {% if cards_data %}
        <div class="whitespace-pre-wrap bg-gray-200 p-3 rounded font-mono max-h-96 overflow-auto">
            {% for card in cards_data %}
            <div class="mb-4 border-b border-gray-300 pb-2">
                {{ card }}
            </div>
            {% endfor %}
        </div>
        {% elif error %}
        <p class="text-red-600">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

API_URL = "https://api.hearthstonejson.com/v1/latest/enUS/cards.json"

def fetch_all_cards():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; HearthstoneCardSearch/1.0)"
        }
        response = requests.get(API_URL, headers=headers)
        if response.status_code != 200:
            return None, f"Failed to fetch cards: {response.status_code}"
        if not response.text.strip():
            return None, "Empty response from API"
        return response.json(), None
    except Exception as e:
        return None, str(e)

def search_cards(cards, queries):
    results = []
    queries_lower = [q.lower() for q in queries]
    for card in cards:
        card_name = card.get("name", "").lower()
        card_id = card.get("id", "").lower()
        for q in queries_lower:
            if q == card_name or q == card_id or q in card_name or q in card_id:
                import re
                raw_text = card.get('text', 'N/A')
                # Remove square bracket tags like [x], [b], [/b], etc.
                clean_text = re.sub(r'\[/?[^\]]+\]', '', raw_text)
                # Remove HTML tags like <b>, </b>, etc.
                clean_text = re.sub(r'<[^>]+>', '', clean_text)
                # Remove $ symbols from card text
                clean_text = clean_text.replace('$', '')
                card_str = (
                    f"Card id: {card.get('id', 'N/A')}\n"
                    f"Name: {card.get('name', 'N/A')}\n"
                    f"Attack: {card.get('attack', 'N/A')}\n"
                    f"Health: {card.get('health', 'N/A')}\n"
                    f"Mana Cost: {card.get('cost', 'N/A')}\n"
                    f"Card Text: {clean_text.strip()}\n"
                )
                results.append(card_str)
                break
    return results

@app.route("/", methods=["GET", "POST"])
def index():
    cards_data = []
    error = None
    if request.method == "POST":
        card_queries_text = request.form.get("card_queries")
        if card_queries_text:
            queries = [line.strip() for line in card_queries_text.splitlines() if line.strip()]
            all_cards, err = fetch_all_cards()
            if err:
                error = err
            else:
                cards_data = search_cards(all_cards, queries)
                if not cards_data:
                    error = "No matching cards found."
    return render_template_string(HTML_TEMPLATE, cards_data=cards_data, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
