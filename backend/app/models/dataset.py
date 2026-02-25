import pandas as pd
from pathlib import Path

class GameDataset:
    def __init__(self):
        pd.options.display.max_rows = 10000
        
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        csv_path = BASE_DIR/ "data" / "vgsales.csv"
        self.df = pd.read_csv(csv_path)

        #fill and clean data
        self.df['User_Score'] = pd.to_numeric(self.df['User_Score'], errors='coerce')
        mean_score = self.df['User_Score'].mean()
        self.df['User_Score'] = self.df['User_Score'].fillna(mean_score)

        self.df.loc[self.df['Name'] =='Stronghold 3', 'Publisher'] = 'SouthPeak Games'

        correction_dev = {
            'AMF Bowling 2004': 'Black Market Games',
            'Blitz: The League II': 'Midway Games',
            'Harry Potter and the Deathly Hallows - Part 2':'EA Bright Light',
            'The Wolf Among Us': 'Telltale Games'
        }
        for game, developer in correction_dev.items():
            self.df.loc[self.df['Name'] == game, 'Developer'] = developer

        correction_rating = {
            '100 Classic Books': 'E',
            '15 Days': 'T',
            'Achtung Panzer: Kharkov 1943': 'T',
            'Act of Aggression': 'T',
            'A Game of Thrones: Genesis': 'M',
            'Agatha Christie: The ABC Murders': 'T',
            "Agatha Christie's The ABC Murders": 'T',
            'AMF Bowling 2004': 'E',
            'Atelier Sophie: The Alchemist of the Mysterious Book': 'T',
            'Back to the Future: The Game': 'T',
            'Battle Worlds: Kronos': 'E10+',
            'Blitz: The League II': 'M',
            'Botanicula': 'E',
            'Bus Simulator 16': 'E',
            'Captain Morgane and the Golden Turtle': 'E10+',
            'Cities: Skylines Snowfall': 'E',
            'Colin McRae Rally 04': 'E',
            'Dark Souls III': 'M',
            'Dead or Alive Xtreme 3: Fortune': 'M',
            'Deponia': 'T',
            "Dino Dini's Kick Off Revival": 'E',
            'DoDonPachi Resurrection': 'T',
            'Euro Truck Simulator 2': 'E',
            'Football Manager 2013': 'E',
            'Football Manager 2015': 'E',
            'Football Manager Live': 'E',
            'Goodbye Deponia': 'T',
            'Harry Potter and the Deathly Hallows - Part 2': 'T',
            'Hearts of Iron IV': 'E10+',
            'Inazuma Eleven Strikers': 'E',
            'Machinarium': 'E10+',
            'Metro: Last Light': 'M',
            'Monster Rancher': 'E',
            'Off-Road Drive': 'E',
            'Oil Rush': 'E10+',
            'One Piece Unlimited Cruise SP': 'E10+',
            'Prison Architect': 'M',
            'Pro Cycling Manager 2016': 'E',
            'Pro Evolution Soccer 2012': 'E',
            'Pro Evolution Soccer 2015': 'E',
            'R4: Ridge Racer Type 4': 'E',
            'Robinson: The Journey': 'E',
            'Root Letter': 'M',
            'Saint Seiya: Brave Soldiers': 'T',
            'Saint Seiya: Sanctuary Battle': 'T',
            'Serious Sam 3: BFE': 'M',
            'Singstar: Ultimate Party': 'T',
            'Stellaris': 'E10+',
            'Stronghold Kingdoms': 'E10+',
            'SuperCar Challenge': 'E',
            'The Binding of Isaac': 'M',
            'The Book of Unwritten Tales 2': 'T',
            'The Inner World': 'T',
            'The Lost Chronicles of Zerzura': 'T',
            'The Night of the Rabbit': 'E10+',
            'The Void': 'M',
            'The Wolf Among Us': 'M',
            'Toy Soldiers: War Chest': 'T',
            'Transport Fever': 'E',
            'Trapped Dead': 'M',
            'War for the Overworld': 'T',
            'WipEout XL': 'E',
            'Wolfenstein: The Old Blood': 'M',
            'Zombie Army Trilogy': 'M'
        }
        for game, rating_val in correction_rating.items():
            self.df.loc[self.df['Name'] == game, 'Rating'] = rating_val

        self.df['Name'] = self.df['Name'].str.strip()
        self.df['Genre'] = self.df['Genre'].str.strip()

        self.df = self.df.sort_values('Global_Sales', ascending=False).drop_duplicates('Name')

        
    def get_df(self):
        return self.df
