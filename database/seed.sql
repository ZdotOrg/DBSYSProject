-- ============================================================
-- SAMPLE SEED DATA FOR ANIME TRACKER
-- Populates database with 50 popular anime for testing
-- ============================================================

-- Insert Studios
INSERT INTO studios (name, mal_id) VALUES
('Bones', 4),
('Madhouse', 11),
('MAPPA', 569),
('ufotable', 43),
('Wit Studio', 858),
('Production I.G', 10),
('Kyoto Animation', 2),
('A-1 Pictures', 56),
('Trigger', 803),
('Sunrise', 14),
('Studio Pierrot', 1),
('Toei Animation', 18),
('J.C.Staff', 7),
('Shaft', 44),
('Studio Ghibli', 21),
('CloverWorks', 1835),
('David Production', 287),
('White Fox', 314);

-- Insert Producers
INSERT INTO producers (name, mal_id) VALUES
('Aniplex', 17),
('Shueisha', 16),
('Dentsu', 53),
('Mainichi Broadcasting System', 143),
('Fuji TV', 127),
('Bandai Namco Entertainment', 1365),
('Sony Music Entertainment', 166),
('Kodansha', 10),
('TV Tokyo', 160),
('Kadokawa', 1696);

-- ============================================================
-- ANIME ENTRIES (50 Popular Anime)
-- ============================================================

INSERT INTO anime (mal_id, title, title_english, title_japanese, type, episodes, status, aired_from, aired_to, duration, rating, score, scored_by, rank, popularity, synopsis, season, year, image_url) VALUES

-- Shonen Action
(5114, 'Fullmetal Alchemist: Brotherhood', 'Fullmetal Alchemist: Brotherhood', '鋼の錬金術師 FULLMETAL ALCHEMIST', 'TV', 64, 'Finished Airing', '2009-04-05', '2010-07-04', '24 min per ep', 'R', 9.09, 1500000, 1, 3, 'Two brothers search for the Philosopher''s Stone to restore their bodies after a failed alchemical ritual.', 'Spring', 2009, 'https://cdn.myanimelist.net/images/anime/1223/96541.jpg'),

(9253, 'Steins;Gate', 'Steins;Gate', 'Steins;Gate', 'TV', 24, 'Finished Airing', '2011-04-06', '2011-09-14', '24 min per ep', 'PG-13', 9.07, 1200000, 2, 5, 'A self-proclaimed mad scientist discovers a way to send messages to the past, leading to dire consequences.', 'Spring', 2011, 'https://cdn.myanimelist.net/images/anime/5/73199.jpg'),

(28977, 'Gintama°', 'Gintama: Silver Soul Arc', '銀魂°', 'TV', 51, 'Finished Airing', '2015-04-08', '2016-03-30', '24 min per ep', 'PG-13', 9.06, 180000, 3, 420, 'Continuation of Gintoki''s adventures in an alternate feudal Japan invaded by aliens.', 'Spring', 2015, 'https://cdn.myanimelist.net/images/anime/3/72078.jpg'),

(38524, 'Shingeki no Kyojin Season 3 Part 2', 'Attack on Titan Season 3 Part 2', '進撃の巨人 Season 3 Part 2', 'TV', 10, 'Finished Airing', '2019-04-29', '2019-07-01', '24 min per ep', 'R', 9.05, 950000, 4, 15, 'Eren and the Survey Corps discover the truth about the Titans and the world outside the walls.', 'Spring', 2019, 'https://cdn.myanimelist.net/images/anime/1517/100633.jpg'),

(40028, 'Shingeki no Kyojin: The Final Season', 'Attack on Titan: The Final Season', '進撃の巨人 The Final Season', 'TV', 16, 'Finished Airing', '2020-12-07', '2021-03-29', '23 min per ep', 'R', 8.78, 850000, 25, 8, 'The war between Marley and Eldia intensifies as Eren takes drastic action.', 'Winter', 2021, 'https://cdn.myanimelist.net/images/anime/1000/110531.jpg'),

(9969, 'Gintama''', 'Gintama''', '銀魂''', 'TV', 51, 'Finished Airing', '2011-04-04', '2012-03-26', '24 min per ep', 'PG-13', 9.03, 175000, 5, 450, 'Gintoki, Shinpachi, and Kagura continue their hilarious adventures in Edo.', 'Spring', 2011, 'https://cdn.myanimelist.net/images/anime/4/50361.jpg'),

(918, 'Gintama', 'Gintama', '銀魂', 'TV', 201, 'Finished Airing', '2006-04-04', '2010-03-25', '24 min per ep', 'PG-13', 8.93, 280000, 15, 140, 'In an alternate Edo period, samurai Gintoki runs an odd-jobs business with his friends.', 'Spring', 2006, 'https://cdn.myanimelist.net/images/anime/10/73274.jpg'),

(11061, 'Hunter x Hunter (2011)', 'Hunter x Hunter', 'HUNTER×HUNTER（2011）', 'TV', 148, 'Finished Airing', '2011-10-02', '2014-09-24', '23 min per ep', 'PG-13', 9.03, 1100000, 6, 7, 'Young Gon Freecss becomes a Hunter to find his father and embarks on an adventure filled with friends and foes.', 'Fall', 2011, 'https://cdn.myanimelist.net/images/anime/1337/99013.jpg'),

(34096, 'Gintama.', 'Gintama.', '銀魂.', 'TV', 12, 'Finished Airing', '2017-01-09', '2017-03-27', '24 min per ep', 'PG-13', 9.01, 140000, 8, 550, 'The Yorozuya trio face their most dangerous foe yet in this penultimate arc.', 'Winter', 2017, 'https://cdn.myanimelist.net/images/anime/3/83528.jpg'),

(820, 'Ginga Eiyuu Densetsu', 'Legend of the Galactic Heroes', '銀河英雄伝説', 'OVA', 110, 'Finished Airing', '1988-12-01', '1997-03-01', '25 min per ep', 'R', 9.00, 85000, 10, 700, 'Two military geniuses face off in an epic space opera spanning decades of war.', NULL, 1988, 'https://cdn.myanimelist.net/images/anime/13/13225.jpg'),

