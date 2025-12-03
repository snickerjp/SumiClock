# 設計書

## 概要

テンプレートベースの時計画像生成システムは、Figmaなどのデザインツールで作成したSVGテンプレートを使用して、動的に時刻情報を合成した画像を生成します。これにより、プログラムでの描画に比べて、より柔軟で美しいデザインが可能になります。

## アーキテクチャ

### システム構成

```
┌─────────────────────────────────────────────────────────┐
│                     FastAPI Application                  │
│  ┌────────────────────────────────────────────────────┐ │
│  │              /clock.png エンドポイント              │ │
│  └────────────────┬───────────────────────────────────┘ │
│                   │                                      │
│  ┌────────────────▼───────────────────────────────────┐ │
│  │           TemplateClockGenerator                    │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  1. テンプレート読み込み                      │  │ │
│  │  │  2. レイアウト設定読み込み                    │  │ │
│  │  │  3. 動的データ生成（時刻、日付）              │  │ │
│  │  │  4. SVG処理・合成                            │  │ │
│  │  │  5. PNG変換                                  │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    ファイルシステム                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ templates/   │  │ layouts/     │  │ config.yaml  │  │
│  │  - clock.svg │  │  - clock.yml │  │              │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                         Redis                            │
│              (生成画像のキャッシュ)                       │
└─────────────────────────────────────────────────────────┘
```

### レイヤー構成

1. **APIレイヤー** (`src/api.py`)
   - HTTPリクエストの処理
   - キャッシュ管理
   - エラーハンドリング

2. **ジェネレーターレイヤー** (`src/template_clock_generator.py`)
   - テンプレート処理
   - 画像合成
   - ビジネスロジック

3. **データレイヤー** (`src/template_loader.py`, `src/layout_config.py`)
   - テンプレートファイルの読み込み
   - レイアウト設定の読み込み・検証

## コンポーネントとインターフェース

### 1. TemplateClockGenerator

テンプレートベースの時計画像生成を担当するメインクラス。

```python
class TemplateClockGenerator:
    """SVGテンプレートを使用して時計画像を生成する"""
    
    def __init__(
        self,
        template_path: str,
        layout_config_path: str,
        timezone: str = "UTC"
    ):
        """
        Args:
            template_path: SVGテンプレートファイルのパス
            layout_config_path: レイアウト設定ファイルのパス
            timezone: タイムゾーン（IANA形式）
        """
        pass
    
    def create_clock_image(self) -> Image.Image:
        """
        現在時刻を使用して時計画像を生成
        
        Returns:
            PIL Image オブジェクト（グレースケールモード）
        
        Raises:
            TemplateNotFoundError: テンプレートファイルが見つからない
            LayoutConfigError: レイアウト設定が不正
            SVGProcessingError: SVG処理に失敗
        """
        pass
```

### 2. TemplateLoader

テンプレートファイルの読み込みとキャッシュを管理。

```python
class TemplateLoader:
    """テンプレートファイルの読み込みとキャッシュ管理"""
    
    def __init__(self, templates_dir: str = "templates"):
        """
        Args:
            templates_dir: テンプレートディレクトリのパス
        """
        pass
    
    def load_svg_template(self, template_name: str) -> str:
        """
        SVGテンプレートを文字列として読み込む
        
        Args:
            template_name: テンプレートファイル名
        
        Returns:
            SVGファイルの内容（文字列）
        
        Raises:
            TemplateNotFoundError: ファイルが見つからない
        """
        pass
    
    def clear_cache(self) -> None:
        """キャッシュをクリア"""
        pass
```

### 3. LayoutConfig

レイアウト設定の読み込みと検証。

```python
@dataclass
class TextElement:
    """テキスト要素の設定"""
    x: int
    y: int
    font_family: str
    font_size: int
    color: str
    align: str  # "left", "center", "right"
    placeholder: str  # SVG内のプレースホルダー名

@dataclass
class LayoutConfig:
    """レイアウト設定"""
    template_name: str
    width: int
    height: int
    time_element: TextElement
    date_element: Optional[TextElement] = None
    
    @classmethod
    def from_yaml(cls, yaml_path: str) -> "LayoutConfig":
        """
        YAMLファイルからレイアウト設定を読み込む
        
        Args:
            yaml_path: YAMLファイルのパス
        
        Returns:
            LayoutConfig インスタンス
        
        Raises:
            LayoutConfigError: 設定が不正
        """
        pass
    
    def validate(self) -> None:
        """
        設定値を検証
        
        Raises:
            LayoutConfigError: 検証エラー
        """
        pass
```

### 4. SVGProcessor

SVGテンプレートの処理とPNG変換。

