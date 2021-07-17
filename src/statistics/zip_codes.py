from urllib.request import urlopen
import json
import re
import pandas as pd
import plotly.express as px
from src.odoo.odoo_connector import OdooConnector
from src.odoo.odoo_arguments import parse_odoo_arguments


def ExtractPopulationDensity(members):
    population_density = dict()
    known_trouble_makers = ["82544", "91171"]
    for member in members:
        zip_code = member["zip"]
        match = re.match(r"(?<!\d)(\w+[\-\ ])?(\d{4,5})", str(zip_code))
        if match and match.group() not in known_trouble_makers:
            population_density[match.group()] = population_density.get(zip_code, 0) + 1
    return pd.DataFrame(
        list(population_density.items()),
        columns=["zip_code", "population_density"],
    )


def FetchGeoJson():
    print("fetching geojson of german zip codes")
    with urlopen(
        "https://raw.githubusercontent.com/yetzt/postleitzahlen/master/data/postleitzahlen.geojson"
    ) as response:
        return json.load(response)


def CreatePopulatinDensityPlot(population_density, zip_codes):
    fig = px.choropleth(
        population_density,
        geojson=zip_codes,
        locations="zip_code",
        featureidkey="properties.postcode",
        color="population_density",
        color_continuous_scale="Oranges",
        # range_color=(0, 100),
        scope="europe",
        labels={"population_density": "Wohndichte Foodhub"},
    )
    fig.update_geos(fitbounds="locations")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()


def CreateDemographicPlot():
    args = parse_odoo_arguments()
    members = OdooConnector(
        args.url, args.db, args.username, args.password
    ).get_all_members()
    CreatePopulatinDensityPlot(ExtractPopulationDensity(members), FetchGeoJson())


if __name__ == "__main__":
    CreateDemographicPlot()
