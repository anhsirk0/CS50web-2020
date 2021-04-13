from django import template
import random
import datetime

register = template.Library()

@register.filter
def get_first_img(hotel):
    image = f"https:{hotel.imgurls.split('|')[0]}"
    return image


@register.filter
def get_random_img(hotel):
    imgs = hotel.imgurls.split('|')
    l = len(imgs)
    if l < 2:
        return f"https:{imgs[0]}"
    else: 
        return f"https:{imgs[random.randint(1,l-1)]}"

@register.filter
def get_highlights(hotel,s=False):

    h_list = hotel.highlight.split("|")
    new = []
    for i in range(len(h_list)):
        same = False
        for j in range(i+1, len(h_list)):
            i_item = h_list[i].lower()
            j_item = h_list[j].lower()

            i_item = ''.join(ch for ch in i_item if ch.isalnum())
            j_item = ''.join(ch for ch in j_item if ch.isalnum())
            if i_item == j_item:
                same = True
                break
            if i_item.split(" ") == j_item.split(" "):
                same = True
                break
        if not same:
            new.append(h_list[i])
    if s:
        new = sorted(new, key=len)
    return new


@register.filter
def get_images(hotel):
    images = [f"https:{i}" for i in hotel.imgurls.split("|")]
    return images


@register.filter
def get_overview(hotel):
    o = hotel.overview.split("|")
    o.pop(-1)
    overview = "".join(c for c in o)
    return overview


@register.filter
def get_stars(hotel):
    s = int(hotel.rating.split(" ")[0])
    stars = [1]*s + [0]*(5 - s)
    return stars

@register.filter
def get_by_index(list, i):
    new = list*5
    return new[int(i)]

@register.filter
def make_range(b, a=0):
    new = list(range(int(a),int(b)))
    return new
    
@register.simple_tag
def get_date():
    now = datetime.datetime.now()
    date = now.strftime("%b %d, %Y")
    return date

@register.simple_tag
def get_next_date():
    now = datetime.datetime.now()
    now += datetime.timedelta(days=1)
    date = now.strftime("%b %d, %Y")
    return date

@register.simple_tag
def create_tracking_id():
    pass