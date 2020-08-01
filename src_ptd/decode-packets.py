from aprspy import APRS
import pandas as pd


class DecodePackets:

    def __init__(self, src: str, outfile: str, infiletype: str):
        """Class initialization
        :param src: source data filename
        """
        self.src = src
        self.outfile = outfile
        self.infiletype = infiletype
        self._readfile()
        self._decode()

    def _readfile(self):
        headings = ['datetime', 'packet']
        if self.infiletype == "lynn":
            colspecs = [(13, 32), (32, 1000)]
            self.packets = pd.read_fwf(self.src, names=headings, header=None, colspecs=colspecs)
        elif self.infiletype == "patrick":
            colspecs = [(0, 19), (19, 1000)]
            self.packets = pd.read_fwf(self.src, names=headings, header=None, colspecs=colspecs)

    def _decode(self):
        raw, typelist, callsign, tslist, latlist, lonlist, altlist, commentlist, messagelist = ([] for i in range(9))
        sourcelist, addresseelist, statuslist, courselist, bearinglist, speedlist = ([] for i in range(6))
        errortimes, errorpackets = ([] for i in range(2))
        for row in self.packets.itertuples():
            print(row)
            try:
                decoded = APRS.parse(row.packet, row.datetime)
            except:
                errortimes.append(row.datetime)
                errorpackets.append(row.packet)
                continue
            if type(decoded).__name__ == 'PositionPacket':
                typelist.append('Position')
                tslist.append(decoded._ts)
                latlist.append(decoded.latitude)
                lonlist.append(decoded.longitude)
                altlist.append(decoded.altitude)
                commentlist.append(decoded.comment)
                messagelist.append('None')
                sourcelist.append(decoded.source)
                addresseelist.append('None')
                statuslist.append('None')
                courselist.append(decoded.course)
                bearinglist.append(decoded.bearing)
                speedlist.append(decoded.speed)
            elif type(decoded).__name__ == 'MessagePacket':
                typelist.append('Message')
                tslist.append(decoded._ts)
                latlist.append('None')
                lonlist.append('None')
                altlist.append('None')
                commentlist.append('None')
                messagelist.append(decoded.message)
                sourcelist.append(decoded.source)
                addresseelist.append(decoded.addressee)
                statuslist.append('None')
                courselist.append('None')
                bearinglist.append('None')
                speedlist.append('None')
            elif type(decoded).__name__ == 'StatusPacket':
                typelist.append('Status')
                tslist.append(decoded._ts)
                latlist.append('None')
                lonlist.append('None')
                altlist.append('None')
                commentlist.append('None')
                messagelist.append('None')
                sourcelist.append(decoded.source)
                addresseelist.append('None')
                statuslist.append(decoded.status_message)
                courselist.append('None')
                bearinglist.append('None')
                speedlist.append('None')
            elif type(decoded).__name__ == 'ObjectPacket':
                typelist.append('Object')
                tslist.append(decoded._ts)
                latlist.append('None')
                lonlist.append('None')
                altlist.append('None')
                commentlist.append('None')
                messagelist.append('None')
                sourcelist.append(decoded.source)
                addresseelist.append('None')
                statuslist.append('None')
                courselist.append('None')
                bearinglist.append('None')
                speedlist.append('None')
            else:
                print(type(decoded).__name__)
                print('Not able to decode this packet type yet...')
#                errortimes.append(row.datetime)
#                errorpackets.append(row.packet)
        decoded_df = pd.DataFrame(
            {'type': typelist,
             'timestamp': tslist,
             'source': sourcelist,
             'addressee': addresseelist,
             'latitude': latlist,
             'longitude': lonlist,
             'altitude': altlist,
             'comment': commentlist,
             'message': messagelist,
             'status': statuslist,
             'course': courselist,
             'bearing': bearinglist,
             'speed': speedlist}
        )
        decoded_df = decoded_df.set_index(['timestamp'])
        decoded_df.to_csv(self.outfile, na_rep="None")

rawdir = "/Users/ptduran/Desktop/APRS/raw/APRS_20190305-20200720_partial/"
rawfile = "KJ4OVR.LOG"
decodeddir = "/Users/ptduran/Desktop/APRS/decoded/APRS_20190305-20200720_partial/"

test = DecodePackets(rawdir+rawfile, decodeddir+rawfile+"-decoded.csv", "patrick")

#test = DecodePackets("/Users/ptduran/PycharmProjects/aprspy/packets/KJ4OVR-2015.LOG", "lynn")

# packet = APRS.parse('KJ4OVR-5>APDR12,TCPIP*,qAC,T2ZURICH:=3005.31N/08123.84W$039/001/A=-00042 !SN!', '2015-01-01 09:40:33')

# print(packet.__dict__)
# print(packet.latitude)
# print(packet.longitude)
