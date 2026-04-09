"""
SQLAlchemy models for Anime Tracker
Matches the PostgreSQL schema structure
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index, CheckConstraint
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# ============================================================
# JUNCTION TABLES (Many-to-Many Relationships)
# ============================================================

anime_genres = db.Table(
    'anime_genres',
    db.Column('anime_id', db.Integer, db.ForeignKey('anime.anime_id', ondelete='CASCADE'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.genre_id', ondelete='CASCADE'), primary_key=True)
)

anime_themes = db.Table(
    'anime_themes',
    db.Column('anime_id', db.Integer, db.ForeignKey('anime.anime_id', ondelete='CASCADE'), primary_key=True),
    db.Column('theme_id', db.Integer, db.ForeignKey('themes.theme_id', ondelete='CASCADE'), primary_key=True)
)

anime_demographics = db.Table(
    'anime_demographics',
    db.Column('anime_id', db.Integer, db.ForeignKey('anime.anime_id', ondelete='CASCADE'), primary_key=True),
    db.Column('demographic_id', db.Integer, db.ForeignKey('demographics.demographic_id', ondelete='CASCADE'), primary_key=True)
)

anime_studios = db.Table(
    'anime_studios',
    db.Column('anime_id', db.Integer, db.ForeignKey('anime.anime_id', ondelete='CASCADE'), primary_key=True),
    db.Column('studio_id', db.Integer, db.ForeignKey('studios.studio_id', ondelete='CASCADE'), primary_key=True)
)

anime_producers = db.Table(
    'anime_producers',
    db.Column('anime_id', db.Integer, db.ForeignKey('anime.anime_id', ondelete='CASCADE'), primary_key=True),
    db.Column('producer_id', db.Integer, db.ForeignKey('producers.producer_id', ondelete='CASCADE'), primary_key=True)
)


# ============================================================
# CORE ENTITIES
# ============================================================

class User(db.Model):
    """User model"""
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    anime_list = relationship('UserAnimeList', back_populates='user', cascade='all, delete-orphan')
    genre_preferences = relationship('UserGenrePreference', back_populates='user', cascade='all, delete-orphan')
    theme_preferences = relationship('UserThemePreference', back_populates='user', cascade='all, delete-orphan')
    demographic_preferences = relationship('UserDemographicPreference', back_populates='user', cascade='all, delete-orphan')
    studio_preferences = relationship('UserStudioPreference', back_populates='user', cascade='all, delete-orphan')
    recommendations = relationship('UserRecommendation', back_populates='user', cascade='all, delete-orphan')
    
    __table_args__ = (
        Index('idx_users_username', 'username'),
        Index('idx_users_email', 'email'),
    )
    
    def __repr__(self):
        return f'<User {self.username}>'


class Anime(db.Model):
    """Anime model"""
    __tablename__ = 'anime'
    
    anime_id = db.Column(db.Integer, primary_key=True)
    mal_id = db.Column(db.Integer, unique=True)
    title = db.Column(db.String(500), nullable=False)
    title_english = db.Column(db.String(500))
    title_japanese = db.Column(db.String(500))
    type = db.Column(db.String(50))  # TV, Movie, OVA, Special, ONA, Music
    episodes = db.Column(db.Integer)
    status = db.Column(db.String(50))  # Currently Airing, Finished Airing, Not yet aired
    aired_from = db.Column(db.Date)
    aired_to = db.Column(db.Date)
    duration = db.Column(db.String(100))
    rating = db.Column(db.String(50))  # G, PG, PG-13, R, R+, Rx
    score = db.Column(db.Numeric(4, 2))
    scored_by = db.Column(db.Integer)
    rank = db.Column(db.Integer)
    popularity = db.Column(db.Integer)
    synopsis = db.Column(db.Text)
    background = db.Column(db.Text)
    season = db.Column(db.String(20))  # Winter, Spring, Summer, Fall
    year = db.Column(db.Integer)
    image_url = db.Column(db.Text)
    trailer_url = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Many-to-Many Relationships
    genres = relationship('Genre', secondary=anime_genres, back_populates='anime')
    themes = relationship('Theme', secondary=anime_themes, back_populates='anime')
    demographics = relationship('Demographic', secondary=anime_demographics, back_populates='anime')
    studios = relationship('Studio', secondary=anime_studios, back_populates='anime')
    producers = relationship('Producer', secondary=anime_producers, back_populates='anime')
    
    # One-to-Many Relationships
    user_entries = relationship('UserAnimeList', back_populates='anime', cascade='all, delete-orphan')
    recommendations = relationship('UserRecommendation', back_populates='anime', cascade='all, delete-orphan')
    
    __table_args__ = (
        Index('idx_anime_mal_id', 'mal_id'),
        Index('idx_anime_title', 'title'),
        Index('idx_anime_type', 'type'),
        Index('idx_anime_status', 'status'),
        Index('idx_anime_score', 'score'),
        Index('idx_anime_popularity', 'popularity'),
        Index('idx_anime_season_year', 'season', 'year'),
    )
    
    def __repr__(self):
        return f'<Anime {self.title}>'


# ============================================================
# METADATA MODELS
# ============================================================

class Genre(db.Model):
    """Genre model"""
    __tablename__ = 'genres'
    
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    mal_id = db.Column(db.Integer, unique=True)
    
    # Relationships
    anime = relationship('Anime', secondary=anime_genres, back_populates='genres')
    user_preferences = relationship('UserGenrePreference', back_populates='genre', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Genre {self.name}>'


class Theme(db.Model):
    """Theme model"""
    __tablename__ = 'themes'
    
    theme_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    mal_id = db.Column(db.Integer, unique=True)
    
    # Relationships
    anime = relationship('Anime', secondary=anime_themes, back_populates='themes')
    user_preferences = relationship('UserThemePreference', back_populates='theme', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Theme {self.name}>'


class Demographic(db.Model):
    """Demographic model"""
    __tablename__ = 'demographics'
    
    demographic_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    mal_id = db.Column(db.Integer, unique=True)
    
    # Relationships
    anime = relationship('Anime', secondary=anime_demographics, back_populates='demographics')
    user_preferences = relationship('UserDemographicPreference', back_populates='demographic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Demographic {self.name}>'


class Studio(db.Model):
    """Studio model"""
    __tablename__ = 'studios'
    
    studio_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    mal_id = db.Column(db.Integer, unique=True)
    
    # Relationships
    anime = relationship('Anime', secondary=anime_studios, back_populates='studios')
    user_preferences = relationship('UserStudioPreference', back_populates='studio', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Studio {self.name}>'


class Producer(db.Model):
    """Producer model"""
    __tablename__ = 'producers'
    
    producer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    mal_id = db.Column(db.Integer, unique=True)
    
    # Relationships
    anime = relationship('Anime', secondary=anime_producers, back_populates='producers')
    
    def __repr__(self):
        return f'<Producer {self.name}>'


# ============================================================
# USER INTERACTION MODELS
# ============================================================

class UserAnimeList(db.Model):
    """User's anime watchlist and ratings"""
    __tablename__ = 'user_anime_list'
    
    list_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.anime_id', ondelete='CASCADE'), nullable=False)
    watch_status = db.Column(db.String(50), nullable=False)  # Watching, Completed, On Hold, Dropped, Plan to Watch
    user_score = db.Column(db.Integer)
    episodes_watched = db.Column(db.Integer, default=0)
    start_date = db.Column(db.Date)
    finish_date = db.Column(db.Date)
    is_rewatching = db.Column(db.Boolean, default=False)
    times_rewatched = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='anime_list')
    anime = relationship('Anime', back_populates='user_entries')
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'anime_id', name='unique_user_anime'),
        CheckConstraint('user_score >= 1 AND user_score <= 10', name='check_user_score_range'),
        Index('idx_user_anime_list_user', 'user_id'),
        Index('idx_user_anime_list_anime', 'anime_id'),
        Index('idx_user_anime_list_status', 'watch_status'),
        Index('idx_user_anime_list_updated', 'updated_at'),
    )
    
    def __repr__(self):
        return f'<UserAnimeList user={self.user_id} anime={self.anime_id} status={self.watch_status}>'


