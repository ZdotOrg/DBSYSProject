-- ============================================================
-- ANIME RECOMMENDATION ALGORITHM - FIXED VERSION
-- Content-Based Filtering using SQL
-- No Time Decay (Option C)
-- ============================================================

-- ============================================================
-- STEP 1: CALCULATE USER GENRE PREFERENCES
-- ============================================================

CREATE OR REPLACE FUNCTION calculate_user_genre_preferences(p_user_id INTEGER)
RETURNS TABLE (
    genre_id INTEGER,
    genre_name VARCHAR(100),
    weighted_score DECIMAL(10, 4),
    rating_count INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        g.genre_id,
        g.name AS genre_name,
        AVG(ual.user_score)::DECIMAL(10, 4) AS weighted_score,
        COUNT(ual.anime_id)::INTEGER AS rating_count
    FROM user_anime_list ual
    JOIN anime_genres ag ON ual.anime_id = ag.anime_id
    JOIN genres g ON ag.genre_id = g.genre_id
    WHERE ual.user_id = p_user_id
      AND ual.user_score IS NOT NULL
      AND ual.user_score > 0
    GROUP BY g.genre_id, g.name
    HAVING COUNT(ual.anime_id) >= 1
    ORDER BY weighted_score DESC;
END;
$$ LANGUAGE plpgsql;


-- ============================================================
-- STEP 2: CALCULATE USER THEME PREFERENCES
-- ============================================================

CREATE OR REPLACE FUNCTION calculate_user_theme_preferences(p_user_id INTEGER)
RETURNS TABLE (
    theme_id INTEGER,
    theme_name VARCHAR(100),
    weighted_score DECIMAL(10, 4),
    rating_count INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        t.theme_id,
        t.name AS theme_name,
        AVG(ual.user_score)::DECIMAL(10, 4) AS weighted_score,
        COUNT(ual.anime_id)::INTEGER AS rating_count
    FROM user_anime_list ual
    JOIN anime_themes at ON ual.anime_id = at.anime_id
    JOIN themes t ON at.theme_id = t.theme_id
    WHERE ual.user_id = p_user_id
      AND ual.user_score IS NOT NULL
      AND ual.user_score > 0
    GROUP BY t.theme_id, t.name
    HAVING COUNT(ual.anime_id) >= 1
    ORDER BY weighted_score DESC;
END;
$$ LANGUAGE plpgsql;


-- ============================================================
-- STEP 3: CALCULATE USER DEMOGRAPHIC PREFERENCES
-- ============================================================

CREATE OR REPLACE FUNCTION calculate_user_demographic_preferences(p_user_id INTEGER)
RETURNS TABLE (
    demographic_id INTEGER,
    demographic_name VARCHAR(100),
    weighted_score DECIMAL(10, 4),
    rating_count INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        d.demographic_id,
        d.name AS demographic_name,
        AVG(ual.user_score)::DECIMAL(10, 4) AS weighted_score,
        COUNT(ual.anime_id)::INTEGER AS rating_count
    FROM user_anime_list ual
    JOIN anime_demographics ad ON ual.anime_id = ad.anime_id
    JOIN demographics d ON ad.demographic_id = d.demographic_id
    WHERE ual.user_id = p_user_id
      AND ual.user_score IS NOT NULL
      AND ual.user_score > 0
    GROUP BY d.demographic_id, d.name
    HAVING COUNT(ual.anime_id) >= 1
    ORDER BY weighted_score DESC;
END;
$$ LANGUAGE plpgsql;


-- ============================================================
-- STEP 4: CALCULATE USER STUDIO PREFERENCES
-- ============================================================

CREATE OR REPLACE FUNCTION calculate_user_studio_preferences(p_user_id INTEGER)
RETURNS TABLE (
    studio_id INTEGER,
    studio_name VARCHAR(255),
    weighted_score DECIMAL(10, 4),
    rating_count INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.studio_id,
        s.name AS studio_name,
        AVG(ual.user_score)::DECIMAL(10, 4) AS weighted_score,
        COUNT(ual.anime_id)::INTEGER AS rating_count
    FROM user_anime_list ual
    JOIN anime_studios ast ON ual.anime_id = ast.anime_id
    JOIN studios s ON ast.studio_id = s.studio_id
    WHERE ual.user_id = p_user_id
      AND ual.user_score IS NOT NULL
      AND ual.user_score > 0
    GROUP BY s.studio_id, s.name
    HAVING COUNT(ual.anime_id) >= 1
    ORDER BY weighted_score DESC;
END;
$$ LANGUAGE plpgsql;


-- ============================================================
-- STEP 5: STORE USER PREFERENCES IN DATABASE
-- ============================================================

CREATE OR REPLACE FUNCTION update_all_user_preferences(p_user_id INTEGER)
RETURNS VOID AS $$
BEGIN
    DELETE FROM user_genre_preferences WHERE user_id = p_user_id;
    DELETE FROM user_theme_preferences WHERE user_id = p_user_id;
    DELETE FROM user_demographic_preferences WHERE user_id = p_user_id;
    DELETE FROM user_studio_preferences WHERE user_id = p_user_id;
    
    INSERT INTO user_genre_preferences (user_id, genre_id, weighted_score, rating_count)
    SELECT p_user_id, genre_id, weighted_score, rating_count
    FROM calculate_user_genre_preferences(p_user_id);
    
    INSERT INTO user_theme_preferences (user_id, theme_id, weighted_score, rating_count)
    SELECT p_user_id, theme_id, weighted_score, rating_count
    FROM calculate_user_theme_preferences(p_user_id);
    
    INSERT INTO user_demographic_preferences (user_id, demographic_id, weighted_score, rating_count)
    SELECT p_user_id, demographic_id, weighted_score, rating_count
    FROM calculate_user_demographic_preferences(p_user_id);
    
    INSERT INTO user_studio_preferences (user_id, studio_id, weighted_score, rating_count)
    SELECT p_user_id, studio_id, weighted_score, rating_count
    FROM calculate_user_studio_preferences(p_user_id);
END;
$$ LANGUAGE plpgsql;


-- ============================================================
-- STEP 6: GENERATE RECOMMENDATIONS 
-- ============================================================

CREATE OR REPLACE FUNCTION generate_recommendations(
    p_user_id INTEGER,
    p_limit INTEGER DEFAULT 10
)
RETURNS TABLE (
    rec_anime_id INTEGER,
    rec_title VARCHAR(500),
    rec_title_english VARCHAR(500),
    rec_type VARCHAR(50),
    rec_episodes INTEGER,
    rec_score DECIMAL(4, 2),
    rec_image_url TEXT,
    rec_synopsis TEXT,
    rec_recommendation_score DECIMAL(10, 4),
    rec_genre_score DECIMAL(10, 4),
    rec_theme_score DECIMAL(10, 4),
    rec_demographic_score DECIMAL(10, 4),
    rec_studio_score DECIMAL(10, 4)
) AS $$
DECLARE
    v_user_id INTEGER := p_user_id;  -- Use a local variable to avoid ambiguity
BEGIN
    PERFORM update_all_user_preferences(v_user_id);
    
    RETURN QUERY
    WITH 
    watched_anime AS (
        SELECT ual.anime_id
        FROM user_anime_list ual
        WHERE ual.user_id = v_user_id
    ),
    
    genre_matches AS (
        SELECT 
            ag.anime_id,
            AVG(ugp.weighted_score) AS genre_score
        FROM anime_genres ag
        JOIN user_genre_preferences ugp ON ag.genre_id = ugp.genre_id
        WHERE ugp.user_id = v_user_id
        GROUP BY ag.anime_id
    ),
    
    theme_matches AS (
        SELECT 
            at.anime_id,
            AVG(utp.weighted_score) AS theme_score
        FROM anime_themes at
        JOIN user_theme_preferences utp ON at.theme_id = utp.theme_id
        WHERE utp.user_id = v_user_id
        GROUP BY at.anime_id
    ),
    
    demographic_matches AS (
        SELECT 
            ad.anime_id,
            AVG(udp.weighted_score) AS demographic_score
        FROM anime_demographics ad
        JOIN user_demographic_preferences udp ON ad.demographic_id = udp.demographic_id
        WHERE udp.user_id = v_user_id
        GROUP BY ad.anime_id
    ),
    
    studio_matches AS (
        SELECT 
            ast.anime_id,
            AVG(usp.weighted_score) AS studio_score
        FROM anime_studios ast
        JOIN user_studio_preferences usp ON ast.studio_id = usp.studio_id
        WHERE usp.user_id = v_user_id
        GROUP BY ast.anime_id
    )
    
    SELECT 
        a.anime_id,
        a.title,
        a.title_english,
        a.type,
        a.episodes,
        a.score,
        a.image_url,
        a.synopsis,
        (
            COALESCE(gm.genre_score * 0.40, 0) +
            COALESCE(tm.theme_score * 0.25, 0) +
            COALESCE(dm.demographic_score * 0.20, 0) +
            COALESCE(sm.studio_score * 0.15, 0)
        )::DECIMAL(10, 4) AS recommendation_score,
        COALESCE(gm.genre_score, 0)::DECIMAL(10, 4) AS genre_score,
        COALESCE(tm.theme_score, 0)::DECIMAL(10, 4) AS theme_score,
        COALESCE(dm.demographic_score, 0)::DECIMAL(10, 4) AS demographic_score,
        COALESCE(sm.studio_score, 0)::DECIMAL(10, 4) AS studio_score
    FROM anime a
    LEFT JOIN genre_matches gm ON a.anime_id = gm.anime_id
    LEFT JOIN theme_matches tm ON a.anime_id = tm.anime_id
    LEFT JOIN demographic_matches dm ON a.anime_id = dm.anime_id
    LEFT JOIN studio_matches sm ON a.anime_id = sm.anime_id
    WHERE 
        a.anime_id NOT IN (SELECT wa.anime_id FROM watched_anime wa)
        AND (
            gm.genre_score IS NOT NULL OR
            tm.theme_score IS NOT NULL OR
            dm.demographic_score IS NOT NULL OR
            sm.studio_score IS NOT NULL
        )
        AND a.score IS NOT NULL
        AND a.episodes IS NOT NULL
    ORDER BY recommendation_score DESC, a.score DESC
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- HELPER QUERY: Get User's Top Preferences Summary
-- ============================================================

CREATE OR REPLACE FUNCTION get_user_preference_summary(p_user_id INTEGER)
RETURNS TABLE (
    preference_type VARCHAR(50),
    preference_name VARCHAR(255),
    weighted_score DECIMAL(10, 4),
    rating_count INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'Genre'::VARCHAR(50) AS preference_type,
        genre_name::VARCHAR(255) AS preference_name,
        weighted_score,
        rating_count
    FROM calculate_user_genre_preferences(p_user_id)
    ORDER BY weighted_score DESC
    LIMIT 3;
    
    RETURN QUERY
    SELECT 
        'Theme'::VARCHAR(50) AS preference_type,
        theme_name::VARCHAR(255) AS preference_name,
        weighted_score,
        rating_count
    FROM calculate_user_theme_preferences(p_user_id)
    ORDER BY weighted_score DESC
    LIMIT 3;
    
    RETURN QUERY
    SELECT 
        'Demographic'::VARCHAR(50) AS preference_type,
        demographic_name::VARCHAR(255) AS preference_name,
        weighted_score,
        rating_count
    FROM calculate_user_demographic_preferences(p_user_id)
    ORDER BY weighted_score DESC
    LIMIT 2;
    
    RETURN QUERY
    SELECT 
        'Studio'::VARCHAR(50) AS preference_type,
        studio_name::VARCHAR(255) AS preference_name,
        weighted_score,
        rating_count
    FROM calculate_user_studio_preferences(p_user_id)
    ORDER BY weighted_score DESC
    LIMIT 3;
END;
$$ LANGUAGE plpgsql;


-- ============================================================
-- TESTING QUERIES
-- ============================================================

-- Test: Generate recommendations for user 1
-- SELECT * FROM generate_recommendations(1, 10);

-- Test: Get preference summary for user 1
-- SELECT * FROM get_user_preference_summary(1);