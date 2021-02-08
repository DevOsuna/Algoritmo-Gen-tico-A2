from geopy.distance import geodesic
from typing import List

class DemandPoint:

    def __init__(self, ID, demand, latitude, longitude):
        self.ID = ID
        self.demand = demand
        self.latitude = latitude
        self.longitude = longitude
        self.possibleCoverage = []
        

    def setPossibleCoverage(self, locations):

        self.possibleCoverage.clear()

        coordinatesA = ((self.latitude, self.longitude))

        for location in locations:
            coordinatesB = ((location.latitude, location.longitude))

            if geodesic(coordinatesA, coordinatesB).km <= location.cover_range:
                self.possibleCoverage.append(location)


    def isCover(self, locations):
        
        for location in locations:
            
            if self.isInRange(location):
                self.isCovered = True
                return True

        self.isCovered = False
        return False
    
    
    def isInRange(self, location):

        coordinatesA = ((self.latitude, self.longitude))
        coordinatesB = ((location.latitude, location.longitude))

        if geodesic(coordinatesA, coordinatesB).km <= location.cover_range:
            return True

        return False

    def __str__(self):
        data = "Punto de demanda: " + str(self.ID) + "\t\t\t\t\tDemanda " + str(self.demand) + "\t cubierto por ["
        for i in self.possibleCoverage:
            data = data + str(i.ID) + ","
        return data + "]"