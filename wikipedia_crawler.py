import nltk as nltk
import os, subprocess
import wikipediaapi
import time

outDir = 'wikisummaries'

if not os.path.isdir(outDir):
    subprocess.call(['mkdir', outDir])

'''

pages = ['Yoghurt', 'Milk', 'Wine', 'Probiotics', 'Kimchi', 'Kefir', 'Cheese',
    'Tempeh', 'Miso', 'Sauerkraut', 'Dairy', 'Buttermilk', 'Natto', 'Rye bread']

for page in pages:
    with open('%s/wiki_%s.txt' % (outDir, page), 'w') as f:
        f.write(wikipedia.WikipediaPage(page).content)
'''

wiki_wiki = wikipediaapi.Wikipedia('en')
genecats = wiki_wiki.page("Category:Physics")
# print(genecats.summary)
# print(nltk.sent_tokenize(genecats.summary))
all_cats = set()
counter = 0


def print_categorymembers(categorymembers, file_name_prepend, lines, level=0, max_level=20):
    for c in categorymembers.values():
        # print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
        if c.namespace == wikipediaapi.Namespace.CATEGORY and level < max_level and c.title not in all_cats:
            if c.title in all_cats:
                print("ALERT " + c.title)
            else:
                all_cats.add(c.title)
            try:
                next_cat_members = c.categorymembers
                lines.extend(print_categorymembers(next_cat_members, file_name_prepend, lines, level=level + 1,
                                                   max_level=max_level))
                for cat in c.categorymembers:
                    try:
                        page = wiki_wiki.page(cat)
                        summary = page.summary
                        sentences = nltk.sent_tokenize(summary)
                        lines.extend(sentences)
                    except:
                        print("#Exception reading " + str(cat))
                    # with open('%s/%s.txt' % (outDir, "error_log"), 'a+') as errorFile:
                    # errorFile.write("\n" % str(cat))
                    # errorFile.close()

                    if len(lines) > 100:
                        time_str = str(time.time()).replace('.', '_')
                        with open('%s/%s_%s.txt' % (outDir, file_name_prepend, time_str), 'w') as f:
                            for item in lines:
                                f.write("%s\n" % item)
                            f.close()
                        lines.clear()
            except:
                print("#Exception reading cat " + str(c))
    # with open('%s/%s.txt' % (outDir, "error_log"), 'a+') as errorFile:
    # errorFile.write("\n" % str(c))
    # errorFile.close()

    return lines


# cat = wiki_wiki.page("Category:Genes_by_human_chromosome")
cat = wiki_wiki.page("Category:Life_sciences")
print("Category members: Category:Life_sciences")
lines = print_categorymembers(cat.categorymembers, "life_sci", [])

with open('%s/%s_%s.txt' % (outDir, "life_sci", "end"), 'w') as f:
    for item in lines:
        f.write("%s\n" % item)
    f.close()

# print(cat.categorymembers.values())
# print(cat.categorymembers.__sizeof__())
