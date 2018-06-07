#Linux command line tips

#### Tar Files
+ *create tar* tar-c 
+ *create tar with name* tar -cf name.tar folder
+ *list files of archive* tar -tf name.tar
+ *Execute Files* tar -xf name.tar
#### Conperession
+ *Compress File* tar -czf name.tar.gz nameFolder
+ *BZip2 compression* tar -cjf name.tar.bz2 folder
+ *Decompress gz* tar -xzf name.tar.gz
+ *Decompress BZip2* tar -xvjf name.tar.bz2
+ *Extract to folder* tar -xzvf compressed.tar.gz -C folder/

#### ZIP
+ *Compress ALL* zip -r name.zip folder
+ *Unzip* unzip file.zip
+ *to zip files* gzip *.extention
+ *to unzip files* gunzip *.gz
+ *to bzip2 files* bzip2 *.extention
+ *to unzip bzip2 files* bunzip2 *.bz2

### Searching and Extracting Data from Files
+ cat
+ less -n _number_
+ head -n _number_
+ tail -f /var/log/secure _will track the file in real time_
### Analyzing Text
+ ls -lrt >> output.log
+ head -n 1 file.txt
+ _put in another file lines_ head -n 1 file.txt > file2.txt 
+ `>>` will keep the old data that was in previous file 
_If we want to cut line we can cut it on separator and get everything after it_
+ cut -d" " 6 -f 6- filename.txt
_Sort will sort Alphabeticly_
+ sort filename.txt
+ echo >> file.txt _will add empty line_
_Word,Line Count_
+ wc -lw
### Pipes and RegEX


