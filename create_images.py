from PIL import Image, ImageDraw
import os

def create_cat_image(filename, mood="idle", size=128):
    """draw een cute virtuele kat :3"""
    big_canvas = 500
    img = Image.new("RGBA", (big_canvas, big_canvas), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    #basis colors
    fur = "#E6C29F"
    inner_ear = "#F0DBC5"
    outline = "#5D4037"
    eye_black = "#2D2D2D"
    nose = "#FF9999"
    blush = "#FFCCCC"

    #mood aanpassingen
    if mood == "dirty":
        fur = "#BFA588"
    elif mood == "sad":
        fur = "#D1C4E9"
    elif mood == "tired":
        fur = "#C4B5A9"
    elif mood == "happy":
        fur = "#FFD8A8"

    #helper function
    def rect(x, y, w, h):
        return [x - w/2, y - h/2, x + w/2, y + h/2]

    #cat body 
    draw.arc([300, 250, 450, 400], start=0, end=160, fill=fur, width=45)

    draw.ellipse(rect(250, 380, 220, 160), fill=fur, outline=outline, width=5)

    draw.polygon([(140,180),(170,80),(240,150)], fill=fur, outline=outline)
    draw.polygon([(160,170),(175,100),(220,150)], fill=inner_ear)
    draw.polygon([(360,180),(330,80),(260,150)], fill=fur, outline=outline)
    draw.polygon([(340,170),(325,100),(280,150)], fill=inner_ear)

    draw.ellipse(rect(250,220,320,260), fill=fur, outline=outline, width=5)

    eye_y = 230
    left_eye_x, right_eye_x = 180, 320
    eye_size = 35

    if mood == "tired":
        draw.line([left_eye_x-20, eye_y, left_eye_x+20, eye_y], fill=outline, width=5)
        draw.line([right_eye_x-20, eye_y, right_eye_x+20, eye_y], fill=outline, width=5)
    elif mood == "happy":
        draw.arc(rect(left_eye_x, eye_y+10, 50, 50), start=180, end=0, fill=outline, width=5)
        draw.arc(rect(right_eye_x, eye_y+10, 50, 50), start=180, end=0, fill=outline, width=5)
    else:
        draw.ellipse(rect(left_eye_x, eye_y, eye_size*2, eye_size*2), fill=eye_black)
        draw.ellipse(rect(right_eye_x, eye_y, eye_size*2, eye_size*2), fill=eye_black)
        draw.ellipse(rect(left_eye_x-10, eye_y-10, 15, 15), fill="white")
        draw.ellipse(rect(right_eye_x-10, eye_y-10, 15, 15), fill="white")

    #blush
    if mood != "dirty":
        draw.ellipse(rect(140,260,40,20), fill=blush)
        draw.ellipse(rect(360,260,40,20), fill=blush)

    #nose
    draw.polygon([(240,260),(260,260),(250,275)], fill=nose)

    #mouth
    mouth_y = 275
    if mood == "sad":
        draw.arc(rect(250, mouth_y+10, 40, 20), start=180, end=0, fill=outline, width=4)
    elif mood == "happy":
        draw.chord(rect(250, mouth_y, 40, 40), start=0, end=180, fill="#663333")
    else:
        draw.arc(rect(235, mouth_y, 30, 20), start=0, end=180, fill=outline, width=4)
        draw.arc(rect(265, mouth_y, 30, 20), start=0, end=180, fill=outline, width=4)

    #whiskers
    if mood != "tired":
        whisker = "#AA8866"
        for i in range(2):
            off = i*15
            draw.line([120,240+off,160,250+off], fill=whisker, width=3)
            draw.line([380,240+off,340,250+off], fill=whisker, width=3)

    #paws
    draw.ellipse(rect(210,440,50,40), fill="white", outline=outline, width=4)
    draw.ellipse(rect(290,440,50,40), fill="white", outline=outline, width=4)

    #effect depending on mood
    if mood == "dirty":
        draw.ellipse(rect(200,200,30,30), fill="#8D6E63")
        draw.ellipse(rect(300,350,40,40), fill="#8D6E63")
        draw.ellipse(rect(180,320,25,25), fill="#8D6E63")
    elif mood == "sad":
        draw.ellipse(rect(170,260,10,20), fill="#81D4FA")
        draw.ellipse(rect(330,260,10,20), fill="#81D4FA")
    elif mood == "tired":
        zzz_x, zzz_y = 400, 180
        draw.line([zzz_x,zzz_y,zzz_x+25,zzz_y], fill=outline, width=4)
        draw.line([zzz_x+25,zzz_y,zzz_x,zzz_y+15], fill=outline, width=4)
        draw.line([zzz_x,zzz_y+15,zzz_x+25,zzz_y+15], fill=outline, width=4)
        draw.line([zzz_x+5,zzz_y+20,zzz_x+30,zzz_y+20], fill=outline, width=3)
        draw.line([zzz_x+30,zzz_y+20,zzz_x+5,zzz_y+35], fill=outline, width=3)
        draw.line([zzz_x+5,zzz_y+35,zzz_x+30,zzz_y+35], fill=outline, width=3)
        draw.line([zzz_x+10,zzz_y+40,zzz_x+35,zzz_y+40], fill=outline, width=2)
        draw.line([zzz_x+35,zzz_y+40,zzz_x+10,zzz_y+55], fill=outline, width=2)
        draw.line([zzz_x+10,zzz_y+55,zzz_x+35,zzz_y+55], fill=outline, width=2)

    #schaal naar juiste grootte........
    try:
        final_img = img.resize((size, size), Image.LANCZOS)
    except:
        final_img = img.resize((size, size), Image.ANTIALIAS)

    #save
    img.save(os.path.join("assets/images", filename))
    print(f"Aangemaakt: assets/images/{filename}")


def create_simple_icon(filename, icon_type="food", size=64):
    """maak simpele icoontjes"""
    img = Image.new("RGBA", (size, size), (255,255,255,0))
    draw = ImageDraw.Draw(img)

    cx, cy = size//2, size//2
    bg_r = size//3
    draw.ellipse([cx-bg_r, cy-bg_r, cx+bg_r, cy+bg_r], fill="lightgray", outline="black", width=2)

    if icon_type == "food":
        w, h = size//2, size//4
        draw.ellipse([cx-w//2, cy-h//2, cx+w//2, cy+h//2], fill="orange", outline="black", width=1)
        tail = [(cx+w//2,cy),(cx+w//2+size//6,cy-size//8),(cx+w//2+size//6,cy+size//8)]
        draw.polygon(tail, fill="orange", outline="black", width=1)
        draw.ellipse([cx-w//4, cy-size//16, cx-w//6, cy], fill="black")
    elif icon_type == "play":
        r = size//4
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill="red", outline="black", width=2)
        draw.line([cx,cy-r,cx,cy+r], fill="white", width=2)
        draw.line([cx-r,cx, cx+r,cy], fill="white", width=2)
    elif icon_type == "clean":
        hw, hh = size//3, size//4
        draw.ellipse([cx-hw//2, cy-hh//2, cx+hw//2, cy+hh//2], fill="lightblue", outline="black", width=1)
        tw = size//10
        for i in range(3):
            x = cx-hw//3 + i*tw
            draw.rectangle([x, cy-hh, x+tw//2, cy-hh//2], fill="lightblue", outline="black", width=1)
    elif icon_type == "sleep":
        bed_w, bed_h = size * 0.7, size * 0.4
        kussen_h = bed_h * 0.4
        draw.ellipse([cx - bed_w/2, cy - bed_h/2, cx + bed_w/2, cy + bed_h/2], fill="#FFA07A",outline="brown",width=2)
        draw.ellipse([cx - bed_w/2 + 5, cy - bed_h/2 + 5, cx + bed_w/2 - 5, cy - bed_h/2 + kussen_h],fill="#FFFACD",)
        draw.text((cx - 15, cy - bed_h/2 + 5),"Zzz",fill="blue")

    img.save(os.path.join("assets/images", filename))
    print(f"aangemaakt: assets/images/{filename}")


#maak kat images
create_cat_image("pet_idle.png", "idle")
create_cat_image("pet_happy.png", "happy")
create_cat_image("pet_sad.png", "sad")
create_cat_image("pet_dirty.png", "dirty")
create_cat_image("pet_tired.png", "tired")
create_simple_icon("icon_sleep.png", "sleep")

#maak iconen
create_simple_icon("icon_food.png", "food")
create_simple_icon("icon_play.png", "play")
create_simple_icon("icon_clean.png", "clean")

print("\n" + "="*50)
print("succesvol afbeeldingen aangemaakt")
print("Locatie: assets/images/")
print("="*50)
