#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from json import load

with open("data.json", "r") as doc:
    data = load(doc)

ans1_x, ans1_y = zip(*data["ans1"])
ans2_x, ans2_y = zip(*data["ans2"])

plt.plot(ans1_x, ans1_y, "r,")
plt.plot(ans2_x, ans2_y, "ko")
plt.show()