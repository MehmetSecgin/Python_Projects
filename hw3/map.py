import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


def draw_map(file_name, map_color, map_name, out):
    print(f"Read the file '{file_name}'")
    direct_flights = pd.read_csv(file_name, sep=";")
    print("Read the file 'airports.dat'")
    airports = pd.read_csv('airports.dat', skiprows=1,
                           names=['ID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 'Latitude', 'Longitude', 'Altitude',
                                  'Timezone', 'DST', 'DZ', 'Type', 'Source'])
    print("Merged the two files")
    table = direct_flights.merge(airports, on='IATA')

    print("The canvas is drawn and the focus is on Europe")
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([-13, 50, 33, 69], crs=ccrs.PlateCarree())
    print("The lines and colors has been distinguished.")
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle='-')
    print("TLL Airports Location has been read from the data")
    TLL_data = table.loc[table["IATA"] == "TLL"]
    for row in table.itertuples():
        print(f"\t* Drawn the route from TLL to {row.IATA} Airport in {row.Country}")
        plt.plot([row.Longitude, TLL_data['Longitude']], [row.Latitude, TLL_data['Latitude']], color=map_color,
                 linewidth=0.8,
                 marker='.', transform=ccrs.Geodetic())
        plt.text(row.Longitude, row.Latitude, row.IATA, horizontalalignment='right',
                 transform=ccrs.Geodetic())
    print("The title is now present on the map")
    plt.title(map_name, fontsize=10)
    print("The plot is shown and saved into the directory.")
    print()
    plt.savefig(f'./maps/{out}.png')
    plt.show()


if __name__ == '__main__':
    draw_map('otselennud.csv', 'blue',
             'Map of Direct Flights to Tallinn Airport (before COVID-19) by Mehmet Ali Seçgin', 'before_covid')
    draw_map('flights21.csv', 'red', 'Map of Direct Flights to Tallinn Airport (Apr 2021) by Mehmet Ali Seçgin',
             'april_21')
