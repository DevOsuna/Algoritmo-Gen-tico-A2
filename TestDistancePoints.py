from DemandPoint import DemandPoint
from LocationPoint import LocationPoint

def test():
      
    a = LocationPoint(1, 2.5, 200, 16.7526451, -93.1677644)
    b = DemandPoint(2, 100, 16.7463165, -93.1802099)
    c = DemandPoint(3, 50, 16.7476316, -93.1934278)
    d = LocationPoint(4, 2.5, 80, 16.7582555, -93.188127)

    listaLocations = []
    listaLocations.append(a)
    listaLocations.append(d)
    
    lista = []
    lista.append(a)
    lista.append(b)
    lista.append(c)
    lista.append(d)

    a.setPossibleCoverage(listaLocations)
    b.setPossibleCoverage(listaLocations)
    c.setPossibleCoverage(listaLocations)
    d.setPossibleCoverage(listaLocations)

    print(a)
    print(b)
    print(c)
    print(d)

if __name__ == '__main__':
    test()