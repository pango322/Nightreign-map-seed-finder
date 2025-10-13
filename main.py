import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import time
import maps_databases

root = ctk.CTk()
root.geometry("1200x1200+100+100")
map_size=(1000,1000)
icon_size=(1,1)

placeholder = ImageTk.PhotoImage(Image.open("assets/placeholder.png").resize((int(74*icon_size[0]), int(74*icon_size[1]))))
ruins =        ImageTk.PhotoImage(Image.open("assets/ruins.png").resize((int(108*icon_size[0]), int(57*icon_size[1]))))
fort =         ImageTk.PhotoImage(Image.open("assets/Fort.png").resize((int(80*icon_size[0]), int(64*icon_size[1]))))
camp =         ImageTk.PhotoImage(Image.open("assets/camp.png").resize((int(106*icon_size[0]), int(64*icon_size[1]))))
great_church = ImageTk.PhotoImage(Image.open("assets/Great_Church.png").resize((int(73*icon_size[0]), int(64*icon_size[1]))))
city =         ImageTk.PhotoImage(Image.open("assets/city.png").resize(map_size))
crater =       ImageTk.PhotoImage(Image.open("assets/crater.png").resize(map_size))
mountain =     ImageTk.PhotoImage(Image.open("assets/mountain.png").resize(map_size))
normal =       ImageTk.PhotoImage(Image.open("assets/normal.png").resize(map_size))
swamp =        ImageTk.PhotoImage(Image.open("assets/swamp.png").resize(map_size))


name_to_img = {
    "placeholder": placeholder,
    "ruins": ruins,
    "fort": fort,
    "camp": camp,
    "great_church": great_church,
}

Affinities = [
    "none",
    "fire",
    "lightning",
    "holy",
    "bleed",
    "frostbite",
    "poison",
    "magic",
    "frenzy",
    "death",
    "sleep",
]
aff_to_img = {}
for a in Affinities:
    if a != "none":
        aff_to_img[a] = ImageTk.PhotoImage(Image.open(f"assets/aff/{a}.png").resize((32,32)))
        #tk.Label(root, image=aff_to_img[a]).pack()
#clean easy to read no embeded for loop

bosses = ["Tricephalos","Gaping jaw","Sentient pest","Augur","Equilibrious beast","Darkdrift knight","Fissure in the fog","Night aspect"]
boss_to_img = {}
for b in bosses:
    boss_to_img[b] = ImageTk.PhotoImage(Image.open(f"assets/{b}.png"))

class Icon:
    def __init__(self, x, y, img, aff = "none"):
        self.x = x
        self.y = y

        self.img = img
        self.aff = aff
    def changeaff(self, aff):
        self.aff = aff
        drawall()
    def changeimg(self, img):
        self.img = img
        drawall()

normal_spots = [
    (0.23, 0.28, placeholder), (0.69, 0.23, placeholder), (0.28, 0.45, placeholder), (0.31, 0.56, placeholder),
    (0.27, 0.67, placeholder), (0.77, 0.43, placeholder), (0.63, 0.59, placeholder), (0.74, 0.64, placeholder),
    (0.61, 0.68, placeholder), (0.74, 0.75, placeholder), (0.39, 0.78, placeholder), (0.63, 0.29, placeholder),
    (0.58, 0.42, placeholder), (0.41, 0.31, placeholder), (0.40, 0.19, placeholder), (0.63, 0.48, placeholder)
]
mountain_spots = [
    (0.69, 0.23, placeholder), (0.21, 0.46, placeholder), (0.31, 0.56, placeholder),
    (0.27, 0.67, placeholder), (0.77, 0.43, placeholder), (0.63, 0.59, placeholder), (0.74, 0.64, placeholder),
    (0.61, 0.68, placeholder), (0.74, 0.75, placeholder), (0.39, 0.78, placeholder), (0.63, 0.29, placeholder),
    (0.58, 0.42, placeholder), (0.65, 0.48, placeholder)
]
crater_spots = [
    (0.23, 0.28, placeholder), (0.69, 0.23, placeholder), (0.28, 0.45, placeholder), (0.31, 0.56, placeholder),
    (0.27, 0.67, placeholder), (0.77, 0.43, placeholder), (0.63, 0.59, placeholder), (0.74, 0.64, placeholder),
    (0.61, 0.68, placeholder), (0.74, 0.75, placeholder), (0.39, 0.78, placeholder)
]
swamp_spots = [
    (0.23, 0.28, placeholder), (0.69, 0.23, placeholder), (0.28, 0.45, placeholder), (0.31, 0.56, placeholder),
    (0.27, 0.67, placeholder), (0.77, 0.43, placeholder), (0.74, 0.75, fort), (0.39, 0.78, placeholder),
    (0.64, 0.29, placeholder), (0.58, 0.42, placeholder), (0.41, 0.31, placeholder), (0.40, 0.19, placeholder),
    (0.65, 0.47, placeholder)
]
city_spots = [
    (0.23, 0.28, placeholder), (0.69, 0.23, placeholder), (0.28, 0.45, placeholder), (0.77, 0.43, placeholder),
    (0.63, 0.59, placeholder), (0.74, 0.64, placeholder), (0.61, 0.68, placeholder), (0.74, 0.75, placeholder),
    (0.63, 0.29, placeholder), (0.58, 0.42, placeholder), (0.41, 0.31, placeholder), (0.40, 0.19, placeholder),
    (0.65, 0.47, placeholder)
]
normal_icons = []
for a in normal_spots:
    normal_icons.append(Icon(a[0], a[1], a[2])) #initialize the icons position before anything just so we have it ready
