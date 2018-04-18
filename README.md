# final_project
final project


Data sources used, including instructions for a user to access the data sources (e.g., API keys or client secrets needed, along with a pointer to instructions on how to obtain these and instructions for how to incorporate them into your program (e.g., secrets.py file format))
-Yelp fusion API and Walkscore API
-You will need an API key for both of these API's, name them YELP_API_KEY and WALKABILITY_API_KEY and save them into a file called secrets.py
-You can go on both API websites to create an app and get an API key
-For the yelp API key make sure you use the business search API
https://www.walkscore.com/professional/api.php
https://www.yelp.com/developers/documentation/v3/business_search


Brief description of how your code is structured, including the names of significant data processing functions (just the 2-3 most important functions--not a complete list) and class definitions.
-Created two caching files, one for yelp and one for Walkscore
-Then I create one database of restaurants for yelp and one for walkscore and populated them by iterating through the json files in each cache
-I made four functions to process information for each graphic display_address
-Then used interactive code to call each function


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
Pittsburgh

Type into the command line either (price, walkscore, rating, or type) and then the city you want
For example:
ratings Chicago
price Miami
walkscore Los Angeles
type Orlando

rating, price, review, and type all lead to different plotly graphs of maps and show each restaurant as a dot with associated information
rating, price, and walkscore are color coded 
