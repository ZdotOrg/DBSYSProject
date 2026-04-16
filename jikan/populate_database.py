"""
JIKAN API - POPULATE DATABASE SCRIPT
=====================================
This script fetches anime data from the Jikan API (MyAnimeList unofficial API)
and populates your PostgreSQL database with anime, genres, themes, studios, etc.

USAGE:
    python populate_database.py [--start-page 1] [--max-pages 50] [--batch-size 25]

FEATURES:
    - Fetches anime data in batches (respects Jikan rate limits)
    - Inserts anime, genres, themes, demographics, studios, producers
    - Progress tracking with resume capability
    - Handles API errors and rate limiting gracefully
    - Avoids duplicates (checks mal_id before inserting)

RATE LIMITS:
    - Jikan API: 3 requests/second, 60 requests/minute
    - This script adds delays to stay within limits
"""

import sys
import os
import time
import argparse
import requests
from datetime import datetime

# Add parent directory to path to import database module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import db
from population.config import config


# ============================================================
# JIKAN API CONFIGURATION
# ============================================================

JIKAN_BASE_URL = "https://api.jikan.moe/v4"
REQUEST_DELAY = 0.35  # Delay between requests (3 requests/second = 0.33s)
RETRY_DELAY = 5  # Delay before retrying failed requests
MAX_RETRIES = 3


# ============================================================
# API HELPER FUNCTIONS
# ============================================================

