from .models import InstrumentPriceModifier


def prepare_db(session):
    # Insert instruments into DB
    InstrumentPriceModifier.insert(session, name='INSTRUMENT1', value=1.0)
    InstrumentPriceModifier.insert(session, name='INSTRUMENT2', value=1.0)