# ============================================================
# USER PREFERENCE MODELS
# ============================================================

class UserGenrePreference(db.Model):
    """User's weighted genre preferences"""
    __tablename__ = 'user_genre_preferences'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id', ondelete='CASCADE'), primary_key=True)
    weighted_score = db.Column(db.Numeric(10, 4), nullable=False)
    rating_count = db.Column(db.Integer, nullable=False)
    last_calculated = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='genre_preferences')
    genre = relationship('Genre', back_populates='user_preferences')
    
    __table_args__ = (
        Index('idx_user_genre_prefs_user', 'user_id'),
    )
    
    def __repr__(self):
        return f'<UserGenrePreference user={self.user_id} genre={self.genre_id} score={self.weighted_score}>'


class UserThemePreference(db.Model):
    """User's weighted theme preferences"""
    __tablename__ = 'user_theme_preferences'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    theme_id = db.Column(db.Integer, db.ForeignKey('themes.theme_id', ondelete='CASCADE'), primary_key=True)
    weighted_score = db.Column(db.Numeric(10, 4), nullable=False)
    rating_count = db.Column(db.Integer, nullable=False)
    last_calculated = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='theme_preferences')
    theme = relationship('Theme', back_populates='user_preferences')
    
    __table_args__ = (
        Index('idx_user_theme_prefs_user', 'user_id'),
    )
    
    def __repr__(self):
        return f'<UserThemePreference user={self.user_id} theme={self.theme_id} score={self.weighted_score}>'


