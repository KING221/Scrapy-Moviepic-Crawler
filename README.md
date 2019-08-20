# Scrapy-Moviepic-Crawler
## 项目简介
  Scrapy爬取豆瓣电影图片，将图片通过`<ImagePipeline>`下载到本地并将信息存储至MongoDB。

## 模块说明
### Items.py 
```
class HppicItem(scrapy.Item):
    # define the fields for your item here like:
    links = scrapy.Field()   #初步存储图片的链接，之后要关联到MongoDB
    nums = scrapy.Field()  #存储图片的链接编号，也就是和豆瓣电影图片“Pxxxxx”那段内容，以此作为图片的名称
```

### hpscrapy.py
```
links = p.xpath('div[@class="photo-show"]/div[@class="photo-wp"]/a/img/@src').extract()
```
  这句话是提取链接的source。具体情况具体分析，有的是```@href```，本例用了```@src```，因为源码使用的也是```@src``` 定义。

```
nums = links[0].split('/')[-1].replace('.jpg','')
```
  上一句提取出来的```links[0]``` 是字符串，所以能进行通过斜杠分隔的操作。

### pipelines.py
```
class MyImagesPipeline(ImagesPipeline):  #图片下载器
    def get_media_requests(self, item, info):  #这里的def后面的函数名是固定不变的，下面那个也是
        for links in item['links']:
            yield Request(links, meta={'item':item})  #'index':item['links'].index(links)

    def file_path(self, request, response=None, info=None):  #对图片进行命名
        item = request.meta['item']
        image_name = item['nums']  #以item里的nums进行命名
        return '%s.jpg'%(image_name)
```

```
class HppicPipeline(object):  #pymongo相关的配置，大部分都可以固定，只有两处需要改动
    def __init__(self):
        host = '127.0.0.1'
        port = 27017
        dbname = 'HP'  #数据库名字
        sheetname = 'pic_info'  #表格名字
        client = pymongo.MongoClient(host=host, port=port)
        mydb = client[dbname]
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item
```

### settings.py
```
ITEM_PIPELINES = {
    'HPPIC.pipelines.HppicPipeline': 300,
    'HPPIC.pipelines.MyImagesPipeline':1
}
IMAGES_STORE='D:\HP_PIC'
```
  除了数据库的pipelines，还可以进行图片下载器的设置。还得设置图片下载路径。
  相关截图如下：
![image](https://github.com/KING221/Scrapy-Moviepic-Crawler/blob/6f76d500de7a58a103e16851f54226e05dd4d025/PIC/QQ拼音截图20190820234433.png)
![image](https://github.com/KING221/Scrapy-Moviepic-Crawler/blob/master/QQ拼音截图20190820234830.png)
