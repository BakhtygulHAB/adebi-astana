import json,os,requests,time
from PIL import Image
from io import BytesIO
SOURCES=json.loads(r'''[{"key":"r2-01","url":"https://sputnik.kz/img/1416/86/14168644_181%3A0%3A2912%3A2048_1920x0_80_0_0_1fc370e594e464d1bf694a2c8de86556.jpg"},{"key":"r2-02","url":"https://sputnik.kz/img/07e5/05/08/17000716_0%3A0%3A2996%3A2000_1920x0_80_0_0_d1bc9f22a416e6144b86b1f4adb1cb2c.jpg"},{"key":"r2-03","url":"https://adebiportal.kz/upload/318/2020/04/24/84ba67944f26511f1478818b26aefcfb.jpg"},{"key":"r2-04","url":"https://inbusiness.kz/uploads/49/images/UKrAySJp.jpg"},{"key":"r2-05","url":"https://weproject.media/upload/medialibrary/bd3/bd3e3114be3020622dbfc981e47c43c1.jpg"},{"key":"r2-06","url":"https://informburo.kz/storage/photos/127/615957983fc4a.jpg"},{"key":"r3-01","url":"https://ais.citypass.kz/media/attractions/1-4.jpg"},{"key":"r3-02","url":"https://putidorogi-nn.ru/images/stories/aziya/kazahstan/bayterek_2.jpg"},{"key":"r3-03","url":"https://cf.bstatic.com/xdata/images/hotel/max1024x768/622890574.jpg?k=0a09ecfed900eb2e313629dfcae9622e69a88ebffde1092b48d5c06382d6a398&o="},{"key":"r3-04","url":"https://sputnik.kz/img/old/345/26/3452601_469%3A0%3A1450%3A1080_1920x0_80_0_0_356ddc170d25522ab18c84fff61c1f56.jpg"}]''')
os.makedirs("photos",exist_ok=True)
ok=[];bad=[]
for item in SOURCES:
 key,url=item["key"],item["url"]
 try:
  resp=requests.get(url,timeout=40,headers={"User-Agent":"Mozilla/5.0 (compatible; LiteraryAstana/1.0; photo citation)"})
  resp.raise_for_status()
  im=Image.open(BytesIO(resp.content)).convert("RGB")
  if im.width < 200 or im.height < 180:raise RuntimeError(f"Small image {im.size}")
  im.thumbnail((1500,1200))
  im.save("photos/"+key+".jpg","JPEG",quality=85,optimize=True)
  ok.append(key)
  print("OK",key,im.size,flush=True)
 except Exception as e:
  bad.append([key,str(e)])
  print("ERROR",key,str(e),flush=True)
open("photos/STATUS.json","w").write(json.dumps({"ok":ok,"errors":bad},ensure_ascii=False,indent=2))