```python
class SVGProcessor:
    """SVGテンプレートの処理"""
    
    def replace_placeholders(
        self,
        svg_content: str,
        replacements: Dict[str, str]
    ) -> str:
        """
        SVG内のプレースホルダーを置換
        
        Args:
            svg_content: SVGファイルの内容
            replacements: プレースホルダーと置換値の辞書
        
        Returns:
            置換後のSVG文字列
        """
        pass
    
    def svg_to_png(
        self,
        svg_content: str,
        width: int,
        height: int
    ) -> Image.Image:
        """
        SVGをPNG画像に変換
        
        Args:
            svg_content: SVG文字列
            width: 出力画像の幅
            height: 出力画像の高さ
        
        Returns:
            PIL Image オブジェクト
        
        Raises:
            SVGProcessingError: 変換に失敗
        """
        pass
```

## データモデル

### テンプレートファイル構造

```
templates/
├── clock-minimal.svg          # ミニマルデザイン
├── clock-with-date.svg        # 日付付きデザイン
└── clock-weather.svg          # 天気情報付き（将来）
```

### レイアウト設定ファイル（YAML）

```yaml
# layouts/clock-minimal.yml
template_name: "clock-minimal.svg"
width: 1448
height: 1072

time_element:
  placeholder: "{{TIME}}"
  x: 724  # 中央
  y: 536  # 中央
  font_family: "Noto Sans CJK"
  font_size: 200
  color: "#000000"
  align: "center"

date_element:
  placeholder: "{{DATE}}"
  x: 724
  y: 700
  font_family: "Noto Sans CJK"
  font_size: 60
  color: "#000000"
  align: "center"
```

### SVGテンプレート例

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg width="1448" height="1072" xmlns="http://www.w3.org/2000/svg">
  <!-- 背景 -->
  <rect width="1448" height="1072" fill="#FFFFFF"/>
  
  <!-- 装飾要素 -->
  <circle cx="724" cy="200" r="50" fill="none" stroke="#000000" stroke-width="2"/>
  
  <!-- 時刻プレースホルダー -->
  <text 
    x="724" 
    y="536" 
    font-family="Noto Sans CJK" 
    font-size="200" 
    text-anchor="middle" 
    fill="#000000">
    {{TIME}}
  </text>
  
  <!-- 日付プレースホルダー -->
  <text 
    x="724" 
    y="700" 
    font-family="Noto Sans CJK" 
    font-size="60" 
    text-anchor="middle" 
    fill="#000000">
    {{DATE}}
  </text>
</svg>
```

### 設定ファイル（config.yaml）

```yaml
redis:
  host: redis
  port: 6379
  cache_expire_seconds: 30

clock:
  timezone: "Asia/Tokyo"
  
  # テンプレートモード設定
  use_template: true  # false の場合は既存の描画方式
  template_name: "clock-minimal.svg"
  layout_config: "layouts/clock-minimal.yml"
  
  # フォールバック設定（既存）
  width: 1448
  height: 1072
  font_size: 200
  font_path: /usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc
```

## 正確性プロパティ

*プロパティとは、システムのすべての有効な実行において真であるべき特性や動作のことです。これは、人間が読める仕様と機械で検証可能な正確性保証の橋渡しとなります。*

### プロパティ1: テンプレート読み込みの冪等性

*任意の*テンプレートファイルに対して、同じファイルを複数回読み込んでも、同じ内容が返されること

**検証: 要件1.1**

### プロパティ2: プレースホルダー置換の完全性

*任意の*SVGテンプレートと置換辞書に対して、すべてのプレースホルダーが正確に置換され、置換後のSVGに元のプレースホルダーが残っていないこと

**検証: 要件4.2**

### プロパティ3: 画像サイズの保持

*任意の*レイアウト設定に対して、生成される画像のサイズが設定で指定された幅と高さと一致すること

**検証: 要件3.4, 4.4**

### プロパティ4: タイムゾーン変換の正確性

*任意の*タイムゾーンに対して、生成される時刻文字列が指定されたタイムゾーンの現在時刻を正確に表していること

**検証: 要件3.3**

### プロパティ5: レイアウト設定の検証

*任意の*不正なレイアウト設定（負の座標、無効なフォントサイズなど）に対して、システムが適切な検証エラーを発生させること

**検証: 要件2.5**

### プロパティ6: グレースケール出力の保証

*任意の*テンプレートに対して、生成される画像が常にグレースケールモード（'L'）であること

**検証: 要件3.5**

### プロパティ7: SVG-PNG変換のラウンドトリップ

*任意の*有効なSVGに対して、PNG変換後の画像が元のSVGの視覚的表現を保持していること（ピクセル単位での完全一致ではなく、視覚的等価性）

**検証: 要件4.3**

## エラーハンドリング

### カスタム例外

```python
class TemplateSystemError(Exception):
    """テンプレートシステムの基底例外"""
    pass

