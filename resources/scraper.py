import asyncio
import re

import aiohttp
from bs4 import BeautifulSoup

from utils import is_valid_url
from urllib.parse import urlparse

visited_urls = []
extracted_emails = []
tag_checklist = ['#', '', None, '/']

lock = asyncio.Lock()


async def scrape_page(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            return soup


async def get_all_urls(url, netloc):
    global visited_urls

    soup = await scrape_page(url=url)
    a_tags = soup.select('a')
    new_urls = []

    for a_tag in a_tags:
        href = a_tag.get('href')

        if href in tag_checklist or not is_valid_url(url=href) or netloc not in href:
            continue
        async with lock:
            if href not in visited_urls and href not in new_urls:
                new_urls.append(href)

    return new_urls, soup


async def extract_emails(soup):
    global extracted_emails
    email_list = []
    html = soup.select_one('html') or None
    if html:
        html = html.text
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_regex, html)
    for email in emails:
        async with lock:
            if email not in extracted_emails and email not in email_list:
                email_list.append(email)

    return email_list


async def scraper(url):
    global visited_urls, extracted_emails
    parsed_base_url = urlparse(url)
    netloc = parsed_base_url.netloc
    url_list, soup = await get_all_urls(url=url, netloc=netloc)
    email_list = await extract_emails(soup=soup)

    async with lock:
        visited_urls.extend(url_list)
        extracted_emails.extend(email_list)

    if url_list:
        tasks = [scraper(url=_url) for _url in url_list]
        await asyncio.gather(*tasks)

    return visited_urls, extracted_emails
