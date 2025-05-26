from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from config import first_setup, MONGO_URI, MONGO_DB


# Globals to hold the database connection and collections
client = None
db = None
users = None
logs = None


async def init_db():
    """
    Asynchronously initializes the MongoDB connection and sets global database references.
    Only initializes if first_setup is False.
    """
    global client, db, users, logs

    if first_setup:
        print("Skipping database initialization as first_setup is True.")
        return False

    try:
        client = AsyncIOMotorClient(
            MONGO_URI,
            maxPoolSize=50,
            connectTimeoutMS=5000,
            serverSelectionTimeoutMS=5000,
            waitQueueTimeoutMS=5000,
        )

        await client.admin.command("ping")
        db = client[MONGO_DB]
        users = db["users"]
        logs = db["logs"]
        print("MongoDB connection established successfully.")
        return True
    except ConnectionFailure as e:
        raise Exception(
            f"Failed to connect to MongoDB: {str(e)}. Please check your connection settings."
        ) from e


async def test_db_connection(uri=None, db_name=None):
    """
    Tests the MongoDB connection and returns True if successful, False otherwise.

    Args:
        uri (str, optional): MongoDB URI to test. Defaults to MONGO_URI from config
        db_name (str, optional): MongoDB database name to test. Defaults to MONGO_DB from config
    """
    try:
        test_uri = uri if uri is not None else MONGO_URI
        test_db = db_name if db_name is not None else MONGO_DB

        if test_uri is None or test_db is None:
            return False

        test_client = AsyncIOMotorClient(
            test_uri,
            maxPoolSize=50,
            connectTimeoutMS=5000,
            serverSelectionTimeoutMS=5000,
            waitQueueTimeoutMS=5000,
        )

        await test_client.admin.command("ping")
        testing_db = test_client[test_db]
        test_client.close()
        return True
    except ConnectionFailure:
        return False


async def close_db_connection():
    """
    Closes the MongoDB client connection if it exists.
    """
    global client
    if client:
        client.close()
        print("[MongoDB] Connection closed.")
        client = None