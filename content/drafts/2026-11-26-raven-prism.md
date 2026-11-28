---
title: "Raven Resonance「Raven Prism」は目で操作する Linux のメガネ、電池はつるごと差し替え・1,499ドル"
slug: raven-prism
date: 2026-11-26
part: face
maker: Raven Resonance
model: Raven Prism 1
summary: "見るだけで選び、つるの先の電池を電源を切らずに替える。米サンフランシスコの会社が作る、スマホの要らない Linux のメガネ型コンピューター"
thumbnail: /img/raven-prism/thumb.jpg
thumbnail_crop: [300, 0, 1110, 675, 1200]   # 右のレンズと RAVEN の文字を枠いっぱいに見せる
thumbnail_credit: Raven Resonance 公式サイト
price: "1,499ドル(米国、予約金49ドル、掲載時点)"
status: overseas
get: "米国の公式サイトで予約受付中(予約金49ドル、全額返金可)。本体は1,499ドルで、いま予約すると出荷は2027年夏"
jp:
  giteki: {mark: q, text: "Wi-Fi と Bluetooth を使う。型番が公式に無く、総務省の検索では見つからない(掲載時点)"}
  buy: {mark: ng, text: "いまの出荷先は米国だけ。次は EU で、日本の予定は書かれていない"}
  app: {mark: q, text: "スマホのアプリは要らず、メガネの中の Raven OS で動く。日本語のアプリは未確認"}
  lang: {mark: q, text: "公式サイトは英語だけ。日本語の表示や入力は未確認"}
  verdict: "日本へは送ってもらえず、米国でも新しい予約は2027年夏の出荷になる。日本に向けた発表があるまでは見送り、国内で表示つきのメガネが欲しいなら Even G2 が近い"
specs:
  - ["表示", "右目だけ。フルカラーの回折導波路、光源は LCoS。視線の少し外側に出す"]
  - ["視野角", "30°(対角)"]
  - ["明るさ", "1,500ニト以上"]
  - ["操作", "目の動き(Pupil Labs と共同のモデル)。Bluetooth のキーボード・マウス・コントローラー"]
  - ["プロセッサ", "4コアの64bit ARM。目の操作は本体の FPGA で処理"]
  - ["メモリ・保存", "RAM は最大4GB、保存は32GB以上"]
  - ["OS", "Raven OS(独自の Linux)"]
  - ["カメラ", "1,300万画素、水平84°。手で外すカバー付き"]
  - ["マイク・スピーカー", "マイク4つ、スピーカー2つ"]
  - ["通信", "Wi-Fi(2.4GHz・5GHz)、Bluetooth 5"]
  - ["電池", "Raven Wings(つるの先の差し替え式)。2組と充電ケースが付く"]
  - ["度付き", "内蔵。いまの順番は −4.5〜+4.5、乱視 ±3.0"]
  - ["重さ", "70g未満(It's FOSS の報道。公式は無し)"]
alternatives:
  - name: "Even G2"
    why: "国内で買える、レンズに文字を映すメガネ。36gでカメラが無く、度付きにもできる。99,800円から(掲載時点)"
    query: "Even G2 スマートグラス"
sources:
  - title: "Raven Prism"
    url: "https://raven.computer/"
    publisher: "Raven Resonance 公式サイト"
  - title: "Reserve Raven Prism"
    url: "https://raven.computer/reserve"
    publisher: "Raven Resonance 公式サイト"
  - title: "Developer"
    url: "https://raven.computer/developer"
    publisher: "Raven Resonance 公式サイト"
  - title: "Raven Prism Smart Glasses Announced with Unique Hot-swappable Battery"
    url: "https://roadtovr.com/raven-prism-smart-glasses-reveal-awe-2026/"
    publisher: "Road to VR"
  - title: "Raven Prism impressions"
    url: "https://skarredghost.com/2026/08/06/raven-prism-impressions/"
    publisher: "The Ghost Howls"
  - title: "Raven Prism Linux smart glasses"
    url: "https://itsfoss.com/news/raven-prism-linux-smart-glass/"
    publisher: "It's FOSS"
  - title: "Raven Resonance Prism Linux smart glasses"
    url: "https://newatlas.com/wearables/raven-resonance-prism-linux-smart-glasses/"
    publisher: "New Atlas"
---

Raven Prism は、スマホにつながなくても単体で動く、Linux のメガネ型コンピューターだ。画面は見るだけで操作し、電池はつるの先ごと、電源を切らずに差し替える。米サンフランシスコの Raven Resonance が6月の AWE 2026 で初めて見せ、いまは米国で1,499ドルの予約を受けている。

