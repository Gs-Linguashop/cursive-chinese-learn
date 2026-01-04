## 更新SVG字形

`python3 src/glif_to_svg.py ../MingjianCaoshuHeiti/MingjianCaoshuHeiti.ufo "" font/MingjianCaoshuHeiti-svg/ --all_glyphs`

## 更新[草书结构字典](dictionary.md)

`python3 src/tsv_to_md_table.py ../MingjianCaoshuHeiti/src/dictionary.txt dictionary/dictionary.md`

## 更新.md文件中的字形链接

`python3 src/add_links.py dictionary/dictionary.md font/MingjianCaoshuHeiti-svg/ -o dictionary/dictionary.md --link-folder "../font/MingjianCaoshuHeiti-svg/" --exceptions-file ../MingjianCaoshuHeiti/src/dictionary.txt`

`python3 src/add_links.py practice/chars_3500_linked.md font/MingjianCaoshuHeiti-svg/ -o practice/chars_3500_linked.md --link-folder "../font/MingjianCaoshuHeiti-svg/" --exceptions-file ../MingjianCaoshuHeiti/src/dictionary.txt`

`python3 practice/src/split_md_table.py practice/chars_3500_linked.md`

`python3 practice/src/tools.py practice/chars_3500_linked.md -o practice/chars_3500_with_image.md`

## 做视频

将课件链接放在系列的README.md中

## 同步GitHub和Gitee