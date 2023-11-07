from os.path import exists
from datetime import date
from urllib.parse import urlparse
import feedparser

feedfilepath = "feeds.txt"
today = date.today()

class DailyNews:
    def __init__(self, url):
        self.out = []
        self.is_available = self.is_validurl(url)
        self.url = url
        self.sitename = self.get_sitename(url)

    def get_sitename(self, url):
        inputurl = urlparse(url)
        return inputurl.netloc.split(".")[-2].title()

    def is_validurl(self, url):
        inputurl = urlparse(url)
        if all([inputurl.scheme, inputurl.netloc]):
            return True
        else:
            return False
    
    def cleanup_summary(self, msg):
        msgout = msg[0:200].replace("`", "")
        if msgout.startswith("<"):
            return ""
        else:
            return msgout

    def generate_markdown(self):
        if self.is_available:
            for item in feedparser.parse(self.url)["entries"]:
                is_today = False
                if "updated_parsed" in item:
                    if item.updated_parsed >= today.timetuple():
                        is_today = True
                if "published_parsed" in item:
                    if item.published_parsed >= today.timetuple():
                        is_today = True

                if is_today:
                    desc = self.cleanup_summary(item.summary)
                    self.out.append("## [%s] %s" % (self.sitename, item.title))
                    if desc:
                        self.out.append("```\n%s\n```\n" % desc)
                    self.out.append("Link: [Click](%s)\n" % item.links[0]["href"])
        return self.out


if __name__ == "__main__":
    out = []
    if exists(feedfilepath):
        with open(feedfilepath, "r") as feedfile:
            for site in feedfile.readlines():
                obj = DailyNews(url=site)
                out += obj.generate_markdown()
    else:
        print("[ERROR] Feedfile Missing.")
    
    with open("current.md", "w") as outfile:
        outfile.write("\n".join(out))