# Slovak news article scraper

- ta3.com

`python .\scraper.py --template=https://www.ta3.com/clanok/ --max-article-id=123 --output-file=ta3.txt --log-file=ta3_log.txt --desc-html-class=article-perex --body-html-class=article-content`

As of 04-Sep-2021, highest article id on ta3.com is around 211018

- pravda.sk

`python .\scraper.py --template=https://spravy.pravda.sk/clanok/ --max-article-id=123 --output-file=pravda_sk.txt --log-file=pravda_sk_log.txt --desc-html-class=article-detail-perex --body-html-class=article-detail-body`

As of 04-Sep-2021, highest article id on pravda.sk is around 599664