mountain_icons = []
for a in mountain_spots:
    mountain_icons.append(Icon(a[0], a[1], a[2])) #initialize the icons position before anything just so we have it ready
crater_icons = []
for a in crater_spots:
    crater_icons.append(Icon(a[0], a[1], a[2])) #initialize the icons position before anything just so we have it ready
swamp_icons = []
for a in swamp_spots:
    swamp_icons.append(Icon(a[0], a[1], a[2])) #initialize the icons position before anything just so we have it ready
city_icons = []
for a in city_spots:
    city_icons.append(Icon(a[0], a[1], a[2])) #initialize the icons position before anything just so we have it ready

canvas = tk.Canvas(root, width=map_size[0], height=map_size[1], bd = 0, highlightthickness = 2, bg = root.cget("background"))
def drawall():
    global active_map, current_icons, current_boss
    map = active_map
    icons = current_icons
    canvas.delete("all")
    canvas.create_image(map_size[0]/2, map_size[1]/2, image=map)
    for i in icons:
        base = canvas.create_image(i.x*map_size[0], i.y*map_size[1], image=i.img)
        if i.aff != 'none':
            canvas.create_image(i.x * map_size[0] + 32, i.y * map_size[1] + 32, image=aff_to_img[i.aff])
        canvas.tag_bind(base, "<Button-1>", lambda e, icon=i: openOptions(icon))

    canvas.create_image(100, 900, image=boss_to_img[current_boss])

def openOptions(icon):
    optionWindow = tk.Toplevel(root)
    optionWindow.attributes("-topmost", True)
    x, y = root.winfo_pointerx(), root.winfo_pointery()
    optionWindow.geometry(f"+{x-10}+{y-10}")
    optionWindow.overrideredirect(True),
    optionWindow.focus_force()
    optionWindow.bind("<FocusOut>", lambda e: (checksimilar(),optionWindow.destroy()))
    optionWindow.bind("<Escape>", lambda e: (checksimilar(), optionWindow.destroy()))

    #now we can move on to populating the optionwindow
    firstRow = ctk.CTkFrame(optionWindow, fg_color="transparent", bg_color="transparent")
    firstRow.pack(side="top", pady=10)
    for img in (camp, fort, ruins, great_church):
        ctk.CTkButton(firstRow, image=img, text='', command=lambda i=img: (icon.changeimg(i))).pack(side="left", padx=10)

    secondRow = firstRow = ctk.CTkFrame(optionWindow, fg_color="transparent", bg_color="transparent")
    firstRow.pack(side="top")

    for aff in (Affinities):
        if aff != "none":
            ctk.CTkButton(secondRow, text="", image=aff_to_img[aff], width=32,height=32, command= lambda a=aff: (icon.changeaff(a), checksimilar(), optionWindow.destroy())).pack(side="left", padx=1)
        else:
            ctk.CTkButton(secondRow, text="none", width=32,height=32, command= lambda a=aff: (icon.changeaff(a), checksimilar(), optionWindow.destroy())).pack(side="left", padx=1)

def checksimilar():
    image_to_name = {v: k for k, v in name_to_img.items()}
    #image_to_name = {ruins: "ruins", fort: "fort", camp: "camp", great_church: "great_church", placeholder: "placeholder"}

    spot_count = len(current_icons)
    known = {}
    for i in range(spot_count):
        ic = current_icons[i]
        if ic.aff not in placeholder:
            sname = image_to_name.get(ic.img)
            if ic.aff not in known:
                known[i] = (sname, ic.aff)

    matches = []
    for seed_id, data in maps_databases.map_database.items():
        seq = []
        for k, v in data:
            if k == "boss":
                continue
        seq.append((k,v))
        if len(seq) >= spot_count:
            break

    ok = True
    for idx in known:
        if idx >= len(seq):
            ok = False
            break
        ks, kv = seq[idx]
        ks2, kv2 = known[idx]
        if ks != ks2 or kv != kv2:
            ok = False
            break

    if ok:
        matches.append(seed_id)

    if len(matches) == 1:
        print(f"Detected {matches[0]} seeds")
    elif len(matches) == 0:
        print("No matching seed yet.")
    else:
        print(f"your seed is: {matches}")


