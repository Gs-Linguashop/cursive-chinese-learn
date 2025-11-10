# 做视频

将课件链接放在系列的README.md中

# 更新UFO字形

保存更新文件。更新介绍文档。

# 更新SVG字形

`python3 src/glif_to_svg.py font/MingjianCaoshuHeiti.ufo "" src/MingjianCaoshuHeiti-svg/ --all_glyphs`

# 更新.md文件中的字形链接

`python3 src/add_links.py dictionary/dictionary.md src/MingjianCaoshuHeiti-svg/ -o dictionary/dictionary.md --link-folder "../src/MingjianCaoshuHeiti-svg/"`

`python3 src/add_links.py practice/chars_3500_linked.md src/MingjianCaoshuHeiti-svg/ -o practice/chars_3500_linked.md --link-folder "../src/MingjianCaoshuHeiti-svg/"`

`python3 practice/src/tools.py practice/chars_3500_linked.md -o practice/chars_3500_with_image.md`

# 同步GitHub和Gitee