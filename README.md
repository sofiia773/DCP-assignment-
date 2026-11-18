# DCP-assignment-

## Description of the project

Daily Drink Tracker is a project that collects and analyses my daily drink consumption.

I record information about each drink, including the date, time, drink type, location, mood, energy level and taste rating.

The aim of this project is to understand my drinking habits, identify which drinks I choose most often and explore possible relationships between drink choices, mood and energy levels.

The data is stored in a CSV file, checked using Python and loaded into an SQLite database.




## Data Dictionary

| Column | Type | Units / Values | How I record it |
|--------|------|----------------|-----------------|
| date | Date | DD-MM-YYYY | The date I had a drink |
| time | Time | HH:MM| The time I start drinking |
| drink_type | Category | coffee/tea/soft drink | The drink I choose |
| location | Category | homу/university/cafe/other | Where I drink it |
| mood | Category | happy/neutral/sad | My mood after drinking |
| energy | Integer rating | 1–5 | My energy after drinking |
| taste_rating | Integer rating | 1–5 | My rating of the drink's taste after finishing it |
