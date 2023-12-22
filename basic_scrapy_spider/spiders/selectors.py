# selectors.py

# Selectors
COMPANY_NAME = 'div[itemprop="name"].css-19rjr9w.e1wnkr790::text'
COMPANY_NAME_SELECTOR = 'h1.css-1bpmjfq.e1tiznh50::text'
TITLE_SELECTOR = 'h2[data-testid="title"] span.css-15r9gu1.eu4oa1w0::text'
REVIEW_CARD = ".css-lw17hn.eu4oa1w0"
REVIEW_BODY_SELECTOR = 'span[itemprop="reviewBody"] span.css-1cxc9zk.e1wnkr790 span.css-15r9gu1.eu4oa1w0::text'

DATE_SELECTOR = "div.css-8a5o2x.e1wnkr790 span.css-xvmbeo.e1wnkr790::text"


LOCATION_SELECTOR = ".css-8a5o2x.e1wnkr790 a:last-child::text"
JOB_ROLE_SELECTOR = 'span[itemprop="author"] a::text'
JOB_INFO_SELECTOR = "div.css-8a5o2x.e1wnkr790 span.css-xvmbeo.e1wnkr790::text"

RATING_SELECTOR = 'div[itemprop="reviewRating"] button.css-1c33izo.e1wnkr790::text'
RATING_TOOL_SELECTOR = ".css-1a7ugs2.eu4oa1w0 div.css-1exgkxc.e37uo190"
CATEGORY_RATING_SELECTOR = "./div/@aria-label"
RATING_CATEGORY_SELECTOR = "span.css-1pftocx.e1wnkr790::text"

CONS_PROS_DIV_SELECTOR = "div.css-hxk5yu.eu4oa1w0"
PROS_SELECTOR = './/div[1]/div[@class="css-1z0411s e1wnkr790"]'
CONS_SELECTOR = './/div[2]/div[@class="css-1z0411s e1wnkr790"]'
PROS_SPANS = "span.css-15r9gu1.eu4oa1w0::text"
CONS_SPANS = "span.css-15r9gu1.eu4oa1w0::text"


BALANCE_CAT = "balance"
BENEFITS_CAT = "benefits"
SECURITY_CAT = "security"
MANAGMENT_CAT = "management"
CULTURE_CAT = "culture"
