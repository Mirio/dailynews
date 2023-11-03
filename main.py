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
    
    def is_validurl(self, url):
        inputurl = urlparse(url)
        if all([inputurl.scheme, inputurl.netloc]):
            return True
        else:
            return False
    
    def cleanup_summary(self, msg):
        msgout = msg.summary[0:200].replace("`", "")
        if msgout.startswith("<"):
            return ""
        else:
            return msgout

    def generate_markdown(self):
        for item in feedparser.parse(self.url)["entries"]:
            if item.updated_parsed >= today.timetuple():
                self.out.append("## %s" % item.title)
                self.out.append("```%s```\n" % self.cleanup_summary(item.summary))
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