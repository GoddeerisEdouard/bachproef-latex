import json
from typing import NamedTuple, List, Optional

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


def start_webdriver() -> webdriver:
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(log_level=0).install()), options=options)
    return driver


class CarModelData(NamedTuple):
    car_model: str
    car_buildyear: Optional[str]


class CarBrandModels(NamedTuple):
    brand: str
    models: List[CarModelData]


def get_car_models_by_car_url(webdriver, car_url) -> List[CarModelData]:
    webdriver.get(car_url)
    car_models_for_current_brand_elements = webdriver.find_elements(By.XPATH,
                                                                    "//div[@style='font-size: 1.25em; margin: 10px !important;']")
    car_model_data_list = []

    for car_model_with_buildyear_element in car_models_for_current_brand_elements:

            car_model_with_buildyear_split_by_spaces = car_model_with_buildyear_element.text.split(" ")
            # if there's a known build year in the list
            if len(car_model_with_buildyear_split_by_spaces) == 2:
                car_model_name = car_model_with_buildyear_split_by_spaces[:-1]
                car_model_buildyear = car_model_with_buildyear_split_by_spaces[-1]
            else:
                car_model_name = car_model_with_buildyear_split_by_spaces[0]
                car_model_buildyear = None
            car_model_data_list.append(CarModelData(car_model_name, car_model_buildyear))

    return car_model_data_list


def get_all_carbrand_names(webdriver):
    CAR_BRANDSLIST_URL = "https://www.car.info/en-se/brands"
    webdriver.get(CAR_BRANDSLIST_URL)
    div_element_table_with_all_carnames = webdriver.find_element(By.CSS_SELECTOR,
                                                                 "#content > main > div > div > div.mb-5")
    unordered_list_per_alfabet_letter = div_element_table_with_all_carnames.find_elements(By.CSS_SELECTOR, "ul")
    list_carbrand_car_url_tuple = []  # example [("Volvo", "www...",), ("Ferrari", "www...",)]
    # loop through every unordered list element, this is a table containing the elements of each seperate car brand(A -Z)
    print("Storing car links for each car brand...")
    for ul_alfabet_letter in unordered_list_per_alfabet_letter:
        alfabet_letter = ul_alfabet_letter.find_element(By.CSS_SELECTOR, "h2").text
        print(f"Storing all car brands starting with {alfabet_letter}")
        carbrand_elements_for_current_letter = ul_alfabet_letter.find_elements(By.CLASS_NAME, "link_grey")
        for carbrand_element in carbrand_elements_for_current_letter:
            car_brand = carbrand_element.text
            car_brand_link = carbrand_element.get_attribute("href")
            list_carbrand_car_url_tuple.append((car_brand, car_brand_link,))

    return list_carbrand_car_url_tuple


def get_formatted_car_data(webdriver) -> List[CarBrandModels]:
    car_brands_and_url_tuple_list = get_all_carbrand_names(webdriver)

    car_data = []
    for carbrand_car_url in car_brands_and_url_tuple_list:
        car_brand_name = carbrand_car_url[0]
        print(f"Getting car models for {car_brand_name}...")
        car_model_data_list = get_car_models_by_car_url(webdriver, carbrand_car_url[1])
        car_data.append(CarBrandModels(car_brand_name, car_model_data_list))

    return car_data


if __name__ == '__main__':
    webdriver = start_webdriver()

    car_data = get_formatted_car_data(webdriver)

    # write car data to json file
    json_format_car_brand_models = {}
    for car_brand_models in car_data:
        json_format_car_brand_models[car_brand_models.brand] = [car_brand_model._asdict() for car_brand_model in
                                                                car_brand_models.models]

    # Storing in a json file for easy access
    with open("car_data.json", "w") as f:
        json.dump(json_format_car_brand_models, f, indent=2)
