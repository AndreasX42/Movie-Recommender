import chromadb

client = chromadb.PersistentClient(path="chromadb/")
movie_collection = client.get_collection(name="movies")
user_collection = client.get_collection(name="users")
