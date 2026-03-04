# -*- coding: utf-8 -*-
"""
قائمة مواقع الأنمي المدعومة
"""

ANIME_SITES = {
    "1": {"name": "witanime", "url": "https://witanime.com", "type": "arabic"},
    "2": {"name": "animeiat", "url": "https://animeiat.tv", "type": "arabic"},
    "3": {"name": "anime4up", "url": "https://anime4up.com", "type": "arabic"},
    "4": {"name": "animerco", "url": "https://animerco.com", "type": "arabic"},
    "5": {"name": "shahiid-anime", "url": "https://shahiid-anime.net", "type": "arabic"},
    "6": {"name": "arabsama", "url": "https://arabsama.net", "type": "arabic"},
    "7": {"name": "animelayer", "url": "https://animelayer.net", "type": "arabic"},
    "8": {"name": "animelek", "url": "https://animelek.com", "type": "arabic"},
    "9": {"name": "mycima", "url": "https://mycima.tv", "type": "arabic"},
    "10": {"name": "animetitans", "url": "https://animetitans.net", "type": "arabic"},
    "11": {"name": "animebladders", "url": "https://animebladders.com", "type": "arabic"},
    "12": {"name": "xsanime", "url": "https://xsanime.com", "type": "arabic"},
    "13": {"name": "animevideo", "url": "https://animevideo.org", "type": "arabic"},
    "14": {"name": "animefire", "url": "https://animefire.net", "type": "arabic"},
    "15": {"name": "movizland", "url": "https://movizland.com", "type": "arabic"},
    "16": {"name": "animeblkom", "url": "https://animeblkom.net", "type": "arabic"},
    "17": {"name": "otakuarabic", "url": "https://otakuarabic.com", "type": "arabic"},
    "18": {"name": "animenz", "url": "https://animenz.org", "type": "arabic"},
    "19": {"name": "animetvn", "url": "https://animetvn.com", "type": "arabic"},
    "20": {"name": "faselhd", "url": "https://faselhd.top", "type": "arabic"},
    "21": {"name": "crunchyroll", "url": "https://crunchyroll.com", "type": "english"},
    "22": {"name": "9anime", "url": "https://9anime.to", "type": "english"},
    "23": {"name": "gogoanime", "url": "https://gogoanime.lu", "type": "english"},
    "24": {"name": "animixplay", "url": "https://animixplay.to", "type": "english"},
    "25": {"name": "zoro.to", "url": "https://zoro.to", "type": "english"},
    "26": {"name": "aniwatch", "url": "https://aniwatch.to", "type": "english"},
    "27": {"name": "kickassanime", "url": "https://kickassanime.mx", "type": "english"},
    "28": {"name": "animepahe", "url": "https://animepahe.com", "type": "english"},
    "29": {"name": "animekaizoku", "url": "https://animekaizoku.com", "type": "english"},
    "30": {"name": "nyaa", "url": "https://nyaa.si", "type": "torrent"},
    "31": {"name": "anidl", "url": "https://anidl.org", "type": "english"},
    "32": {"name": "animesuge", "url": "https://animesuge.to", "type": "english"},
    "33": {"name": "yugenanime", "url": "https://yugenanime.tv", "type": "english"},
    "34": {"name": "animedao", "url": "https://animedao.to", "type": "english"},
    "35": {"name": "animeheaven", "url": "https://animeheaven.ru", "type": "english"},
    "36": {"name": "animeowl", "url": "https://animeowl.net", "type": "english"},
    "37": {"name": "kissanime", "url": "https://kissanime.com.ru", "type": "english"},
    "38": {"name": "animeflv", "url": "https://animeflv.net", "type": "spanish"},
    "39": {"name": "jkanime", "url": "https://jkanime.net", "type": "spanish"},
    "40": {"name": "monoschinos", "url": "https://monoschinos.com", "type": "spanish"},
    "41": {"name": "animefenix", "url": "https://animefenix.com", "type": "spanish"},
    "42": {"name": "tioanime", "url": "https://tioanime.com", "type": "spanish"},
    "43": {"name": "animeid", "url": "https://animeid.tv", "type": "spanish"},
    "44": {"name": "legionanime", "url": "https://legionanime.com", "type": "spanish"},
    "45": {"name": "latanime", "url": "https://latanime.org", "type": "spanish"},
    "46": {"name": "animeblix", "url": "https://animeblix.com", "type": "spanish"},
    "47": {"name": "animeonline", "url": "https://animeonline.ninja", "type": "spanish"},
    "48": {"name": "animeyabu", "url": "https://animeyabu.com", "type": "japanese"},
    "49": {"name": "animelab", "url": "https://animelab.com", "type": "english"},
    "50": {"name": "funimation", "url": "https://funimation.com", "type": "english"},
    "51": {"name": "hidive", "url": "https://hidive.com", "type": "english"},
    "52": {"name": "wakanim", "url": "https://wakanim.tv", "type": "multi"},
    "53": {"name": "aniplus", "url": "https://aniplus-asia.com", "type": "english"},
    "54": {"name": "animedlr", "url": "https://animedlr.com", "type": "english"},
    "55": {"name": "animenova", "url": "https://animenova.org", "type": "arabic"},
}

QUALITY_OPTIONS = ["360p", "480p", "720p", "1080p", "1440p", "4K"]

DOWNLOAD_SERVERS = [
    "mega", "mediafire", "google_drive", "solidfiles",
    "uptobox", "dropbox", "direct", "fembed",
    "streamsb", "dood", "mixdrop", "uqload",
    "streamtape", "mp4upload", "vidcloud", "streamlare"
]

def get_sites_list():
    """إرجاع قائمة المواقع المتاحة"""
    return "\n".join([f"{key}. {site['name']} ({site['type']})"
                      for key, site in ANIME_SITES.items()])

def get_site_info(site_id):
    """الحصول على معلومات موقع معين"""
    return ANIME_SITES.get(site_id)
