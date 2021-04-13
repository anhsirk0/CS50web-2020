
def get_highlights(highlight):
    h_list = highlight.split("|")
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
    return new

def get_imgurls(imgurls):
    images = [f"https:{i}" for i in imgurls.split("|")]
    return images

def get_overview(overview):
    o = overview.split("|")
    o.pop(-1)
    overview = "".join(c for c in o)
    return overview

def get_stars(stars):
    s = int(stars.split(" ")[0])
    stars = [1]*s + [0]*(5 - s)
    return stars
