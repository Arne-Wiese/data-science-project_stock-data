import pandas as pd


sectors_dict = {
    "XLC": "Communication Services (XLC)",
    "XLY": "Consumer Discretionary (XLY)",
    "XLP": "Consumer Staples (XLP)",
    "XLE": "Energy (XLE)",
    "XLF": "Financials (XLF)",
    "XLV": "Health Care (XLV)",
    "XLI": "Industrials (XLI)",
    "XLB": "Materials (XLB)",
    "XLRE": "Real Estate (XLRE)",
    "XLK": "Technology (XLK)",
    "XLU": "Utilities (XLU)"
}


class DataSchemaSentiment:
    STOCK = "4. close_smoothed"
    SENTIMENT = "ticker_sentiment_smoothed"
    SENTIMENT_SHIFTED = "ticker_sentiment_smoothed_shifted"
    DATE = "Date"
    DAY = "day"


class DataSchemaSector:
    SECTOR = "sector"
    CORRELATION = "correlation"


class DataSchemaEvent:
    SYMBOL = "symbol"
    PRICE = "5. adjusted close"
    DATE = "date"


class DataSchemaSectorAnalyis:
    PRICE = "value"
    SYMBOL = "symbol"
    DATE = "date"


def load_sentiment_data(path: str) -> pd.DataFrame:
    # load the data from the CSV file
    data = pd.read_csv(
        path,
        dtype={
            DataSchemaSentiment.STOCK: float,
            DataSchemaSentiment.SENTIMENT: float,
            DataSchemaSentiment.SENTIMENT_SHIFTED: float,
            DataSchemaSentiment.DATE: str,
        },
        parse_dates=[DataSchemaSentiment.DATE],
    )
    data[DataSchemaSentiment.DAY] = data[DataSchemaSentiment.DATE].dt.day.astype(
        str)
    return data


def load_sector_data(path: str) -> pd.DataFrame:
    # load the data from the CSV file
    data = pd.read_csv(
        path,
        dtype={
            DataSchemaSector.SECTOR: str,
            DataSchemaSector.CORRELATION: float,
        },
    )
    return data


def load_event_data(path: str) -> pd.DataFrame:
    # load the data from the CSV file
    data = pd.read_csv(
        path,
        dtype={
            DataSchemaEvent.SYMBOL: str,
            DataSchemaEvent.PRICE: float,
            DataSchemaEvent.DATE: str,
        },
        parse_dates=[DataSchemaEvent.DATE]
    )
    #data[DataSchemaEvent.YEAR] = data[DataSchemaEvent.DATE].dt.year.astype(str)
    #data[DataSchemaEvent.MONTH] = data[DataSchemaEvent.DATE].dt.month.astype(str)
    return data

def load_sector_analysis_data(path: str) -> pd.DataFrame:
    # load the data from the CSV file
    data = pd.read_csv(
        path,
        dtype={
            DataSchemaSectorAnalyis.SYMBOL: str,
            DataSchemaSectorAnalyis.PRICE: float,
            DataSchemaSectorAnalyis.DATE: str,
        },
        parse_dates=[DataSchemaEvent.DATE]
    )
    #data[DataSchemaEvent.YEAR] = data[DataSchemaEvent.DATE].dt.year.astype(str)
    #data[DataSchemaEvent.MONTH] = data[DataSchemaEvent.DATE].dt.month.astype(str)
    return data