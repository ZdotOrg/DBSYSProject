-- ============================================================
-- ANIME TRACKER DATABASE SCHEMA
-- PostgreSQL Implementation
-- ============================================================

-- Drop existing tables (in reverse dependency order)
DROP TABLE IF EXISTS user_recommendations CASCADE;
DROP TABLE IF EXISTS user_theme_preferences CASCADE;
DROP TABLE IF EXISTS user_studio_preferences CASCADE;
DROP TABLE IF EXISTS user_demographic_preferences CASCADE;
DROP TABLE IF EXISTS user_genre_preferences CASCADE;
DROP TABLE IF EXISTS user_anime_list CASCADE;
DROP TABLE IF EXISTS anime_producers CASCADE;
DROP TABLE IF EXISTS anime_studios CASCADE;
DROP TABLE IF EXISTS anime_demographics CASCADE;
DROP TABLE IF EXISTS anime_themes CASCADE;
DROP TABLE IF EXISTS anime_genres CASCADE;
DROP TABLE IF EXISTS producers CASCADE;
DROP TABLE IF EXISTS studios CASCADE;
DROP TABLE IF EXISTS demographics CASCADE;
DROP TABLE IF EXISTS themes CASCADE;
DROP TABLE IF EXISTS genres CASCADE;
DROP TABLE IF EXISTS anime CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ============================================================
-- CORE ENTITIES
-- ============================================================

-- Users Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Anime Table
CREATE TABLE anime (
    anime_id SERIAL PRIMARY KEY,
    mal_id INTEGER UNIQUE,
    title VARCHAR(500) NOT NULL,
    title_english VARCHAR(500),
    title_japanese VARCHAR(500),
    type VARCHAR(50), -- TV, Movie, OVA, Special, ONA, Music
    episodes INTEGER,
    status VARCHAR(50), -- Currently Airing, Finished Airing, Not yet aired
    aired_from DATE,
    aired_to DATE,
    duration VARCHAR(100), -- e.g., "24 min per ep"
    rating VARCHAR(50), -- G, PG, PG-13, R, R+, Rx
    score DECIMAL(4, 2), -- Average MAL score (0.00 to 10.00)
    scored_by INTEGER, -- Number of users who scored it
    rank INTEGER,
    popularity INTEGER,
    synopsis TEXT,
    background TEXT,
    season VARCHAR(20), -- Winter, Spring, Summer, Fall
    year INTEGER,
    image_url TEXT,
    trailer_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- METADATA TABLES
-- ============================================================

-- Genres Table
CREATE TABLE genres (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    mal_id INTEGER UNIQUE
);

-- Themes Table
CREATE TABLE themes (
    theme_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    mal_id INTEGER UNIQUE
);

-- Demographics Table
CREATE TABLE demographics (
    demographic_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    mal_id INTEGER UNIQUE
);

-- Studios Table
CREATE TABLE studios (
    studio_id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    mal_id INTEGER UNIQUE
);

-- Producers Table
CREATE TABLE producers (
    producer_id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    mal_id INTEGER UNIQUE
);

-- ============================================================
-- JUNCTION TABLES (Many-to-Many Relationships)
-- ============================================================

-- Anime-Genre Relationships
CREATE TABLE anime_genres (
    anime_id INTEGER NOT NULL REFERENCES anime(anime_id) ON DELETE CASCADE,
    genre_id INTEGER NOT NULL REFERENCES genres(genre_id) ON DELETE CASCADE,
    PRIMARY KEY (anime_id, genre_id)
);

-- Anime-Theme Relationships
CREATE TABLE anime_themes (
    anime_id INTEGER NOT NULL REFERENCES anime(anime_id) ON DELETE CASCADE,
    theme_id INTEGER NOT NULL REFERENCES themes(theme_id) ON DELETE CASCADE,
    PRIMARY KEY (anime_id, theme_id)
);

-- Anime-Demographic Relationships
CREATE TABLE anime_demographics (
    anime_id INTEGER NOT NULL REFERENCES anime(anime_id) ON DELETE CASCADE,
    demographic_id INTEGER NOT NULL REFERENCES demographics(demographic_id) ON DELETE CASCADE,
    PRIMARY KEY (anime_id, demographic_id)
);

-- Anime-Studio Relationships
CREATE TABLE anime_studios (
    anime_id INTEGER NOT NULL REFERENCES anime(anime_id) ON DELETE CASCADE,
    studio_id INTEGER NOT NULL REFERENCES studios(studio_id) ON DELETE CASCADE,
    PRIMARY KEY (anime_id, studio_id)
);

-- Anime-Producer Relationships
CREATE TABLE anime_producers (
    anime_id INTEGER NOT NULL REFERENCES anime(anime_id) ON DELETE CASCADE,
    producer_id INTEGER NOT NULL REFERENCES producers(producer_id) ON DELETE CASCADE,
    PRIMARY KEY (anime_id, producer_id)
);

-- ============================================================
-- USER INTERACTION TABLES
-- ============================================================

-- User Anime List (Watchlist)
CREATE TABLE user_anime_list (
    list_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    anime_id INTEGER NOT NULL REFERENCES anime(anime_id) ON DELETE CASCADE,
    watch_status VARCHAR(50) NOT NULL, -- Watching, Completed, On Hold, Dropped, Plan to Watch
    user_score INTEGER CHECK (user_score >= 1 AND user_score <= 10),
    episodes_watched INTEGER DEFAULT 0,
    start_date DATE,
    finish_date DATE,
    is_rewatching BOOLEAN DEFAULT FALSE,
    times_rewatched INTEGER DEFAULT 0,
    notes TEXT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, anime_id)
);

-- ============================================================
-- USER PREFERENCE TABLES (For Recommendation Algorithm)
-- ============================================================

