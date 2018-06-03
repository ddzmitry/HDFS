from mrjob.job import MRJob
from mrjob.step import MRStep

class RatingsBreakdown(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_ratings,
                   reducer=self.reducer_count_ratings),
            MRStep(reducer=self.reducer_sorted_output),

        ]

    def mapper_get_ratings(self, _, line):
        (userID, movieID, rating, timestamp) = line.split('\t')
        yield movieID, 1

    def reducer_count_ratings(self, key, values):
        # Rating Counts
        # we set up as 00000 number and key of the movie
        yield str(sum(values)).zfill(5), key

    def reducer_sorted_output(self,count,movies):
        for movie in movies:
            # return movie and its count
            yield movie,count

if __name__ == '__main__':
    RatingsBreakdown.run()
