
import glob,requests,os,m3u8,zhead,re,tqdm,difflib,time,string
from urllib.parse import unquote,quote
from concurrent.futures import ThreadPoolExecutor
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from lxml import etree
from playwright.sync_api import sync_playwright  #pip install playwright --- playwright install --- playwright codegen -b firefox ----text_content()获取所有标签中间的文本---
from playwright.async_api import async_playwright  #pip install playwright --- playwright install --- playwright codegen -b firefox ----text_content()获取所有标签中间的文本---

class CustomError(Exception):  # 自定义错误信息
    def __init__(self,ErrorInfo): self.errorinfo=ErrorInfo
    def __str__(self): return self.errorinfo
    
downpath = 'D:\\userfolder\\Downloads' # 创建临时文件夹和下载文件夹
tmppath = 'c:\\temp'
if not os.path.exists(downpath): os.mkdir(downpath)
if not os.path.exists(tmppath): os.mkdir(tmppath)
header=zhead.head()

def urlhead(url): return url[:url.index('/',8)] # 获取url的第一级域名

def downmp4(frameurl, mp4url, title, lesson):  #多线程下载mp4视频
    print(f'\n{mp4url}')
    _headers = zhead.head()        #检测嵌套网站
    headers = requests.head(url=mp4url, headers=_headers, allow_redirects=False).headers
    if headers.get('Location') is not None: return downmp4(headers.get('Location'), title, lesson)

    filesize = int(headers.get('Content-Length') )
    block = 16*1024*1024
    filename = f"{downpath}\\{title}\\{lesson}.mp4"
    print(f'{filesize//block+1} 线程下载 {filename} {filesize/1024/1024} MB')
    if filesize/(1024*1024)>350 or filesize/(1024*1024)<20: raise
    if not os.path.exists(f"{downpath}\\{title}"): os.mkdir(f"{downpath}\\{title}")
    with open(filename, 'wb') as fp: pass   #fp.truncate(filesize)
    def Handler(start):
        _headers['Range'] = f'bytes={start}-{start+block-1}'
        response = requests.get(url=mp4url, headers=_headers, stream=True )
        bsize = int(response.headers.get('Content-Length'))
        bartqdm = tqdm.tqdm( total=bsize, desc=f'线程{start//block+1}', leave=0, ncols=99, unit_scale=True, unit='MB' )
        with open(filename, 'r+b') as f:
            f.seek(start)
            stime=time.time()
            for count, chunk in enumerate( response.iter_content(1024) ):
                if count/((time.time()-stime+0.000001))<300 and count>11: return Handler(start)
                f.write(chunk)
                bartqdm.update(1024)
    with ThreadPoolExecutor(max_workers=5) as pool:
        for start in range(0, filesize, block): pool.submit(Handler, start)

def downm3u8(frameurl, m3u8url, title, lesson, first, end, max_workers):  #多线程下载m3u8视频 
    print(f'\n{title}\\{lesson}.mp4--{frameurl}')
    headval=zhead.head() # headval.update({'Referer': urlhead(frameurl)})
    m3u8url = quote(m3u8url, safe=string.printable)
    while 1:
        print(f'{m3u8url}')  #检测嵌套m3u8
        playlist = m3u8.load(uri=m3u8url, headers=headval, verify_ssl=False)
        for i in playlist.playlists:
            if i.absolute_uri !='': break
        else: break
        m3u8url = i.absolute_uri
    try:
        for i in playlist.keys:
            if i.absolute_uri !='': break
        key = requests.get(url=i.absolute_uri, headers=headval).content
        print(i.absolute_uri, key)
    except Exception: key = 0

    for tspath in glob.glob(f'{tmppath}\\*.*'): os.remove(tspath)   #清理临时文件
    count=[0]            #多线程下载
    if end==0: end=len(playlist.segments[first:])+first-1
    def download_ts(tsurl, num):
        try:
            tsfile = requests.get(tsurl, headers=headval, timeout=1).content
            if key: tsfile = AES.new(key=key, mode=AES.MODE_CBC, iv=key).decrypt(pad(data_to_pad=tsfile, block_size=AES.block_size) )
            # tsfile = bytearray(tsfile)  # convert bytes to bytearray for mutable operations
            # tsfile[:4] = b"\xff" * 4  # set first 4 bytes to b'\xff' 从G@开始截取 
            suoyin = tsfile.index(b'\x47\x40')
            with open(f"{tmppath}\\{num:0>5d}.ts", "wb") as f: f.write(tsfile)
            if os.path.getsize(f"{tmppath}\\{num:0>5d}.ts") <1000: raise
        except Exception: return download_ts(tsurl, num)
        count[0]=count[0]+1
        tqdm.tqdm.write(f"\r{tsurl} {count[0]}/{len(playlist.segments[first:end+1]) }", end="  ")
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        for num, seg in enumerate(playlist.segments[first:end+1]): pool.submit(download_ts, seg.absolute_uri, num+first)
    print()
    #tmpfiles = glob.glob(f'{tmppath}\\*.ts')
    #if len(playlist.segments) < 9 : raise CustomError('文件错误')

    if not os.path.exists(f'{downpath}\\{title}'): os.mkdir(f'{downpath}\\{title}')  #合并m3u8
    filename = '%s\\%s\\%s.mp4'%(downpath, title, lesson )
    version = 3   #playlist.data['version']
    target = playlist.data['targetduration']
    m3u8list = ['#EXTM3U\n', f'#EXT-X-VERSION:{version}\n', f'#EXT-X-TARGETDURATION:{target}\n', '#EXT-X-PLAYLIST-TYPE:VOD\n', '#EXT-X-MEDIA-SEQUENCE:0\n', ]
    m3u8path = f'{tmppath}\\tspath.m3u8'
    for num in range(first,end+1):
        extinf = playlist.data['segments'][num]['duration']
        m3u8list.extend((f'#EXTINF:{extinf},\n', f"{tmppath}\\{num:0>5d}.ts\n"))
    m3u8list.append('#EXT-X-ENDLIST\n')
    with open(m3u8path, 'w') as fobj: fobj.writelines(m3u8list)
    os.system(f'ffmpeg -v warning -hide_banner -stats -i {m3u8path} -c:v copy -c:a copy {filename} -y -loglevel quiet')

