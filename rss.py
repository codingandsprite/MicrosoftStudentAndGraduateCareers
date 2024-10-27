from collections import namedtuple
from datetime import datetime
import requests

LAST_PAGE = 5

POSTS = dict()

Post = namedtuple("Post", ["link", "title", "date"])

url = "https://gcsservices.careers.microsoft.com/search/api/v1/search?lc=United%20States&exp=Students%20and%20graduates&l=en_us&pg={page}&pgSz=20&o=Recent&flt=true"

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Bearer undefined',
    'origin': 'https://jobs.careers.microsoft.com',
    'priority': 'u=1, i',
    'referer': 'https://jobs.careers.microsoft.com/',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'x-correlationid': '627facc8-1372-6ac5-cf4f-42cc563da5e7',
    'x-subcorrelationid': '966278b6-bdeb-8462-ee83-cc3d9cda27db',
}

for page in range(1, LAST_PAGE+1):
    response = requests.get(
        url=url.format(page=page),
        headers=headers,
    )

    jobs = dict(response.json())
    jobs = jobs['operationResult']['result']['jobs']
    for job in jobs:
        id = job['jobId']
        title = job['title']
        date = datetime.fromisoformat(job['postingDate'])
        link = "https://jobs.careers.microsoft.com/global/en/job/"+id+"/"
        POSTS[link] = Post(link, title, date)

STREAM = sorted(
    [POSTS[key] for key in POSTS.keys()], key=lambda x: x.date, reverse=True
)

if __name__ == "__main__":

    NOW = datetime.now()
    XML = "\n".join(
        [
            r"""<?xml version="1.0" encoding="UTF-8" ?>""",
            r"""<rss version="2.0">""",
            r"""<channel>""",
            r"""<title>Microsoft Student and Graduate Careers</title>""",
            r"""<description>Microsoft Student and Graduate Careers</description>""",
            r"""<language>en-us</language>""",
            r"""<pubDate>"""
            + NOW.strftime("%a, %d %b %Y %H:%M:%S GMT")
            + r"""</pubDate>""",
            r"""<lastBuildDate>"""
            + NOW.strftime("%a, %d %b %Y %H:%M:%S GMT")
            + r"""</lastBuildDate>""",
            "\n".join(
                [
                    r"""<item><title><![CDATA["""
                    + x.title
                    + r"""]]></title><link>"""
                    + x.link
                    + r"""</link><pubDate>"""
                    + x.date.strftime('%a, %d %b %Y %H:%M:%S %z')
                    + r"""</pubDate></item>"""
                    for x in STREAM
                ]
            ),
            r"""</channel>""",
            r"""</rss>""",
        ]
    )

    print(XML)
