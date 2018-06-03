#### putty login
_ssh user@127.0.0.1 -p 2222_
#### see HDFS file system
_hadoop fs -ls_
#### make a directory
_hadoop fs -mkdir <name>_
#### add to hadoop from Linux server
_hadoop fs -copyFromLocal <name>_
_hadoop fs -copyFromLocal <name> <locationFolder>/<name>_
#### remove data from hadoop cluster
_hadoop fs -rm <folder>/<file>_
#### remove directory 
_hadoop fs -rmdir  <dir>_
#### run python script
**python <name>.py -r hadoop --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar <dataset>**

#### PigScript
**ratings = LOAD '/ml-100k/u.data' AS (userID:int, movieID:int, rating:int, ratingTime:int);**
  
  **metadata = LOAD '/ml-100k/u.item' USING PigStorage('|')**
  	**AS**
      **(movieID:int, movieTitle:chararray, releaseDate:chararray, videoRelease:chararray, imdbLink:chararray);**
  
  **nameLookup = FOREACH metadata GENERATE movieID, movieTitle, ToUnixTime(ToDate(releaseDate,'dd-MMM-yyyy'))**
  	**AS releaseTime;**
      
  **raitingsByMovie = GROUP ratings BY movieID;**
  
  **avgRatings = FOREACH raitingsByMovie GENERATE group AS movieID, AVG(ratings.rating) AS avgRating;**
  
  **fiveStarMovies = FILTER avgRatings BY avgRating > 4.0;**
  
  **fiveStarWithData = JOIN fiveStarMovies BY movieID, nameLookup BY movieID;**
  
  **OldfiveStarMovies = ORDER fiveStarWithData BY nameLookup::releaseTime;**
  
  **DUMP OldfiveStarMovies**