-- Popular Action/Adventure
(16498, 'Shingeki no Kyojin', 'Attack on Titan', '進撃の巨人', 'TV', 25, 'Finished Airing', '2013-04-07', '2013-09-29', '24 min per ep', 'R', 8.54, 2500000, 70, 1, 'Humanity lives inside cities surrounded by walls to protect against man-eating Titans.', 'Spring', 2013, 'https://cdn.myanimelist.net/images/anime/10/47347.jpg'),

(1535, 'Death Note', 'Death Note', 'DEATH NOTE', 'TV', 37, 'Finished Airing', '2006-10-04', '2007-06-27', '23 min per ep', 'R', 8.62, 2200000, 50, 2, 'A high school student discovers a notebook that kills anyone whose name is written in it.', 'Fall', 2006, 'https://cdn.myanimelist.net/images/anime/9/9453.jpg'),

(20, 'Naruto', 'Naruto', 'NARUTO -ナルト-', 'TV', 220, 'Finished Airing', '2002-10-03', '2007-02-08', '23 min per ep', 'PG-13', 7.98, 1400000, 320, 9, 'Naruto Uzumaki, a young ninja, seeks recognition and dreams of becoming the Hokage.', 'Fall', 2002, 'https://cdn.myanimelist.net/images/anime/13/17405.jpg'),

(1735, 'Naruto: Shippuuden', 'Naruto: Shippuden', 'NARUTO -ナルト- 疾風伝', 'TV', 500, 'Finished Airing', '2007-02-15', '2017-03-23', '23 min per ep', 'PG-13', 8.26, 1300000, 150, 11, 'Naruto returns after two years of training to face the Akatsuki organization.', 'Winter', 2007, 'https://cdn.myanimelist.net/images/anime/5/17407.jpg'),

(21, 'One Piece', 'One Piece', 'ONE PIECE', 'TV', NULL, 'Currently Airing', '1999-10-20', NULL, '24 min per ep', 'PG-13', 8.71, 1000000, 30, 13, 'Monkey D. Luffy and his pirate crew search for the ultimate treasure, the One Piece.', 'Fall', 1999, 'https://cdn.myanimelist.net/images/anime/6/73245.jpg'),

(269, 'Bleach', 'Bleach', 'BLEACH', 'TV', 366, 'Finished Airing', '2004-10-05', '2012-03-27', '24 min per ep', 'PG-13', 7.92, 750000, 380, 34, 'Ichigo Kurosaki becomes a Soul Reaper and defends humans from evil spirits.', 'Fall', 2004, 'https://cdn.myanimelist.net/images/anime/3/40451.jpg'),

(31964, 'Boku no Hero Academia 2nd Season', 'My Hero Academia 2', '僕のヒーローアカデミア 2', 'TV', 25, 'Finished Airing', '2017-04-01', '2017-09-30', '24 min per ep', 'PG-13', 8.39, 900000, 110, 10, 'Izuku Midoriya continues his journey to become the greatest hero at U.A. High School.', 'Spring', 2017, 'https://cdn.myanimelist.net/images/anime/12/85221.jpg'),

(30276, 'One Punch Man', 'One Punch Man', 'ワンパンマン', 'TV', 12, 'Finished Airing', '2015-10-05', '2015-12-21', '24 min per ep', 'R', 8.49, 1700000, 95, 6, 'A hero who can defeat any opponent with a single punch searches for a worthy challenge.', 'Fall', 2015, 'https://cdn.myanimelist.net/images/anime/12/76049.jpg'),

(11757, 'Sword Art Online', 'Sword Art Online', 'ソードアート・オンライン', 'TV', 25, 'Finished Airing', '2012-07-08', '2012-12-23', '24 min per ep', 'PG-13', 7.20, 1600000, 750, 4, 'Players are trapped in a virtual reality MMORPG where death in-game means death in real life.', 'Summer', 2012, 'https://cdn.myanimelist.net/images/anime/11/39717.jpg'),

(22319, 'Tokyo Ghoul', 'Tokyo Ghoul', '東京喰種トーキョーグール', 'TV', 12, 'Finished Airing', '2014-07-04', '2014-09-19', '24 min per ep', 'R', 7.79, 1300000, 460, 12, 'A college student becomes a half-ghoul after an encounter with a flesh-eating monster.', 'Summer', 2014, 'https://cdn.myanimelist.net/images/anime/5/64449.jpg'),

-- Sci-Fi & Mecha
(30, 'Neon Genesis Evangelion', 'Neon Genesis Evangelion', '新世紀エヴァンゲリオン', 'TV', 26, 'Finished Airing', '1995-10-04', '1996-03-27', '24 min per ep', 'PG-13', 8.35, 750000, 125, 41, 'Teenagers pilot giant mechs to defend Earth from mysterious beings called Angels.', 'Fall', 1995, 'https://cdn.myanimelist.net/images/anime/10/21707.jpg'),

(6547, 'Angel Beats!', 'Angel Beats!', 'Angel Beats!', 'TV', 13, 'Finished Airing', '2010-04-03', '2010-06-26', '24 min per ep', 'PG-13', 8.09, 900000, 250, 29, 'A boy wakes up in the afterlife and joins a group rebelling against God.', 'Spring', 2010, 'https://cdn.myanimelist.net/images/anime/10/22061.jpg'),

(1, 'Cowboy Bebop', 'Cowboy Bebop', 'カウボーイビバップ', 'TV', 26, 'Finished Airing', '1998-04-03', '1999-04-24', '24 min per ep', 'R', 8.75, 850000, 28, 40, 'Bounty hunters travel through space in 2071, chasing criminals and confronting their pasts.', 'Spring', 1998, 'https://cdn.myanimelist.net/images/anime/4/19644.jpg'),

(1575, 'Code Geass: Hangyaku no Lelouch', 'Code Geass: Lelouch of the Rebellion', 'コードギアス 反逆のルルーシュ', 'TV', 25, 'Finished Airing', '2006-10-06', '2007-07-29', '24 min per ep', 'R', 8.70, 1200000, 32, 14, 'An exiled prince gains the power to control minds and leads a rebellion against an empire.', 'Fall', 2006, 'https://cdn.myanimelist.net/images/anime/5/50331.jpg'),

(32281, 'Kimi no Na wa.', 'Your Name.', '君の名は。', 'Movie', 1, 'Finished Airing', '2016-08-26', '2016-08-26', '1 hr 46 min', 'PG-13', 8.83, 1400000, 19, 16, 'Two teenagers mysteriously swap bodies and must find each other across time and space.', NULL, 2016, 'https://cdn.myanimelist.net/images/anime/5/87048.jpg'),

