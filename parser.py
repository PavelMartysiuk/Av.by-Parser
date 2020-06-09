from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
import tables
from collections import defaultdict


class AvParser:
    def __init__(self):
        self.url = 'https://av.by/'
        self.response = None
        self.paginator_links = None

    def check_connect(self, url):
        try:
            response = requests.get(url)
        except HTTPError as httperr:
            print(f'Error : {httperr}')
        except Exception as exc:
            print(f'Error : {exc}')
        else:
            response.encoding = 'utf-8'
            self.response = response.text

    def conversion_to_soup(self):
        self.soup = BeautifulSoup(self.response, 'html.parser')

    def parse_car_marks_model(self, url):
        """Universal parser for car models and car mark"""
        MARK_MODEL_INDEX = 0
        self.check_connect(url)
        if self.response:
            self.conversion_to_soup()
            marks_models_block = self.soup.find('ul', class_='brandslist')
            marks_models_list = marks_models_block.find_all('li')  # soup objects
            self.marks_models = {mark.text.strip().split()[MARK_MODEL_INDEX]: mark.find('a').get('href') for mark in
                                 marks_models_list}  # {mark or model:link,}, format mark.text is mark quantity (also model)

    def parse_car_marks(self):
        self.parse_car_marks_model(self.url)
        marks = self.marks_models
        marks_to_bd = ([tables.CarMark(mark=mark, link=link) for mark, link in marks.items()])
        sess = tables.Session()
        sess.add_all(marks_to_bd)
        sess.commit()

    def parse_car_models(self):
        sess = tables.Session()
        car_objects = sess.query(tables.CarMark).all()
        for car_obj in car_objects:
            self.parse_car_marks_model(car_obj.link)
            models = self.marks_models
            models_to_bd = (
                [tables.CarModel(model=model, link=link, mark_id=car_obj.id) for model, link in models.items()])
            sess = tables.Session()
            sess.add_all(models_to_bd)
            sess.commit()

    def get_quantity_pages(self, url):

        """Func finds all links in paginator on page."""
        self.check_connect(url)
        if self.response:
            self.conversion_to_soup()
        try:
            paginator_block = self.soup.find('div', class_='')
            links_block = paginator_block.find_all('a')
            self.paginator_links = [link.get('href') for link in links_block]
        except AttributeError:
            print("Page doesn't have a paginator")

    def get_car_advertisement_info(self):
        """Func parses cars info from one page of paginator"""
        self.car_info = defaultdict(list)
        cars_blocks = self.soup.find_all('div', class_='listing-item')
        for car_block in cars_blocks:
            link = car_block.find('a').get('href')
            year_content_block = car_block.find('div', class_='listing-item-desc')
            year = year_content_block.find('span').text
            content = year_content_block.text.strip()  # many sentents with /n. For exaple 2013, \n    автомат,\n 2.0 л.,\n     бензин, седан, 110 миль
            content = ' '.join(content.split())
            cost_location_block = car_block.find('div', class_='listing-item-price')
            cost = cost_location_block.find('small').text
            location = cost_location_block.find('p', class_='listing-item-location').text
            self.car_info[link].extend((year, content, cost, location))

    def parse_advertisements(self):
        sess = tables.Session()
        car_objs = sess.query(tables.CarModel).all()
        YEAR_INDEX = 0
        CONTENT_INDEX = 1
        COST_INDEX = 2
        LOCATION_INDEX = 3
        for car_obj in car_objs:
            advertisements_link = car_obj.link
            self.get_quantity_pages(advertisements_link)
            if self.paginator_links:
                for link in self.paginator_links:
                    self.check_connect(link)
                    if self.response:
                        self.conversion_to_soup()
                        self.get_car_advertisement_info()
                        car_to_bd = ([
                            tables.Car(mark_id=car_obj.mark_id, model_id=car_obj.id, link=link, year=info[YEAR_INDEX],
                                       content=info[COST_INDEX],
                                       cost=info[COST_INDEX], location=info[LOCATION_INDEX]) for link, info in
                            self.car_info.items()])
                        sess = tables.Session()
                        sess.add_all(car_to_bd)
                        sess.commit()
            else:
                self.get_car_advertisement_info()
                car_to_bd = ([
                    tables.Car(mark_id=car_obj.mark_id, model_id=car_obj.id, link=link, year=info[YEAR_INDEX],
                               content=info[CONTENT_INDEX],
                               cost=info[COST_INDEX], location=info[LOCATION_INDEX]) for link, info in
                    self.car_info.items()])
                sess = tables.Session()
                sess.add_all(car_to_bd)
                sess.commit()


if __name__ == '__main__':
    av_parser = AvParser()
    av_parser.parse_car_marks()
    av_parser.parse_car_models()
    av_parser.parse_advertisements()
