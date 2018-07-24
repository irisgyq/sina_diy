# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class InformationItem(Item):
    """personal information"""
    UId = Field() #用户 id
    VIPlevel = Field() #vip 等级
    Tag = Field() #用户标签
    URL = Field() #用户首页 url
    Nickname = Field() #昵称
    Gender = Field() #性别
    Birthday = Field() #生日
    BriefIntroduction = Field() #简介
    Authentication = Field() #认证身份
    AuthenticationInformation = Field() #认证介绍
    Province = Field() #省份
    City = Field() #城市
    Educational_Experience = Field() #教育经历
    Num_Tweets = Field() #微博数
    Num_Follows = Field() #关注数
    Num_Fans = Filed() #粉丝数

class TweetsItem(Item):
	"""微博信息"""
	WId = Field() #微博id
	Is_Topic = Field() #涉及的话题
	Is_At = Field() #被@的人
	Is_URL = Field() #包含的链接
	Is_Image = Field() #包含图片的数量
	Is_Vedio = Field() #是否包含视频
	Transfer_From = Filed() #原微博的用户
	KeyWord = Field() #搜索关键字，通过这个关键字搜索出微博的话题
	UId = Field() #用户id
	WContent = Field() #微博内容
	PubtiME = Field() #发布时间
	Tools = Field() #使用的设备
	Like = Field() #点赞数
    Comment = Field() #评论数
    Transfer = Field() #转发数

class CommentsItem(Item):
	"""评论信息"""
	Comment_Time = Field() #评论时间
	Comment_UId = Field() #评论的用户id
	Origin_WId = Field() #原微博id
	Comment_Str = Field() #评论
	Comment_Nickname = Field() #评论用户昵称
	Comment_Like = Field() #点赞数
	Tool = Field() #使用设备

class TransfersItem(Item):
	"""转发信息"""
	Origin_WId = Field() #原微博id
	Transfer_Time = Field() #转发时间
	Transfer_UId = Field() #转发用户id
	Transfer_Str = Field() #转发内容
	Transfer_Nickname = Field() #昵称
	Transfer_Like = Field() #点赞数
	Tool = Field() #使用设备