-- Drama & Slice of Life
(9756, 'Mahou Shoujo Madoka★Magica', 'Puella Magi Madoka Magica', '魔法少女まどか★マギカ', 'TV', 12, 'Finished Airing', '2011-01-07', '2011-04-22', '24 min per ep', 'PG-13', 8.36, 900000, 123, 35, 'A girl is offered the chance to become a magical girl, but the price is higher than expected.', 'Winter', 2011, 'https://cdn.myanimelist.net/images/anime/11/55225.jpg'),

(2167, 'Clannad: After Story', 'Clannad: After Story', 'CLANNAD〜AFTER STORY〜', 'TV', 24, 'Finished Airing', '2008-10-03', '2009-03-27', '24 min per ep', 'PG-13', 8.93, 650000, 16, 60, 'Tomoya and Nagisa face the challenges of adulthood, family, and tragedy.', 'Fall', 2008, 'https://cdn.myanimelist.net/images/anime/10/19621.jpg'),

(23273, 'Shigatsu wa Kimi no Uso', 'Your Lie in April', '四月は君の嘘', 'TV', 22, 'Finished Airing', '2014-10-10', '2015-03-20', '23 min per ep', 'PG-13', 8.64, 1000000, 44, 25, 'A piano prodigy who can no longer hear music meets a violinist who changes his life.', 'Fall', 2014, 'https://cdn.myanimelist.net/images/anime/3/67177.jpg'),

(28851, '3-gatsu no Lion', 'March comes in like a lion', '3月のライオン', 'TV', 22, 'Finished Airing', '2016-10-08', '2017-03-18', '25 min per ep', 'PG-13', 8.36, 160000, 124, 450, 'A young professional shogi player struggles with loneliness and finds a new family.', 'Fall', 2016, 'https://cdn.myanimelist.net/images/anime/9/114795.jpg'),

(37491, 'Gintama.: Shirogane no Tamashii-hen', 'Gintama.: Silver Soul Arc', '銀魂. 銀ノ魂篇', 'TV', 14, 'Finished Airing', '2018-01-08', '2018-03-26', '24 min per ep', 'PG-13', 8.98, 95000, 12, 830, 'The final battle for Edo begins as Gintoki and his friends face their greatest enemy.', 'Winter', 2018, 'https://cdn.myanimelist.net/images/anime/1776/96566.jpg'),

-- Romance & School
(2904, 'Code Geass: Hangyaku no Lelouch R2', 'Code Geass: Lelouch of the Rebellion R2', 'コードギアス 反逆のルルーシュR2', 'TV', 25, 'Finished Airing', '2008-04-06', '2008-09-28', '24 min per ep', 'R', 8.91, 1000000, 17, 22, 'Lelouch continues his rebellion against Britannia with heightened stakes.', 'Spring', 2008, 'https://cdn.myanimelist.net/images/anime/4/21517.jpg'),

(4181, 'Clannad', 'Clannad', 'CLANNAD -クラナド-', 'TV', 23, 'Finished Airing', '2007-10-05', '2008-03-28', '24 min per ep', 'PG-13', 8.00, 650000, 305, 58, 'A delinquent high schooler meets a shy girl and helps her revive the drama club.', 'Fall', 2007, 'https://cdn.myanimelist.net/images/anime/1804/95033.jpg'),

(14741, 'Chuunibyou demo Koi ga Shitai!', 'Love, Chunibyo & Other Delusions', '中二病でも恋がしたい！', 'TV', 12, 'Finished Airing', '2012-10-04', '2012-12-20', '24 min per ep', 'PG-13', 7.70, 450000, 530, 95, 'A boy tries to forget his embarrassing middle school persona but meets a girl who hasn''t.', 'Fall', 2012, 'https://cdn.myanimelist.net/images/anime/3/46984.jpg'),

(24705, 'Kiseijuu: Sei no Kakuritsu', 'Parasyte -the maxim-', '寄生獣 セイの格率', 'TV', 24, 'Finished Airing', '2014-10-09', '2015-03-26', '23 min per ep', 'R', 8.33, 850000, 130, 48, 'A teenager must coexist with an alien parasite that failed to take over his brain.', 'Fall', 2014, 'https://cdn.myanimelist.net/images/anime/3/73178.jpg'),

(35180, '3-gatsu no Lion 2nd Season', 'March comes in like a lion 2nd Season', '3月のライオン 第2シリーズ', 'TV', 22, 'Finished Airing', '2017-10-14', '2018-03-31', '25 min per ep', 'PG-13', 8.91, 140000, 18, 520, 'Rei continues to grow as a shogi player and person with the help of the Kawamoto sisters.', 'Fall', 2017, 'https://cdn.myanimelist.net/images/anime/3/88469.jpg'),

-- Comedy
(15417, 'Gintama'': Enchousen', 'Gintama: Enchousen', '銀魂'' 延長戦', 'TV', 13, 'Finished Airing', '2012-10-04', '2013-03-28', '24 min per ep', 'PG-13', 9.02, 150000, 7, 600, 'The Yorozuya continue their odd jobs and misadventures in Edo.', 'Fall', 2012, 'https://cdn.myanimelist.net/images/anime/4/50361.jpg'),

(33255, 'Saiki Kusuo no Ψ-nan', 'The Disastrous Life of Saiki K.', '斉木楠雄のΨ難', 'TV', 120, 'Finished Airing', '2016-07-04', '2016-12-26', '4 min per ep', 'PG-13', 8.41, 400000, 108, 110, 'A psychic high schooler tries to live a normal life despite his overwhelming powers.', 'Summer', 2016, 'https://cdn.myanimelist.net/images/anime/8/80859.jpg'),

(37976, 'Gintama.: Shirogane no Tamashii-hen - Kouhan-sen', 'Gintama.: Silver Soul Arc - Second Half War', '銀魂. 銀ノ魂篇 後半戦', 'TV', 14, 'Finished Airing', '2018-07-09', '2018-10-08', '24 min per ep', 'PG-13', 8.99, 90000, 11, 900, 'The final chapter of Gintama as all storylines converge for the ultimate conclusion.', 'Summer', 2018, 'https://cdn.myanimelist.net/images/anime/1271/96010.jpg'),

