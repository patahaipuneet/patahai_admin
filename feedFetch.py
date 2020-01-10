#!/usr/bin/python3
import feedparser, pymysql, bs4
import re,datetime,time,schedule
import json

def feedJob(cron_id,url,cursor,etag,md):
    only_big=re.compile(r'(\.jpe?g)|(\.png)')
    etag_new=md_new=d=None
    if etag:
        d = feedparser.parse(url,etag=etag)
    if md:
        d = feedparser.parse(url,modified=modified)
    if not d:
        d = feedparser.parse(url)
    if d.get("status") == 304:
            return
    if 'modified_parsed' in d.keys():
        md_new=datetime.datetime(*(d.modified_parsed[0:6]))
        md_new=md.isoformat(' ')
    if 'etag' in d.keys():
        etag_new=d.etag
    if etag != etag_new or md != md_new:
        c1.execute("UPDATE rss_cron SET rss_cron.etag = %s , rss_cron.modified = %s where id = %s",(etag_new,md_new,cron_id))
    l=len(d.entries)
    for j in range(l):
        feed = d.entries[j]
        image=videoid=title=link=summary=content=tags=pd=None
        keys=feed.keys()
        if not keys:
            print(cron_id,'*******')
            return
        summary=feed.summary
        if 'content' in keys:
            summary = feed.content
        if "image" in keys:
            image=feed.image['href']
        elif "media_thumbnail" in keys:
            image=feed.media_thumbnail[0]['url']
        elif "storyimage" in keys:
            image = feed.storyimage
        elif "media_content" in keys:
            image=feed['media_content'][0]['url']
            
        
        if not image:
            soup = bs4.BeautifulSoup(feed.summary, "html.parser")
            ilink= soup.find('img',{'src' :only_big})
            if ilink and 'icon' not in ilink['src']:
                image = ilink['src'].lstrip('/')
        link= str(feed.links[0]['href'])
        if 'published_parsed' in keys and feed.published_parsed is not None:
            pd=datetime.datetime(*(feed.published_parsed[0:6]))
            pd=pd.isoformat(' ')
        cursor.execute("INSERT IGNORE INTO cards VALUES(null,%s,%s,%s,%s,%s,%s)",(cron_id,str(feed.title),str(link),str(summary),str(image),pd))
    db.commit()

    


db = pymysql.connect(host='localhost',user='root',passwd='root',db='patahai')


c1=db.cursor()


c1.execute("SELECT id,rss_url,duration,etag,modified  FROM rss_cron where status=1") # REGEXP WHERE rss_url 'youtube'
urllist=c1.fetchall()
x = len(urllist)

for i in range(x):
    cron_id = str(urllist[i][0])
    duration =int(urllist[i][2])
    url=urllist[i][1]
    etag=urllist[i][3]
    md=urllist[i][4]
    cursor=db.cursor()
    print('schdeule...',url)
    schedule.every(duration).seconds.do(feedJob,cron_id=cron_id,url=url,cursor=cursor,etag=etag,md=md)
    

while True:
    schedule.run_pending()
    print('sleeping...')
    time.sleep(5)
