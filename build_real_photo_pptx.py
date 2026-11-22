from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN,MSO_ANCHOR
from PIL import Image,ImageOps
from io import BytesIO
import os,json,qrcode

BASE="https://bakhtygulhab.github.io/adebi-astana/"
routes=[
{"name":"ҚАЛАМГЕРЛЕР ЖОЛЫ","color":"1556C5","titles":["С. Сейфуллин мұражайы","С. Сейфуллин ескерткіші","«Үш би»","Жаяу Мұса","Абай","«Үш арыс»","Алаш қайраткерлері"],"paths":["01.html","02.html","03.html","04.html","05.html","06.html","07.html"]},
{"name":"АҚЫНДАР МЕН АҒАРТУШЫЛАР","color":"007D69","titles":["Пушкин","Жамбыл","Б. Момышұлы","әл-Фараби","«Жерұйық» саябағы","Ы. Алтынсарин"],"paths":["r2-01.html","r2-02.html","r2-03.html","r2-04.html","r2-05.html","r2-06.html"]},
{"name":"АҢЫЗДАН МОНУМЕНТКЕ","color":"D56C0A","titles":["«Қазақ елі»","«Бәйтерек»","Алпамыс батыр","Құрманғазы"],"paths":["r3-01.html","r3-02.html","r3-03.html","r3-04.html"]}
]
prs=Presentation();prs.slide_width=Inches(13.333);prs.slide_height=Inches(7.5)
S=MSO_SHAPE
def color(h):return RGBColor.from_string(h)
def box(slide,x,y,w,h,fill,round=False,stroke=None):
 shp=slide.shapes.add_shape(S.ROUNDED_RECTANGLE if round else S.RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h))
 shp.fill.solid();shp.fill.fore_color.rgb=color(fill)
 shp.line.fill.background() if not stroke else None
 if stroke:shp.line.color.rgb=color(stroke)
 return shp
def text(slide,txt,x,y,w,h,size,ink,bold=False,align=None):
 shape=slide.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
 tf=shape.text_frame;tf.word_wrap=True;tf.margin_left=Inches(.02);tf.margin_right=Inches(.02);tf.margin_top=Inches(.02);tf.margin_bottom=0
 p=tf.paragraphs[0];p.text=txt;p.font.name="Arial";p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=color(ink)
 if align:p.alignment=align
 return shape
def picture(slide,filename,x,y,w,h,url):
 im=Image.open(filename).convert("RGB")
 wide=int(w*150);high=int(h*150)
 fit=ImageOps.contain(im,(wide,high),method=Image.Resampling.LANCZOS)
 bg=Image.new("RGB",(wide,high),(234,242,248));bg.paste(fit,((wide-fit.width)//2,(high-fit.height)//2))
 b=BytesIO();bg.save(b,"JPEG",quality=86);b.seek(0)
 pic=slide.shapes.add_picture(b,Inches(x),Inches(y),Inches(w),Inches(h));pic.click_action.hyperlink.address=url
def qr(slide,url,x,y,size):
 code=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,box_size=6,border=2);code.add_data(url);code.make(fit=True)
 b=BytesIO();code.make_image(fill_color="#0b255b",back_color="white").convert("RGB").save(b,"PNG");b.seek(0)
 image=slide.shapes.add_picture(b,Inches(x),Inches(y),Inches(size),Inches(size));image.click_action.hyperlink.address=url
for ridx,route in enumerate(routes):
 ri=ridx+1;sl=prs.slides.add_slide(prs.slide_layouts[6]);sl.background.fill.solid();sl.background.fill.fore_color.rgb=color("F2F6FC")
 box(sl,0,0,13.333,1.48,"0B255B");box(sl,0,1.48,13.333,.07,route["color"])
 text(sl,"ӘДЕБИ АСТАНА  •  3 ЭКСКУРСИЯ БАҒЫТЫ",.45,.20,11,.33,12.6,"C8DAFA",True)
 text(sl,str(ri)+"-БАҒЫТ  «"+route["name"]+"»",.45,.65,12.5,.65,28 if ri!=2 else 25,"FFFFFF",True)
 text(sl,str(len(route["titles"]))+" аялдама   •   ҚАЗ / РУС / ENG   •   QR-код арқылы тиісті веб-парақты ашыңыз",.47,1.68,12,.36,12.5,"48617F")
 rows=([list(range(4)),list(range(4,7))] if ri==1 else [list(range(3)),list(range(3,6))] if ri==2 else [[0,1],[2,3]])
 for rn,indices in enumerate(rows):
  width=(3.10 if ri==1 and rn==0 else 3.77 if ri==1 else 3.95 if ri==2 else 5.18)
  gap=.16 if ri==1 else .26 if ri==2 else .34
  h=2.12 if ri<3 else 2.13
  top=2.22+rn*(h+.24)
  xx=(13.333-len(indices)*width-(len(indices)-1)*gap)/2
  for col,j in enumerate(indices):
   x=xx+col*(width+gap);url=BASE+route["paths"][j]
   box(sl,x,top,width,h,"FFFFFF",True,"D8E3F1")
   box(sl,x+.17,top+.18,.45,.44,route["color"],True)
   text(sl,str(j+1),x+.18,top+.21,.42,.32,16,"FFFFFF",True,PP_ALIGN.CENTER)
   text(sl,route["titles"][j],x+.74,top+.13,width-.89,.61,15 if ri!=1 else 13.3,"0B255B",True)
   qsize=1.02 if ri<3 else 1.12
   px=x+.17;py=top+.82;qx=x+width-qsize-.16;pw=qx-px-.14;ph=1.12
   imagepath=("stop-"+str(j+1).zfill(2)+".jpg") if ri==1 else ("photos/r"+str(ri)+"-"+str(j+1).zfill(2)+".jpg")
   if not os.path.isfile(imagepath):raise FileNotFoundError(imagepath)
   picture(sl,imagepath,px,py,pw,ph,url);qr(sl,url,qx,py,qsize)
 note="Нақты фотосуреттер қолданылды. Фото дереккөздері: PHOTO_SOURCES.md (GitHub жобасында)."
 text(sl,note,.45,6.88,12.4,.24,10.5,"586F90")
 text(sl,"Сайт: "+BASE+"   •   Фото мен QR-кодқа басуға болады   •   PPTX элементтері өңделеді",.45,7.16,12.4,.2,9.4,"8998AB")
os.makedirs("presentations",exist_ok=True)
prs.save("presentations/Adebi_Astana_3_bagyt_real_photos_QR.pptx")
print("PRESENTATION SAVED: 3 slides, 17 linked QR codes")
