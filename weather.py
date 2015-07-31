import json,urllib2,io,os,sys
import config

from PIL import Image,ImageDraw,ImageFont

if not config.key:
        print "Hey, you didn't put in a Wunderground API key! We need that to run! Edit config.py accordingly :)"
        print "http://www.wunderground.com/weather/api"
        sys.exit()

font = ImageFont.truetype("DejaVuSans.ttf",28) # font to be used, and the size of the font
cityfont = ImageFont.truetype("DejaVuSans.ttf",52) # font to be used, and the size of the font
wfont = ImageFont.truetype("DejaVuSans.ttf",32) #change the font. I want the temps to be easily visble

date = [' ', ' ', ' ', ' ']
high = [0,0,0,0]
low  = [0,0,0,0]
icon = [' ', ' ', ' ', ' ']
 
 
d1dloc = (80,80)
d1hloc = (80,180)       # day 1 high location
d1lloc = (80,212)       # day 1 low location
d2dloc = (209,80)
d2hloc = (209,180)      # day 2 ...
d2lloc = (209,212)
d3dloc = (354,80)
d3hloc = (354,180)      # day 3 ...
d3lloc = (354,212)
 
if config.dir:
	dir = config.dir
else:
	dir = os.path.dirname(os.path.abspath(__file__))

cities = map(str,config.cities)

for city in cities:
        forecasturl=("http://api.wunderground.com/api/"+config.key+"/forecast/q/"+city+".json")
        geourl=("http://api.wunderground.com/api/"+config.key+"/geolookup/q/"+city+".json")
	forecastdata = json.load(urllib2.urlopen(forecasturl))
	geodata = json.load(urllib2.urlopen(geourl))

	cityname = geodata["location"]["city"]

        im = Image.new("RGB", (config.width,config.height), "black")
        draw = ImageDraw.Draw(im)
        w,h = draw.textsize(cityname,cityfont)
        draw.text(((config.width/2)-(w/2),10),cityname,(255,255,255),font=cityfont)
 
 
        i = 1
        for index,day in enumerate(forecastdata["forecast"]["simpleforecast"]["forecastday"]):
                if i <= 3:
                        date[index] = day["date"]["weekday_short"]
                        high[index] = day["high"]["fahrenheit"]
                        low[index]  = day["low"]["fahrenheit"]
                        icon[index] = str(day["icon_url"])
                        iconloc     = [(80,120),(209,120),(354,120),(500,500)]
                        icond       = urllib2.urlopen(icon[index])
                        icone       = io.BytesIO(icond.read())
                        iconimg     = Image.open(icone)
                        im.paste(iconimg,iconloc[index],iconimg.convert('RGBA'))
                i = i + 1
 
        draw.text(d1dloc,str(date[0]),(255,255,255),font=font)
        draw.text(d2dloc,str(date[1]),(255,255,255),font=font)
        draw.text(d3dloc,str(date[2]),(255,255,255),font=font)
        draw.text(d1hloc,str(high[0]),config.hcolor,font=wfont)        # draw the day 1 high
        draw.text(d2hloc,str(high[1]),config.hcolor,font=wfont)        # day 2 high
        draw.text(d3hloc,str(high[2]),config.hcolor,font=wfont)        # day 3 high
        draw.text(d1lloc,str(low[0]),config.lcolor,font=wfont)         # day 1 low
        draw.text(d2lloc,str(low[1]),config.lcolor,font=wfont)         # day 2 low
        draw.text(d3lloc,str(low[2]),config.lcolor,font=wfont)         # day 3 low
        filename = dir + "//" + cityname.replace(' ','') + ".png"
 
        im.save(filename,"png")
        print filename
