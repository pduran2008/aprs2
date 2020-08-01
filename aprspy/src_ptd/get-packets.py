import pandas as pd
import simplekml

class GetPackets:

    def __init__(self, callsign: list, outputtype: str, timerange=None, latlonrad=None):
        """Class initialization
        :param src: source data filename
        """
        self.callsign = callsign
        self.timerange = timerange
        self.latlonrad = latlonrad
        self.outputtype = outputtype
        self._readfile()
        self._selectpackets()
        self._returnpackets()
        if self.outputtype == "kml":
            self._createkml()

    def _readfile(self):
        self.packetdf = pd.read_csv("/Users/ptduran/Desktop/APRS/decoded/KJ4OVR_2012-2015.LOG", parse_dates=True)

    def _selectpackets(self):

        self.subsetdf = self.packetdf[self.packetdf.source.isin(self.callsign)]  # Data filtered by callsign
        if self.timerange:  # Filter data by time
            self.subsetdf = self.subsetdf[(self.subsetdf['timestamp'] >= self.timerange[0]) &
                                          (self.subsetdf['timestamp'] <= self.timerange[1])]

        if self.latlonrad:  # Filter data by location
            def _latlon_distance(lat1, lon1, lat2, lon2):
                '''
                Uses Haversine Equation adapted from:
                https://www.movable-type.co.uk/scripts/latlong.html
                '''

                import math

                lat1 = math.radians(lat1)
                lon1 = math.radians(lon1)
                lat2 = math.radians(lat2)
                lon2 = math.radians(lon2)

                delta_lat = lat2 - lat1
                delta_lon = lon2 - lon1

                a = (math.sin(delta_lat / 2)) ** 2 + math.cos(lat1) * math.cos(lat2) * (math.sin(delta_lon / 2)) ** 2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                self.d = 6371 * c * 1000  # m
                return (self.d)

            distlist = []
            for row in self.subsetdf.itertuples():
                if row.longitude != 'None' and row.longitude != 'None':
                    dist = _latlon_distance(self.latlonrad[0], self.latlonrad[1],
                                            float(row.latitude), float(row.longitude))
                    distlist.append(dist)
                else:
                    distlist.append(-9999)
            self.subsetdf['distance'] = distlist
            self.subsetdf = self.subsetdf[(self.latlonrad[2] >= self.subsetdf['distance'])]
            self.subsetdf = self.subsetdf[self.subsetdf['distance'] >= 0]

    def _returnpackets(self):
        self.subsetdf
        return (self.subsetdf)

    def _createkml(self):
        kml = simplekml.Kml(name="test")
#        linecoords = [tuple()]
#        for row in self.subsetdf.itertuples():
#            if row.latitude:
#                lat = float(row.latitude)
#                lon = float(row.longitude)
#                coords = (lat, lon)
#                linecoords.append(coords)
#        trackline = kml.newlinestring(name="Track", coords=linecoords)
#        kml.save("testline.kml")
        for row in self.subsetdf.itertuples():
            print(row)
            pnt = kml.newpoint(name=row.timestamp, coords=[(row.longitude,row.latitude)])
            pnt.style.labelstyle.scale = 0.75
            pnt.style.balloonstyle.text = "Time: "+row.timestamp+" Local Time"+"\n"+\
                                          "Source: "+row.source+"\n"+\
                                          "Latitude: "+row.latitude+"\n"+\
                                          "Longitude: "+row.longitude+"\n"\
                                          "Altitude: "+row.altitude+"\n"\
                                          "Course: "+row.course+"\n"\
                                          "Bearing: "+row.bearing+"\n"\
                                          "Speed "+row.speed+"\n"\
                                          "Comment: "+row.comment
#            pnt.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/phone.png"
#            pnt.style.iconstyle.color = "FF64F05A14"  # Blue...not working for some reason
        kml.save("/Users/ptduran/PycharmProjects/aprspy/aprspy/output/test.kml")
        print(kml.kml())

#selectedpackets = GetPackets(["KJ4OVR-2", "KJ4OVR-5", "KJ4OVR-9", "KJ4OVR-12"], "kml",
#                             ["2014-10-11 00:00:00", "2014-10-11 23:59:59"])

#selectedpackets = GetPackets(["KJ4OVR-2", "KJ4OVR-5", "KJ4OVR-9", "KJ4OVR-12"], "kml",
#                             ["2009-10-11 00:00:00", "2016-10-11 23:59:59"])

