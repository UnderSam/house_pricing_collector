import pymongo

client = pymongo.MongoClient("mongodb+srv://admin:<password>@pricing-cluster.kvcsc6z.mongodb.net/?retryWrites=true&w=majority")
db = client.test