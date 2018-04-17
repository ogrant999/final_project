# final_project
final project


Data sources used, including instructions for a user to access the data sources (e.g., API keys or client secrets needed, along with a pointer to instructions on how to obtain these and instructions for how to incorporate them into your program (e.g., secrets.py file format))
-Yelp fusion API and Walkscore API
-You will need an API key for both of these API's, name them YELP_API_KEY and WALKABILITY_API_KEY and save them into
a file called secrets.py
-You can go on both API websites to create an app and get an API key
https://www.walkscore.com/professional/api.php
https://www.yelp.com/developers/documentation/v3/business_search


Any other information needed to run the program (e.g., pointer to getting started info for plotly)
-
Brief description of how your code is structured, including the names of significant data processing functions (just the 2-3 most important functions--not a complete list) and class definitions.
-Created two caching files, one for yelp and one for Walkscore
-Then I create two databases for yelp and one for walkscore and populated them by iterating through the json

If there are large data structures (e.g., lists, dictionaries) that you create to organize your data for presentation, briefly describe them.
-
Brief user guide, including how to run the program and how to choose presentation options.
-run python3 final_proj.py
-This programs works for:
Chicago
Detroit
Los Angeles
New York
Atlanta
San Francisco
Orlando
Miami
Philadelphia
St. Louis

Type into the command line the city you want, and either (price, review, rating, or type)
For example: Chicago rating
