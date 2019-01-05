#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

# Author: NetworkRanger
# Date: 2019/1/5 下午10:06

from selenium import webdriver

def main():
    driver = webdriver.Firefox()
    driver.get('http://example.webscraping.com/search')
    driver.find_element_by_id('search_item').send_keys('.')
    driver.execute_script("document.getElementById('page_size').options[1].text = '1000'")
    driver.find_element_by_id('search').click()
    driver.implicitly_wait(30)
    links = driver.find_element_by_css_selector('#results a')
    countries = [link.text for link in links]
    driver.close()
    print countries

if __name__ == '__main__':
    main()