def fetch_anime_page(page=1, limit=25):
    """
    Fetch a page of anime from Jikan API
    
    Args:
        page: Page number (1-indexed)
        limit: Number of results per page (max 25)
    
    Returns:
        dict: API response with anime list
    """
    url = f"{JIKAN_BASE_URL}/anime"
    params = {
        'page': page,
        'limit': limit,
        'order_by': 'popularity',
        'sort': 'asc'
    }
    
    for attempt in range(MAX_RETRIES):
        try:
            print(f"  Fetching page {page} (attempt {attempt + 1}/{MAX_RETRIES})...")
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limited
                print(f"  Rate limited. Waiting {RETRY_DELAY * 2} seconds...")
                time.sleep(RETRY_DELAY * 2)
            else:
                print(f"  Error {response.status_code}: {response.text}")
                time.sleep(RETRY_DELAY)
        
        except requests.exceptions.RequestException as e:
            print(f"  Request failed: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    
    return None


def fetch_anime_details(mal_id):
    """
    Fetch detailed information for a specific anime
    
    Args:
        mal_id: MyAnimeList ID
    
    Returns:
        dict: Detailed anime information
    """
    url = f"{JIKAN_BASE_URL}/anime/{mal_id}/full"
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json().get('data')
            elif response.status_code == 429:
                time.sleep(RETRY_DELAY * 2)
            else:
                return None
        
        except requests.exceptions.RequestException:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    
    return None


# ============================================================
# DATABASE INSERTION FUNCTIONS
# ============================================================

def insert_or_get_genre(conn, name, mal_id=None):
    """Insert genre if not exists, return genre_id"""
    cur = conn.cursor()
    
    # Check if exists
    cur.execute("SELECT genre_id FROM genres WHERE name = %s", (name,))
    result = cur.fetchone()
    
    if result:
        cur.close()
        return result[0]
    
    # Insert new
    cur.execute(
        "INSERT INTO genres (name, mal_id) VALUES (%s, %s) RETURNING genre_id",
        (name, mal_id)
    )
    genre_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return genre_id


def insert_or_get_theme(conn, name, mal_id=None):
    """Insert theme if not exists, return theme_id"""
    cur = conn.cursor()
    
    cur.execute("SELECT theme_id FROM themes WHERE name = %s", (name,))
    result = cur.fetchone()
    
    if result:
        cur.close()
        return result[0]
    
    cur.execute(
        "INSERT INTO themes (name, mal_id) VALUES (%s, %s) RETURNING theme_id",
        (name, mal_id)
    )
    theme_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return theme_id


def insert_or_get_demographic(conn, name, mal_id=None):
    """Insert demographic if not exists, return demographic_id"""
    cur = conn.cursor()
    
    cur.execute("SELECT demographic_id FROM demographics WHERE name = %s", (name,))
    result = cur.fetchone()
    
    if result:
        cur.close()
        return result[0]
    
    cur.execute(
        "INSERT INTO demographics (name, mal_id) VALUES (%s, %s) RETURNING demographic_id",
        (name, mal_id)
    )
    demographic_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return demographic_id


def insert_or_get_studio(conn, name, mal_id=None):
    """Insert studio if not exists, return studio_id"""
    cur = conn.cursor()
    
    cur.execute("SELECT studio_id FROM studios WHERE name = %s", (name,))
    result = cur.fetchone()
    
    if result:
        cur.close()
        return result[0]
    
    cur.execute(
        "INSERT INTO studios (name, mal_id) VALUES (%s, %s) RETURNING studio_id",
        (name, mal_id)
    )
    studio_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return studio_id


def insert_or_get_producer(conn, name, mal_id=None):
    """Insert producer if not exists, return producer_id"""
    cur = conn.cursor()
    
    cur.execute("SELECT producer_id FROM producers WHERE name = %s", (name,))
    result = cur.fetchone()
    
    if result:
        cur.close()
        return result[0]
    
    cur.execute(
        "INSERT INTO producers (name, mal_id) VALUES (%s, %s) RETURNING producer_id",
        (name, mal_id)
    )
    producer_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return producer_id


def anime_exists(conn, mal_id):
    """Check if anime already exists in database"""
    cur = conn.cursor()
    cur.execute("SELECT anime_id FROM anime WHERE mal_id = %s", (mal_id,))
    result = cur.fetchone()
    cur.close()
    return result is not None


def insert_anime(conn, anime_data):
    """
    Insert anime and all related data into database
    
    Args:
        conn: Database connection
        anime_data: Anime data from Jikan API
    
    Returns:
        int: anime_id if successful, None if failed
    """
    mal_id = anime_data.get('mal_id')
    
    # Check if already exists
    if anime_exists(conn, mal_id):
        print(f"    Anime {mal_id} already exists, skipping...")
        return None
    
    cur = conn.cursor()
    
    try:
        # Extract anime data
        title = anime_data.get('title', 'Unknown')
        title_english = anime_data.get('title_english')
        title_japanese = anime_data.get('title_japanese')
        anime_type = anime_data.get('type')
        episodes = anime_data.get('episodes')
        status = anime_data.get('status')
        
        # Dates
        aired = anime_data.get('aired', {})
        aired_from = aired.get('from', '').split('T')[0] if aired.get('from') else None
        aired_to = aired.get('to', '').split('T')[0] if aired.get('to') else None
        
        duration = anime_data.get('duration')
        rating = anime_data.get('rating')
        score = anime_data.get('score')
        scored_by = anime_data.get('scored_by')
        rank = anime_data.get('rank')
        popularity = anime_data.get('popularity')
        synopsis = anime_data.get('synopsis')
        background = anime_data.get('background')
        
        # Season and year
        season = anime_data.get('season')
        year = anime_data.get('year')
        
        # Images
        images = anime_data.get('images', {}).get('jpg', {})
        image_url = images.get('large_image_url') or images.get('image_url')
        
        trailer = anime_data.get('trailer', {})
        trailer_url = trailer.get('url')
        
        # Insert anime
        cur.execute("""
            INSERT INTO anime (
                mal_id, title, title_english, title_japanese,
                type, episodes, status, aired_from, aired_to,
                duration, rating, score, scored_by, rank, popularity,
                synopsis, background, season, year, image_url, trailer_url
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING anime_id
        """, (
            mal_id, title, title_english, title_japanese,
            anime_type, episodes, status, aired_from, aired_to,
            duration, rating, score, scored_by, rank, popularity,
            synopsis, background, season, year, image_url, trailer_url
        ))
        
        anime_id = cur.fetchone()[0]
        
        # Insert genres
        for genre in anime_data.get('genres', []):
            genre_id = insert_or_get_genre(conn, genre['name'], genre['mal_id'])
            cur.execute(
                "INSERT INTO anime_genres (anime_id, genre_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (anime_id, genre_id)
            )
        
        # Insert themes
        for theme in anime_data.get('themes', []):
            theme_id = insert_or_get_theme(conn, theme['name'], theme['mal_id'])
            cur.execute(
                "INSERT INTO anime_themes (anime_id, theme_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (anime_id, theme_id)
            )
        
        # Insert demographics
        for demo in anime_data.get('demographics', []):
            demo_id = insert_or_get_demographic(conn, demo['name'], demo['mal_id'])
            cur.execute(
                "INSERT INTO anime_demographics (anime_id, demographic_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (anime_id, demo_id)
            )
        
        # Insert studios
        for studio in anime_data.get('studios', []):
            studio_id = insert_or_get_studio(conn, studio['name'], studio['mal_id'])
            cur.execute(
                "INSERT INTO anime_studios (anime_id, studio_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (anime_id, studio_id)
            )
        
        # Insert producers
        for producer in anime_data.get('producers', []):
            producer_id = insert_or_get_producer(conn, producer['name'], producer['mal_id'])
            cur.execute(
                "INSERT INTO anime_producers (anime_id, producer_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (anime_id, producer_id)
            )
        
        conn.commit()
        cur.close()
        print(f"    ✓ Inserted: {title} (MAL ID: {mal_id})")
        return anime_id
    
    except Exception as e:
        conn.rollback()
        cur.close()
        print(f"    ✗ Error inserting anime {mal_id}: {e}")
        return None


# ============================================================
# MAIN POPULATE FUNCTION
# ============================================================

def populate_database(start_page=1, max_pages=50, batch_size=25):
    """
    Main function to populate database with anime from Jikan API
    
    Args:
        start_page: Starting page number
        max_pages: Maximum number of pages to fetch
        batch_size: Number of anime per page (max 25)
    """
    print("=" * 60)
    print("ANIME DATABASE POPULATION - JIKAN API")
    print("=" * 60)
    print(f"Start Page: {start_page}")
    print(f"Max Pages: {max_pages}")
    print(f"Batch Size: {batch_size}")
    print("=" * 60)
    
    # Initialize database connection
    from app import create_app
    app = create_app('development')
    
    with app.app_context():
        conn = db.get_connection()
        
        total_inserted = 0
        total_skipped = 0
        
        try:
            for page in range(start_page, start_page + max_pages):
                print(f"\n[Page {page}/{start_page + max_pages - 1}]")
                
                # Fetch page of anime
                response = fetch_anime_page(page, batch_size)
                
                if not response or 'data' not in response:
                    print(f"  Failed to fetch page {page}. Stopping.")
                    break
                
                anime_list = response['data']
                pagination = response.get('pagination', {})
                
                print(f"  Found {len(anime_list)} anime")
                
                if not anime_list:
                    print("  No more anime found. Stopping.")
                    break
                
                # Insert each anime
                for anime_data in anime_list:
                    result = insert_anime(conn, anime_data)
                    
                    if result:
                        total_inserted += 1
                    else:
                        total_skipped += 1
                    
                    # Rate limiting delay
                    time.sleep(REQUEST_DELAY)
                
                print(f"  Progress: {total_inserted} inserted, {total_skipped} skipped")
                
                # Check if there are more pages
                if not pagination.get('has_next_page', False):
                    print("\n  Reached last page.")
                    break
                
                # Delay between pages
                time.sleep(REQUEST_DELAY * 2)
        
        finally:
            db.return_connection(conn)
        
        print("\n" + "=" * 60)
        print("POPULATION COMPLETE")
        print("=" * 60)
        print(f"Total Inserted: {total_inserted}")
        print(f"Total Skipped: {total_skipped}")
        print(f"Total Processed: {total_inserted + total_skipped}")
        print("=" * 60)


# ============================================================
# COMMAND LINE INTERFACE
# ============================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Populate anime database from Jikan API')
    parser.add_argument('--start-page', type=int, default=1, help='Starting page number')
    parser.add_argument('--max-pages', type=int, default=50, help='Maximum number of pages to fetch')
    parser.add_argument('--batch-size', type=int, default=25, help='Anime per page (max 25)')
    
    args = parser.parse_args()
    
    populate_database(
        start_page=args.start_page,
        max_pages=args.max_pages,
        batch_size=args.batch_size
    )