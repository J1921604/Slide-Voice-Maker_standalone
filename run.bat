@echo off
REM ============================================
REM Slide Voice Maker - ワンクリック実行
REM ============================================
REM スタンドアロン版（index.html単独）を起動します
REM サーバー不要Python不要で動作します
REM ============================================

echo.
echo ======================================
echo Slide Voice Maker (スタンドアロン版)
echo ======================================
echo.
echo index.htmlをブラウザで開きます...
echo.

REM デフォルトブラウザでindex.htmlを開く
start "" "%~dp0index.html"

echo.
echo ブラウザで index.html が開きました。
echo.
echo 【使い方】
echo 1. PDF入力ボタンでPDFを選択
echo 2. 原稿CSV入力ボタンでCSVを読み込み
echo 3. TTS再生ボタンで音声を確認
echo 4. 原稿を編集してCSV出力PPTX出力
echo.
echo このウィンドウは閉じても構いません。
echo.
pause
