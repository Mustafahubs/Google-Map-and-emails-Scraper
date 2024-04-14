from Automations import PopularDefs
pd = PopularDefs()


items_xpath = '//div[@role="feed"]/div/div/a'
name_xpath = '//div[@role="main"]//h1'
address_xpath = '//button[@data-item-id="address"]'
# address_xpath = '//img[contains(@src,"place_gm_blue_24dp.png")]/parent::div/parent::div/following-sibling::div/div[1]'
phone_xpath = '//button[contains(@data-item-id,"phone:tel")]'
# phone_xpath = '//img[contains(@src,"phone_gm_blue_24dp.png")]/parent::div/parent::div/following-sibling::div/div[1]'
website_xpath = '//a[@data-item-id="authority"]'
# website_xpath = '//img[contains(@src,"public_gm_blue_24dp.png")]/parent::div/parent::div/following-sibling::div/div[1]'
reviews_xpath = '//button[@jsaction="pane.reviewChart.moreReviews"]//span'
# reviews_xpath = '//div[@jsaction="pane.reviewChart.moreReviews"]//span[contains(text(),"reviews")]'
ratings_xpath = '//div[@jsaction="pane.reviewChart.moreReviews"]//div[@class="fontDisplayLarge"]'
# ratings_xpath = '//div[@jsaction="pane.reviewChart.moreReviews"]//div[@class="fontDisplayLarge"]'
# images_xpath = '//img[@decoding="async"]'
images_xpath = '//button/img[@decoding="async"]'
time_btn_xpath = '//button[@data-item-id="oh"] | //div[contains(@jsaction, "pane.openhours")]'
time_xpath = '//div[contains(@aria-label,"Friday")]'
description_xpath = '//div[contains(@aria-label,"About")]'
category_xpath = '//button[contains(@jsaction,"category")]'