# RESAS_APIの利用法

1. [概要](#anchor1)
1. [利用方法](#anchor2)
1. [2045年の人口予測をjsonに追加する](#anchor3)

---
<br>
<br>

<a id="anchor1"></a>
## 概要
[RESAS](https://opendata.resas-portal.go.jp/)とは地域経済分析システムであり、APIを利用することでRESASで提供されているデータを受け取ることが可能。
<br><br>提供されるデータは市町村、特許、税関、農業など様々あるので、このセクションに興味のある方はご利用前に[RESAS-APIのドキュメント](https://opendata.resas-portal.go.jp/docs/api/v1/index.html)をご確認ください。<br><br>


今回はRESASを利用して既存のjsonファイルに情報を追加することを目標とします。
<br><br>



<a id="anchor2"></a>

## 利用方法
1.ユーザー登録<br>
[こちら](https://opendata.resas-portal.go.jp/)からアクセスし右上のRESAS-API利用登録・ログインから新規登録を行います。
<br>
<br>
<br>
<br>
2.API利用準備<br>
取得したAPIキーはenvなりconfig.jsonなりで外部ファイルに保存してください。configファイルを作成する場合は.gitignoreにconfigファイルを追加してください。

```.gitignore:title
api_key.json
```

```api_key.json:title
{
	"X-API-KEY":"xxxxxxxxxxxxx"
}
```

3.実際に利用してみる<br>
まず初めに必要なライブラリをimportし、api_keyを開いて変数にいれます。
```
import json
import urllib.request
import pprint
import pandas as pd

with open('./api_key.json') as f:
    api_key = json.load(f)
```

アクセスするAPIのエンドポイントを変数として持ちます。
```
apiEndPoint = 'https://opendata.resas-portal.go.jp/'
```
以後リクエストを送る際はapiEndPointに指定されたオプションをつなげてURLを作成します。
<br>
<br>
### 演習１
東京都の[市区町村一覧](https://opendata.resas-portal.go.jp/docs/api/v1/cities.html)をjsonで作成せよ。
<br>
<br>
一応回答としてcityJson.jsonを添付します。これ以降もcityJson.jsonを利用しますのでご自身で作成されたファイルを利用したい場合は適宜入れ替えてください。<br>
<br>作成したJsonを読み込みます。
```
with open('./cityJson.json') as f:
    cityData = json.load(f)
```
<br><br>

<a id="anchor3"></a>

## 2045年の人口予測を取ってくる
[こちら](https://resas.go.jp/population-sum/#/graph/13/13101/0.0/2015/0/5.333900736553437/41.42090017812787/142.29371418128918/-)に書いてあるデータを取ってくることができるのでやってみます。<br><br>

RESAS-APIのページは[こちら](https://opendata.resas-portal.go.jp/docs/api/v1/population/sum/estimate.html)です。<br>
今回は市区町村ごとに2045年のデータを取得し、先ほど作成したJsonに追加します。<br><br>
<br>

cityDataがおわるまでcitydataに入れ続けます。つまり市区町村の最初から最後までfor文を回します。
```
i = 0 #あとで使います。
for citydata in cityData['result]: 
```
<br>
<br>

今回利用するためのURLを作成し、リクエストを飛ばします。その後リクエストを成形したものをMunicipalityという変数に保存します。
```
	urlPopulation = apiEndPoint + "api/v1/population/sum/estimate?prefCode=13&cityCode=" + citydata['cityCode']
	req = urllib.request.Request(urlPopulation, headers=api_key)
    with urllib.request.urlopen(req) as response:
        Municipality = response.read()
```
<br>
<br>
<br>
Municipalityのままだと使いにくいので一度Jsonに変換します。

```
cityJsonAddMunicipality = json.loads(Municipality)
```
<br>
なお、リクエストしたAPIは失敗することもあるので失敗した場合は何もしないというif文を加えます

```
	if not cityJsonAddMunicipality['result'] is None:
```
<br>
<br>
<br>
cityJsonAddMunicipalityに入っているJsonの要素のうち必要なのは人口の項目の2045年に該当する箇所なためそこだけを指定し、以前に作成したcityDataに加え、for文の処理は終ります。
```
        cityData['result'][i].update(cityJsonAddMunicipality['result']['data'][0]['data'][-1])
        i+=1
```
<br>

これで市区町村のJsonにデータを加えることができました。<br>
これを出力したい場合は以下のコードを記述します。今回は上書きしているので上書きしたくない場合は"cityData.json"を別のファイルに指定してください。

```
with open("cityData.json", 'w') as outfile:
    json.dump(cityData, outfile, indent=4, ensure_ascii=False)
```
<br>



