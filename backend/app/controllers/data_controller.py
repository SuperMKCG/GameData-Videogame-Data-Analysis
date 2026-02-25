import pandas as pd
import requests
import os
from app.models.dataset import GameDataset

class DataController:
    def __init__(self, df):
        self.df = df
        self.rawg_api_key = os.getenv("RAWG_API_KEY")
    
    # Filtering Global sales
    def top_global_sales(self):
        top_games = (
            self.df
            .sort_values(by='Global_Sales', ascending=False)
            .head(10)
            [['Name', 'Global_Sales', 'User_Score', 'Genre', 'Rating', 'Publisher']]
        )
        return top_games.to_dict(orient='records')
    
    #Filtering Sales by game genre
    def sales_by_genre(self):
        sales_genre = (
            self.df
            .groupby('Genre')['Global_Sales']
            .sum()
            .sort_values(ascending=False)
            .head(3)
            .reset_index()
        )
        return sales_genre.to_dict(orient='records')
    
    #Filtering Top publishers
    def top_publishers(self):
        top_pub = (
            self.df
            .groupby('Publisher')['Global_Sales']
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
        )
        return top_pub.to_dict(orient='records')
    
    #Filtering Sales by region
    def sales_by_region(self):
        sales_region = [
            {'Region': 'North America', 'Sales': float(self.df['NA_Sales'].sum())},
            {'Region': 'Europe', 'Sales': float(self.df['EU_Sales'].sum())},
            {'Region': 'Japan', 'Sales': float(self.df['JP_Sales'].sum())},
            {'Region': 'Other', 'Sales': float(self.df['Other_Sales'].sum())}

        ]
        return sales_region
    
    #Get images for the recommended games
    def get_game_image(self, game_name):
        url = "https://api.rawg.io/api/games"
        params = {
            "key" : self.rawg_api_key,
            "search": game_name,
            "page_size": 1
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data["results"]:
            return data["results"][0]["background_image"]
        return None


    #Filtering best games for the community
    def recommended_games(self,genre, rating, min_score):
        
        self.df['User_Score'] = pd.to_numeric(self.df['User_Score'], errors='coerce')

        rating_map = {
            "E": "Todos",
            "E10+": "Mayores de 10",
            "T": "Adolescentes",
            "M": "Maduro (+17)",
            "AO": "Solo adultos (+18)",
            "RP": "Pendiente"
        }

        max_score = min_score + 1

        if min_score == 9:
            filtered = self.df[
                (self.df['Genre'] == genre) &
                (self.df['Rating'] == rating) &
                (self.df['User_Score'] >= min_score) &
                (self.df['Publisher'].notna()) &
                (self.df['Publisher'].str.lower() != 'unknown')
            ]
        else:
            filtered = self.df[
                (self.df['Genre'] == genre) &
                (self.df['Rating'] == rating) &
                (self.df['User_Score'] >= min_score) &
                (self.df['User_Score'] < max_score) &
                (self.df['Publisher'].notna()) &
                (self.df['Publisher'].str.lower() != 'unknown')
            ]

        filtered = filtered.sort_values(by='User_Score', ascending=False)

        result = filtered.head(10).to_dict(orient='records')

        for game in result:
            game['Rating'] = rating_map.get(game['Rating'], game['Rating'])
            game['Image'] = self.get_game_image(game['Name'])
        
        return result


