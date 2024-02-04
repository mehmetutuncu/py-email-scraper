import asyncio
import sys
import time

from exception import InvalidArgumentException, InvalidURLException
from utils import is_valid_url

from scraper import scraper


def main():
    start_time = time.time()
    parameters = sys.argv
    if len(parameters) != 2:
        raise InvalidArgumentException()
    website_url = parameters[-1]
    if not is_valid_url(url=website_url):
        raise InvalidURLException()
    visited_urls, extracted_emails = asyncio.run(scraper(url=website_url))
    end_time = time.time()
    execution_time = "{:.2f}".format(end_time - start_time)

    print(f"Extracted Email Count: {len(extracted_emails)}\n"
          f"Visited Url Count: {len(visited_urls)}\n"
          f"Runtime: {execution_time} sec\n"
          f"Extracted Email List: {extracted_emails}")


if __name__ == '__main__':
    main()
