import requests
import base64
import time

# --- 1. CONFIGURATION ---
WP_URL = "http://localhost:8080/wp-json/wp/v2/posts"
WP_USER = "pancreasz"     # e.g., "admin"
WP_APP_PASSWORD = "l13p 8ajb eSYc SeHF DYOa BHhY" # e.g., "xxxx xxxx xxxx xxxx xxxx xxxx"

# Encode the credentials for Basic Auth
credentials = f"{WP_USER}:{WP_APP_PASSWORD}"
token = base64.b64encode(credentials.encode())
headers = {
    "Authorization": f"Basic {token.decode('utf-8')}",
    "Content-Type": "application/json"
}

# --- 2. EXTRACT (Simulated API Data) ---
# In a production environment, this data would come from a requests.get() to TMDB or OMDB.
movie_data_source = [
    {
        "title": "Manchester by the Sea (2016)",
        "synopsis": "A depressed uncle is asked to take care of his teenage nephew after the boy's father dies. A raw look at grief that doesn't offer easy closures.",
        "director": "Kenneth Lonergan"
    },
    {
        "title": "Requiem for a Dream (2000)",
        "synopsis": "The drug-induced utopias of four Coney Island people are shattered when their addictions run deep. A relentless downward spiral.",
        "director": "Darren Aronofsky"
    },
    {
        "title": "The Pianist (2002)",
        "synopsis": "A Polish Jewish musician struggles to survive the destruction of the Warsaw ghetto of World War II.",
        "director": "Roman Polanski"
    },
    {
        "title": "Dear Zachary (2008)",
        "synopsis": "A filmmaker decides to memorialize a murdered friend when his friend's ex-girlfriend announces she is expecting his son. A profoundly heartbreaking documentary.",
        "director": "Kurt Kuenne"
    }
]

# --- 3. TRANSFORM & LOAD ---
print("Starting the ETL Pipeline to WordPress...")

for movie in movie_data_source:
    # Transform: Format the data into WordPress-friendly HTML blocks
    formatted_content = f"""
    <p><strong>Synopsis:</strong> {movie['synopsis']}</p>
    <p><em>Directed by {movie['director']}</em></p>
    """
    
    # Prepare the payload for the WordPress REST API
    wp_payload = {
        "title": movie['title'],
        "content": formatted_content,
        "status": "publish" # Pushes it live immediately
    }
    
    # Load: Send the POST request to the server
    response = requests.post(WP_URL, headers=headers, json=wp_payload)
    
    if response.status_code == 201:
        print(f"✅ Success: '{movie['title']}' loaded into database.")
    else:
        print(f"❌ Failed to load '{movie['title']}'. Error: {response.status_code}")
        print(response.text)
        
    time.sleep(1) # Be polite to our local server

print("Pipeline complete. Check your WordPress frontend!")