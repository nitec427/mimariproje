import sqlite3 as dbapi2
from passlib.hash import pbkdf2_sha256 as hasher

from models import Entry
from login_management import User


class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile

    def create(self):
        with dbapi2.connect(self.dbfile) as connection:

            connection.execute(
                """CREATE TABLE ENTRIES (ID INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, pleasant INTEGER, interesting INTEGER,
                beautiful INTEGER, normal INTEGER, calm INTEGER, spacious INTEGER, bright INTEGER, opennes INTEGER, simpleness INTEGER, 
                safe INTEGER, firstFloorUse INTEGER, prop1FloorWind INTEGER, pavementQuality INTEGER, scenery INTEGER, pavementContinuity INTEGER,
                streetLink INTEGER, buildingScale INTEGER, propStreetWall INTEGER, propSkyAcross INTEGER, streetWidth INTEGER,
                vivid INTEGER, damagedBuilding INTEGER, humanPopulation INTEGER, carParking INTEGER, allStreetFurn INTEGER,
                smallPlant INTEGER, histBuildings INTEGER, contemporaryBuildings INTEGER, urbanFeat INTEGER, greenness INTEGER,
                accentColor INTEGER, publicSpaceUsage INTEGER, community INTEGER, trafficVol INTEGER, posSamples CLOB, negSamples CLOB)""")

            connection.execute("CREATE TABLE USERS (Username TEXT PRIMARY KEY, Password TEXT)")

            # Create first user
            username = "admin"
            password = hasher.hash("admin")

            new_user = User(username, password)
            self.addUser(new_user)

    def addEntry(self, newEntry):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO ENTRIES (Username, pleasant, interesting, beautiful, normal, calm, spacious, bright, opennes,
            simpleness, safe, firstFloorUse, prop1FloorWind, pavementQuality, scenery, pavementContinuity, streetLink,
            buildingScale, propStreetWall, propSkyAcross, streetWidth, vivid, damagedBuilding, humanPopulation, carParking,
            allStreetFurn, smallPlant, histBuildings, contemporaryBuildings, urbanFeat, greenness, accentColor,
            publicSpaceUsage, community, trafficVol, posSamples, negSamples)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

            cursor.execute(query, (newEntry.username, newEntry.pleasant, newEntry.interesting, newEntry.beautiful, newEntry.normal, newEntry.calm,
                                   newEntry.spacious, newEntry.bright, newEntry.opennes, newEntry.simpleness, newEntry.safe, newEntry.firstFloorUse,
                                   newEntry.prop1FloorWind, newEntry.pavementQuality, newEntry.scenery, newEntry.pavementContinuity, newEntry.streetLink,
                                   newEntry.buildingScale, newEntry.propStreetWall, newEntry.propSkyAcross, newEntry.streetWidth, newEntry.vivid,
                                   newEntry.damagedBuilding, newEntry.humanPopulation, newEntry.carParking, newEntry.allStreetFurn, newEntry.smallPlant,
                                   newEntry.histBuildings, newEntry.contemporaryBuildings, newEntry.urbanFeat, newEntry.greenness, newEntry.accentColor,
                                   newEntry.publicSpaceUsage, newEntry.community, newEntry.trafficVol, newEntry.posSamples, newEntry.negSamples))
            cursor.close()

    def addUser(self, new_user):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO USERS (username, password)
            VALUES (?, ?)"""
            cursor.execute(query, (new_user.get_username(), new_user.get_password()))
            cursor.close()


    def getPassword(self, username):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """SELECT Password FROM USERS                    
            WHERE username = ?"""
            cursor.execute(query, (username,))
            password = cursor.fetchone()
            if password != None:
                password = password[0]
            cursor.close()
            return password