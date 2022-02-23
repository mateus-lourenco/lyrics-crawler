# Lyrics crawler with Scrapy 🎵

webcrawler to generate a database to store songs lyrics for NLP and sentiment analysis

## How to run 🚀

### Create a Python virtual enviroment 🐍
```
python -m virtualenv .venv
```
#### Linux 🐧
```
source .venv/bin/activate
```
#### Windows 🗔
```
.venv\Scripts\activate.exe
```

### Install MongoDB 🖥
> install [mongodb](https://docs.mongodb.com/manual/installation/)

### Install all requirements 📰
 ```
 pip install -r requirements.txt
 ```

### Run the Spider 🕷️
```
scrapy crawl lyricsSpider
```
