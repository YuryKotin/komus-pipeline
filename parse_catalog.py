import scrapy
from math import ceil

css_paths_1 = {
    'block_selectors'   : ' .block-wrapper--empty',
    'category_name'     : ' .b-account__item--label ::text',
    'subblock_selectors': ' .b-info__link--category',
    'subcategory_name'  : ' ::text',
    'subcategory_link'  : ' ::attr(href)',
    'count_articles'    : ' .b-colored--lg ::text'
}

css_paths_2 = {
    'block_selectors'   : ' .categories__item',
    'category_name'     : ' .categories__name::text',
    'subblock_selectors': ' .categories__subcategory',
    'subcategory_name'  : ' .categories__link::text',
    'subcategory_link'  : ' .categories__link ::attr(href)',
    'count_articles'    : ' .categories__amount--subcategory ::text'
}

css_paths = [css_paths_1, css_paths_2]


def select_css(selector):
    for paths in css_paths:
        blocks = selector.css(
                    paths['block_selectors']
            ).extract()
        if len(blocks) > 0:
            return paths
    # if nothing returned
    raise ValueError("Page can't be parsed")


class Catalog:
    def __init__(self, page_html):
        page_selector = scrapy.Selector(text=page_html)
        self.css_paths = select_css(page_selector)
        self.data = []

        block_selectors = self.get_block_selectors(page_selector)
        for block_selector in block_selectors:
            category_name = self.get_category_name(block_selector)

            for subblock_selector in self.get_subblock_selectors(block_selector):
                subcategory_name = self.get_subcategory_name(subblock_selector)
                link = self.get_subcategory_link(subblock_selector)
                n_articles = self.count_articles(subblock_selector)

                n_pages = ceil(n_articles / 30)

                self.data.append(
                    {
                        'category': category_name,
                        'subcategory': subcategory_name,
                        'n_pages': n_pages,
                        'link': link,
                    }
                )

    def get_block_selectors(self, page_selector):
        css_path = self.css_paths['block_selectors']
        return get_selector_list(page_selector, css_path)

    def get_category_name(self, block_selector):
        css_path = self.css_paths['category_name']
        name = clean_str(
            block_selector.css(css_path).extract()[0]
        )
        return name

    def get_subblock_selectors(self, block_selector):
        css_path = self.css_paths['subblock_selectors']
        return get_selector_list(block_selector, css_path)

    def get_subcategory_name(self, subblock_selector):
        css_path = self.css_paths['subcategory_name']
        return clean_str(
            subblock_selector.css(css_path).extract()[0]
        )

    def get_subcategory_link(self, subblock_selector):
        css_path = self.css_paths['subcategory_link']
        return subblock_selector.css(css_path).extract()[0]

    def count_articles(self, subblock_selector):
        css_path = self.css_paths['count_articles']
        n_articles = subblock_selector.css(css_path).extract()[0]
        n_articles = n_articles.replace('(', '').replace(')', '')
        return int(n_articles)


def get_selector_list(selector, css_path):
    return [
        scrapy.Selector(text=el)
        for el in
        selector.css(css_path).extract()
    ]


def clean_str(str_or_list):
    clean = ''.join(
        str_or_list
    ).replace('\n', '').strip()
    return clean
