import sys
from collections import defaultdict
import pyperclip
import requests
from lxml import html
import cssselect


def pluralize(noun='', lang='all', noclip=False):
    """
    A script that checks for plural noun forms on Wiktionary.
    The script can take three arguments, all of which are optional.
    First - word.
    Second - language.
    Third - flag signifying if the output should be copied to clipboard.
    When function run as a script, the last argument should be 'noclip' to set the flag to False.
    For nouns consisting of two and more words, please, use underscore (_) instead of space.
    Note that if a few forms are returned as output, they may vary in meaning.

    Example input 1:
        wiktionary_pluralize.py person en
    Output 1:
        The output below has been copied to the clipboard.
        people or persons
    
    Example input 2:
        python wiktionary_pluralize.py день
    Output 2:
        ru: дни
        uk: дні

    Example input 3:
        python wiktionary_pluralize.py lehti fi noclip
    Output 2:
        lehdet
    """
    
    if not noun:
        noun = input('What noun do you want to pluralize? Type it: ').strip().replace(' ', '_')

    page = requests.get('https://en.wiktionary.org/wiki/' + noun)
    tree = html.fromstring(page.content)

    if 'Wiktionary does not yet have an entry' in tree.xpath('//*[@id="mw-content-text"]/div[1]/div/b'):
        return f'\Wiktionary does not yet have an entry for {noun}.'

    #for languages with plurals between perenthesis
    word_path = '//*[@id="mw-content-text"]/div[1]/p/strong'

    #else table before hr

    langs_plurals_dict = defaultdict(set)
    for word_tag in tree.xpath(word_path):
        #path to check for part of speech
        if 'Noun' in word_tag.getparent().getprevious().text_content():

            #checking if there's a plural form in parenthesis after the noun
            for i_tag in word_tag.getparent().findall('i'):
                if i_tag.text_content() in ['masculine plural', 'feminine plural', 'nominative plural', 'plural']:
                    #getting plural form from parenthesis
                    plural_form_tag = i_tag.getnext()
                    langs_plurals_dict[plural_form_tag.attrib['lang']].add(plural_form_tag.text_content())
                    #for cases like: person (plural persons or (by suppletion) people)
                    if plural_form_tag.getnext() is not None and (next_tag := plural_form_tag.getnext()).text_content() == 'or':
                        #stepping over following tags that don't have lang attribute
                        while not next_tag.get('lang'):
                            next_tag = next_tag.getnext()
                        langs_plurals_dict[plural_form_tag.attrib['lang']].add(next_tag.text_content())

            #checking for declension table
            else:
                next_tag = word_tag.getparent().getnext()
                while next_tag.getnext() is not None and (next_tag := next_tag.getnext()).tag != 'hr':
                    if next_tag.tag == 'table':
                        for el in next_tag.findall('tbody/tr/th[@class="case-column"]'):
                            if el.text_content() == '\n':
                                for i, th in enumerate(el.getparent().getchildren()):
                                    if th.text_content() == 'plural\n':
                                        #to get td tag right beneath plural column subsract 1
                                        td_index = i - 1
                                        break
                                #going to the next row and getting the plural form from there
                                language = el.getparent().getnext().cssselect('td')[td_index].getchildren()[0].attrib['lang']
                                plural_form = el.getparent().getnext().cssselect('td')[td_index].text_content().strip()
                                langs_plurals_dict[language].add(plural_form)


    if not langs_plurals_dict or lang == 'noclip':
        print('\nEither no plural form for the word is available or incorrect input.')
        print(pluralize.__doc__)
    elif lang == 'all':
        for lang, plurals in langs_plurals_dict.items():
            plurals = ' or '.join(plurals)
            print(f'{lang}: {plurals}')
    else:
        if not noclip:
            pyperclip.copy(' or '.join(langs_plurals_dict[lang]))
            print('The output below has been copied to the clipboard.')
        print(' or '.join(langs_plurals_dict[lang]))


if __name__ == '__main__':
    # execute only if run as a script
    if len(sys.argv) == 1:
        pluralize(noclip=True)
    elif len(sys.argv) == 2:
        flag = True if sys.argv[1] == 'noclip' else False
        if flag:
            pluralize(noclip=flag)
        else:
            pluralize(noun=sys.argv[1], noclip=flag)
    elif len(sys.argv) == 3:
        pluralize(noun=sys.argv[1], lang=sys.argv[2], noclip=False)
    elif len(sys.argv) == 4:
        flag = True if sys.argv[3] == 'noclip' else False
        pluralize(noun=sys.argv[1], lang=sys.argv[2], noclip=flag)
    else:
        print("\nIf you're trying to provide a noun consisting of two words, please, use underscore (_) instead of space.")
