"""

This script syncs your existing anime database with fresh data from Jikan API.
Updates scores, episodes, status, and other fields that may have changed.

USAGE:
    python sync_updates.py [--limit 100] [--days-since 7]

FEATURES:
    - Updates existing anime with latest data from MAL
    - Focuses on frequently changing fields (score, episodes, status)
    - Can target anime that haven't been updated recently
    - Respects Jikan API rate limits
    - Logs all changes for review

RECOMMENDED SCHEDULE FOR PRODUCTION:
    - Daily: Top 100 most popular anime
    - Weekly: All anime updated in last 30 days
    - Monthly: Full database sync
"""

import sys
import os
import time
import argparse
import requests
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import db
from population.config import config


# ============================================================
# JIKAN API CONFIGURATION
# ============================================================

JIKAN_BASE_URL = "https://api.jikan.moe/v4"
REQUEST_DELAY = 0.35
RETRY_DELAY = 5
MAX_RETRIES = 3


# ============================================================
# API HELPER FUNCTIONS
# ============================================================

def fetch_anime_by_mal_id(mal_id):
    """
    Fetch anime details from Jikan API by MAL ID
    
    Args:
        mal_id: MyAnimeList ID
    
    Returns:
        dict: Anime data or None if failed
    """
    url = f"{JIKAN_BASE_URL}/anime/{mal_id}/full"
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json().get('data')
            elif response.status_code == 429:
                time.sleep(RETRY_DELAY * 2)
            elif response.status_code == 404:
                return None  # Anime not found
            else:
                time.sleep(RETRY_DELAY)
        
        except requests.exceptions.RequestException:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    
    return None


# ============================================================
# DATABASE QUERY FUNCTIONS
# ============================================================

def get_anime_to_update(conn, limit=None, days_since=None):
    """
    Get list of anime from database that need updating
    
    Args:
        conn: Database connection
        limit: Maximum number of anime to return
        days_since: Only get anime not updated in X days
    
    Returns:
        list: Anime records with mal_id and current data
    """
    cur = conn.cursor()
    
    query = "SELECT anime_id, mal_id, title, score, episodes, status, updated_at FROM anime WHERE mal_id IS NOT NULL"
    params = []
    
    if days_since:
        query += " AND updated_at < %s"
        cutoff_date = datetime.now() - timedelta(days=days_since)
        params.append(cutoff_date)
    
    query += " ORDER BY popularity ASC"  # Most popular first
    
    if limit:
        query += " LIMIT %s"
        params.append(limit)
    
    cur.execute(query, params if params else None)
    results = cur.fetchall()
    cur.close()
    
    return results


def update_anime_data(conn, anime_id, new_data):
    """
    Update anime record with fresh data from Jikan
    
    Args:
        conn: Database connection
        anime_id: Internal anime_id
        new_data: Fresh data from Jikan API
    
    Returns:
        dict: Changes made (field -> (old_value, new_value))
    """
    cur = conn.cursor()
    
    # Get current data
    cur.execute("""
        SELECT score, episodes, status, scored_by, rank, popularity, synopsis, image_url
        FROM anime WHERE anime_id = %s
    """, (anime_id,))
    current = cur.fetchone()
    
    if not current:
        cur.close()
        return None
    
    changes = {}
    
    # Extract new values
    new_score = new_data.get('score')
    new_episodes = new_data.get('episodes')
    new_status = new_data.get('status')
    new_scored_by = new_data.get('scored_by')
    new_rank = new_data.get('rank')
    new_popularity = new_data.get('popularity')
    new_synopsis = new_data.get('synopsis')
    
    new_images = new_data.get('images', {}).get('jpg', {})
    new_image_url = new_images.get('large_image_url') or new_images.get('image_url')
    
    # Track changes
    if current[0] != new_score:
        changes['score'] = (current[0], new_score)
    
    if current[1] != new_episodes:
        changes['episodes'] = (current[1], new_episodes)
    
    if current[2] != new_status:
        changes['status'] = (current[2], new_status)
    
    if current[3] != new_scored_by:
        changes['scored_by'] = (current[3], new_scored_by)
    
    if current[4] != new_rank:
        changes['rank'] = (current[4], new_rank)
    
    if current[5] != new_popularity:
        changes['popularity'] = (current[5], new_popularity)
    
    # Update database
    cur.execute("""
        UPDATE anime SET
            score = %s,
            episodes = %s,
            status = %s,
            scored_by = %s,
            rank = %s,
            popularity = %s,
            synopsis = %s,
            image_url = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE anime_id = %s
    """, (
        new_score, new_episodes, new_status, new_scored_by,
        new_rank, new_popularity, new_synopsis, new_image_url,
        anime_id
    ))
    
    conn.commit()
    cur.close()
    
    return changes



