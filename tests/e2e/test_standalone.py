"""
スタンドアロン版 index.html のE2Eテスト

ブラウザ自動化（Selenium/Playwright）なしで、
index.htmlの構造とスクリプトの基本的な整合性を検証します。
"""

import re
from pathlib import Path

import pytest


@pytest.mark.e2e
def test_standalone_index_html_exists():
    """index.htmlがリポジトリルートに存在することを確認"""
    repo_root = Path(__file__).resolve().parents[2]
    index_path = repo_root / "index.html"
    assert index_path.exists(), "index.htmlが存在しません"
    assert index_path.is_file(), "index.htmlがファイルではありません"


@pytest.mark.e2e
def test_standalone_index_html_has_standalone_mode():
    """index.htmlにSTANDALONE_MODE = true が設定されていることを確認"""
    repo_root = Path(__file__).resolve().parents[2]
    index_path = repo_root / "index.html"
    content = index_path.read_text(encoding="utf-8")
    
    # STANDALONE_MODE = true を検索
    pattern = r"const\s+STANDALONE_MODE\s*=\s*true"
    assert re.search(pattern, content), "STANDALONE_MODE = true が見つかりません"


@pytest.mark.e2e
def test_standalone_index_html_has_required_cdn_libraries():
    """必要なCDNライブラリ（React, PDF.js, PptxGenJS等）が読み込まれていることを確認"""
    repo_root = Path(__file__).resolve().parents[2]
    index_path = repo_root / "index.html"
    content = index_path.read_text(encoding="utf-8")
    
    required_cdns = [
        "unpkg.com/react@18",  # React
        "unpkg.com/react-dom@18",  # ReactDOM
        "unpkg.com/@babel/standalone",  # Babel
        "cdnjs.cloudflare.com/ajax/libs/pdf.js",  # PDF.js
        "unpkg.com/pptxgenjs",  # PptxGenJS
        "cdn.tailwindcss.com",  # Tailwind CSS
    ]
    
    for cdn in required_cdns:
        assert cdn in content, f"CDN {cdn} が見つかりません"


@pytest.mark.e2e
def test_standalone_index_html_has_web_speech_api():
    """Web Speech API（speechSynthesis）の使用が確認できることを確認"""
    repo_root = Path(__file__).resolve().parents[2]
    index_path = repo_root / "index.html"
    content = index_path.read_text(encoding="utf-8")
    
    # speechSynthesis の使用を検索
    assert "speechSynthesis" in content, "Web Speech API (speechSynthesis) が使用されていません"
    assert "SpeechSynthesisUtterance" in content, "SpeechSynthesisUtterance が使用されていません"


@pytest.mark.e2e
def test_standalone_index_html_has_localstorage():
    """LocalStorageの使用が確認できることを確認"""
    repo_root = Path(__file__).resolve().parents[2]
    index_path = repo_root / "index.html"
    content = index_path.read_text(encoding="utf-8")
    
    # localStorage の使用を検索
    assert "localStorage" in content, "localStorage が使用されていません"
    assert "saveProjectToLocalStorage" in content or "localStorage.setItem" in content, \
        "LocalStorageへの保存機能が見つかりません"
    assert "loadProjectFromLocalStorage" in content or "localStorage.getItem" in content, \
        "LocalStorageからの読み込み機能が見つかりません"


@pytest.mark.e2e
def test_standalone_index_html_has_pdfjs_integration():
    """PDF.jsの統合が確認できることを確認"""
    repo_root = Path(__file__).resolve().parents[2]
    index_path = repo_root / "index.html"
    content = index_path.read_text(encoding="utf-8")
    
    # PDF.jsの使用を検索
    assert "pdfjsLib.getDocument" in content, "PDF.js の getDocument() が使用されていません"
    assert "convertPdfToImages" in content or "pdfToImages" in content, \
        "PDF→画像変換関数が見つかりません"


@pytest.mark.e2e
def test_standalone_index_html_has_pptx_export():
    """PPTX出力機能が確認できることを確認"""
    repo_root = Path(__file__).resolve().parents[2]
    index_path = repo_root / "index.html"
    content = index_path.read_text(encoding="utf-8")
    
    # PptxGenJSの使用を検索
    assert "PptxGenJS" in content or "pptxgen" in content, "PptxGenJS が使用されていません"
    assert "exportPptx" in content or "generatePptx" in content, \
        "PPTX出力関数が見つかりません"


@pytest.mark.e2e
def test_standalone_index_html_has_csv_export():
    """CSV出力機能が確認できることを確認"""
    repo_root = Path(__file__).resolve().parents[2]
    index_path = repo_root / "index.html"
    content = index_path.read_text(encoding="utf-8")
    
    # CSV出力関数を検索
    assert "downloadCsv" in content or "exportCsv" in content, \
        "CSV出力関数が見つかりません"


