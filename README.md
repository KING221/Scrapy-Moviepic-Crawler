# Scrapy-Moviepic-Crawler
## 项目简介
  Scrapy爬取豆瓣电影图片，将图片通过`<ImagePipeline>`下载到本地并将信息存储至MongoDB。

## Items.py 
```
class HppicItem(scrapy.Item):
    # define the fields for your item here like:
    links = scrapy.Field()   #初步存储图片的链接，之后要关联到MongoDB
    nums = scrapy.Field()  #存储图片的链接编号，也就是和豆瓣电影图片“Pxxxxx”那段内容，以此作为图片的名称
```

## hpscrapy.py
```
links = p.xpath('div[@class="photo-show"]/div[@class="photo-wp"]/a/img/@src').extract()
```
  这句话是提取链接的source。具体情况具体分析，有的是```@href```，本例用了```@src```，因为源码使用的也是```@src``` 定义。

```
nums = links[0].split('/')[-1].replace('.jpg','')
```
  上一句提取出来的```links[0]``` 是字符串，所以能进行通过斜杠分隔的操作。

