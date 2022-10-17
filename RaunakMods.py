import requests
import os
import telebot
import requests
import json
import os
import time
import base64
import re

bot = telebot.TeleBot("5782722535:AAEUKkjSV-BIcbfdxC0rgKnK52OTOUxAaBU", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, """Hehe Boi, Send me a Instagram Link
	""")
def getReq(url):
    hrd = {
        "COOKIE": 'ig_nrcb=1; ig_did=BFD3E742-E921-4EE5-8EF5-1A865D64922A; mid=Y0uSPAABAAHOWWylRL98Gp6FEZJh; csrftoken=ENAzqO2gTJNrDzo17facUssoj1WB7AgZ; sessionid=45532886071:39WELrqwXx5AHC:2:AYd8-v62J1F_NR7Lavj-Oih2WSyxHs1vE0pKmwvmpA; ds_user_id=45532886071; shbid="5501\05445532886071\0541697433693:01f7156350a98ceece12122fc8146c37960667af6c599deb20dab672aebe287ce4d0c3e1"; shbts="1665897693\05445532886071\0541697433693:01f7a79b33ef0dce5dd44c2e95b4207125c55b21ddf2403c5b0fb206d249a753fcd88319"; dpr=1.2375000715255737; datr=3pRLY9NehSXz8U203i7DitvT; rur="EAG\05445532886071\0541697458486:01f7741b56974e76659baca1bd42dc2430dc1dbd4b3bc4bed47e261fd64a3071465e9f64"',
        }
    ret =  requests.get(url, headers=hrd)
    return ret
    
def base64En(json):
     sample_string_bytes = json.encode("ascii")
   	 base64_bytes = base64.b64encode(sample_string_bytes)
     base64_string = base64_bytes.decode("ascii") 
     return base64_string   
     
     
def getUrl(text):
    if "https://" in text:
        getAfterHttps = text.split("https://", 1)[1]
        getUrl = "https://"+ getAfterHttps.split(" ", 1)[0]
        return getUrl
    elif "http://" in text:
        getAfterHttp = text.split("http://", 1)[1]
        getUrl = "http://"+ getAfterHttp.split(" ", 1)[0]
        return getUrl
    else:
        return "nourl"
        
def sendPosts(chat, ata):
  data = json.loads(str(ata))
  items = data.get("items")
  for item in items:
    media_type = item.get("media_type")
    if media_type == 2:
        link = item.get("video_versions")[0]["url"]
        print(link)
        bot.send_message(chat, getReq("https://nepmods.xyz/add.php?url="+base64En(link)))
        bot.send_video(chat, getReq(link).content, supports_streaming=False, timeout=100000)
    else:
        carousel_media = item.get("carousel_media", 0)
        if carousel_media != 0:
          for media in carousel_media:
            image = media.get("image_versions2").get("candidates")[0]
            link = image.get("url")
            bot.send_photo(chat, getReq(link).content)
        else:
            image = item.get("image_versions2").get("candidates")[0]
            link = image.get("url")
            bot.send_photo(chat, getReq(link).content)
            
def sendStory(chat, ata):
  data = json.loads(str(ata))
  reels_media = data.get("data").get("reels_media")
  for reel_media in reels_media:
    items = reel_media.get("items")
    for story in item:
      isVideo = story.get("is_video")
      if(isVideo): 
        videoRes = story.get("video_resources")
        for video in videoRes:
            link = video.get("src")
            bot.send_message(chat, getReq("https://nepmods.xyz/add.php?url="+base64En(link)))
            bot.send_video(chat, getReq(link).content, supports_streaming=False, timeout=100000)
      else:
        link = story.get("display_url")
        bot.send_photo(chat, getReq(link).content)
    
    
def getKey(url, chat):
    l = url.split("/")
    h = ""
    for x in l:
      if "?" in x:
       print(x)    
      else:
         g = x + "/"
         h += g
   
    key = ""
    ret = ""
    if "/p/" in h:
        key = h.split("/p/")[1].replace("/", "")
        url = "https://www.instagram.com/p/"+key+"/?__a=1&__d=dis"
        ret = getReq(url).text
    elif "/reel/" in h:
        key = h.split("/reel/")[1].replace("/", "")
        url = "https://www.instagram.com/p/"+key+"/?__a=1&__d=dis"
        print(url)
        ret =  getReq(url).text
    else:
        key = h.split("https://www.instagram.com/")[1].replace("/", "")
        getId = "https://www.instagram.com/"+key+"/?__a=1&__d=dis"
        id = json.loads(getReq(getId).text)["graphql"]["user"]["id"]
        
        url = "https://www.instagram.com/graphql/query/?query_hash=de8017ee0a7c9c45ec4260733d81ea31&variables=%7B%22reel_ids%22%3A%5B"+str(id)+"%5D%2C%22tag_names%22%3A%5B%5D%2C%22location_ids%22%3A%5B%5D%2C%22highlight_reel_ids%22%3A%5B%5D%2C%22precomposed_overlay%22%3Afalse%2C%22show_story_viewer_list%22%3Atrue%2C%22story_viewer_fetch_count%22%3A50%2C%22story_viewer_cursor%22%3A%22%22%7D"
       
        ret =  getReq(url).text
    return ret
       

    
def getType(data):
    open("data.json", "w").write(data)
    d = json.loads(data)
    try:
        return d["items"][0]["media_type"]
    except:
        return d["data"]["reels_media"][0]["__typename"]
    
    
@bot.message_handler(func = lambda message : True)
def echo_all(message):
    if "www.instagram.com/" in message.text:
        link = getUrl(message.text)
        
        data = getKey(link, message.chat.id)
        type = getType(data)
        print(type)
        if type == "GraphReel":
            r = getReq(json.loads(data)["data"]["reels_media"][0]["owner"]["profile_pic_url"])
            bot.send_photo(message.chat.id, r.content)
            bot.send_message(message.chat.id, "Sending Stories")
            sendStory(message.chat.id, data)
        else:
            #bot.send_message(message.chat.id, "Sending Posts")
            sendPosts(message.chat.id, data)
            

bot.infinity_polling()
