
import os
from flask import Flask, render_template, request

app = Flask(__name__)

# Set APP_VERSION to v1, v2, or v3
VERSION = os.getenv("APP_VERSION", "v1").lower()

if VERSION not in ("v1", "v2", "v3"):
    VERSION = "v1"

# Sample recommendation data
ITEMS = [
    {"name": "Inception", "category": "Sci-Fi", "rating": 8.8},
    {"name": "Interstellar", "category": "Sci-Fi", "rating": 8.7},
    {"name": "The Dark Knight", "category": "Action", "rating": 9.0},
    {"name": "3 Idiots", "category": "Comedy", "rating": 8.4},
    {"name": "Jai Bhim", "category": "Drama", "rating": 8.7},
    {"name": "Avengers Endgame", "category": "Action", "rating": 8.4},
    {"name": "Coco", "category": "Animation", "rating": 8.4},
    {"name": "Dangal", "category": "Drama", "rating": 8.3},
]

@app.route("/", methods=["GET"])
def home():
    category = request.args.get("category", "All")
    min_rating_text = request.args.get("min_rating", "0")
    sort_by = request.args.get("sort_by", "name")

    try:
        min_rating = float(min_rating_text)
        min_rating = max(0, min(10, min_rating))
    except (ValueError, TypeError):
        min_rating = 0

    results = ITEMS.copy()

    # Version 1: Display all items.
    # Version 2 and 3: Apply filters.
    if VERSION in ("v2", "v3"):
        if category != "All":
            results = [
                item for item in results
                if item["category"] == category
            ]

        results = [
            item for item in results
            if item["rating"] >= min_rating
        ]

    # Version 3: Sort the filtered results.
    if VERSION == "v3":
        if sort_by == "rating":
            results.sort(key=lambda item: item["rating"], reverse=True)
        elif sort_by == "category":
            results.sort(key=lambda item: item["category"].lower())
        else:
            results.sort(key=lambda item: item["name"].lower())

    categories = sorted({item["category"] for item in ITEMS})

    return render_template(
        "index.html",
        items=results,
        categories=categories,
        version=VERSION,
        category=category,
        min_rating=min_rating,
        sort_by=sort_by,
    )

@app.route("/health")
def health():
    return {"status": "healthy", "version": VERSION}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
