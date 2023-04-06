from PIL import Image, ImageDraw, ImageFont, ImageOps
from Recipes import AllRecipes
import textwrap
import os

def makeTrans(img, RGBA):
    img = img.convert("RGBA")
    pixdata = img.load()
    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == RGBA:
                pixdata[x, y] = (255, 255, 255, 0)

    return img

def newWidth(img, img_new_width):
    img_width, img_height = img.size
    img_new_height = int((img_new_width/img_width)*img_height)
    img_resize = img.resize((img_new_width, img_new_height), Image.NEAREST)

    return img_resize

def centralizeTextInImage(Title, Font, Img, ImgX, ImgY, **kwargs):
    FontWidth, FontHeight = draw.textsize(Title, font = Font)
    ImgWidth, ImgHeight = Img.size
    TextX = int((ImgWidth-FontWidth)/2 + ImgX)
    if 'Yoffset' in kwargs:
        Yoffset = kwargs['Yoffset']
    else:
        Yoffset = 0
    TextY = int((ImgHeight-FontHeight)/2 + ImgY + Yoffset)

    return (TextX, TextY)

def centralizeImageX(PageWidth, Img, **kwargs):
    if 'center' in kwargs:
        centerX = PageWidth * kwargs['center']
        offSet = PageWidth/2 - centerX
    else:
        offSet = 0
    ImgWidth = Img.width
    ImgX = int((PageWidth - ImgWidth)/2 - offSet)

    return ImgX

def replace_str_index(text,index=0,replacement=''):

    return f'{text[:index]}{replacement}{text[index+1:]}'

def wrapText(text, width):
    placeholderText = text.replace('\n\n','\nplaceholder\n')
    wrappedPlaceholderText = '\n'.join(['\n   '.join(textwrap.wrap(line, width, break_long_words=False, replace_whitespace=False))\
        for line in placeholderText.splitlines() if line.strip() != ''])
    wrappedText = wrappedPlaceholderText.replace('\nplaceholder\n', '\n\n')

    return wrappedText

def fillTextBackground(position, text, font, fillColor, margin):
    left, top, right, bottom = draw.textbbox(position, text, font=font)
    draw.rectangle((left-margin, top-margin, right+margin, bottom+margin), fill=fillColor)
    draw.text(position, text, font=font, fill="black")

def fillImageBackground(position, dimensions, fillColor, margin):
    left, top = position
    right, bottom = position[0] + dimensions[0], position[1] + dimensions[1]
    draw.rectangle((left-margin, top-margin, right+margin, bottom+margin), fill=fillColor)

def convert_images_to_pdf(images_folder, pdf_file):
    images = []
    for file in os.listdir(images_folder):
        if file.endswith(".png"):
            image = Image.open(os.path.join(images_folder, file))
            image.load() 
            imageConverted = Image.new("RGB", image.size, (255, 255, 255))
            imageConverted.paste(image, mask=image.split()[3])
            images.append(imageConverted)
    images[0].save(pdf_file, save_all=True, append_images=images[1:])

