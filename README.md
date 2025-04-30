# ListMajorFacilities

## What it does

主要な施設をクエリし，施設名と座標をファイルへ出力

## How it works

OpenStreetMapsのOverPassAPIを使用．

なお，クエリしているのは:

Tag: 'amenity','leisure','shop','tourism','historic'\
Element: 'node','way'(Work-in-progress)

クエリ -> response_XXX.json (クエリ出力) -> 整形 -> output_XXX.txt (施設名＋座標)

### Execution time

体感では札幌のnodeだけなら1分もかからない程度

## Limitations

- wayに分類されるもの中規模以上の建物や敷地（公園等）は未実装
- 整形時に若干フィルタしていますが，適切がどうかは微妙
  - name:ja, name タグがないもの (ie. "name:en","name:zh", "name:ja-XX"などのみを持っているelement)
