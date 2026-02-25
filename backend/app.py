
from app.models.dataset import GameDataset
from app.controllers.data_controller import DataController
from app.routes import app
import pandas as pd

dataset = GameDataset()

df = dataset.get_df()

controller = DataController(df)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
