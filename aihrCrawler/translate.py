from glob import glob
import os
from google_trans_new import google_translator
from scrapy import Selector

translator = google_translator()
# translate_text = translator.translate('สวัสดีจีน',lang_tgt='en')


file = glob('files/*.html')

translations_dictionary = {

}

all_texts = []

with open(file[0], mode='r', encoding='utf-8') as f:
    file_content = f.read()
    file_len = len(file_content)
    response = Selector(text=file_content)
    response_translate = file_content
    all_p_tags = response.css('*').getall()
    all_contents = response.css("#content :not(noscript,script,style) *::text").getall()
    all_contents = response.css("#content  div.content-body *::text").getall()
    test_parsed = [" ".join(i.split()) for i in all_contents if not i.isspace()]
    test_parsed_string = "\n".join(test_parsed)

    all_p_tags_texts = response.css('*::text').getall()
    all_texts.extend(all_p_tags_texts)

    all_p_tags_translations = ["test" for i in all_p_tags_texts]
    translations_dict = dict(zip(all_p_tags_texts, all_p_tags_translations))

    for i in translations_dict:
        response_translate = response_translate.replace(i, translations_dict[i])

    # for i in all_p_tags_texts:
    #     if i not in translations_dictionary:
    #         translations_dictionary[i] = translations_dict[i]

    # all_texts = response.css("*")
#
#     test_2 = response.css("#content > div.content-body > *::text").getall()
#     test_parsed = [" ".join(i.split()) for i in test_2 if not i.isspace()]
#     test_parsed_string = "\n".join(test_parsed)
#     len_test = len(test_parsed_string)
#     translate_text = translator.translate('สวัสดีจีน', lang_tgt='en')
#
#     translate_text = translator.translate(text[2], lang_tgt='en')
