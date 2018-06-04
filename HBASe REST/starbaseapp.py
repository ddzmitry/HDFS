from starbase import Connection

c = Connection("127.0.0.1","8002")

ratings = c.table('ratings')

if(ratings.exists()):
    print("Dropping existing table\n")
    ratings.drop()

ratings.create('rating')
print('parsing the ml-100k ratings data....\n')
ratingFile = open("C:/Users/ddzmi/Downloads/ml-100k/ml-100k/u.data","r")

batch = ratings.batch()

for line in ratingFile:
    (userID, movieID, rating, timestamp) = line.split()
    batch.update(userID,{'rating':{movieID:rating}})

ratingFile.close()

print("Commiting ratings data to HBase vie REST servise\n")
batch.commit(finalize=True)
print("Get Back Ratings for some user....\n")
print (ratings.fetch("1"))
print("get rating for user ID 2 : \n")
print (ratings.fetch("33"))
