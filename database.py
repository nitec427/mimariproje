import sqlite3 as dbapi2
from passlib.hash import pbkdf2_sha256 as hasher
from helpers import read_img_files
import random
from collections import Counter
from login_management import User

# generate random number for each user in its entirety ()


class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile

    def create(self):
        with dbapi2.connect(self.dbfile) as connection:

            # Create users table
            connection.execute(
                "CREATE TABLE USERS (Username TEXT PRIMARY KEY, Password TEXT)")

            # Create images table
            connection.execute(
                "CREATE TABLE IMAGES (Image_ID INTEGER PRIMARY KEY AUTOINCREMENT, Image_Path TEXT)")
            # !! Image path'ler database'e eklenmeli !!

            # Create entries table
            connection.execute(
                """
                CREATE TABLE ENTRIES (ID INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Image_ID INTEGER, pleasant INTEGER,
                interesting INTEGER, beautiful INTEGER, normal INTEGER, calm INTEGER, spacious INTEGER, bright INTEGER,
                opennes INTEGER, simpleness INTEGER, safe INTEGER, walkability INTEGER, firstFloorUse INTEGER, prop1FloorWind INTEGER,
                pavementQuality INTEGER, scenery INTEGER, pavementContinuity INTEGER, streetLink INTEGER, buildingScale INTEGER,
                propStreetWall INTEGER, propSkyAcross INTEGER, streetWidth INTEGER, vivid INTEGER, damagedBuilding INTEGER,
                humanPopulation INTEGER, carParking INTEGER, allStreetFurn INTEGER, smallPlant INTEGER, histBuildings INTEGER,
                contemporaryBuildings INTEGER, urbanFeat INTEGER, greenness INTEGER, accentColor INTEGER, publicSpaceUsage INTEGER,
                community INTEGER, trafficVol INTEGER, posSamples CLOB, negSamples CLOB,
                FOREIGN KEY (Username) REFERENCES USERS(Username),
                FOREIGN KEY (Image_ID) REFERENCES IMAGES(Image_ID))
                """)

            # Create admin
            username = "admin"
            password = hasher.hash("admin")

            new_user = User(username, password)
            self.addUser(new_user)
            image_counts, image_paths = read_img_files.read_files(
                'unprocessed')

    def addNewImages(self):
        with dbapi2.connect(self.dbfile) as connection:
            image_counts, image_paths = read_img_files.read_files(
                'unprocessed')
            cursor = connection.cursor()
            cursor.execute("select * from images")
            results = cursor.fetchall()
            db_img_count = len(results)
            # if new images are added
            if db_img_count != image_counts:
                my_arr = [i+db_img_count +
                          1 for i in range(image_counts - db_img_count)]
                random.shuffle(my_arr)
                result = tuple(zip(image_paths[db_img_count:], my_arr))
                sorted_result = sorted(result, key=lambda x: x[1])
                for i in range(image_counts - db_img_count):
                    path = "/" + sorted_result[i][0]
                    self.addImage(image_id=(i+1+db_img_count), image_path=path)

    def addEntry(self, newEntry):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO ENTRIES (Username, Image_ID, pleasant, interesting, beautiful, normal, calm, spacious,
            bright, opennes, simpleness, safe, walkability, firstFloorUse, prop1FloorWind, pavementQuality, scenery,
            pavementContinuity, streetLink, buildingScale, propStreetWall, propSkyAcross, streetWidth, vivid, damagedBuilding,
            humanPopulation, carParking, allStreetFurn, smallPlant, histBuildings, contemporaryBuildings, urbanFeat,
            greenness, accentColor, publicSpaceUsage, community, trafficVol, posSamples, negSamples)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

            cursor.execute(query, (newEntry.username, newEntry.image_id, newEntry.pleasant, newEntry.interesting, newEntry.beautiful,
                                   newEntry.normal, newEntry.calm, newEntry.spacious, newEntry.bright, newEntry.opennes,
                                   newEntry.simpleness, newEntry.safe, newEntry.walkability, newEntry.firstFloorUse,
                                   newEntry.prop1FloorWind, newEntry.pavementQuality, newEntry.scenery, newEntry.pavementContinuity,
                                   newEntry.streetLink, newEntry.buildingScale, newEntry.propStreetWall, newEntry.propSkyAcross,
                                   newEntry.streetWidth, newEntry.vivid, newEntry.damagedBuilding, newEntry.humanPopulation,
                                   newEntry.carParking, newEntry.allStreetFurn, newEntry.smallPlant, newEntry.histBuildings,
                                   newEntry.contemporaryBuildings, newEntry.urbanFeat, newEntry.greenness, newEntry.accentColor,
                                   newEntry.publicSpaceUsage, newEntry.community, newEntry.trafficVol, newEntry.posSamples,
                                   newEntry.negSamples))
            cursor.close()

    def addUser(self, new_user):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO USERS (username, password)
            VALUES (?, ?)"""
            cursor.execute(
                query, (new_user.get_username(), new_user.get_password()))
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

    # Kullanıcı sisteme tekrar giriş yaptığında kaldığı yerden devam edebilmesi için bi sonraki resmin id'sini alır

    def getNextImage(self, username):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """
            SELECT Image_ID FROM IMAGES
            WHERE Image_ID NOT IN (SELECT Image_ID
                                    FROM ENTRIES
                                    WHERE Username = ?)       
            ORDER BY RANDOM()
            LIMIT 1;
            """

            cursor.execute(query, (username,))
            next_image_id = cursor.fetchone()
            cursor.close()

            if next_image_id == None:
                return None

            return int(next_image_id[0])

    def getNextImagePath(self, username):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """
            SELECT Image_ID, Image_Path FROM IMAGES
            WHERE Image_ID NOT IN (SELECT Image_ID
                                    FROM ENTRIES
                                    WHERE Username = ?)       
            ORDER BY RANDOM()
            LIMIT 1;
            """

            cursor.execute(query, (username,))
            next_image_id = cursor.fetchone()
            cursor.close()

            if next_image_id == None:
                return None

            return next_image_id[1]

    def getImagePath(self, image_id):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """SELECT Image_Path FROM IMAGES
            WHERE Image_ID = ?;
            """
            cursor.execute(query, (image_id,))

            image_path = cursor.fetchone()[0]

            cursor.close()

            return image_path

    def addImage(self, image_id, image_path):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """INSERT OR IGNORE INTO IMAGES (Image_ID, Image_Path)
            VALUES (?,?);"""
            cursor.execute(query, (image_id, image_path))

            cursor.close()
