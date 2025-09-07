# 做视频

将课件链接放在系列的README.md中

# 更新SVG字形

`python3 src/glif_to_svg.py src/JingdianCaoshuHeiti.ufo "" src/JingdianCaoshuHeiti-svg/ --all_glyphs`

# 更新.md文件中的字形链接

`python3 src/add_links.py dictionary/dictionary.md src/JingdianCaoshuHeiti-svg/ -o dictionary/dictionary.md --link-folder "../src/JingdianCaoshuHeiti-svg/"`

`python3 src/add_links.py practice/chars_3500_linked.md src/JingdianCaoshuHeiti-svg/ -o practice/chars_3500_linked.md --link-folder "../src/JingdianCaoshuHeiti-svg/"`

`python3 practice/src/tools.py practice/chars_3500_linked.md -o practice/chars_3500_with_image.md`