# -*- coding: utf-8 -*-

# Define here the target websites for your scraped items

from scrapy.spider import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from sina_diy.items import InformationItem, TweetsItem, CommentsItem, TransfersItem

class Spider(CrawlSpider):
	name = "sinaDiy"
	host = "http://weibo.cn"
	start_urls = [2722063121] #input your target WId

	scrawl_ID = set(start_urls)
	finish_ID = set()

	def start_requests(self):
		while self.scrawl_ID.__len__():
			ID = self.scrawl_ID.pop()
			self.finish_ID.add(ID)  # 加入已爬队列
			ID = str(ID)

			url_tweets = "http://weibo.cn/%s/profile?filter=1&page=1" % ID
			url_information = "http://weibo.cn/attgroup/opening?uid=%s" % ID
			yield Request(url=url_information, meta={"ID": ID}, callback=self.personalInformation)  # 去爬个人信息
			yield Request(url=url_tweets, meta={"ID": ID}, callback=self.weiboInformation)  # 去爬微博

	def personalInformation(self, response):
		informationItems = InformationItem()
		selector = Selector(response)
		text0 = selector.xpath('body/div[@class="u"]/div[@class="tip2"]').extract_first()
		if text0:
			num_tweets = re.findall(u'\u5fae\u535a\[(\d+)\]', text0)  # 微博数
			num_follows = re.findall(u'\u5173\u6ce8\[(\d+)\]', text0)  # 关注数
			num_fans = re.findall(u'\u7c89\u4e1d\[(\d+)\]', text0)  # 粉丝数
			if num_tweets:
				informationItems["Num_Tweets"] = int(num_tweets[0])
			if num_follows:
				informationItems["Num_Follows"] = int(num_follows[0])
			if num_fans:
				informationItems["Num_Fans"] = int(num_fans[0])
			informationItems["UId"] = response.meta["ID"]
			url_information1 = "http://weibo.cn/%s/info" % response.meta["ID"]
			yield Request(url=url_information1, meta={"item": informationItems}, callback=self.personDetails)

	def personDetails(self, response):
		informationItems = response.meta["item"]
		selector = Selector(response)
		text1 = ";".join(selector.xpath('body/div[@class="c"]/text()').extract())  # 获取标签里的所有text()
		nickname = re.findall(u'\u6635\u79f0[:|\uff1a](.*?);', text1)  # 昵称
		gender = re.findall(u'\u6027\u522b[:|\uff1a](.*?);', text1)  # 性别
		place = re.findall(u'\u5730\u533a[:|\uff1a](.*?);', text1)  # 地区（包括省份和城市）
		signature = re.findall(u'\u7b80\u4ecb[:|\uff1a](.*?);', text1)  # 个性签名
		birthday = re.findall(u'\u751f\u65e5[:|\uff1a](.*?);', text1)  # 生日
		url = re.findall(u'\u4e92\u8054\u7f51[:|\uff1a](.*?);', text1)  # 首页链接

		if nickname:
			informationItems["Nickname"] = nickname[0]
		if gender:
			informationItems["Gender"] = gender[0]
		if place:
			place = place[0].split(" ")
			informationItems["Province"] = place[0]
			if len(place) > 1:
				informationItems["City"] = place[1]
		if signature:
			informationItems["BriefIntroduction"] = signature[0]
		if birthday:
			try:
				birthday = datetime.datetime.strptime(birthday[0], "%Y-%m-%d")
				informationItems["Birthday"] = birthday - datetime.timedelta(hours=8)
			except Exception:
				pass
		if url:
			informationItems["URL"] = url[0]
		yield informationItems

	def weiboInformation(self, response):
		selector = Selector(response)
		tweets = selector.xpath('body/div[@class="c" and @id]')
		for tweet in tweets:
			tweetsItems = TweetsItem()
			id = tweet.xpath('@id').extract_first()  # 微博ID
			content = tweet.xpath('div/span[@class="ctt"]/text()').extract_first()  # 微博内容
			like = re.findall(u'\u8d5e\[(\d+)\]', tweet.extract())  # 点赞数
			transfer = re.findall(u'\u8f6c\u53d1\[(\d+)\]', tweet.extract())  # 转载数
			comment = re.findall(u'\u8bc4\u8bba\[(\d+)\]', tweet.extract())  # 评论数
			others = tweet.xpath('div/span[@class="ct"]/text()').extract_first()  # 求时间和使用工具（手机或平台）

			tweetsItems["UId"] = response.meta["ID"]
			tweetsItems["WId"] = id
			if content:
				tweetsItems["WContent"] = content.strip(u"[\u4f4d\u7f6e]")  # 去掉最后的"[位置]"
			if like:
				tweetsItems["Like"] = int(like[0])
			if transfer:
				tweetsItems["Transfer"] = int(transfer[0])
			if comment:
				tweetsItems["Comment"] = int(comment[0])
			if others:
				others = others.split(u"\u6765\u81ea")
				tweetsItems["PubTime"] = others[0]
				if len(others) == 2:
					tweetsItems["Tools"] = others[1]
			yield tweetsItems
		url_next = selector.xpath('body/div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
		if url_next:
			yield Request(url=self.host + url_next[0], meta={"ID": response.meta["ID"]}, callback=self.weiboInformation)