# MAIN SYNC FUNCTION


def sync_updates(limit=100, days_since=None):
    """
    Main function to sync anime updates from Jikan API
    
    Args:
        limit: Maximum number of anime to update
        days_since: Only update anime not updated in X days
    """
    print("=" * 60)
    print("ANIME DATABASE SYNC - JIKAN API")
    print("=" * 60)
    print(f"Limit: {limit if limit else 'No limit'}")
    print(f"Days Since Last Update: {days_since if days_since else 'All'}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    from app import create_app
    app = create_app('development')
    
    with app.app_context():
        conn = db.get_connection()
        
        total_checked = 0
        total_updated = 0
        total_unchanged = 0
        total_failed = 0
        
        change_log = []
        
        try:
            # Get anime to update
            print("\nFetching anime list from database...")
            anime_list = get_anime_to_update(conn, limit, days_since)
            print(f"Found {len(anime_list)} anime to check\n")
            
            for i, anime_row in enumerate(anime_list, 1):
                anime_id, mal_id, title, current_score, current_eps, current_status, updated_at = anime_row
                
                print(f"[{i}/{len(anime_list)}] Checking: {title} (MAL: {mal_id})")
                
                # Fetch fresh data from Jikan
                new_data = fetch_anime_by_mal_id(mal_id)
                
                if not new_data:
                    print(f"  ✗ Failed to fetch data")
                    total_failed += 1
                    time.sleep(REQUEST_DELAY)
                    continue
                
                # Update database and track changes
                changes = update_anime_data(conn, anime_id, new_data)
                
                if changes:
                    print(f"  ✓ Updated ({len(changes)} changes)")
                    for field, (old, new) in changes.items():
                        print(f"    - {field}: {old} → {new}")
                        change_log.append({
                            'anime': title,
                            'mal_id': mal_id,
                            'field': field,
                            'old': old,
                            'new': new
                        })
                    total_updated += 1
                else:
                    print(f"  • No changes")
                    total_unchanged += 1
                
                total_checked += 1
                
                # Rate limiting
                time.sleep(REQUEST_DELAY)
                
                # Progress report every 10 anime
                if i % 10 == 0:
                    print(f"\n  Progress: {total_updated} updated, {total_unchanged} unchanged, {total_failed} failed\n")
        
        finally:
            db.return_connection(conn)
        
        # Final Report
        print("\n" + "=" * 60)
        print("SYNC COMPLETE")
        print("=" * 60)
        print(f"Total Checked: {total_checked}")
        print(f"Total Updated: {total_updated}")
        print(f"Total Unchanged: {total_unchanged}")
        print(f"Total Failed: {total_failed}")
        print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Save change log
        if change_log:
            log_file = f"sync_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(log_file, 'w') as f:
                f.write("ANIME SYNC CHANGE LOG\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for change in change_log:
                    f.write(f"{change['anime']} (MAL {change['mal_id']})\n")
                    f.write(f"  {change['field']}: {change['old']} → {change['new']}\n\n")
            
            print(f"\nChange log saved to: {log_file}")


# ============================================================
# COMMAND LINE INTERFACE
# ============================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sync anime database with Jikan API')
    parser.add_argument('--limit', type=int, default=100, help='Max number of anime to update')
    parser.add_argument('--days-since', type=int, help='Only update anime not updated in X days')
    
    args = parser.parse_args()
    
    sync_updates(
        limit=args.limit,
        days_since=args.days_since
    )