(50265, 'Spy x Family', 'SPY x FAMILY', 'SPY×FAMILY', 'TV', 12, 'Finished Airing', '2022-04-09', '2022-06-25', '24 min per ep', 'PG-13', 8.50, 800000, 92, 17, 'A spy, an assassin, and a telepath form a fake family for their separate missions.', 'Spring', 2022, 'https://cdn.myanimelist.net/images/anime/1441/122795.jpg'),

-- Thriller & Mystery
(19, 'Monster', 'Monster', 'MONSTER', 'TV', 74, 'Finished Airing', '2004-04-07', '2005-09-28', '24 min per ep', 'R', 8.86, 350000, 20, 120, 'A brain surgeon saves a boy''s life, only to discover he has created a monster.', 'Spring', 2004, 'https://cdn.myanimelist.net/images/anime/10/18793.jpg'),

(205, 'Samurai Champloo', 'Samurai Champloo', 'サムライチャンプルー', 'TV', 26, 'Finished Airing', '2004-05-20', '2005-03-19', '24 min per ep', 'R', 8.49, 550000, 96, 75, 'Two samurai and a girl embark on a journey to find the samurai who smells of sunflowers.', 'Spring', 2004, 'https://cdn.myanimelist.net/images/anime/5/6965.jpg'),

(17074, 'Monogatari Series: Second Season', 'Monogatari Series: Second Season', '〈物語〉シリーズ セカンドシーズン', 'TV', 26, 'Finished Airing', '2013-07-07', '2013-12-29', '27 min per ep', 'R', 8.76, 350000, 27, 135, 'Koyomi Araragi continues to help girls with supernatural afflictions.', 'Summer', 2013, 'https://cdn.myanimelist.net/images/anime/10/51837.jpg'),

(34572, 'Black Clover', 'Black Clover', 'ブラッククローバー', 'TV', 170, 'Finished Airing', '2017-10-03', '2021-03-30', '24 min per ep', 'PG-13', 8.13, 650000, 220, 37, 'A boy born without magic aims to become the Wizard King in a world where magic is everything.', 'Fall', 2017, 'https://cdn.myanimelist.net/images/anime/1800/112550.jpg'),

(42938, 'Fruits Basket: The Final', 'Fruits Basket: The Final', 'フルーツバスケット The Final', 'TV', 13, 'Finished Airing', '2021-04-06', '2021-06-29', '24 min per ep', 'PG-13', 8.97, 140000, 13, 380, 'The Soma family curse reaches its conclusion as secrets are revealed.', 'Spring', 2021, 'https://cdn.myanimelist.net/images/anime/1085/114792.jpg'),

-- Sports
(20583, 'Haikyuu!!', 'Haikyu!!', 'ハイキュー!!', 'TV', 25, 'Finished Airing', '2014-04-06', '2014-09-21', '24 min per ep', 'PG-13', 8.44, 850000, 102, 27, 'A short boy joins his high school volleyball team and aims for the nationals.', 'Spring', 2014, 'https://cdn.myanimelist.net/images/anime/7/76014.jpg'),

(2236, 'Hajime no Ippo: New Challenger', 'Hajime no Ippo: New Challenger', 'はじめの一歩 New Challenger', 'TV', 26, 'Finished Airing', '2009-01-06', '2009-06-30', '24 min per ep', 'PG-13', 8.75, 130000, 29, 850, 'Ippo continues his boxing career facing new challenges and powerful opponents.', 'Winter', 2009, 'https://cdn.myanimelist.net/images/anime/1382/93210.jpg'),

(10087, 'Fate/Zero', 'Fate/Zero', 'Fate/Zero', 'TV', 13, 'Finished Airing', '2011-10-02', '2011-12-25', '24 min per ep', 'R', 8.27, 750000, 145, 54, 'Seven mages summon heroic spirits to fight for the Holy Grail in a deadly battle royale.', 'Fall', 2011, 'https://cdn.myanimelist.net/images/anime/2/73199.jpg'),

(11741, 'Fate/Zero 2nd Season', 'Fate/Zero 2nd Season', 'Fate/Zero 2ndシーズン', 'TV', 12, 'Finished Airing', '2012-04-08', '2012-06-24', '24 min per ep', 'R', 8.54, 720000, 71, 61, 'The Holy Grail War reaches its climax as alliances crumble and fates are decided.', 'Spring', 2012, 'https://cdn.myanimelist.net/images/anime/8/41077.jpg');

-- ============================================================
-- ANIME-GENRE RELATIONSHIPS
-- ============================================================

-- Fullmetal Alchemist: Brotherhood (Action, Adventure, Drama, Fantasy)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 5114), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 5114), (SELECT genre_id FROM genres WHERE name = 'Adventure')),
((SELECT anime_id FROM anime WHERE mal_id = 5114), (SELECT genre_id FROM genres WHERE name = 'Drama')),
((SELECT anime_id FROM anime WHERE mal_id = 5114), (SELECT genre_id FROM genres WHERE name = 'Fantasy'));

-- Steins;Gate (Sci-Fi, Thriller, Drama)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 9253), (SELECT genre_id FROM genres WHERE name = 'Sci-Fi')),
((SELECT anime_id FROM anime WHERE mal_id = 9253), (SELECT genre_id FROM genres WHERE name = 'Thriller')),
((SELECT anime_id FROM anime WHERE mal_id = 9253), (SELECT genre_id FROM genres WHERE name = 'Drama'));

-- Gintama° (Action, Comedy, Sci-Fi)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 28977), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 28977), (SELECT genre_id FROM genres WHERE name = 'Comedy')),
((SELECT anime_id FROM anime WHERE mal_id = 28977), (SELECT genre_id FROM genres WHERE name = 'Sci-Fi'));

-- Attack on Titan Season 3 Part 2 (Action, Drama)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 38524), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 38524), (SELECT genre_id FROM genres WHERE name = 'Drama'));

-- Attack on Titan: The Final Season (Action, Drama)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 40028), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 40028), (SELECT genre_id FROM genres WHERE name = 'Drama'));

