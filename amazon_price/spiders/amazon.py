# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class AmazonSpider(scrapy.Spider):
    name = 'amazon'

    def start_requests(self):
        yield SplashRequest(
            url='https://www.amazon.com/ZENY-Portable-Compact-Full-Automatic-Apartment/dp/B07H9TZ6WS',
            callback=self.parse,
        )

    def parse(self, response):
        print(response.xpath('//title'))
        item = {
			'url': response.url,
            'product': response.xpath('//span[@id="productTitle"]/text()').extract_first().strip(),
            #'price': response.xpath('//span[@id="priceblock_ourprice"]/text()').extract_first()
            'price': float(
                        response.css("span#priceblock_ourprice::text").re_first("\$(.*)") or 0
                        )
            }
        yield item

        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "motox201305@gmail.com"  # Enter your address
        receiver_email = "couponlalala@gmail.com"  # Enter receiver address
        password = "1234mail"
        #password = input("Type your password and press enter: ")
        message = MIMEMultipart("alternative")
        message["Subject"] = "Amazon price drop"
        message["From"] = sender_email
        message["To"] = receiver_email
        # Create the plain-text and HTML version of your message
        text = """\
        Hello"""
        html = """\
         <h1> Hey, we found a good deal! </h1>
        <table border="1">
        <tr><td>
            <p><strong>Product:</strong> {{item.product}}</p>
            <p><strong>Price:</strong> {{item.price}}</p>
                <p>Visit the product page at {{item.url}} </p>
        </td></tr>
        </table>"""
        #.format(product=item['product'],price=item['price'],url=item['url'])
        
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        
        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)
        print(1)
        
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        print(2)
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            print(3)
            server.sendmail(sender_email, receiver_email, message)
