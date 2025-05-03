from flask import Flask, render_template, request, redirect, url_for
from textblob import TextBlob

app = Flask(__name__)

# Mood-to-embed-URL map
mood_playlists = {
    "happy": "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad": "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1",
    "angry": "https://open.spotify.com/embed/playlist/37i9dQZF1DWX83CujKHHOn",
    "relaxed": "https://open.spotify.com/embed/playlist/37i9dQZF1EIdJ9DvHRUKGM",
    "energetic": "https://open.spotify.com/embed/playlist/37i9dQZF1DX8tZsk68tuDw"
}

def detect_mood_from_text(text):
    # Using TextBlob for sentiment analysis
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity  # Get sentiment polarity (-1 to 1)
    
    # Map sentiment to mood
    if sentiment > 0.2:
        return "happy"
    elif sentiment < -0.2:
        return "sad"
    else:
        return "relaxed"  # Neutral sentiment

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        mood = None
        message = ""
        user_input = request.form.get("sentence", "").strip()
        
        if user_input:  # If there's text input, detect mood
            mood = detect_mood_from_text(user_input)
            return redirect(url_for("index", mood=mood))
        
        mood_input = request.form.get("mood", "").lower()
        if mood_input in mood_playlists:
            return redirect(url_for("index", mood=mood_input))
        else:
            return redirect(url_for("index", error="no_match"))

    mood = request.args.get("mood")
    error = request.args.get("error")
    embed_url = mood_playlists.get(mood) if mood else None
    message = "Sorry, I don’t have a playlist for that mood yet!" if error == "no_match" else ""

    return render_template("index.html", embed_url=embed_url, mood=mood, message=message)

if __name__ == "__main__":
    app.run(debug=True)