def checksimilar():
    # Build reverse lookup for structure names from images
    image_to_name = {v: k for k, v in name_to_img.items()}

    # What we currently know (skip placeholders)
    spot_count = len(current_icons)
    known = {}  # idx -> (structure_name, affinity)
    for idx, ic in enumerate(current_icons):
        if ic.img is placeholder:
            continue
        sname = image_to_name.get(ic.img)
        if not sname:
            continue
        known[idx] = (sname, ic.aff)

    matches = []
    for seed_id, data in db.items():
        # Build seed's (structure, affinity) sequence for this map length (ignore boss)
        seq = []
        for k, v in data:
            if k == "boss":
                continue
            seq.append((k, v))
            if len(seq) >= spot_count:
                break

        ok = True
        for idx, (sname, aff) in known.items():
            if idx >= len(seq):
                ok = False
                break
            ks, kv = seq[idx]
            if ks != sname or kv != aff:
                ok = False
                break

        if ok:
            matches.append(seed_id)

    if len(matches) == 1:
        print(f"Detected seed: {matches[0]}")
        setseed(matches[0])
    elif len(matches) == 0:
        print("No matching seed yet.")
    else:
        print(f"Candidate seeds: {matches}")

def Set_boss_preset(newboss):
    global current_boss, active_map
    current_boss = newboss
    drawall()
def Set_map_preset(newmap):
    global db
    name_to_map = {"normal": normal, "mountain": mountain, "crater": crater, "swamp": swamp, "city": city}
    name_to_icons = {"normal": normal_icons, "mountain": mountain_icons, "crater": crater_icons, "swamp": swamp_icons, "city": city_icons}
    global current_boss, active_map, current_icons
    active_map = name_to_map[newmap]
    current_icons = name_to_icons[newmap]
    if active_map == normal:
        db = maps_databases.normal_database
    if active_map == crater:
        db = maps_databases.crater_database
    if active_map == swamp:
        db = maps_databases.swamp_database
    if active_map == city:
        db = maps_databases.city_database
    if active_map == mountain:
        db = maps_databases.mountain_database

    drawall()

seed =  ctk.StringVar(value="000")
def setseed(n):
    global seed, current_boss, current_icons
    seed.set(n)
    current_boss, current_icons = datatoicons(n)
    drawall()

def seedselectionbox():
    t1 = ctk.CTkToplevel(root)
    t1.geometry("+100+100")
    t1.attributes("-topmost", True)
    t1.focus_force()
    scroll_frame = ctk.CTkScrollableFrame(t1, width=120, height=500)
    for num in [f"{i:03}" for i in range(320)]:
        ctk.CTkButton(scroll_frame, text=num, command=lambda n=num: setseed(n)).pack(pady=2)
    scroll_frame.pack(side="top", fill="x")


def giveData(seed, current_boss, current_icons):
    datasheet = ctk.CTkToplevel(root)
    datasheet.attributes("-topmost", True)
    datasheet.focus_force()
    datasheet.geometry(f"{map_size[0]/2}x{map_size[1]/2}")
    textboxtext = transcribedata()
    label = ctk.CTkTextbox(datasheet, width=map_size[0]/2, height=map_size[1]/2)
    print(textboxtext, end="")
    label.insert("0.0",text=textboxtext)
    label.pack(side="top", padx=10)

def transcribedata():
    image_to_name = {ruins: "ruins", fort: "fort", camp: "camp", great_church: "great_church", placeholder: "placeholder"}
    transcript = f"\t\"{seed.get()}\": [\n\t\t(\"boss\",\"{current_boss}\"),\n"
    for i in current_icons:
        transcript = transcript + (f"\t\t(\"{image_to_name.get(i.img)}\",\"{i.aff}\"),\n")
    transcript = transcript + (f"\t],\n")
    return transcript

def datatoicons(seed_str):
    data = db[seed_str]
    if not data:
        return None, [] #in the event its not documented
    boss_name = ""
    for k, v in data:
        if k == "boss":
            boss_name = v
            break

    if active_map is mountain:
        spots = mountain_spots
    elif active_map is crater:
        spots = crater_spots
    elif active_map is swamp:
        spots = swamp_spots
    elif active_map is city:
        spots = city_spots
    else:
        spots = normal_spots

    icons = []
    s = 0
    for k, v in data:
        if k == "boss":
            continue
        if s >= len(spots):
            break
        x, y, _ = spots[s]
        img = name_to_img.get(k, placeholder)
        aff = v if v in Affinities else "none"
        icons.append(Icon(x, y, img, aff))
        s += 1

    return boss_name, icons

active_map = normal
db = maps_databases.normal_database

current_boss = bosses[0]
current_icons = normal_icons
drawall()

boss_selection = ctk.CTkComboBox(root, values=bosses, command=Set_boss_preset)
map_selection = ctk.CTkComboBox(root, values=["normal", "crater", "mountain", "swamp", "city"], command=Set_map_preset)
dataButton = ctk.CTkButton(root, text="give Data", command=lambda: giveData(seed, current_boss, current_icons))

setseedbutton = ctk.CTkButton(root, text="Seed Selection", command=seedselectionbox)
map_selection.pack()
ctk.CTkLabel(root, textvariable=seed).pack()
boss_selection.pack(side="top", padx=10, pady=10)
canvas.pack(padx=5, pady=5)
#dataButton.pack(padx=5, pady=5)
#setseedbutton.pack(padx=5, pady=5)
root.mainloop()

