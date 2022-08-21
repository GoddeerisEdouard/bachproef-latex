import datetime
import json
from typing import NamedTuple, Optional


class AutoVerzekeringData(NamedTuple):
    ouder_dan_2_jaar: bool
    brandstoftype: Optional[str]
    eerste_inschrijving: Optional[int]
    auto_merk: Optional[str]
    auto_model: Optional[str]
    cataloguswaarde: Optional[int] = -1
    chassisnummer: Optional[int] = None


def request_car_insurance():
    voertuig_ouderdom = ""
    while voertuig_ouderdom not in ["y", "n"]:
        voertuig_ouderdom = input("Is uw voertuig ouder dan 2 jaar? (y/n) ")

    chassisnummer = input("Vul uw chassisnummer in, als u dit niet heeft, druk Enter ")
    if not chassisnummer:
        chassisnummer = -1
        print("Vul info over uw auto in:")
        brandstoftype = input("Brandstoftype: ")
        eerste_inschrijving = -1
        while 1800 > eerste_inschrijving or eerste_inschrijving > datetime.datetime.now().year:
            eerste_inschrijving = input("Eerste inschrijving: ")
            try:
                eerste_inschrijving = int(eerste_inschrijving)
            except ValueError:
                eerste_inschrijving = -1
                pass
        merk = ""
        with open("car_data.json") as f:
            car_data = json.load(f)
        auto_model_keuzes = None
        while auto_model_keuzes is None:
            merk = input("Merk: ")
            auto_model_keuzes = car_data.get(merk)
        print("Kies uw automodel:")
        for teller, auto_model_keuze in enumerate(auto_model_keuzes):
            print(f"{teller + 1}. {auto_model_keuze['car_model']}")

        gekozen_auto_model = -1
        while not 0 <= gekozen_auto_model - 1 < len(auto_model_keuzes) - 1:
            gekozen_auto_model = input("keuze: ")
            try:
                gekozen_auto_model = int(gekozen_auto_model)
            except ValueError:
                gekozen_auto_model = -1
                pass
        gekozen_auto_model_gevalideerd = auto_model_keuzes[gekozen_auto_model]

        cataloguswaarde = -1
        while cataloguswaarde < 0:
            cataloguswaarde = input("Cataloguswaarde: ")
            try:
                cataloguswaarde = int(cataloguswaarde)
            except ValueError:
                cataloguswaarde = -1
                pass

        autoverzekering_data = AutoVerzekeringData(ouder_dan_2_jaar=voertuig_ouderdom == "y",
                                                   brandstoftype=brandstoftype, eerste_inschrijving=eerste_inschrijving,
                                                   auto_merk=merk, auto_model=gekozen_auto_model_gevalideerd,
                                                   cataloguswaarde=cataloguswaarde,
                                                   chassisnummer=chassisnummer)

    else:
        autoverzekering_data = AutoVerzekeringData(ouder_dan_2_jaar=voertuig_ouderdom == "y",
                                                   chassisnummer=chassisnummer)

    return autoverzekering_data


if __name__ == '__main__':
    car_insurance_data = request_car_insurance()
    print(
        f"Door middel van opgevraagde data EN validatie kan volgende informatie verwerkt worden:\n{car_insurance_data}")