-- User Genre Preferences
CREATE TABLE user_genre_preferences (
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    genre_id INTEGER NOT NULL REFERENCES genres(genre_id) ON DELETE CASCADE,
    weighted_score DECIMAL(10, 4) NOT NULL,
    rating_count INTEGER NOT NULL,
    last_calculated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, genre_id)
);

-- User Demographic Preferences
CREATE TABLE user_demographic_preferences (
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    demographic_id INTEGER NOT NULL REFERENCES demographics(demographic_id) ON DELETE CASCADE,
    weighted_score DECIMAL(10, 4) NOT NULL,
    rating_count INTEGER NOT NULL,
    last_calculated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, demographic_id)
);

-- User Studio Preferences
CREATE TABLE user_studio_preferences (
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    studio_id INTEGER NOT NULL REFERENCES studios(studio_id) ON DELETE CASCADE,
    weighted_score DECIMAL(10, 4) NOT NULL,
    rating_count INTEGER NOT NULL,
    last_calculated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, studio_id)
);

-- User Theme Preferences
CREATE TABLE user_theme_preferences (
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    theme_id INTEGER NOT NULL REFERENCES themes(theme_id) ON DELETE CASCADE,
    weighted_score DECIMAL(10, 4) NOT NULL,
    rating_count INTEGER NOT NULL,
    last_calculated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, theme_id)
);

-- ============================================================
-- RECOMMENDATIONS TABLE
-- ============================================================

-- User Recommendations
CREATE TABLE user_recommendations (
    recommendation_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    anime_id INTEGER NOT NULL REFERENCES anime(anime_id) ON DELETE CASCADE,
    recommendation_score DECIMAL(10, 4) NOT NULL,
    genre_score DECIMAL(10, 4),
    theme_score DECIMAL(10, 4),
    demographic_score DECIMAL(10, 4),
    studio_score DECIMAL(10, 4),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, anime_id)
);

-- ============================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================

-- Anime indexes
CREATE INDEX idx_anime_mal_id ON anime(mal_id);
CREATE INDEX idx_anime_title ON anime(title);
CREATE INDEX idx_anime_type ON anime(type);
CREATE INDEX idx_anime_status ON anime(status);
CREATE INDEX idx_anime_score ON anime(score DESC);
CREATE INDEX idx_anime_popularity ON anime(popularity);
CREATE INDEX idx_anime_season_year ON anime(season, year);

-- User indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- User anime list indexes
CREATE INDEX idx_user_anime_list_user ON user_anime_list(user_id);
CREATE INDEX idx_user_anime_list_anime ON user_anime_list(anime_id);
CREATE INDEX idx_user_anime_list_status ON user_anime_list(watch_status);
CREATE INDEX idx_user_anime_list_updated ON user_anime_list(updated_at DESC);

-- Junction table indexes
CREATE INDEX idx_anime_genres_anime ON anime_genres(anime_id);
CREATE INDEX idx_anime_genres_genre ON anime_genres(genre_id);
CREATE INDEX idx_anime_themes_anime ON anime_themes(anime_id);
CREATE INDEX idx_anime_themes_theme ON anime_themes(theme_id);
CREATE INDEX idx_anime_demographics_anime ON anime_demographics(anime_id);
CREATE INDEX idx_anime_demographics_demo ON anime_demographics(demographic_id);
CREATE INDEX idx_anime_studios_anime ON anime_studios(anime_id);
CREATE INDEX idx_anime_studios_studio ON anime_studios(studio_id);
CREATE INDEX idx_anime_producers_anime ON anime_producers(anime_id);
CREATE INDEX idx_anime_producers_producer ON anime_producers(producer_id);

-- Preference table indexes
CREATE INDEX idx_user_genre_prefs_user ON user_genre_preferences(user_id);
CREATE INDEX idx_user_demo_prefs_user ON user_demographic_preferences(user_id);
CREATE INDEX idx_user_studio_prefs_user ON user_studio_preferences(user_id);
CREATE INDEX idx_user_theme_prefs_user ON user_theme_preferences(user_id);

-- Recommendations indexes
CREATE INDEX idx_recommendations_user ON user_recommendations(user_id);
CREATE INDEX idx_recommendations_score ON user_recommendations(recommendation_score DESC);
CREATE INDEX idx_recommendations_generated ON user_recommendations(generated_at DESC);

-- ============================================================
-- TRIGGERS FOR AUTOMATIC TIMESTAMP UPDATES
-- ============================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for anime table
CREATE TRIGGER update_anime_updated_at
BEFORE UPDATE ON anime
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger for user_anime_list table
CREATE TRIGGER update_user_anime_list_updated_at
BEFORE UPDATE ON user_anime_list
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- ============================================================
-- INITIAL METADATA INSERTS (Common genres, themes, demographics)
-- ============================================================

-- Insert common genres
INSERT INTO genres (name, mal_id) VALUES
('Action', 1),
('Adventure', 2),
('Comedy', 4),
('Drama', 8),
('Fantasy', 10),
('Horror', 14),
('Mystery', 7),
('Romance', 22),
('Sci-Fi', 24),
('Slice of Life', 36),
('Sports', 30),
('Supernatural', 37),
('Thriller', 41);

-- Insert common themes
INSERT INTO themes (name, mal_id) VALUES
('School', 23),
('Mecha', 18),
('Music', 19),
('Military', 38),
('Psychological', 40),
('Historical', 13),
('Isekai', 62),
('Magic', 66),
('Vampire', 32);

-- Insert demographics
INSERT INTO demographics (name, mal_id) VALUES
('Shounen', 27),
('Shoujo', 25),
('Seinen', 42),
('Josei', 43),
('Kids', 15);