for pages, Recipe in enumerate(AllRecipes):  
    if pages % 6 == 0:
        colorTheme = (173, 216, 230, 255)
        colorThemeFont = (0, 0, 130, 255)
        colorName = "blue"
        RecipeBoxYCenter = 1550     #Middle
        StarsY = 700                #Top
        PhotoY = 2250               #Bottom
    if pages % 6 == 1:
        colorTheme = (203, 195, 227, 255)
        colorThemeFont = (48, 25, 52, 255)
        colorName = "purple"
        RecipeBoxYCenter = 2750    #Bottom
        StarsY = 1900              #Middle
        PhotoY = 600               #Top
    if pages % 6 == 2:
        colorTheme = (255, 255, 0, 255)
        colorThemeFont = (79, 69, 6, 255)
        colorName = "yellow"
        RecipeBoxYCenter = 1300    #Top
        StarsY = 3300              #Bottom
        PhotoY = 2000              #Middle
    if pages % 6 == 3:
        colorTheme = (173, 216, 230, 255)
        colorThemeFont = (0, 0, 130, 255)
        colorName = "blue"
        RecipeBoxYCenter = 2750    #Bottom
        StarsY = 700               #Top
        PhotoY = 850               #Middle
    if pages % 6 == 4:
        colorTheme = (203, 195, 227, 255)
        colorThemeFont = (48, 25, 52, 255)
        colorName = "purple"
        RecipeBoxYCenter = 2500    #Middle
        StarsY = 3300              #Bottom
        PhotoY = 600               #Top
    if pages % 6 == 5:
        colorTheme = (255, 255, 0, 255)
        colorThemeFont = (79, 69, 6, 255)
        colorName = "yellow"
        RecipeBoxYCenter = 1300    #Top
        StarsY = 2100              #Middle
        PhotoY = 2250               #Bottom
    
    #Instantiate page
    PageWidth, PageHeight = (2480, 3508)
    Page = Image.new("RGBA", (PageWidth, PageHeight), (255, 255, 255))
    draw = ImageDraw.Draw(Page)
    Background = Image.open("layout/kitchen_pattern.jpg")
    Page.paste(Background, (0,0))

    #Add title Ribbon
    BlueRibbon = Image.open(f"layout/ribbon_{colorName}.png")
    TransBlueRibbon = makeTrans(BlueRibbon, (0, 0, 0, 255))
    TransBlueRibbonResize = newWidth(TransBlueRibbon, 2000)
    RibbonX = centralizeImageX(PageWidth, TransBlueRibbonResize)
    RibbonY =  150
    Page.paste(TransBlueRibbonResize, (RibbonX, RibbonY), TransBlueRibbonResize)

    #Add title
    title = Recipe.name
    font_title = ImageFont.truetype("fonts/arial.ttf", 90)
    TitleX, TitleY = centralizeTextInImage(title, font_title, TransBlueRibbonResize, RibbonX, RibbonY, Yoffset = -80)
    draw.text((TitleX, TitleY), title, font = font_title, fill=colorThemeFont)

    #Add recipes
    RecipeList = Recipe.recipes
    NoOfRecipes = len(RecipeList)
    if NoOfRecipes == 1:
        centerIncrementations = [0.5]
        maxTextWidth = 100
    if NoOfRecipes == 2:
        centerIncrementations = [0.25, 0.75]
        maxTextWidth = 65
    if NoOfRecipes == 3:
        centerIncrementations = [0.2, 0.5, 0.8]
        maxTextWidth = 30
    for i, recipe in enumerate(RecipeList):
        font_Recipe = ImageFont.truetype("fonts/arial.ttf", 40)
        RecipeStr = recipe
        RecipeStr = wrapText(RecipeStr, maxTextWidth)

        #Create Text box for Recipe
        RecipeWidth, RecipeHeight = draw.textsize(RecipeStr, font = font_Recipe)
        count = 0
        while RecipeHeight > 1250:
            count += 2
            font_Recipe = ImageFont.truetype("fonts/arial.ttf", 40 - count)
            RecipeWidth, RecipeHeight = draw.textsize(RecipeStr, font = font_Recipe)
        RecipeBox = Image.new("RGBA", (RecipeWidth + 100, RecipeHeight + 100), (255, 255, 255))
        RecipeBox = ImageOps.expand(RecipeBox,border=10,fill=colorTheme)
        RecipeBoxX = centralizeImageX(PageWidth, RecipeBox, center = centerIncrementations[i])
        RecipeBoxY = int(RecipeBoxYCenter - RecipeBox.height/2)
        Page.paste(RecipeBox, (RecipeBoxX, RecipeBoxY))

        #Print ingredient list in box    
        RecipeTextX, RecipeTextY = centralizeTextInImage(RecipeStr, font_Recipe, RecipeBox, RecipeBoxX, RecipeBoxY)
        draw.text((RecipeTextX, RecipeTextY), RecipeStr, font = font_Recipe, fill=colorThemeFont)

    #Add stars
    RatingDict = Recipe.rating
    RatingList = list(RatingDict.values())
    AvgRating = sum(RatingList) / len(RatingList)
    AvgRatingRounded = round(AvgRating*2)/2
    if (AvgRatingRounded % 1) == 0:
        AvgRatingRounded = int(AvgRatingRounded)
    Stars = Image.open(f"layout/{AvgRatingRounded}stars.png")
    TransStars = makeTrans(Stars, (255, 255, 255, 255))
    TransStarsResize = newWidth(TransStars, 600)
    StarX = centralizeImageX(PageWidth, TransStarsResize)
    StarY = 350
    Page.paste(TransStarsResize, (StarX, StarY), TransStarsResize)

    #Add stars per person
    RatingDict = Recipe.rating
    NoOfRatings = len(RatingDict)
    centerIncrementations = 1 / (NoOfRatings + 1)
    center = centerIncrementations
    for i, rating in enumerate(RatingDict):
        Person = rating
        NoStars = RatingDict[rating]

        #Add stars per person
        Stars = Image.open(f"layout/{NoStars}stars.png")
        font_names = ImageFont.truetype("fonts/arial.ttf", 50)
        TransStars = makeTrans(Stars, (255, 255, 255, 255))
        TransStarsResize = newWidth(TransStars, 500)
        StarsX = centralizeImageX(PageWidth, TransStarsResize, center = center)
        if (i % 2) == 0 and len(RatingDict) > 3:
            StarsYTop = StarsY - 50
            fillImageBackground((StarsX, StarsYTop), TransStarsResize.size, "white", 5)
            Page.paste(TransStarsResize, (StarsX, StarsYTop), TransStarsResize)
            PersonX, PersonY = centralizeTextInImage(Person, font_names, TransStarsResize, StarsX, StarsYTop, Yoffset = -70)
        elif (i % 2) == 1 and len(RatingDict) > 3:
            StarsYBottom = StarsY + 50
            fillImageBackground((StarsX, StarsYBottom), TransStarsResize.size, "white", 5)
            Page.paste(TransStarsResize, (StarsX, StarsYBottom), TransStarsResize)
            PersonX, PersonY = centralizeTextInImage(Person, font_names, TransStarsResize, StarsX, StarsYBottom, Yoffset = -70)
        else:
            fillImageBackground((StarsX, StarsY), TransStarsResize.size, "white", 5)
            Page.paste(TransStarsResize, (StarsX, StarsY), TransStarsResize)

        #Add name of person that gave stars
            PersonX, PersonY = centralizeTextInImage(Person, font_names, TransStarsResize, StarsX, StarsY, Yoffset = -70)
        draw.text((PersonX, PersonY), Person, font = font_names, fill=colorThemeFont)
        fillTextBackground((PersonX, PersonY), Person, font_names, "white", 5)

        center += centerIncrementations

    #Add photo
    Photo = Image.open(f"photos/{Recipe.photo}")
    PhotoResize = newWidth(Photo, 2000)
    PhotoResizeBorder = ImageOps.expand(PhotoResize,border=25,fill='pink')
    PhotoX = centralizeImageX(PageWidth, PhotoResizeBorder)
    Page.paste(PhotoResizeBorder, (PhotoX, PhotoY))

    #Add page number
    WeekNo = Recipe.week
    font_week = ImageFont.truetype("fonts/arial.ttf", 90)
    WeekNoX, WeekNoY = centralizeTextInImage(WeekNo, font_week, Page, 0, 0, Yoffset = -1650)
    draw.text((WeekNoX, WeekNoY), WeekNo, font = font_week, fill=colorThemeFont)
    fillTextBackground((WeekNoX, WeekNoY), WeekNo, font_week, "white", 5)

    Page.save(f"pages/Page{pages + 1}.png", quality = 100)

convert_images_to_pdf("pages/", "book.pdf")
