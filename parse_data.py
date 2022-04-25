import scrapy

css_paths_1 = {
    'title'      : ' .b-product-list__item__descr--title ::text',
    'price'      : ' .b-product-list__price > span:nth-child(1) ::text',
    'old_price'  : ' .b-product-list__price--old ::text',
    'article'    : '::attr(data-id)',
    'description': ' .b-productParamsList--list',
    'url'        : ' .b-link--inherit.i-mr15 ::attr(href)',
    'blocks'      : ' li.b-menu__item.b-product-list__item.js-item.js-product-item'
}

css_paths = [css_paths_1]


def select_css(html):
    selector = scrapy.Selector(text=html)
    for paths in css_paths:
        blocks = selector.css(
                    paths['blocks']
            ).extract()
        if len(blocks) > 0:
            return paths
    # if nothing returned
    raise ValueError("Page can't be parsed")


class PageData:
    def __init__(self, page, css_paths):
        page_selector = scrapy.Selector(text=page)
        self.css_paths = css_paths
        block_selectors = self.get_item_block_selectors(page_selector)
        self.item_entries = [
            self.get_item_entry(item)
            for item in block_selectors
        ]

    def get_item_entry(self, item_selector):
        title = self.get_title(item_selector)
        price = self.get_price(item_selector)
        old_price = self.get_old_price(item_selector)
        article = self.get_article(item_selector)
        description = self.get_product_description(item_selector)
        url = self.get_product_page_url(item_selector)

        item_entry = {
            'title': title,
            'article': article,
            'description': description,
            'url': url,
        }
        if old_price is not None:
            item_entry['price'] = old_price
            item_entry['discount'] = price
        else:
            item_entry['price'] = price

        return item_entry

    def get_title(self, item_selector):
        css_path = self.css_paths['title']
        title = item_selector.css(css_path).extract()[0]
        title = title.strip('\n').strip()
        return title

    def get_price(self, item_selector):
        css_path = self.css_paths['price']
        price = item_selector.css(css_path).extract()[0]
        price = float(
            price.replace('\xa0', '').replace(',', '.').strip()
        )
        return price

    def get_old_price(self, item_selector):
        css_path = self.css_paths['old_price']
        old_price_raw = item_selector.css(css_path).extract()
        if len(old_price_raw) != 0:
            old_price = float(
                old_price_raw[0].replace('\xa0', '').replace(',', '.').strip()
            )
        else:
            old_price = None
        return old_price

    def get_article(self, item_selector):
        css_path = self.css_paths['article']
        article = item_selector.css(css_path).extract()[0]
        return int(article)

    def get_product_description(self, item_selector):
        css_path = self.css_paths['description']
        description = item_selector.css(css_path).extract()
        if len(description) > 0:
            description = '\n'.join(
                [
                    tt.strip('\n').strip()
                    for tt in
                    scrapy.Selector(text=description[0]).css(' ::text').extract()
                    if tt.strip('\n').strip() != ''
                ])
        else:
            description = ''
        return description

    def get_product_page_url(self, item_selector):
        css_path = self.css_paths['url']
        item_url = item_selector.css(css_path).extract()[0]
        item_url = 'https://www.komus.ru' + item_url
        return item_url

    def get_item_block_selectors(self, page_selector):
        css_path = self.css_paths['blocks']
        return [
            scrapy.Selector(text=block)
            for block in
            page_selector.css(css_path).extract()
        ]
