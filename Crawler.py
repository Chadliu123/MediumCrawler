from bs4 import BeautifulSoup as bs
import requests
import LinkAzureDB
import jieba.analyse


def Crawler(keyword, resultcount, ignore=None):
    # 網址
    url = f"https://medium.com/search/posts?q={keyword}&count={resultcount}&ignore={ignore}"
    # 呼叫網址
    link = requests.get(url, headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "uid=lo_arpU8KehP3fO; sid=1:LGJb8oPE72KIJ7hdf+swxMXZxvvYQpHF1saGJsNjrmSPdMCLa/sYCukY/SeCchzm; optimizelyEndUserId=lo_arpU8KehP3fO; _parsely_visitor={%22id%22:%22pid=f63aa53ec82176ccf0309f3d4cd288da%22%2C%22session_count%22:2%2C%22last_session_ts%22:1600148332800}; _ga=GA1.2.847571216.1589363261; __cfduid=d52b47f2304c41177d5973d7ec2cdba0d1600148331; __cfruid=8b3adde1b50f50090bc94252d42505fb260e249e-1600149745; _parsely_session={%22sid%22:2%2C%22surl%22:%22https://medium.com/search?q=%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E6%2585%25A7%22%2C%22sref%22:%22%22%2C%22sts%22:1600148332800%2C%22slts%22:1589363260250}; lightstep_guid/medium-web=a9e36a691f432073; lightstep_session_id=3ec514a362bcc40d; sz=1519; pr=1.25; tz=-480; _gid=GA1.2.800486480.1600148334; lightstep_guid/lite-web=02f362751b148f39; _gat=1",
        "Host": "medium.com",
        "TE": "Trailers",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0",
    })
    # BeautifulSoup 解析
    content = bs(link.text, "html.parser")
    # 獲取搜尋文章結果
    all_articles = content.find_all("div", class_="postArticle")
    # 建立空白表單
    articles_list = []
    # 載入jieba大字典
    jieba.set_dictionary('./extra_dict/dict.txt.big')
    # 取內容
    for n in all_articles:

        # 取 <div> 裡的 data-post-id，也就是 medium 裡的文章 id
        id = n.get("data-post-id")

        # 取 <time> 裡的 datetime，文章張貼時間
        time = n.select_one("time").get("datetime")

        # 取作者
        author = n.find_all("a", class_="ds-link")
        author = author[0].text

        # 一篇文章裡可能有大標(h3)，小標(h4)，文字(p)，不是每篇都固定有這三種。
        h3 = n.find_all("h3", class_="graf")
        h4 = n.find_all("h4", class_="graf")
        p = n.find_all("p", class_="graf")

        # 取標題，有大標用大標，沒大標用副標
        if [] != h3:
            title = h3[0].text
        elif [] != h4:
            title = h4[0].text
        elif [] != p:
            title = p[0].text

        # 取按讚數
        likes = n.find_all("button", class_="button")
        likes = likes[1].text
        likes = likes.replace(".", "")
        likes = likes.replace("K", "00")
        likes = int(likes)

        # 取url
        url = n.find_all("a", class_="link")
        url = url[2].get("data-action-value")
        # 內文爬蟲
        r1 = requests.get(url, headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "uid=lo_arpU8KehP3fO; sid=1:LGJb8oPE72KIJ7hdf+swxMXZxvvYQpHF1saGJsNjrmSPdMCLa/sYCukY/SeCchzm; optimizelyEndUserId=lo_arpU8KehP3fO; _parsely_visitor={%22id%22:%22pid=f63aa53ec82176ccf0309f3d4cd288da%22%2C%22session_count%22:2%2C%22last_session_ts%22:1600148332800}; _ga=GA1.2.847571216.1589363261; __cfduid=d52b47f2304c41177d5973d7ec2cdba0d1600148331; __cfruid=8b3adde1b50f50090bc94252d42505fb260e249e-1600149745; _parsely_session={%22sid%22:2%2C%22surl%22:%22https://medium.com/search?q=%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E6%2585%25A7%22%2C%22sref%22:%22%22%2C%22sts%22:1600148332800%2C%22slts%22:1589363260250}; lightstep_guid/medium-web=a9e36a691f432073; lightstep_session_id=3ec514a362bcc40d; sz=1519; pr=1.25; tz=-480; _gid=GA1.2.800486480.1600148334; lightstep_guid/lite-web=02f362751b148f39; _gat=1",
            "Host": "medium.com",
            "TE": "Trailers",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0",
        })
        # 取文章內容跟大標
        soup = bs(r1.text, "html.parser")
        post1 = soup.find_all(["p", "h1"])
        text_r = ""
        # 排除最後的贅字
        for m in post1:
            if m.text != "Written by":
                text_r = text_r + "".join(m.text)
        if "的" not in text_r:
            continue
        # 載入停用詞stop words.txt
        jieba.analyse.set_stop_words("./extra_dict/stop_words.txt")
        # 結巴抽取關鍵字
        keywords = jieba.analyse.extract_tags(text_r, topK=5)
        # print(keywords)
        # 關鍵字存進資料庫，在最下面主程式部分

        # 取文章標題圖片 url
        image_url = n.find_all("img", class_="progressiveMedia-image")
        # 沒有圖片 url 就沒有這一段
        if image_url != []:
            image_url = image_url[0].get("data-src")
            if image_url[-5:-1] == ".jpe":
                image_url = image_url
            elif image_url[-4:-1] == ".pn":
                image_url = image_url
            elif image_url[-4:-1] == ".gi":
                image_url = image_url
            elif "https://cdn-images-1.medium.com/fit" in image_url:
                image_url = image_url
            else:
                image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/450px-No_image_available.svg.png"
        else:
            image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/450px-No_image_available.svg.png"

        # 取討論數
        aclass = n.find_all("a", class_="button")
        # 沒有討論就沒有這一段
        try:
            discussion = aclass[1].text
            discussion = discussion.replace(" response", "")
            discussion = int(discussion)
        except:
            discussion = -1

        article = [id, time, title, author, likes, url, image_url, discussion, keywords]
        # 將搜尋結果輸入表格
        articles_list.append(article)

    return articles_list
    # print(table)