# Fruit Cove:
# selectedpackets = GetPackets(callsign=["KJ4OVR-2", "KJ4OVR-5", "KJ4OVR-9", "KJ4OVR-12"], latlonrad=[30.095, -81.621, 20000])

# Lynn & Marta's:
selectedpackets = GetPackets(callsign=["KJ4OVR-2", "KJ4OVR-5", "KJ4OVR-9", "KJ4OVR-12"], outputtype="kml", latlonrad=[27.996684, -80.658998, 500])
print(selectedpackets.subsetdf)

# Sebastian Inlet:
#selectedpackets = GetPackets(callsign=["KJ4OVR-2", "KJ4OVR-5", "KJ4OVR-9", "KJ4OVR-12"], latlonrad=[27.860131, -80.448530, 5000])
#print(selectedpackets.subsetdf)

# Five Rivers:
#selectedpackets = GetPackets(callsign=["KJ4OVR-2", "KJ4OVR-5", "KJ4OVR-9", "KJ4OVR-12"],outputtype="kml", latlonrad=[42.61, -73.89, 1000])

# Wynantskill Christmas House:
#selectedpackets = GetPackets(callsign=["KJ4OVR-2", "KJ4OVR-5", "KJ4OVR-9", "KJ4OVR-12"], latlonrad=[42.691655, -73.643082, 50])
#print(selectedpackets.subsetdf)

# The Red Lion Inn:
#selectedpackets = GetPackets(callsign=["KJ4OVR-2", "KJ4OVR-5", "KJ4OVR-9", "KJ4OVR-12"], latlonrad=[42.281667, -73.311949, 50])
#print(selectedpackets.subsetdf)

# Divine Mercy Shrine:
#selectedpackets = GetPackets(callsign=["KJ4OVR-2", "KJ4OVR-5", "KJ4OVR-9", "KJ4OVR-12"], latlonrad=[42.288929, -73.311311, 200])
#print(selectedpackets.subsetdf)

# National Shrine of Our Lady of Czestochowa:
#selectedpackets = GetPackets(callsign=["KJ4OVR-2", "KJ4OVR-5", "KJ4OVR-9", "KJ4OVR-12"], latlonrad=[40.319262, -75.179332, 1000])
#print(selectedpackets.subsetdf)

# Worthington Terrace, Wynantskill:
#selectedpackets = GetPackets(callsign=["KJ4OVR-2", "KJ4OVR-5", "KJ4OVR-9", "KJ4OVR-12"], latlonrad=[42.685368, -73.628076, 100])
#print(selectedpackets.subsetdf)

# St. Augustine's Church, Troy, NY:
#selectedpackets = GetPackets(callsign=["KJ4OVR-2", "KJ4OVR-5", "KJ4OVR-9", "KJ4OVR-12"], latlonrad=[42.774220, -73.67439, 100])
#print(selectedpackets.subsetdf)

# Prospect Park Tennis Courts, Troy, NY:
#selectedpackets = GetPackets(callsign=["KJ4OVR-2", "KJ4OVR-5", "KJ4OVR-9", "KJ4OVR-12"], latlonrad=[42.723052, -73.683738, 100])
#print(selectedpackets.subsetdf)

# Bethlehem Town Park Tennis Courts, Delmar, NY:
#selectedpackets = GetPackets(callsign=["KJ4OVR-2", "KJ4OVR-5", "KJ4OVR-9", "KJ4OVR-12"], latlonrad=[42.601574, -73.842439, 100])
#print(selectedpackets.subsetdf)

# 55 Queen Anne Drive, Slingerlands, NY:
#selectedpackets = GetPackets(callsign=["KJ4OVR-2", "KJ4OVR-5", "KJ4OVR-9", "KJ4OVR-12"], latlonrad=[42.631305, -73.843447, 100])
#print(selectedpackets.subsetdf)

# 40 Windmill Drive, Glenmont, NY:
#selectedpackets = GetPackets(callsign=["KJ4OVR-2", "KJ4OVR-5", "KJ4OVR-9", "KJ4OVR-12"], latlonrad=[42.576888, -73.810270, 100])
#print(selectedpackets.subsetdf)

# test = GetPackets(["KJ4OVR-2", "KJ4OVR-5", "KJ4OVR-9", "KJ4OVR-12"])

# ALSO DEVELOP A METHOD THAT WILL TAKE A CALLSIGN, LAT, LON, AND RADIUS AND RETURN ALL OF THE DATES ON WHICH THAT CALLSIGN WAS WITHIN THE RADIUS OF THAT LAT, LON POINT

# DEVELOP AS A SEPARATE CLASS A MAPPING CAPABILITY12