-- Gintama'' (Action, Comedy, Sci-Fi)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 9969), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 9969), (SELECT genre_id FROM genres WHERE name = 'Comedy')),
((SELECT anime_id FROM anime WHERE mal_id = 9969), (SELECT genre_id FROM genres WHERE name = 'Sci-Fi'));

-- Gintama (Action, Comedy, Sci-Fi)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 918), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 918), (SELECT genre_id FROM genres WHERE name = 'Comedy')),
((SELECT anime_id FROM anime WHERE mal_id = 918), (SELECT genre_id FROM genres WHERE name = 'Sci-Fi'));

-- Hunter x Hunter (Action, Adventure)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 11061), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 11061), (SELECT genre_id FROM genres WHERE name = 'Adventure'));

-- Attack on Titan (Action, Drama, Fantasy)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 16498), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 16498), (SELECT genre_id FROM genres WHERE name = 'Drama')),
((SELECT anime_id FROM anime WHERE mal_id = 16498), (SELECT genre_id FROM genres WHERE name = 'Fantasy'));

-- Death Note (Mystery, Thriller, Supernatural)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 1535), (SELECT genre_id FROM genres WHERE name = 'Mystery')),
((SELECT anime_id FROM anime WHERE mal_id = 1535), (SELECT genre_id FROM genres WHERE name = 'Thriller')),
((SELECT anime_id FROM anime WHERE mal_id = 1535), (SELECT genre_id FROM genres WHERE name = 'Supernatural'));

-- Naruto (Action, Adventure, Comedy)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 20), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 20), (SELECT genre_id FROM genres WHERE name = 'Adventure')),
((SELECT anime_id FROM anime WHERE mal_id = 20), (SELECT genre_id FROM genres WHERE name = 'Comedy'));

-- Naruto Shippuden (Action, Adventure)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 1735), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 1735), (SELECT genre_id FROM genres WHERE name = 'Adventure'));

-- One Piece (Action, Adventure, Comedy)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 21), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 21), (SELECT genre_id FROM genres WHERE name = 'Adventure')),
((SELECT anime_id FROM anime WHERE mal_id = 21), (SELECT genre_id FROM genres WHERE name = 'Comedy'));

-- Bleach (Action, Adventure, Supernatural)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 269), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 269), (SELECT genre_id FROM genres WHERE name = 'Adventure')),
((SELECT anime_id FROM anime WHERE mal_id = 269), (SELECT genre_id FROM genres WHERE name = 'Supernatural'));

-- My Hero Academia 2 (Action)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 31964), (SELECT genre_id FROM genres WHERE name = 'Action'));

-- One Punch Man (Action, Comedy, Sci-Fi)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 30276), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 30276), (SELECT genre_id FROM genres WHERE name = 'Comedy')),
((SELECT anime_id FROM anime WHERE mal_id = 30276), (SELECT genre_id FROM genres WHERE name = 'Sci-Fi'));

-- Sword Art Online (Action, Adventure, Romance)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 11757), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 11757), (SELECT genre_id FROM genres WHERE name = 'Adventure')),
((SELECT anime_id FROM anime WHERE mal_id = 11757), (SELECT genre_id FROM genres WHERE name = 'Romance'));

-- Tokyo Ghoul (Action, Horror, Mystery)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 22319), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 22319), (SELECT genre_id FROM genres WHERE name = 'Horror')),
((SELECT anime_id FROM anime WHERE mal_id = 22319), (SELECT genre_id FROM genres WHERE name = 'Mystery'));

-- Evangelion (Action, Drama, Sci-Fi)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 30), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 30), (SELECT genre_id FROM genres WHERE name = 'Drama')),
((SELECT anime_id FROM anime WHERE mal_id = 30), (SELECT genre_id FROM genres WHERE name = 'Sci-Fi'));

-- Angel Beats (Drama, Supernatural)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 6547), (SELECT genre_id FROM genres WHERE name = 'Drama')),
((SELECT anime_id FROM anime WHERE mal_id = 6547), (SELECT genre_id FROM genres WHERE name = 'Supernatural'));

-- Cowboy Bebop (Action, Sci-Fi)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 1), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 1), (SELECT genre_id FROM genres WHERE name = 'Sci-Fi'));

-- Code Geass (Action, Drama, Sci-Fi)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 1575), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 1575), (SELECT genre_id FROM genres WHERE name = 'Drama')),
((SELECT anime_id FROM anime WHERE mal_id = 1575), (SELECT genre_id FROM genres WHERE name = 'Sci-Fi'));

-- Your Name (Drama, Romance, Supernatural)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 32281), (SELECT genre_id FROM genres WHERE name = 'Drama')),
((SELECT anime_id FROM anime WHERE mal_id = 32281), (SELECT genre_id FROM genres WHERE name = 'Romance')),
((SELECT anime_id FROM anime WHERE mal_id = 32281), (SELECT genre_id FROM genres WHERE name = 'Supernatural'));

-- Madoka Magica (Drama, Thriller)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 9756), (SELECT genre_id FROM genres WHERE name = 'Drama')),
((SELECT anime_id FROM anime WHERE mal_id = 9756), (SELECT genre_id FROM genres WHERE name = 'Thriller'));

-- Clannad After Story (Drama, Romance, Slice of Life)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 2167), (SELECT genre_id FROM genres WHERE name = 'Drama')),
((SELECT anime_id FROM anime WHERE mal_id = 2167), (SELECT genre_id FROM genres WHERE name = 'Romance')),
((SELECT anime_id FROM anime WHERE mal_id = 2167), (SELECT genre_id FROM genres WHERE name = 'Slice of Life'));

-- Your Lie in April (Drama, Romance)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 23273), (SELECT genre_id FROM genres WHERE name = 'Drama')),
((SELECT anime_id FROM anime WHERE mal_id = 23273), (SELECT genre_id FROM genres WHERE name = 'Romance'));

-- March comes in like a lion (Drama, Slice of Life)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 28851), (SELECT genre_id FROM genres WHERE name = 'Drama')),
((SELECT anime_id FROM anime WHERE mal_id = 28851), (SELECT genre_id FROM genres WHERE name = 'Slice of Life'));

-- Spy x Family (Action, Comedy)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 50265), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 50265), (SELECT genre_id FROM genres WHERE name = 'Comedy'));