class TemplateNotFoundError(TemplateSystemError):
    """テンプレートファイルが見つからない"""
    pass

class LayoutConfigError(TemplateSystemError):
    """レイアウト設定エラー"""
    pass

class SVGProcessingError(TemplateSystemError):
    """SVG処理エラー"""
    pass
```

### エラーハンドリング戦略

1. **ファイル読み込みエラー**
   - テンプレートファイルが見つからない → `TemplateNotFoundError`
   - レイアウト設定ファイルが見つからない → `LayoutConfigError`
   - ログに詳細なパス情報を記録

2. **設定検証エラー**
   - 不正な座標値 → `LayoutConfigError` with 詳細メッセージ
   - 無効なフォント設定 → `LayoutConfigError` with 詳細メッセージ

3. **SVG処理エラー**
   - SVG解析失敗 → `SVGProcessingError`
   - PNG変換失敗 → `SVGProcessingError`
   - 詳細なスタックトレースをログに記録

4. **フォールバック**
   - テンプレートモードが失敗した場合、既存の描画方式にフォールバック
   - フォールバックが発生したことをログに記録

## テスト戦略

### ユニットテスト

1. **TemplateLoader**
   - テンプレートファイルの読み込み
   - キャッシュ機能
   - ファイルが見つからない場合のエラー

2. **LayoutConfig**
   - YAML読み込み
   - 設定検証
   - 不正な設定値の検出

3. **SVGProcessor**
   - プレースホルダー置換
   - SVG-PNG変換
   - エラーハンドリング

4. **TemplateClockGenerator**
   - 画像生成
   - タイムゾーン処理
   - 統合動作

### プロパティベーステスト

各正確性プロパティに対して、プロパティベーステストを実装：

1. **Hypothesis**ライブラリを使用
2. 各テストは最低100回の反復実行
3. ランダムな入力データを生成してプロパティを検証
4. テストコメントに対応するプロパティ番号を明記

```python
# Feature: template-system, Property 1: テンプレート読み込みの冪等性
@given(st.text(min_size=1, max_size=50))
def test_template_loading_idempotency(template_name):
    """同じテンプレートを複数回読み込んでも同じ結果が返される"""
    loader = TemplateLoader()
    result1 = loader.load_svg_template(template_name)
    result2 = loader.load_svg_template(template_name)
    assert result1 == result2
```

### 統合テスト

1. **エンドツーエンドテスト**
   - `/clock.png` エンドポイントのテスト
   - テンプレートモードと既存モードの両方
   - キャッシュ動作の検証

2. **ビジュアルリグレッションテスト**
   - 生成画像のスナップショット比較
   - デザイン変更の検出

## パフォーマンス考慮事項

### 最適化戦略

1. **テンプレートキャッシング**
   - 初回読み込み時にメモリにキャッシュ
   - アプリケーション起動時にプリロード

2. **SVG処理の最適化**
   - cairosvgの設定最適化
   - 不要な処理のスキップ

3. **画像生成キャッシング**
   - 既存のRedisキャッシュを活用
   - キャッシュキーにテンプレート名を含める

### パフォーマンス目標

- テンプレート読み込み: < 10ms（キャッシュヒット時）
- SVG処理: < 100ms
- 全体の画像生成: < 200ms（キャッシュミス時）
- キャッシュヒット時: < 10ms

## セキュリティ考慮事項

1. **ファイルパスの検証**
   - ディレクトリトラバーサル攻撃の防止
   - 許可されたディレクトリ内のファイルのみアクセス

2. **SVG処理のサンドボックス化**
   - 外部リソースの読み込み制限
   - スクリプト実行の無効化

3. **入力検証**
   - レイアウト設定値の範囲チェック
   - プレースホルダー名の検証

## デプロイメント

### Docker対応

```dockerfile
# 追加の依存関係
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libcairo2-dev \
    libpango1.0-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# テンプレートファイルのコピー
COPY templates/ ./templates/
COPY layouts/ ./layouts/
```

### 環境変数

```bash
# テンプレートモードの有効化
SUMICLOCK_USE_TEMPLATE=true
SUMICLOCK_TEMPLATE_NAME=clock-minimal.svg
SUMICLOCK_LAYOUT_CONFIG=layouts/clock-minimal.yml
```

## 将来の拡張

1. **複数テンプレートのサポート**
   - APIパラメータでテンプレート選択
   - テンプレートのホットスワップ

2. **動的要素の追加**
   - 天気情報
   - バッテリー残量
   - カスタムメッセージ

3. **テンプレートエディタ**
   - Web UIでのテンプレート編集
   - リアルタイムプレビュー

4. **PNGテンプレートサポート**
   - SVGが使えない環境向け
   - レイヤー合成方式
