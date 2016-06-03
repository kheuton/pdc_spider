import scrapy
from pdc.items import FileItem
class PDCSpider(scrapy.Spider):
    name = 'PDCSpider'
    start_urls = ['http://web.pdc.wa.gov/MvcQuerySystem/Committee/initiative_committees']

    ITEM_PIPELINES = {'scrapy.pipelines.files.FilesPipeline': 1}
    FILES_STORE = '/home/krheuton/joe_butts_money'

    field_urls = scrapy.Field()


    def parse(self, response):
        print 'At the start url'
        for link in response.xpath('//table/tbody/tr/td/a/@href').extract():

            data_page = link.split('/')[-1]
            cruft = link.split('/')[:-1]

            request_and_flags = data_page.split('?')
            request = request_and_flags[0]
            flags = request_and_flags[1].split('&')

            # Update some flags
            flags.append('tab={req:s}'.format(req=request))

            # Change the request from whatever to excel
            request = 'excel'

            new_flags = '&'.join(flags)
            new_request_and_flags = [request]
            new_request_and_flags.append(new_flags)

            new_request_and_flags = '?'.join(new_request_and_flags)

            new_link = cruft
            new_link.append(new_request_and_flags)

            new_link = '/'.join(new_link)


            excel_link = response.urljoin(new_link)
            print excel_link

            import subprocess
            #subprocess_string = "curl '{el:s}' -H 'Connection: keep-alive'".format(el=excel_link)
            #subprocess.call(subprocess_string,shell=True)
            #print subprocess_string

            item = FileItem()
            item['file_urls'] = [excel_link]

            yield item

            #yield scrapy.Request(response.urljoin(link),
            #                     callback=self.get_the_data)

    def get_the_data(self, response):

        print 'at a datapage'
