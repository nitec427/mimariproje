import sqlite3 as dbapi2

from models import Entry

class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile

    def addEntry(self, newEntry):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO ENTRIES (pleasant, interesting, beautiful, normal, calm, spacious, bright, opennes,
            simpleness, safe, firstFloorUse, prop1FloorWind, pavementQuality, scenery, pavementContinuity, streetLink,
            buildingScale, propStreetWall, propSkyAcross, streetWidth, vivid, damagedBuilding, humanPopulation, carParking,
            allStreetFurn, smallPlant, histBuildings, contemporaryBuildings, urbanFeat, greenness, accentColor,
            publicSpaceUsage, community, trafficVol, posSamples, negSamples)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

            cursor.execute(query, (newEntry.pleasant, newEntry.interesting, newEntry.beautiful, newEntry.normal, newEntry.calm,
                newEntry.spacious, newEntry.bright, newEntry.opennes, newEntry.simpleness, newEntry.safe, newEntry.firstFloorUse,
                newEntry.prop1FloorWind, newEntry.pavementQuality, newEntry.scenery, newEntry.pavementContinuity, newEntry.streetLink,
                newEntry.buildingScale, newEntry.propStreetWall, newEntry.propSkyAcross, newEntry.streetWidth, newEntry.vivid,
                newEntry.damagedBuilding, newEntry.humanPopulation, newEntry.carParking, newEntry.allStreetFurn, newEntry.smallPlant,
                newEntry.histBuildings, newEntry.contemporaryBuildings, newEntry.urbanFeat, newEntry.greenness, newEntry.accentColor,
                newEntry.publicSpaceUsage, newEntry.community, newEntry.trafficVol, newEntry.posSamples, newEntry.negSamples))
            cursor.close()