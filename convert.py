import json
import pickle

# pickleファイルを読み込む
with open('kanedaceo.pickle', 'rb') as f:
    data = pickle.load(f)

# PythonオブジェクトをJSONに変換する
json_data = json.dumps(data)

# JSONファイルに書き込む
with open('example.json', 'w') as f:
    f.write(json_data)