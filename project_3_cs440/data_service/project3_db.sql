-- create a new database (if one does not already exist)
CREATE DATABASE IF NOT EXISTS news_scraper;

-- create a new table (if one does not already exists)
CREATE TABLE IF NOT EXISTS Prev_search(
search VARCHAR(100) NOT NULL,
time_searched time PRIMARY KEY);