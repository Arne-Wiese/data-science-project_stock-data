from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.components.layout import create_layout
from src.data.loader import load_event_data, load_sentiment_data, load_sector_data

SENTIMENT_DATA_PATH = "./data/sentiment.csv"
SECTOR_DATA_PATH = "./data/sector_correlation.csv"
EVENT_DATA_PATH = "./data/event_data.csv"



def main() -> None:

    # load the data and create the data manager
    sentiment_data = load_sentiment_data(SENTIMENT_DATA_PATH)
    sector_data = load_sector_data(SECTOR_DATA_PATH)
    event_data = load_event_data(EVENT_DATA_PATH)


    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Dashboard"
    app.layout = create_layout(app, sentiment_data, sector_data, event_data)
    app.run()


if __name__ == "__main__":
    main()
