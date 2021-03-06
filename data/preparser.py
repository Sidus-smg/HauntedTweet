#!/usr/bin/env python
"""Extract the necessary info from the raw CSV file.
Result of parser will contain only user's public tweets,
and its timestamp.
"""
import re
class Preparser:
    """Preparser."""

    def __init__(self, fileobj=None):
        self._result = []
        if fileobj != None:
            self.file = fileobj

    def extract(self, filter=False):
        "Actually parse the contents. Exclude retweets, replies and links when filter is on."
        ai_tweet = "#_트위터망령"
        pattern = """(?:".*?",){3}"(.*?)",".*?","((?:.|\n|\r)*?)",(?:".*?",){3}".*?"""
        regex_tweet = re.compile(pattern)
        prevtext = ""
        for line in self.file:
            if prevtext == "":
                text = line
            else:
                text = prevtext[:-1] + " " + line
            match_tweet = regex_tweet.search(text)
            if match_tweet == None:
                prevtext = text
            else:
                timestamp = match_tweet.group(1)
                text = match_tweet.group(2).replace('""', '"')
                if timestamp == "timestamp" and text == "text":
                    pass
                elif filter == False:
                    self._result.append((timestamp, text))
                else:
                    if "@" not in text and ai_tweet not in text:
                        self._result.append((timestamp, re.sub(r"https?:\/\/t\.co\/\w+|#[\S]+|[\U00010000-\U0010ffff]", "", text)))
                prevtext = ""
        return self._result

    def save(self, savefile):
        "Save result as filename"
        if self._result == []:
            self.extract()
        for timestamp, text in reversed(self._result):
            savefile.write(timestamp + "\t" + text + "\n")
            