-- Monster (Drama, Mystery, Thriller)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 19), (SELECT genre_id FROM genres WHERE name = 'Drama')),
((SELECT anime_id FROM anime WHERE mal_id = 19), (SELECT genre_id FROM genres WHERE name = 'Mystery')),
((SELECT anime_id FROM anime WHERE mal_id = 19), (SELECT genre_id FROM genres WHERE name = 'Thriller'));

-- Samurai Champloo (Action, Adventure)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 205), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 205), (SELECT genre_id FROM genres WHERE name = 'Adventure'));

-- Black Clover (Action, Comedy, Fantasy)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 34572), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 34572), (SELECT genre_id FROM genres WHERE name = 'Comedy')),
((SELECT anime_id FROM anime WHERE mal_id = 34572), (SELECT genre_id FROM genres WHERE name = 'Fantasy'));

-- Fruits Basket: The Final (Drama, Romance, Supernatural)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 42938), (SELECT genre_id FROM genres WHERE name = 'Drama')),
((SELECT anime_id FROM anime WHERE mal_id = 42938), (SELECT genre_id FROM genres WHERE name = 'Romance')),
((SELECT anime_id FROM anime WHERE mal_id = 42938), (SELECT genre_id FROM genres WHERE name = 'Supernatural'));

-- Haikyuu (Sports, Drama)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 20583), (SELECT genre_id FROM genres WHERE name = 'Sports')),
((SELECT anime_id FROM anime WHERE mal_id = 20583), (SELECT genre_id FROM genres WHERE name = 'Drama'));

-- Fate/Zero (Action, Fantasy, Supernatural)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 10087), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 10087), (SELECT genre_id FROM genres WHERE name = 'Fantasy')),
((SELECT anime_id FROM anime WHERE mal_id = 10087), (SELECT genre_id FROM genres WHERE name = 'Supernatural'));

-- Fate/Zero 2nd Season (Action, Fantasy, Supernatural)
INSERT INTO anime_genres (anime_id, genre_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 11741), (SELECT genre_id FROM genres WHERE name = 'Action')),
((SELECT anime_id FROM anime WHERE mal_id = 11741), (SELECT genre_id FROM genres WHERE name = 'Fantasy')),
((SELECT anime_id FROM anime WHERE mal_id = 11741), (SELECT genre_id FROM genres WHERE name = 'Supernatural'));

-- ============================================================
-- ANIME-THEME RELATIONSHIPS
-- ============================================================

-- Fullmetal Alchemist: Brotherhood (Military)
INSERT INTO anime_themes (anime_id, theme_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 5114), (SELECT theme_id FROM themes WHERE name = 'Military'));

-- Attack on Titan (Military)
INSERT INTO anime_themes (anime_id, theme_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 16498), (SELECT theme_id FROM themes WHERE name = 'Military')),
((SELECT anime_id FROM anime WHERE mal_id = 38524), (SELECT theme_id FROM themes WHERE name = 'Military')),
((SELECT anime_id FROM anime WHERE mal_id = 40028), (SELECT theme_id FROM themes WHERE name = 'Military'));

-- Death Note (School, Psychological)
INSERT INTO anime_themes (anime_id, theme_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 1535), (SELECT theme_id FROM themes WHERE name = 'School')),
((SELECT anime_id FROM anime WHERE mal_id = 1535), (SELECT theme_id FROM themes WHERE name = 'Psychological'));

-- Sword Art Online (Isekai)
INSERT INTO anime_themes (anime_id, theme_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 11757), (SELECT theme_id FROM themes WHERE name = 'Isekai'));

-- Evangelion (Mecha, Psychological)
INSERT INTO anime_themes (anime_id, theme_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 30), (SELECT theme_id FROM themes WHERE name = 'Mecha')),
((SELECT anime_id FROM anime WHERE mal_id = 30), (SELECT theme_id FROM themes WHERE name = 'Psychological'));

-- Angel Beats (School)
INSERT INTO anime_themes (anime_id, theme_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 6547), (SELECT theme_id FROM themes WHERE name = 'School'));

-- Code Geass (Mecha, School, Military)
INSERT INTO anime_themes (anime_id, theme_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 1575), (SELECT theme_id FROM themes WHERE name = 'Mecha')),
((SELECT anime_id FROM anime WHERE mal_id = 1575), (SELECT theme_id FROM themes WHERE name = 'School')),
((SELECT anime_id FROM anime WHERE mal_id = 1575), (SELECT theme_id FROM themes WHERE name = 'Military')),
((SELECT anime_id FROM anime WHERE mal_id = 2904), (SELECT theme_id FROM themes WHERE name = 'Mecha')),
((SELECT anime_id FROM anime WHERE mal_id = 2904), (SELECT theme_id FROM themes WHERE name = 'Military'));

-- Madoka Magica (Magic, Psychological)
INSERT INTO anime_themes (anime_id, theme_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 9756), (SELECT theme_id FROM themes WHERE name = 'Magic')),
((SELECT anime_id FROM anime WHERE mal_id = 9756), (SELECT theme_id FROM themes WHERE name = 'Psychological'));

-- Clannad (School)
INSERT INTO anime_themes (anime_id, theme_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 4181), (SELECT theme_id FROM themes WHERE name = 'School')),
((SELECT anime_id FROM anime WHERE mal_id = 2167), (SELECT theme_id FROM themes WHERE name = 'School'));

-- Your Lie in April (Music, School)
INSERT INTO anime_themes (anime_id, theme_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 23273), (SELECT theme_id FROM themes WHERE name = 'Music')),
((SELECT anime_id FROM anime WHERE mal_id = 23273), (SELECT theme_id FROM themes WHERE name = 'School'));

-- My Hero Academia (School)
INSERT INTO anime_themes (anime_id, theme_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 31964), (SELECT theme_id FROM themes WHERE name = 'School'));

-- Monster (Historical, Psychological)
INSERT INTO anime_themes (anime_id, theme_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 19), (SELECT theme_id FROM themes WHERE name = 'Historical')),
((SELECT anime_id FROM anime WHERE mal_id = 19), (SELECT theme_id FROM themes WHERE name = 'Psychological'));

-- Samurai Champloo (Historical)
INSERT INTO anime_themes (anime_id, theme_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 205), (SELECT theme_id FROM themes WHERE name = 'Historical'));

-- Black Clover (Magic)
INSERT INTO anime_themes (anime_id, theme_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 34572), (SELECT theme_id FROM themes WHERE name = 'Magic'));

