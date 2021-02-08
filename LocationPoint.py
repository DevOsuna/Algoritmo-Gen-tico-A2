from DemandPoint import DemandPoint
from typing import List

class LocationPoint(DemandPoint):

    def __init__(self, ID, cover_range, demand, latitude, longitude):
        
        DemandPoint.__init__(self, ID, demand, latitude, longitude)
        self.cover_range = cover_range


    def demandPointsCoverage(self, demandPoints: List):
        
        for demand in demandPoints:
            if demand.isInRange(self):
                self.demandPointsCoverage.append(demand)

    
    def __str__(self):

        data = "Location: " + str(self.ID) + "\tRCover: " + str(self.cover_range) + "\tDemand " + str(self.demand) + "\t CoverBy ["
        for i in self.possibleCoverage:
            data = data + str(i.ID) + ","
        return data + "]"