@pytest.mark.e2e
def test_standalone_index_html_no_backend_dependency():
    """バックエンド依存（Edge TTS、FFmpeg）が削除されていることを確認"""
    repo_root = Path(__file__).resolve().parents[2]
    index_path = repo_root / "index.html"
    content = index_path.read_text(encoding="utf-8")
    
    # バックエンドAPI呼び出しが存在しないことを確認
    # （STANDALONE_MODE = true の場合、サーバーAPIは使用されないはず）
    # ただし、コメント内や変数名に残存する可能性があるため、厳密すぎないチェック
    
    # バックエンド版への誘導文言/依存が残っていないこと
    forbidden_literals = [
        "src/server.py",
        "start.ps1",
        "Edge TTS",
    ]

    for lit in forbidden_literals:
        assert lit not in content, f"スタンドアロン版に不適切な文言が残存しています: {lit}"

    # API呼び出し(例)が存在しないこと（将来の混入防止）
    forbidden_patterns = [
        r"fetch\(['\"].*?/api/generate_audio",
        r"fetch\(['\"].*?/api/generate_video",
    ]
    
    for pattern in forbidden_patterns:
        matches = re.findall(pattern, content)
        # STANDALONE_MODE分岐でコメントアウトされている可能性を考慮
        # 実際のfetch呼び出しが存在しないことを確認
        active_matches = [m for m in matches if "STANDALONE_MODE" not in content[max(0, content.index(m) - 200):content.index(m)]]
        assert len(active_matches) == 0, f"バックエンドAPI呼び出しが残存しています: {pattern}"


@pytest.mark.e2e
def test_standalone_help_mentions_limitations():
    """ヘルプガイドに『サーバー不要/TTSのみ/音声ファイル生成不可/動画生成不可』が明記されていること"""
    repo_root = Path(__file__).resolve().parents[2]
    index_path = repo_root / "index.html"
    content = index_path.read_text(encoding="utf-8")

    assert "サーバー不要" in content
    assert "音声ファイル生成" in content and "不可" in content
    assert "動画生成" in content and "不可" in content


@pytest.mark.e2e
def test_standalone_index_html_has_babel_presets():
    """Babelの正しいpresets設定があることを確認"""
    repo_root = Path(__file__).resolve().parents[2]
    index_path = repo_root / "index.html"
    content = index_path.read_text(encoding="utf-8")
    
    # data-presets="env,react" が設定されていることを確認
    assert 'data-presets="env,react"' in content or "data-presets='env,react'" in content, \
        "Babelのpresets設定が見つかりません"


@pytest.mark.e2e
def test_standalone_index_html_valid_html():
    """基本的なHTML構造が正しいことを確認"""
    repo_root = Path(__file__).resolve().parents[2]
    index_path = repo_root / "index.html"
    content = index_path.read_text(encoding="utf-8")
    
    # 基本的なHTML要素の存在確認
    assert "<!DOCTYPE html>" in content, "DOCTYPE宣言が見つかりません"
    assert "<html" in content, "<html>タグが見つかりません"
    assert "<head>" in content, "<head>タグが見つかりません"
    assert "<body" in content, "<body>タグが見つかりません"
    assert "</html>" in content, "</html>閉じタグが見つかりません"
    
    # Reactルート要素の存在確認
    assert 'id="root"' in content, "Reactルート要素 (#root) が見つかりません"


@pytest.mark.e2e
def test_standalone_index_html_meta_charset_utf8():
    """UTF-8エンコーディングが設定されていることを確認"""
    repo_root = Path(__file__).resolve().parents[2]
    index_path = repo_root / "index.html"
    content = index_path.read_text(encoding="utf-8")
    
    # charset=UTF-8 の設定を確認
    assert 'charset="UTF-8"' in content or "charset='UTF-8'" in content or 'charset="utf-8"' in content, \
        "UTF-8エンコーディングが設定されていません"


@pytest.mark.e2e
def test_standalone_index_html_has_default_file_loading():
    """デフォルトファイル自動読み込み機能が実装されていることを確認"""
    repo_root = Path(__file__).resolve().parents[2]
    index_path = repo_root / "index.html"
    content = index_path.read_text(encoding="utf-8")
    
    # useEffectでデフォルトファイル読み込みを検索
    assert "useEffect" in content, "useEffect が使用されていません"
    assert "AIドリブン開発・教育体制の構築.pdf" in content, \
        "デフォルトPDFファイル名が見つかりません"
    assert "原稿.csv" in content, "デフォルトCSVファイル名が見つかりません"
    assert "fetch" in content, "fetch API が使用されていません"


@pytest.mark.e2e
def test_default_files_exist():
    """デフォルトファイルが存在することを確認"""
    repo_root = Path(__file__).resolve().parents[2]
    input_dir = repo_root / "input"
    
    # デフォルトPDFファイルの存在確認
    default_pdf = input_dir / "AIドリブン開発・教育体制の構築.pdf"
    assert default_pdf.exists(), f"デフォルトPDFファイルが存在しません: {default_pdf}"
    assert default_pdf.is_file(), f"デフォルトPDFがファイルではありません: {default_pdf}"
    
    # デフォルトCSVファイルの存在確認
    default_csv = input_dir / "原稿.csv"
    assert default_csv.exists(), f"デフォルトCSVファイルが存在しません: {default_csv}"
    assert default_csv.is_file(), f"デフォルトCSVがファイルではありません: {default_csv}"