-- Haikyuu (School)
INSERT INTO anime_themes (anime_id, theme_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 20583), (SELECT theme_id FROM themes WHERE name = 'School'));

-- ============================================================
-- ANIME-DEMOGRAPHIC RELATIONSHIPS
-- ============================================================

-- Shounen anime
INSERT INTO anime_demographics (anime_id, demographic_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 5114), (SELECT demographic_id FROM demographics WHERE name = 'Shounen')),
((SELECT anime_id FROM anime WHERE mal_id = 16498), (SELECT demographic_id FROM demographics WHERE name = 'Shounen')),
((SELECT anime_id FROM anime WHERE mal_id = 38524), (SELECT demographic_id FROM demographics WHERE name = 'Shounen')),
((SELECT anime_id FROM anime WHERE mal_id = 40028), (SELECT demographic_id FROM demographics WHERE name = 'Shounen')),
((SELECT anime_id FROM anime WHERE mal_id = 20), (SELECT demographic_id FROM demographics WHERE name = 'Shounen')),
((SELECT anime_id FROM anime WHERE mal_id = 1735), (SELECT demographic_id FROM demographics WHERE name = 'Shounen')),
((SELECT anime_id FROM anime WHERE mal_id = 21), (SELECT demographic_id FROM demographics WHERE name = 'Shounen')),
((SELECT anime_id FROM anime WHERE mal_id = 269), (SELECT demographic_id FROM demographics WHERE name = 'Shounen')),
((SELECT anime_id FROM anime WHERE mal_id = 11061), (SELECT demographic_id FROM demographics WHERE name = 'Shounen')),
((SELECT anime_id FROM anime WHERE mal_id = 31964), (SELECT demographic_id FROM demographics WHERE name = 'Shounen')),
((SELECT anime_id FROM anime WHERE mal_id = 34572), (SELECT demographic_id FROM demographics WHERE name = 'Shounen')),
((SELECT anime_id FROM anime WHERE mal_id = 20583), (SELECT demographic_id FROM demographics WHERE name = 'Shounen'));

-- Seinen anime
INSERT INTO anime_demographics (anime_id, demographic_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 9253), (SELECT demographic_id FROM demographics WHERE name = 'Seinen')),
((SELECT anime_id FROM anime WHERE mal_id = 1535), (SELECT demographic_id FROM demographics WHERE name = 'Seinen')),
((SELECT anime_id FROM anime WHERE mal_id = 22319), (SELECT demographic_id FROM demographics WHERE name = 'Seinen')),
((SELECT anime_id FROM anime WHERE mal_id = 1), (SELECT demographic_id FROM demographics WHERE name = 'Seinen')),
((SELECT anime_id FROM anime WHERE mal_id = 19), (SELECT demographic_id FROM demographics WHERE name = 'Seinen')),
((SELECT anime_id FROM anime WHERE mal_id = 205), (SELECT demographic_id FROM demographics WHERE name = 'Seinen')),
((SELECT anime_id FROM anime WHERE mal_id = 28851), (SELECT demographic_id FROM demographics WHERE name = 'Seinen')),
((SELECT anime_id FROM anime WHERE mal_id = 35180), (SELECT demographic_id FROM demographics WHERE name = 'Seinen')),
((SELECT anime_id FROM anime WHERE mal_id = 918), (SELECT demographic_id FROM demographics WHERE name = 'Shounen')),
((SELECT anime_id FROM anime WHERE mal_id = 9969), (SELECT demographic_id FROM demographics WHERE name = 'Shounen')),
((SELECT anime_id FROM anime WHERE mal_id = 28977), (SELECT demographic_id FROM demographics WHERE name = 'Shounen'));

-- Shoujo anime
INSERT INTO anime_demographics (anime_id, demographic_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 42938), (SELECT demographic_id FROM demographics WHERE name = 'Shoujo'));

-- ============================================================
-- ANIME-STUDIO RELATIONSHIPS
-- ============================================================

-- Bones productions
INSERT INTO anime_studios (anime_id, studio_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 5114), (SELECT studio_id FROM studios WHERE name = 'Bones'));

-- Madhouse productions
INSERT INTO anime_studios (anime_id, studio_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 11061), (SELECT studio_id FROM studios WHERE name = 'Madhouse')),
((SELECT anime_id FROM anime WHERE mal_id = 30276), (SELECT studio_id FROM studios WHERE name = 'Madhouse')),
((SELECT anime_id FROM anime WHERE mal_id = 19), (SELECT studio_id FROM studios WHERE name = 'Madhouse'));

-- MAPPA productions
INSERT INTO anime_studios (anime_id, studio_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 40028), (SELECT studio_id FROM studios WHERE name = 'MAPPA'));

-- ufotable productions
INSERT INTO anime_studios (anime_id, studio_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 10087), (SELECT studio_id FROM studios WHERE name = 'ufotable')),
((SELECT anime_id FROM anime WHERE mal_id = 11741), (SELECT studio_id FROM studios WHERE name = 'ufotable'));

-- Wit Studio productions
INSERT INTO anime_studios (anime_id, studio_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 16498), (SELECT studio_id FROM studios WHERE name = 'Wit Studio')),
((SELECT anime_id FROM anime WHERE mal_id = 38524), (SELECT studio_id FROM studios WHERE name = 'Wit Studio'));

-- Kyoto Animation productions
INSERT INTO anime_studios (anime_id, studio_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 4181), (SELECT studio_id FROM studios WHERE name = 'Kyoto Animation')),
((SELECT anime_id FROM anime WHERE mal_id = 2167), (SELECT studio_id FROM studios WHERE name = 'Kyoto Animation')),
((SELECT anime_id FROM anime WHERE mal_id = 14741), (SELECT studio_id FROM studios WHERE name = 'Kyoto Animation'));

-- A-1 Pictures productions
INSERT INTO anime_studios (anime_id, studio_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 11757), (SELECT studio_id FROM studios WHERE name = 'A-1 Pictures')),
((SELECT anime_id FROM anime WHERE mal_id = 23273), (SELECT studio_id FROM studios WHERE name = 'A-1 Pictures'));

-- White Fox productions
INSERT INTO anime_studios (anime_id, studio_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 9253), (SELECT studio_id FROM studios WHERE name = 'White Fox'));

