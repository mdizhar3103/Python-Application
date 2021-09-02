import numpy as np
import folium
import pandas as pd

class ShowMap:
    
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
        
    def get_lat_long(self, location):
        return (location.lat, location.long)
    
    def hanging_line(self, point1, point2):
        a = (point2[1] - point1[1])/(np.cosh(point2[0]) - np.cosh(point1[0]))
        b = point1[1] - a*np.cosh(point1[0])
        x = np.linspace(point1[0], point2[0], 100)
        y = a*np.cosh(x) + b

        return (x,y)

    def generate_map(self, orig=None, dest=None):
        #cartodb dark_matter
        origin_xy = self.get_lat_long(self.origin) if orig is None else orig
        destination_xy = self.get_lat_long(self.destination) if dest is None else dest

        center = ( (origin_xy[0] + destination_xy[0])/2, (origin_xy[1] + destination_xy[1])/2)
        flight_map = folium.Map(location=center, tiles="cartodb positron")
        flight_map.fit_bounds([origin_xy, destination_xy])

        origin_kw = {"prefix": "fa", "color": "green", "icon": "plane", "icon_color":'white'}
        folium.Marker(origin_xy, icon=folium.DivIcon(icon_size=(180, 20),
            html='''<div style="
                  font-size: 12pt;
                  font-family: serif;
                  color: black; 
                  text-align: center;
                  background: rgba(255, 255, 255, 0.7);
                  ">
                  {0.origin}
                  </div>'''.format(self),)).add_to(flight_map)
        folium.Marker(origin_xy,  popup = "Flight Origin", icon=folium.Icon(**origin_kw)).add_to(flight_map)

        
        destination_kw = {"prefix": "fa", "color": "red", "icon": "plane", "icon_color":'white', "angle": 90}
        folium.Marker(destination_xy, icon=folium.DivIcon(icon_size=(180, 20),
            html='''<div style="
                  font-size: 12pt;
                  font-family: serif;
                  color: black; 
                  text-align: center;
                  background: rgba(255, 255, 255, 0.7);">
                  {0.destination}
                  </div>'''.format(self),)).add_to(flight_map)
        folium.Marker(destination_xy,  popup = "Flight Origin", icon=folium.Icon(**destination_kw)).add_to(flight_map)
        


        curve = self.hanging_line(origin_xy, destination_xy)
        folium.PolyLine(locations=list(zip(curve[0],curve[1])), color='darkred', no_clip=True).add_to(flight_map)
        return flight_map