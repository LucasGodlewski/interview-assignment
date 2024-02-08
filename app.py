from decimal import Decimal, getcontext

import pandas as pd

import config
from src.core.calculation import Engine
from src.database.db_session import Session
from src.database.models import InstrumentPriceModifier
from src.database.prepare import prepare_db


def run(session, calc):

    for df in pd.read_csv(
        'example_input.txt',
        names=config.HEADER_NAMES,
        chunksize=1000,
        iterator=True,
        date_format='%d-%b-%Y',
        parse_dates=['date'],
    ):

        # chained operation to take advantage of vectorization
        filtered_df = df[df['date'].dt.weekday.isin(config.BUSINESS_DAYS) & (df['date'] < config.END_DATE)]

        for row in filtered_df.itertuples():
            name, date, value = row.instrument, row.date, Decimal(str(row.value))
            # get multiplier from the DB
            if multiplier := InstrumentPriceModifier.get(session, name):
                value *= Decimal(str(multiplier))

            # update engine's register
            calc.add(name, date, value)

    calc.show_mean_for_all()


if __name__ == '__main__':
    getcontext().prec = config.PRECISION
    with Session() as session:
        prepare_db(session)
        run(session, Engine())
