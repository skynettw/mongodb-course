data = list()
score = input("輸入學生分數：")
while score != "":
    data.append(int(score))
    score = input("輸入學生分數：")

print("全部學生的分數：", data)
print("最高分：", max(data))
print("最低分：", min(data))
print("平均分：", sum(data) / len(data))