-- Shaft productions
INSERT INTO anime_studios (anime_id, studio_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 9756), (SELECT studio_id FROM studios WHERE name = 'Shaft')),
((SELECT anime_id FROM anime WHERE mal_id = 17074), (SELECT studio_id FROM studios WHERE name = 'Shaft'));

-- Sunrise productions
INSERT INTO anime_studios (anime_id, studio_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 1575), (SELECT studio_id FROM studios WHERE name = 'Sunrise')),
((SELECT anime_id FROM anime WHERE mal_id = 2904), (SELECT studio_id FROM studios WHERE name = 'Sunrise')),
((SELECT anime_id FROM anime WHERE mal_id = 918), (SELECT studio_id FROM studios WHERE name = 'Sunrise')),
((SELECT anime_id FROM anime WHERE mal_id = 9969), (SELECT studio_id FROM studios WHERE name = 'Sunrise')),
((SELECT anime_id FROM anime WHERE mal_id = 28977), (SELECT studio_id FROM studios WHERE name = 'Sunrise'));

-- CloverWorks productions
INSERT INTO anime_studios (anime_id, studio_id) VALUES
((SELECT anime_id FROM anime WHERE mal_id = 50265), (SELECT studio_id FROM studios WHERE name = 'CloverWorks'));

-- ============================================================
-- TEST USER ACCOUNTS
-- ============================================================

-- Create test users (passwords should be hashed in production - these are placeholders)
INSERT INTO users (username, email, password_hash) VALUES
('testuser1', 'test1@example.com', 'hashed_password_1'),
('testuser2', 'test2@example.com', 'hashed_password_2'),
('animeenthusiast', 'enthusiast@example.com', 'hashed_password_3');

-- ============================================================
-- SAMPLE WATCHLIST ENTRIES
-- ============================================================

-- Test User 1 watchlist
INSERT INTO user_anime_list (user_id, anime_id, watch_status, user_score, episodes_watched, start_date, finish_date) VALUES
((SELECT user_id FROM users WHERE username = 'testuser1'), (SELECT anime_id FROM anime WHERE mal_id = 5114), 'Completed', 10, 64, '2023-01-15', '2023-02-20'),
((SELECT user_id FROM users WHERE username = 'testuser1'), (SELECT anime_id FROM anime WHERE mal_id = 16498), 'Completed', 9, 25, '2023-03-01', '2023-03-15'),
((SELECT user_id FROM users WHERE username = 'testuser1'), (SELECT anime_id FROM anime WHERE mal_id = 9253), 'Completed', 9, 24, '2023-04-01', '2023-04-12'),
((SELECT user_id FROM users WHERE username = 'testuser1'), (SELECT anime_id FROM anime WHERE mal_id = 11061), 'Watching', 9, 50, '2023-05-01', NULL),
((SELECT user_id FROM users WHERE username = 'testuser1'), (SELECT anime_id FROM anime WHERE mal_id = 21), 'Plan to Watch', NULL, 0, NULL, NULL);

-- Test User 2 watchlist
INSERT INTO user_anime_list (user_id, anime_id, watch_status, user_score, episodes_watched, start_date, finish_date) VALUES
((SELECT user_id FROM users WHERE username = 'testuser2'), (SELECT anime_id FROM anime WHERE mal_id = 1535), 'Completed', 8, 37, '2023-01-10', '2023-02-01'),
((SELECT user_id FROM users WHERE username = 'testuser2'), (SELECT anime_id FROM anime WHERE mal_id = 2167), 'Completed', 10, 24, '2023-02-15', '2023-03-05'),
((SELECT user_id FROM users WHERE username = 'testuser2'), (SELECT anime_id FROM anime WHERE mal_id = 23273), 'Completed', 9, 22, '2023-03-10', '2023-03-25'),
((SELECT user_id FROM users WHERE username = 'testuser2'), (SELECT anime_id FROM anime WHERE mal_id = 11757), 'Dropped', 6, 10, '2023-04-01', NULL),
((SELECT user_id FROM users WHERE username = 'testuser2'), (SELECT anime_id FROM anime WHERE mal_id = 32281), 'Plan to Watch', NULL, 0, NULL, NULL);

-- Anime Enthusiast watchlist
INSERT INTO user_anime_list (user_id, anime_id, watch_status, user_score, episodes_watched, start_date, finish_date) VALUES
((SELECT user_id FROM users WHERE username = 'animeenthusiast'), (SELECT anime_id FROM anime WHERE mal_id = 918), 'Completed', 9, 201, '2022-01-01', '2022-06-30'),
((SELECT user_id FROM users WHERE username = 'animeenthusiast'), (SELECT anime_id FROM anime WHERE mal_id = 1), 'Completed', 10, 26, '2022-07-01', '2022-07-15'),
((SELECT user_id FROM users WHERE username = 'animeenthusiast'), (SELECT anime_id FROM anime WHERE mal_id = 1575), 'Completed', 9, 25, '2022-08-01', '2022-08-20'),
((SELECT user_id FROM users WHERE username = 'animeenthusiast'), (SELECT anime_id FROM anime WHERE mal_id = 50265), 'Watching', 8, 8, '2023-05-15', NULL),
((SELECT user_id FROM users WHERE username = 'animeenthusiast'), (SELECT anime_id FROM anime WHERE mal_id = 40028), 'On Hold', 8, 10, '2023-04-01', NULL);

-- ============================================================
-- VERIFICATION QUERIES (Optional - for testing)
-- ============================================================

-- Check total anime count
-- SELECT COUNT(*) as total_anime FROM anime;

-- Check total genres
-- SELECT COUNT(*) as total_genres FROM genres;

-- Check anime with most genres
-- SELECT a.title, COUNT(ag.genre_id) as genre_count
-- FROM anime a
-- JOIN anime_genres ag ON a.anime_id = ag.anime_id
-- GROUP BY a.anime_id, a.title
-- ORDER BY genre_count DESC
-- LIMIT 10;

-- Check user watchlists
-- SELECT u.username, COUNT(ual.list_id) as anime_count
-- FROM users u
-- LEFT JOIN user_anime_list ual ON u.user_id = ual.user_id
-- GROUP BY u.user_id, u.username;

-- ============================================================
-- END OF SEED DATA
-- ============================================================