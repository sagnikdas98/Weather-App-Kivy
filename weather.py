from kivy.app import App
from kivy.uix.listview import ListItemButton
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty
#from kivy.factory import Factory
import requests



class WeatherRoot(BoxLayout):
    current_weather = ObjectProperty()


    def show_current_weather(self,location=None):
        self.clear_widgets()

        if self.current_weather is None:
            self.current_weather=CurrentWeather()

        if location is not None:
            self.current_weather.location = location
        self.current_weather.update_weather()
        self.add_widget(self.current_weather)


    def addlocations(self):
        self.clear_widgets()
        self.add_widget(AddLocationForm())



class AddLocationForm(BoxLayout):
    search_input = ObjectProperty()
    search_result = ObjectProperty()


    def search_location(self):
        global urlresults
        print("1")
        search_temp = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=db50fbbc5e273b6745f0c516e36c6284"
        search_url = search_temp.format(self.search_input.text)
        urlresults = (requests.get(search_url)).json()
        if int(urlresults['cod']) == 404:
            self.search_result.item_strings = ['Non exsistent']
        else:
            self.found_location(urlresults)

    def found_location(self, data):
        print("2")
        city = [(data['name'], data['sys']['country'])]
        self.search_result.item_strings = city
        print(self.search_result.item_strings)

        #self.search_result.adapter.data.clear()
        #self.search_result.adapter.data.extend(city)
        #self.search_result._trigger_reset_populate()

    def args_converter(self,index, data_item):
        print("3")
        city, country =data_item
        print({'location':(city,country)} )
        return {'location':(city,country)}

class LocationButton(ListItemButton):

    location = ListProperty()

    pass


class CurrentWeather(BoxLayout):

    location=ListProperty(['New York', 'US'])
    condition = StringProperty()
    temp=NumericProperty()
    temp_min=NumericProperty()
    temp_max=NumericProperty()


    def update_weather(self):




        global urlresults
        self.condition=urlresults['weather'][0]['description']
        self.temp=urlresults['main']['temp']-273
        self.temp_max=urlresults['main']['temp_max']-273
        self.temp_min=urlresults['main']['temp_min']-273

    pass








class WeatherApp(App):

    pass


WeatherApp().run()
