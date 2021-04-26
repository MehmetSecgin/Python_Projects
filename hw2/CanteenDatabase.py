import datetime as dt
import pandas as pd
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Canteen(Base):
    __tablename__ = 'canteens'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String)
    Location = db.Column(db.String)
    time_open = db.Column(db.types.Time)
    time_closed = db.Column(db.types.Time)
    ProviderID = db.Column(db.Integer, db.ForeignKey('providers.ID'))

    def __init__(self, name, location, open_time, close_time, PID):
        self.Name = name
        self.Location = location
        self.time_open = open_time
        self.time_closed = close_time
        self.ProviderID = PID

    def __repr__(self):
        return "%s at %s, opens at %s till %s" % (
            self.Name, self.Location, self.time_open, self.time_closed)


class Provider(Base):
    __tablename__ = 'providers'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProviderName = db.Column(db.String)

    def __init__(self, id, p_name):
        self.ID = id
        self.ProviderName = p_name

    def __repr__(self):
        return "%s. Provider: %s" % (self.ID, self.ProviderName)


def create_list(file):
    df = pd.read_excel(file, na_filter=False)
    if 'time_open' in df.columns:
        df['time_open'] = pd.to_datetime(df['time_open'], format='%H%M').dt.time
        df['time_closed'] = pd.to_datetime(df['time_closed'], format='%H%M').dt.time
    a = df.to_dict(orient='records')
    return_list = []

    for row in a:
        if file[7:-5] == 'canteen':
            obj = Canteen(row['Name'], row['Location'], row['time_open'],
                          row['time_closed'], row['ProviderID'])
            return_list.append(obj)

        elif file[7:-5] == 'provider':
            obj = Provider(row['ID'], row['ProviderName'])
            return_list.append(obj)
    print(f"The data in {file[7:-5]} excel had been read and added to the database")
    print()
    return return_list


engine = db.create_engine('sqlite:///./diners.db', echo=False)
Base.metadata.create_all(engine)


def main():
    session = sessionmaker(bind=engine)()
    session.add_all(create_list('excels/canteen.xlsx'))
    session.add_all(create_list('excels/provider.xlsx'))
    session.commit()

    bit = Canteen("bitStop KOHVIK", "Raja 4C", dt.time(9, 30), dt.time(16), 4)
    session.add(bit)
    session.commit()

    print("bitStop KOHVIK had been added to the database")
    print()
    print("Query for canteens which are open 16.15-18.00")
    for row in session.query(Canteen).filter(Canteen.time_open <= dt.time(16, 15)).filter(
            Canteen.time_closed >= dt.time(18)).all():
        print("\t* " + row.Name + " is open from " + row.time_open.strftime(
            "%H:%M") + " until " + row.time_closed.strftime("%H:%M"))

    print()
    print("Query for canteens which are serviced by Rahva Toit")
    for row in session.query(Canteen).join(Provider).filter(Provider.ProviderName == "Rahva Toit").all():
        print("\t* " + row.Name)

    print()
    print("Deleting the data for further experiments on the code."
          "If we don't delete the data, It'll cause errors.")
    Canteen.__table__.drop(engine)
    Provider.__table__.drop(engine)

    # close database
    session.close()


main()