# main program
# 這是主程式，定義 search_list 查詢列表 search_key 列表裡要查的字 search_count = 查的總筆數
search_list = ["框架", ]
search_key = 0
search_count = 0

# 輸入關鍵字開始搜尋，20是測試數字
while search_count != 20:
    articles_list = Crawler(search_list[search_key], 10)

    # 關鍵字 list + 1 準備搜下一個
    search_key = search_key + 1

    # 將搜到的 10 筆輸入資料庫
    for n in range(10):
        id = articles_list[n][0]
        data = DB.IntputFindCmd(f"SELECT * FROM main WHERE medium_id = '{articles_list[n][0]}'")
        # 如果回傳空 List 代表文章沒存進去過，才會做存入
        if data == []:
            TitleList = ["medium_id", "title", "author", "pub_date", "likes", "comment", "content_url", "image_url"]
            ContentList = [articles_list[n][0], articles_list[n][2], articles_list[n][3], articles_list[n][1],
                           str(articles_list[n][4]), str(articles_list[n][7]), articles_list[n][5], articles_list[n][6]]
            DB.Insert("main", TitleList, ContentList)
            print(ContentList)

            # keywords存入mainDB的hashtag_set
            keywords = articles_list[n][8]
            print("keywords = ", keywords)
            # hashtag_set_list = DB.IntputFindCmd(f"SELECT hashtag_set FROM main WHERE medium_id = '{articles_list[n][0]}'")
            # print(hashtag_set_list)
            TitleList_h = ["hashtag_set", ]
            ValueList_h = ""
            for h in range(len(keywords)):
                if h + 1 < len(keywords):
                    ValueList_h += keywords[h] + ","
                else:
                    ValueList_h += keywords[h]
            ValueList_h = [ValueList_h]
            DB.Edit("main", TitleList_h, ValueList_h, "medium_id = " + f"'{articles_list[n][0]}'")
            # 將關鍵字存入hashtags資料庫
            if len(keywords) == 0:
                continue
            for k in keywords:
                data = DB.IntputFindCmd(f"SELECT * FROM hashtags WHERE hashtag_name = '{k}'")
                # 如果回傳空 List 代表hashtag沒存進去過，才會做存入
                if data == []:
                    TitleList = ["hashtag_name", "usage_count"]
                    ContentList = [k, "1"]
                    DB.Insert("hashtags", TitleList, ContentList)
                    print(ContentList)
                else:
                    TitleList = ["usage_count", ]
                    # count = 取出該列對應usage_count欄位的數值
                    count = DB.IntputFindCmd(f"SELECT usage_count FROM hashtags WHERE hashtag_name = '{k}'")
                    count = str(count[0][0] + 1)
                    ValueList = [count, ]
                    print(k)
                    DB.Edit("hashtags", TitleList, ValueList, "hashtag_name = " + f"'{k}'")
                # 將所有關鍵字判斷是否在主程式查詢列表中，若無則存入
                if k not in search_list:
                    search_list.append(k)
                else:
                    pass
        else:
            pass
print(search_list)
