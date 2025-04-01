# README

このスクリプトは、指定した元素のスラブ（固体表面）を生成し、任意のガス分子（または原子）をランダムに配置して画像ファイルとして保存する。スクリプトはASE (Atomic Simulation Environment) ライブラリを活用しており、コマンドラインから直接実行するか、モジュールとしてインポートして利用することができる。

## 機能概要

- slabモデルを生成する
- 気相分子・原子をランダムに配置する（配置時、分子はランダムな回転も適用する）
- 配置後の構造から不要な情報を削除し、所定の画像ファイルとして出力する

## 必要要件

- [ASE (Atomic Simulation Environment)](https://wiki.fysik.dtu.dk/ase/)
- Python 3.x
- 標準ライブラリ: random, sys

## インストール

リポジトリからクローンして利用する場合:

```bash
git clone https://github.com/wakamiya0315/atomic_surface_figure.git
cd atomic_surface_figure
pip install -r requirements.txt
```

最新のコードを直接インストールするには:

```bash
pip install git+https://github.com/wakamiya0315/atomic_surface_figure.git
```

## 使用方法

### コマンドラインからの実行

#### スラブのみ生成
1. ターミナルで対象ディレクトリに移動する。
2. 下記コマンドを実行する。

```bash
python make_fcc_surface_figure.py Ag
```

この例では、AgのFCC(111)スラブ画像（"Ag.png"）が生成される。

#### スラブ＋ガス分子配置
1. ターミナルで対象ディレクトリに移動する。
2. 以下のように実行する。

```bash
python make_fcc_surface_figure.py Ni CO 10
```

この例では、NiのFCC(111)スラブにCO分子を10個ランダムに配置し、"Ni_CO_10.png" として画像が保存される。

### モジュールとしての利用

Pythonスクリプト内で関数を直接呼び出すことも可能である。以下は利用例である。

```python
from atmic_surface_figure import make_fcc_surface_figure

# NiのスラブにCO分子を10個配置して "Ni_CO_10.png" として保存する
make_fcc_surface_figure("Ni", "CO", 10)
```

## 関数詳細

### create_slab(element)

指定された元素のFCC(111)面スラブを生成する。  
- 引数:  
    • element - 元素記号（例: "Ag", "Ni"）  
- 戻り値:  
    • 生成されたスラブオブジェクト  

内部では `ase.build.fcc111` を用いてスラブを生成し、サイズや真空層の厚みを設定する。

### add_gas(slab, gas, n)

引数のスラブ上に、指定されたガス分子または原子をランダム配置する。  
- 引数:  
    • slab - スラブオブジェクト  
    • gas - ガス分子の名称（例: "CO"）または原子記号  
    • n - 配置する数  
- 処理内容:  
    • スラブのセル寸法を取得し、各分子の配置位置（x, y, z）をランダムに設定する  
    • 分子生成に失敗した場合は、単一原子として配置する  
    • 分子にはランダムなEuler角で回転を適用し、中心位置に基づき平行移動する

### make_fcc_surface_figure(slab_element, gas_element=None, gas_count=None, image_name=None)

スラブの生成、必要に応じたガス分子の追加、画像出力の一連の処理を行う。  
- 引数:  
    • slab_element - 生成するスラブの元素  
    • gas_element - （オプション）ガス分子または原子の名称  
    • gas_count - （オプション）追加するガスの個数  
    • image_name - （オプション）保存される画像のファイル名（未指定の場合、デフォルト名が設定される）  
- 戻り値:  
    • 最終的なスラブオブジェクト  
- 注意点:  
    • スラブ生成後、不要なadsorbate情報が削除され、ASEの`write`メソッドを利用して画像が保存される。

## 実行時の注意点

- コマンドライン実行時、引数の数が誤っている場合はエラーメッセージが表示され、使い方を案内する。
- ガスとして配置する分子の生成に失敗した場合は、個別の原子としてスラブに追加されるフォールバック処理が実装される。

## 将来的な拡張の可能性

現在はFCC(111)面のみの対応だが、今後は他の表面（例: BCC）のサポートも検討中である。  
例:  
• from surface_figure import make_fcc_surface_figure  
• from surface_figure import make_bcc_surface_figure
