from django.test import TestCase
from django.db import connections
from ..models.VectorEngine import VectorEngine
from ..models.KBitem import * 
from ..models.Query import *
import psycopg2
from dotenv import load_dotenv
import os
import statistics
load_dotenv()


class VectorTest(TestCase):
    vectorCollectionName = "VectorTest"
    allURIs = []

    mainDBConnection = psycopg2.connect(
        host="localhost",
        database = 'Athena',
        user = 'postgres',
        password = os.environ.get("PGVECTOR_PASSWORD", "postgres")
    )
    
    def setUpQueries(self):
        self.allURIs = []
        URI = "https://twitter.com/GuyDealership/status/1678533370958032896?s=20"
        queries = ["car market", "Used car market", "lowering supply should keep the prices high", "Car prices are experience drop in prices", "deflation"]
        URI = testQuery(URI, queries)
        self.allURIs.append(URI)

        URI = "https://twitter.com/WallStreetSilv/status/1679588837301923841?s=20"
        queries = ["twitter", "blockchain", "bitcoin", "centralized digitial currency", "governemnt could freeze your accounts"]
        URI = testQuery(URI, queries)
        self.allURIs.append(URI)

        URI = "https://www.instagram.com/reel/CuNIOoVOR0v/?utm_source=ig_web_copy_link&igshid=MzRlODBiNWFlZA=="
        queries = ["inconsistency with golf swing", "keeping left arm straight on backswing", "where should my club be at the top of my back swing"]
        URI = testQuery(URI, queries)
        self.allURIs.append(URI)

        URI = "https://thestayathomechef.com/how-to-cook-steak/"
        queries = ["recipe for cooking a steak", "temperature a steak should be cooked to", "steak", "cooking a filet"]
        URI = testQuery(URI, queries)
        self.allURIs.append(URI)
        
        URI = "https://www.bhg.com/recipes/how-to/handling-meat/cook-whole-chicken/"
        queries = ["recipe for cooking chicken", "chicken", "baking chicken", "season a chicken"]
        URI = testQuery(URI, queries)
        self.allURIs.append(URI)

        URI = "https://www.instagram.com/reel/CsPAreZuh4T/?igshid=MTc4MmM1YmI2Ng%3D%3D"
        queries = ["drill for lower body movement", "using the gorund to speed up the club", "golf drill for rotating to the ball", "golf drill"]
        URI = testQuery(URI, queries)
        self.allURIs.append(URI)

        URI = "https://www.instagram.com/reel/CszDLDdsa_u/?igshid=MTc4MmM1YmI2Ng%3D%3D"
        queries = ["dill for fixing my slice","stop slicing the golf ball", "golf drill", "drill"]
        URI = testQuery(URI, queries)
        self.allURIs.append(URI)



        



    def createVectorEngine(self):
        return VectorEngine(self.vectorCollectionName)
        
    def changeEmbeddingModel(vectorEngine, embeddings):
        vectorEngine.vectorDatabase = PGVector(
                collection_name=vectorEngine.vectorCollectionName,
                connection_string=vectorEngine.CONNECTION_STRING,
                embedding_function=embeddings,
        )

        return VectorEngine
 
        
    def addTestURIs(self): 
        kbItemList = [] 
        for item in self.allURIs: 
            
            uri = item.URI 

            if 'instagram' in uri or 'twitter' in uri: 
                kbItem = ImageKBItem(URI = uri)
            else: 
                print("textdsdsdsdsd")
                kbItem = TextKBItem(URI = uri)
            
            kbItem.parseURI()
            kbItem.save() 
            print(kbItem.id)
            kbItemList.append(kbItem)
        
        return kbItemList
    

    def emptyTestDB(self): 
        cursor = self.mainDBConnection.cursor()
        sql_empty_query = f"DELETE FROM langchain_pg_embedding WHERE collection_id = %s"
        cursor.execute(sql_empty_query, ("a5cc26f9-a46b-41d6-938c-d748fed2487f",))
        self.mainDBConnection.commit()
        cursor.close()

    def storeTestVectors(self, chunk_size):

        newVectorEngine = self.createVectorEngine()
 
        kbItemList = self.addTestURIs() 

        for kbItem in kbItemList: 
            kbItem.vectorEngine = newVectorEngine
            kbItem.createVector(chunk_size = chunk_size)


    

    def test_chunkSize(self): 
        chunkSizes = [25, 50, 100, 200, 500]
        self.setUpQueries()

        for chunkSize in chunkSizes:
            print("\nITERATION WITH CHUNK SIZE = " + str(chunkSize))
            self.emptyTestDB()
            self.storeTestVectors(chunkSize)

            for resourceQueries in self.allURIs: 
                print("\nTESTS FOR URI: " + resourceQueries.URI)
                matchScores = [] 
                for query in resourceQueries.relevantQueries: 
                    qObject = Query(query)
                    qObject.vectorEngine = self.createVectorEngine()
                    sortedKbItems = qObject.getMatchedDocs()
                    topMatchItem = sortedKbItems[0]

                    topMatchScore = topMatchItem[1]
                    topMatchURI = topMatchItem[0].URI

                    try:
                        self.assertEqual(topMatchURI, resourceQueries.URI)
                        print("QUERY STRING: " + query + " SCORE = " + str(topMatchScore) + " Next Closest Score: " + str(sortedKbItems[1][1] if len(sortedKbItems)>1 else 0))
                        matchScores.append(topMatchScore)

                    except AssertionError:
                        print("QUERY STRING: " + query + " FAIL: MATCHED " + topMatchURI+ "SCORE = " + str(topMatchScore) + " Next Closest Score: " + str(sortedKbItems[1][1] if len(sortedKbItems)>1 else 0) + "Matching " + sortedKbItems[1][0].URI)
                
                print("AVERAGE MATCH SCORE = " + str(statistics.mean(matchScores)))
         
    
    def test_accuracy(self):
        self.setUpQueries()
        self.emptyTestDB()
        self.storeTestVectors(100)

        for resourceQueries in self.allURIs: 
            print("\nTESTS FOR URI: " + resourceQueries.URI)
            matchScores = [] 
            for query in resourceQueries.relevantQueries: 
                qObject = Query(query)
                qObject.vectorEngine = self.createVectorEngine()
                sortedKbItems = qObject.getMatchedDocs()
                topMatchItem = sortedKbItems[0]

                topMatchScore = topMatchItem[1]
                topMatchURI = topMatchItem[0].URI

                try:
                    self.assertEqual(topMatchURI, resourceQueries.URI)
                    print("QUERY STRING: " + query + " SCORE = " + str(topMatchScore) + " Next Closest Score: " + str(sortedKbItems[1][1] if len(sortedKbItems)>1 else 0))
                    matchScores.append(topMatchScore)

                except AssertionError:
                    print("QUERY STRING: " + query + " FAIL: MATCHED " + topMatchURI+ "SCORE = " + str(topMatchScore) + " Next Closest Score: " + str(sortedKbItems[1][1] if len(sortedKbItems)>1 else 0) + "Matching " + sortedKbItems[1][0].URI)
            
            print("AVERAGE MATCH SCORE = " + str(statistics.mean(matchScores)))

        
class testQuery(): 
    def __init__(self, URI, releventQueries):
        self.URI = URI
        self.relevantQueries = releventQueries

        

