# Wearable Mania

腕・指・顔・耳などにつけるウェアラブルガジェットの新製品を、1記事1製品で紹介するサイト(https://wearable.gadgetterminal.com)。
2026-11-19 に本人と決めて始めた。Gadget Terminal(`media\GadgetTerminal`)・充電沼(`media\TapMania`)の姉妹サイト。運営は Star Platinum LLC。収益は紹介料(もしも経由の楽天・Amazon・Yahoo!ショッピング)。

```
content/p/*.md(1記事1製品) → python scripts/build.py → public/ → git push で GitHub Pages に公開
```

## 決まり

- **1記事1製品の深掘りだけ。特集・まとめ記事(「◯選」・比べ記事・買い方ガイド)は書かない**(2026-11-19 本人「GT のように特集やまとめ記事は書かない。1つのガジェットをしっかり深掘りするサイトに」)。まとめを作る案は出さない
- **切り口: どの記事でも「日本で使える？」の欄で、技適と日本で使えない機能(アプリ・健康の機能・決済・言語)に答える**(2026-11-19 本人了承)。身につける物はほぼ全部が無線なので、ここが他のウェアラブルのサイト(国内はスマートウォッチライフなど)との差
- 時計・リングに限らない。顔・耳・首・服・変な物まで(部位は `config/site.yaml` の `parts`)
- 名前は英字の **Wearable Mania**。ロゴにカタカナの「ウェアラブル」を使わない(本人「ダサくない？」)。横に小さく「ウェアラブルガジェット専門」
- 書き方・技適の書き方・front matter の形は `docs/WRITING.md`。**記事を書く前に必ず読む**
- 数字は公式と出典にある物だけ。円に換算しない。「技適なし」「違法」と断定しない(見つからなければ「未確認」)
- 実機は使っていない。「レビュー」と名乗らない
- 本数は週3本まで
- もしもの GT・充電沼の a_id を貼らない。このサイトを新しく登録して、提携が通ったら `config/site.yaml` の `affiliate:` に入れる
- 日本語版 GT・充電沼のファイルは変更しない(GT の `scripts/giteki.py` は読む・動かすだけ)

## 見た目(2026-11-19 「ガラス」に作り直し)

- 本人が3つの方向(暗い地の計器風・ガラス・巨大文字が流れるモーション)から**ガラス**を選んだ。明るい地 `#EEF3F6` に緑・青・薄紫の光がゆっくり流れ、ヘッダー・カード・「日本で使える？」の欄はすりガラスの板。色は `assets/wear.css` の先頭
- **トップの大きな面は置かない**(本人「スクロールするとすぐに楽しそうなガジェットがたくさん並んでるほうが直帰率が下がる」)。頭は1行の「wearable future.」の帯だけで、すぐ一覧。最新の1本だけ2列×2段で6項目の札、ほかは6本の色の線
- 6項目の色: 緑=使える・黄=未確認・赤=使えない・灰=機能なし
- ロゴは W と M に緑の帯が編み込まれたマーク(本人が Gemini で作った `assets/brand/wm-mark-gemini.jpg`)＋ Lexend の文字(本人が10案から9番を選んだ)。マーク・ファビコン・共有用の画像は `python scripts/make_brand_images.py` で作り直せる
- 書体: 英字 Lexend(200 と 800 を混ぜる)、本文 Noto Sans JP、ラベル JetBrains Mono
- スマホ(375px)で横にはみ出さないこと。見本は `mock/`(git には入れない)

## 公開

- `python scripts/build.py` が通ってから push してよい。push すると `deploy.yml` が数分で公開する
- 住所は wearable.gadgetterminal.com(Cloudflare の CNAME → afrorz.github.io、プロキシ オフ)。手順は充電沼の `docs/subdomain-steps.md` と同じ

## コマンド(Windows)

```bash
python scripts/build.py           # public/ を作り直す
python scripts/build.py --serve   # http://localhost:8792
```
