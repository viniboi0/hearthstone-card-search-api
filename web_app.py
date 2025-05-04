from flask import Flask, request, render_template
import requests

app = Flask(__name__)

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
                all_results = search_cards(all_cards, queries)
                if not all_results:
                    error = "No matching cards found."
                else:
                    cards_data = all_results
        else:
            cards_data = []
    else:
        cards_data = []
    return render_template("index.html", cards_data=cards_data, error=error)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