def getvurl(frameurl, htmltxt, title, lesson, first, end, max_workers):  # 不知道该怎么获取视频链接，所以直接搜索所有MP4和m3u8地址。
    htmltxt=unquote(htmltxt).replace("\\", "").replace("amp;", "").replace("u0026", "&")
    htmls = re.split(''''|"''', htmltxt )
    for num,html in enumerate(htmls):
        if '.mp4' in html:
            if html[0] == '/': html = urlhead(frameurl) + html
            try: downmp4(frameurl, html, title, lesson)
            except Exception as e: print(e)
            else: break
        elif '.m3u8' in html:
            if html[0] == '/': html = urlhead(frameurl) + html
            try: downm3u8(frameurl, html, title, lesson, first, end, max_workers)
            except Exception as e: print(e)
            else: break
        if num==len(htmls)-1: raise

def getttml(vidurl, title, lesson, first, end, max_workers):  # 获取视频位置
    print(f'\n{title}\\{lesson}.mp4--{vidurl}')
    # response = requests.get(vidurl, headers=header, allow_redirects=False )
    # jummurl = response.headers.get('Location')
    # if jummurl != None: return getttml(jummurl, title, lesson, first, end, max_workers) # 很多网站都会跳转不知道这样解决是否正确。
    with sync_playwright() as pw:
        brow = pw.chromium.launch(headless=True) # 有些网站要浏览器一直开着才有内容就改为false.
        page = brow.new_context(viewport={"width":960,"height":540}, ignore_https_errors=True).new_page()
        try: page.goto(vidurl)
        except: pass
        for frame in page.frames: # 查找所有frame
            try: getvurl(frame.url, frame.content(), title, lesson, first, end, max_workers)
            except Exception: continue
            else: break
        else: 
            brow.close()
            raise CustomError('\n查找所有frame页面失败')
        brow.close()

def getvids(video):  # 获取视频列表
    res = requests.get(video, headers=header )
    res.encoding = res.apparent_encoding
    htmlxpath = etree.HTML(res.text.replace("\\", "") )
    title = htmlxpath.xpath('//title//text()')[0][:16]
    #title = title.encode('iso-8859-1').decode('gbk') # 中文编码问题把我搞迷糊了不知道该怎么写。
    title = re.sub(r'([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u007a])', '', title).strip() # 
    hrefs, httpend = htmlxpath.xpath('//a//@href'), video[video.index('/', 8) :]
    if hrefs==[]: print(res.text, video )
    return title, [ href for href in hrefs if difflib.SequenceMatcher( None, httpend, href ).quick_ratio() > 0.8 ] # 找到与视频地址相似度大于0.8的所有url，一般就是剧集列表。

def main(video, title, vids, first, end, max_workers): # 主循环，根据剧集列表选择下载哪一集。
    while True:
        for num, vid in enumerate(vids):
            vids[num] = vid if vids[num].split('/')[0] in ['https:', 'http:'] else urlhead(video) + vid
            print(f'\n{num+1:0>2d}: {vids[num]}', end='' )
        part=input(f"\n\n{title}, 你要下载那一集(例如1-5): ")
        s,e=part.split("-")
        #if jump := input(f"\n{title}, 跳过片头片尾(例如9-986): "): first,end=jump.split("-") # 本想跳过片头片尾，但是不怎么好用就放弃了。
        for num in range(int(s)-1,int(e)): 
            lesson = vids[num].split('/')[-2] if vids[num].split('/')[-1]=='' else vids[num].split('/')[-1].split('.')[0]
            if len(vids)==1: lesson = title
            while 1:
                try: getttml(vids[num], title, lesson, int(first), int(end), max_workers)
                except Exception as e: print(e)
                else: break
        

if __name__=="__main__":

    video = 'https://mmm.mmm.mmm/vodplay/155947-1-1.html' # url示例,粘贴你的视频地址.
    
    vids = ()
    
    if not vids: # 获取剧集列表并打印，方便调试。
        vids = getvids(video)
        print('\n',vids)
    main(video, vids[0], vids[1], 0, 0, 999)
