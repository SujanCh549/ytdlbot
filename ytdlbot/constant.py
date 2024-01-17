#!/usr/local/bin/python3
# coding: utf-8

# ytdlbot - constant.py
# 8/16/21 16:59
#

__author__ = "Benny <benny.think@gmail.com>"

import os

from config import (
    AFD_LINK,
    COFFEE_LINK,
    ENABLE_CELERY,
    FREE_DOWNLOAD,
    REQUIRED_MEMBERSHIP,
    TOKEN_PRICE,
)
from database import InfluxDB
from utils import get_func_queue


class BotText:
    start = """
    Welcome to YouTube Downloader Bot.

Type /help For More Information.

Join @Sujan_BotZ To Use This Bot."""

    help = f"""
1. If The Bot Doesn't Work, Try Again Or Dm @Sujan_Bots"""

    about = "YouTube Downloader Bot By ~ @Sujan_BotZ."


    private = "This bot is for private use"

    membership_require = f"You need to join this group or channel to use this bot\n\nhttps://t.me/{REQUIRED_MEMBERSHIP}"

    settings = """
Please The Format And Video Quality For Your video. These Settings Only **apply to YouTube videos**.

High Quality Is Recommended. Medium Quality Is 720P, While Low Quality is 480P.

If You Choose To Send The Video As Document, It Will Not Be Possible To Stream It.

Your current settings:
Video quality: **{0}**
Sending format: **{1}**
"""
    custom_text = os.getenv("CUSTOM_TEXT", "")

    premium_warning = """
    Your File Is Too Big, Do You Want Me To Try To Send It As Premium User? 
    This Is An Experimental Feature So You Can Only Use It Once Per Day.
    Also, The Premium User Will Know Who You Are a What You Are Downloading. 
    You May Be Banned If You Abuse This Feature.
    """

    @staticmethod
    def get_receive_link_text() -> str:
        reserved = get_func_queue("reserved")
        if ENABLE_CELERY and reserved:
            text = f"Tasks Was Added To The Reserved Queue {reserved}. Processing...😊\n\n"
        else:
            text = "Task Was Added To Active Queue.\nProcessing...😊\n\n"

        return text

    @staticmethod
    def ping_worker() -> str:
        from tasks import app as celery_app

        workers = InfluxDB().extract_dashboard_data()
        # [{'celery@BennyのMBP': 'abc'}, {'celery@BennyのMBP': 'abc'}]
        response = celery_app.control.broadcast("ping_revision", reply=True)
        revision = {}
        for item in response:
            revision.update(item)

        text = ""
        for worker in workers:
            fields = worker["fields"]
            hostname = worker["tags"]["hostname"]
            status = {True: "✅"}.get(fields["status"], "❌")
            active = fields["active"]
            load = "{},{},{}".format(fields["load1"], fields["load5"], fields["load15"])
            rev = revision.get(hostname, "")
            text += f"{status}{hostname} **{active}** {load} {rev}\n"

        return text
