from src.odoo.odoo_connector import OdooConnector
from src.odoo.odoo_arguments import parse_odoo_arguments
import plotly.graph_objects as gp
import numpy as np

MAX_AGE = 95
AGE_INTERVAL = 5


def ExtractNoInformation(members):
    no_age = 0
    no_gender = 0
    for member in members:
        if member["gender"] == False:
            no_gender += 1
        if member["age"] == False:
            no_age += 1
    return no_gender, no_age


def ExtractAgesOf(gender, members):
    ages = np.zeros(int(MAX_AGE / AGE_INTERVAL), dtype=int)
    for member in members:
        if member["gender"] == gender:
            if member["age"] != False:
                ages[int(member["age"] / AGE_INTERVAL)] += 1
    return ages


def ExtractAges(members):
    return ExtractAgesOf("female", members), ExtractAgesOf("male", members)


def CreatePlot(female_ages, male_ages, no_gender, no_age):
    y_ages = np.arange(0, MAX_AGE / AGE_INTERVAL)[3:]
    fig = gp.Figure()
    fig.add_trace(
        gp.Bar(
            y=y_ages,
            x=male_ages[3:],
            name="Männer",
            orientation="h",
        )
    )
    fig.add_trace(
        gp.Bar(
            y=y_ages,
            x=female_ages[3:] * -1,
            name="Frauen",
            orientation="h",
        )
    )
    fig.update_layout(
        title="Altersverteilung des FoodHub München",
        title_font_size=22,
        barmode="relative",
        bargap=0.0,
        bargroupgap=0,
        yaxis=dict(
            tickvals=y_ages,
            ticktext=[
                "15 - 19",
                "20 - 24",
                "25 - 29",
                "30 - 34",
                "35 - 39",
                "40 - 44",
                "45 - 49",
                "50 - 54",
                "55 - 59",
                "60 - 64",
                "65 - 69",
                "70 - 74",
                "75 - 79",
                "80 - 84",
                "85 - 89",
                "90 - 95",
            ],
        ),
        xaxis=dict(
            tickvals=[
                -100,
                -90,
                -80,
                -70,
                -60,
                -50,
                -40,
                -30,
                -20,
                -10,
                0,
                10,
                20,
                30,
                40,
            ],
            ticktext=[
                "100",
                "90",
                "80",
                "70",
                "60",
                "50",
                "40",
                "30",
                "20",
                "10",
                "0",
                "10",
                "20",
                "30",
                "40",
            ],
            title="Keine Angabe zum Geschlecht: {}, Keine Angabe zum Alter: {}".format(
                no_gender, no_age
            ),
            title_font_size=14,
        ),
    )

    fig.show()


def CreateDemographicPlot():
    args = parse_odoo_arguments()
    members = OdooConnector(
        args.url, args.db, args.username, args.password
    ).get_all_members()
    female_ages, male_ages = ExtractAges(members)
    no_gender, no_age = ExtractNoInformation(members)
    CreatePlot(female_ages, male_ages, no_gender, no_age)


if __name__ == "__main__":
    CreateDemographicPlot()