class UserDemographicPreference(db.Model):
    """User's weighted demographic preferences"""
    __tablename__ = 'user_demographic_preferences'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    demographic_id = db.Column(db.Integer, db.ForeignKey('demographics.demographic_id', ondelete='CASCADE'), primary_key=True)
    weighted_score = db.Column(db.Numeric(10, 4), nullable=False)
    rating_count = db.Column(db.Integer, nullable=False)
    last_calculated = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='demographic_preferences')
    demographic = relationship('Demographic', back_populates='user_preferences')
    
    __table_args__ = (
        Index('idx_user_demo_prefs_user', 'user_id'),
    )
    
    def __repr__(self):
        return f'<UserDemographicPreference user={self.user_id} demo={self.demographic_id} score={self.weighted_score}>'


class UserStudioPreference(db.Model):
    """User's weighted studio preferences"""
    __tablename__ = 'user_studio_preferences'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    studio_id = db.Column(db.Integer, db.ForeignKey('studios.studio_id', ondelete='CASCADE'), primary_key=True)
    weighted_score = db.Column(db.Numeric(10, 4), nullable=False)
    rating_count = db.Column(db.Integer, nullable=False)
    last_calculated = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='studio_preferences')
    studio = relationship('Studio', back_populates='user_preferences')
    
    __table_args__ = (
        Index('idx_user_studio_prefs_user', 'user_id'),
    )
    
    def __repr__(self):
        return f'<UserStudioPreference user={self.user_id} studio={self.studio_id} score={self.weighted_score}>'


# ============================================================
# RECOMMENDATIONS MODEL
# ============================================================

class UserRecommendation(db.Model):
    """Cached user recommendations"""
    __tablename__ = 'user_recommendations'
    
    recommendation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.anime_id', ondelete='CASCADE'), nullable=False)
    recommendation_score = db.Column(db.Numeric(10, 4), nullable=False)
    genre_score = db.Column(db.Numeric(10, 4))
    theme_score = db.Column(db.Numeric(10, 4))
    demographic_score = db.Column(db.Numeric(10, 4))
    studio_score = db.Column(db.Numeric(10, 4))
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='recommendations')
    anime = relationship('Anime', back_populates='recommendations')
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'anime_id', name='unique_user_recommendation'),
        Index('idx_recommendations_user', 'user_id'),
        Index('idx_recommendations_score', 'recommendation_score'),
        Index('idx_recommendations_generated', 'generated_at'),
    )
    
    def __repr__(self):
        return f'<UserRecommendation user={self.user_id} anime={self.anime_id} score={self.recommendation_score}>'