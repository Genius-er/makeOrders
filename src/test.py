a = """1. 天长地久（朋友）XL
2. 大巍 3x
3. 梁姐 M号
4. 红酒 M
5. 墨海 M
6. 墨海 嫂子 L
7. 庞连红15663724100 XS
8. 绿杨 M
9. 王凯 2X
10. 天长地久 XL
11. SONG   XS
12. 一种生活。 L
13. 中宇 S
14. 小萱 S
15. 萱总 M
16. 家俊 X L
17. 邵野 M
18. 林义祥 2x
19. 砖头子🧱 XL
20. 宏姐 Ｌ
21. 小太阳XS
22. 老潘2x
23. 涛 XL
24. 王磊 L
25. 老师 XL
26. 丽棉.M
27. 日出东方  L
28. H3 S
29. 老周 L
30. 张哥M
31. 肉饼M
32. 志刚2x
33. 钢子🚴 XL
34. 胡彦霞 M
35. 中海 L
36. 王天宇 M
37. 董长安ＸＬ
38. 小伟 3XL
39. 柳松 L
40. 林凤斌 L
41. 莞尔 M
42. 老王Ｌ
43. 圣译XL
44. 回忆江志峰 L
45. 阳光 L
46. L L
47. 侯彦民  M
48. 米仓🚴XL
49. 淡定男孩 L
50. 清静心曦 3XL
51. 李洪伟  3XL
52. 肖哥 Ｍ
53. 小王 XXL"""

# Split the string into a list of lines
lines = a.split('\n')

# Create an empty dictionary to store the count of each size
size_count = {}

# Loop through each line
for line in lines:
    # Get the last word in the line (which should be the size)
    size = line.split(" ")[-1]
    
    # If the size is already in the dictionary, increment its count
    if size in size_count:
        size_count[size] += 1
    # Otherwise, add the size to the dictionary with a count of 1
    else:
        size_count[size] = 1

# Print the count of each size
for size, count in size_count.items():
    print(f"{size}: {count}")

