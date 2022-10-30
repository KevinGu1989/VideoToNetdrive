
import yaml
import os
# 打开yaml文件
fs = open(os.path.join('./', "config.yaml"),encoding="UTF-8")
datas = yaml.load(fs, Loader=yaml.FullLoader)
print(datas)