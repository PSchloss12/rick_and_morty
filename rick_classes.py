import requests
import json
from db_manager import Base
from sqlalchemy import Column, Integer, String, Text

# data through season 5
URL = 'https://rickandmortyapi.com/api/'
LOCATION_URL = 'https://rickandmortyapi.com/api/location/'
CHARACTER_URL = 'https://rickandmortyapi.com/api/character/'
EPISODE_URL = 'https://rickandmortyapi.com/api/episode/'


class Character(Base):
    # create table
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(String)
    species = Column(String)
    type = Column(String)
    origin = Column(String)
    location = Column(String)
    image = Column(String)
    episodes = Column(String)
    url = Column(String)
    
    def __init__(self, url, id=None, name=None, status=None, species=None, type=None, gender=None, origin=None, location=None, image=None, episodes=None) -> None:
        # establish data fields
        self.id: str = id
        self.name: str = name
        self.status: str = status
        self.species: str = species
        self.type: str = type
        self.gender: str = gender
        self.origin: Location = origin
        self.location: Location = location
        self.image: str = image
        self.episodes: list = episodes
        self.url: str = url
    
    def scrape(self, eps = False, locs=False):
        # check url
        if not self.url:
            return
        # check if we already have the data
        if all([self.id, self.name, self.status, self.species, self.location, self.episodes, self.image]) and not eps and not locs:
            return
        # fetch data
        js = json.loads(requests.get(self.url).content.decode('utf8'))
        # set fields
        self.id = js['id']
        self.name: str = js['name']
        self.status: str = js['status']
        self.species: str = js['species']
        self.type: str = js['type']
        self.gender: str = js['gender']
        if locs: # load actual objects
            self.origin: Location = Location(js['origin'].get('url'))
            self.origin.scrape()
            self.location: Location = Location(js['location'].get('url'))
            self.location.scrape()
        else: # just get urls
            self.origin = js['origin'].get('url')
            self.location = js['location'].get('url')
        self.image: str = js['image']
        if eps:
            self.episodes = [Episode(i) for i in js['episode']]
            for e in self.episodes:
                e.scrape()
        else:
            self.episodes: list = js['episode']
    
class Location(Base):
    # establish db cols
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    dimension = Column(String)
    url = Column(String)
    
    def __init__(self, url, id=None, name=None, type=None, dimension=None, characters=None) -> None:
        self.id: str = id
        self.name: str = name
        self.type: str = type
        self.dimension: str = dimension
        self.characters: list = characters
        self.url: str = url
    
    def scrape(self, chars=False):
        # if url was passed and rest are None, fetch own data
        if not all([self.id, self.name, self.type, self.dimension, self.characters]):
            if self.url:
                js = json.loads(requests.get(self.url).content.decode('utf8'))
                self.id: str = js['id']
                self.name: str = js['name']
                self.type: str = js['type']
                self.dimension: str = js['dimension']
                self.characters: list = js['residents']
    # to display location
    def __repr__(self) -> str:
        return f"{self.id}: {self.name} ({self.type}, {self.dimension})"
    def __str__(self) -> str:
        return f"{self.name} ({self.type}, {self.dimension})"
    
class Episode():
    __tablename__ = 'episodes'
    id = Column(Integer, primary_key=True)
    
    def __init__(self, url, id=None, name=None, air_date=None, episode=None, characters=None) -> None:
        self.id: str = id
        self.name: str = name
        self.air_date: str = air_date
        self.episode: str = episode
        self.characters: str = characters
        self.url: str = url
        
    def scrape(self):
        # if url was passed and other attributes are None, fetch own data
        if not all([self.id, self.name, self.air_date, self.episode, self.characters]):
            if self.url:
                js = json.loads(requests.get(self.url).content.decode('utf8'))
                self.id: str = js['id']
                self.name: str = js['name']
                self.air_date: str = js['air_date']
                self.episode: str = js['episode']
                self.characters: str = js['characters']
    # for display purposes
    def __repr__(self) -> str:
        return f"{self.id}: {self.name} ({self.episode}, {self.air_date})"
    def __str__(self) -> str:
        return f"{self.name} ({self.episode})"
    
if __name__ == '__main__':
    c = Character(CHARACTER_URL+'2')
    c.scrape()
    
    l = Location(LOCATION_URL+'1')
    l.scrape()
    # print(l.dimension, l.characters)
    
    e = Episode(EPISODE_URL+'1')
    e.scrape()