## 仕組み

表示は右目だけで、視線の少し外側に出す。フルカラーの回折導波路に LCoS の光源を組み合わせ、視野角は対角30°、明るさは1,500ニト以上。正面の景色をふさがず、目を少し向けたときに情報が見える置き方だ。

![RAVEN の文字が入った Raven Prism 1。フレームの一部が透明(公式サイトの画像)](/img/raven-prism/thumb.jpg "Raven Resonance 公式サイト")

一番の特徴は操作だ。フレームに目の動きを読むセンサーがあり、見ることで項目を選ぶ。読み取りのモデルは、視線計測の Pupil Labs と共同で作り、メガネの中の専用の FPGA で動かす。公式によると、声の認識も本体の中で処理する。Bluetooth のキーボード・マウス・コントローラーもそのまま使える。

中身は4コアの64bit ARM のプロセッサで、RAM は最大4GB、保存は32GB以上。OS は自社の Linux「Raven OS」で、開発者は SSH で入れる。アプリを作る道具(SDK)は GitHub で公開している。通信は Wi-Fi と Bluetooth 5 で、スマホが無くてもネットにつながる。

## 電池の差し替え

電池は「Raven Wings」という、つるの先の細長い部品に入っている。Wings を外して付け替えると、電源を切らずに電池が替わる。The Ghost Howls の実機の記事によると、左右のつるに1本ずつ入り、差し替えの間はフレームの中の小さな電池で動き続ける。

![つるの先の Raven Wings を外しているところ(公式サイトの画像)](/img/raven-prism/swap.webp "Raven Resonance 公式サイト")

箱には Wings が2組と、持ち歩いて Wings を充電するケースが入る。1組でどれだけもつかは、公式に書かれていない。

![付属の Raven Wings 2組。予備を充電しておいて差し替える(公式サイトの画像)](/img/raven-prism/wings.webp "Raven Resonance 公式サイト")

## 使う場面

公式サイトが見せているのは、町を歩きながらスマホから送った道案内を見る、料理をしながらレシピを見る、ニュースやポッドキャストを追う、ブラウザで YouTube を見るといった場面だ。料理のように手が汚れていても、スマホに触らずに済む。

![料理の手順を視界の端に出す(公式サイトのイメージ画像)](/img/raven-prism/cooking.webp "Raven Resonance 公式サイト")

カメラは1,300万画素で、横84°を写す。前に手で外すカバーがあり、付けている間はどのソフトもカメラを使えない。使っている間はリムの「Beakon Lights」が光り、周りの人にも撮っているかがわかる。

度付きのレンズはメガネに組み込む。いまの順番では −4.5〜+4.5、乱視は ±3.0 まで作れる。度は、送り返せばあとで変えられる。

## 近い製品との違い

| | Raven Prism 1 | Even G2 |
|---|---|---|
| 表示 | 右目、フルカラー、30° | 両目、緑、27.5° |
| 明るさ | 1,500ニト以上 | 1,200ニト |
| カメラ | 1,300万画素(カバー付き) | なし |
| スマホ | 要らない(単体で動く) | 要る |
| 度付き | −4.5〜+4.5 | −12.00〜+12.00 |
| 重さ | 70g未満(報道) | 36g |
| 価格 | 1,499ドル(米国) | 99,800円から(国内) |

Even G2 の数字は、このサイトの Even G2 の記事に書いた公式の値。Raven Prism は単体で動くぶん、Even G2 より重く、値段も高い。

## 気になるところ

- 出荷先はいま米国だけ。次は EU で、日本の名前は無い
- いま予約できるのは5番目の順番で、出荷は2027年夏。最初の順番も2027年1月で、AWE のころに報じられた年内の発売から遅れた
- 重さと電池の持ちが、公式に書かれていない
- The Ghost Howls の筆者は、見たのが初期の試作機と断ったうえで、30°を狭く感じ、片目の表示は自分には合わないと書いている
- 初めての製品で、量産の実績はまだ無い

![持ち歩いて Wings を充電するケース(公式サイトの画像)](/img/raven-prism/case.webp "Raven Resonance 公式サイト")

## 発売と価格

価格は1,499ドルで、度付きのレンズも含む(掲載時点)。予約は公式サイトだけで受け付け、49ドルの予約金は全額返金できる。残りは自分の順番が出荷される前に払う。組み立てと検査、出荷は米国で行う。
