#!/usr/bin/env python3
"""
encoding-convert.py — Shift-JIS / EUC-JP / CP932 → UTF-8 変換ツール

Claude Code は Shift-JIS などの日本語エンコーディングが苦手なため、
このスクリプトで UTF-8 に変換してから渡すことで古いサイト・ファイルを読めるようになる。

Usage:
    # ファイルを変換（上書き）
    python tools/encoding-convert.py path/to/file.html

    # ファイルを変換（出力先指定）
    python tools/encoding-convert.py path/to/file.html -o output.html

    # URLから取得して変換
    python tools/encoding-convert.py https://example.com/old-page.html

    # URLから取得して変換・保存
    python tools/encoding-convert.py https://example.com/old-page.html -o page.html

    # ディレクトリ内の全HTMLファイルを一括変換
    python tools/encoding-convert.py ./pages/ --recursive

    # エンコーディングを手動指定
    python tools/encoding-convert.py file.html --from-encoding shift_jis

    # エンコーディングを検出するだけ（変換しない）
    python tools/encoding-convert.py file.html --detect-only
"""

import sys
import argparse
import urllib.request
import urllib.error
from pathlib import Path

# 日本語サイトでよく使われるエンコーディングの優先順位
JAPANESE_ENCODINGS = [
    "utf-8",
    "shift_jis",
    "cp932",      # Windows版 Shift-JIS（Microsoft拡張）
    "euc_jp",
    "iso2022_jp", # JIS
    "utf-16",
]


def detect_encoding(raw: bytes) -> tuple[str, float]:
    """バイト列からエンコーディングを推定する。

    Returns:
        (encoding_name, confidence)  confidence は 0.0〜1.0
    """
    # chardet が使えれば使う（より正確）
    try:
        import chardet
        result = chardet.detect(raw)
        if result and result.get("confidence", 0) > 0.7:
            return result["encoding"], result["confidence"]
    except ImportError:
        pass

    # HTMLのmetaタグからcharsetを探す
    for enc in ["utf-8", "ascii", "shift_jis", "cp932", "euc_jp"]:
        try:
            text = raw.decode(enc, errors="ignore")
            for marker in [
                'charset=shift_jis', 'charset=shift-jis',
                'charset=x-sjis', 'charset=Shift_JIS',
            ]:
                if marker.lower() in text.lower():
                    return "shift_jis", 0.9
            for marker in ['charset=euc-jp', 'charset=euc_jp', 'charset=EUC-JP']:
                if marker.lower() in text.lower():
                    return "euc_jp", 0.9
            for marker in ['charset=iso-2022-jp', 'charset=ISO-2022-JP']:
                if marker.lower() in text.lower():
                    return "iso2022_jp", 0.9
            for marker in ['charset=utf-8', 'charset=UTF-8']:
                if marker.lower() in text.lower():
                    return "utf-8", 0.95
            break
        except Exception:
            continue

    # BOMチェック
    if raw.startswith(b'\xff\xfe') or raw.startswith(b'\xfe\xff'):
        return "utf-16", 1.0
    if raw.startswith(b'\xef\xbb\xbf'):
        return "utf-8-sig", 1.0

    # 各エンコーディングで試してエラーが出ないものを選ぶ（ヒューリスティック）
    for enc in JAPANESE_ENCODINGS:
        try:
            raw.decode(enc)
            return enc, 0.5
        except (UnicodeDecodeError, LookupError):
            continue

    return "utf-8", 0.1  # フォールバック


def fetch_url(url: str) -> bytes:
    """URLからバイト列を取得する。"""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; encoding-convert/1.0; "
            "+https://github.com/hiroshi131206/claude-universal-config)"
        )
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def convert(raw: bytes, from_enc: str | None = None) -> tuple[str, str]:
    """バイト列を UTF-8 文字列に変換する。

    Returns:
        (utf8_text, detected_encoding)
    """
    if from_enc:
        text = raw.decode(from_enc, errors="replace")
        return text, from_enc

    detected_enc, confidence = detect_encoding(raw)
    try:
        text = raw.decode(detected_enc, errors="replace")
        return text, detected_enc
    except (UnicodeDecodeError, LookupError):
        # 最終フォールバック: エラー箇所を置換して強行
        text = raw.decode("utf-8", errors="replace")
        return text, "utf-8 (fallback)"


def process_file(
    path: Path,
    output: Path | None,
    from_enc: str | None,
    detect_only: bool,
    verbose: bool,
) -> bool:
    """単一ファイルを処理する。"""
    try:
        raw = path.read_bytes()
    except OSError as e:
        print(f"ERROR: {path}: {e}", file=sys.stderr)
        return False

    detected_enc, confidence = detect_encoding(raw)
    conf_pct = f"{confidence * 100:.0f}%"

    if detect_only:
        print(f"{path}: {detected_enc} (confidence: {conf_pct})")
        return True

    text, used_enc = convert(raw, from_enc)

    dst = output or path
    try:
        dst.write_text(text, encoding="utf-8")
    except OSError as e:
        print(f"ERROR: write {dst}: {e}", file=sys.stderr)
        return False

    if verbose:
        print(f"  {path} [{used_enc} → UTF-8] → {dst}")
    return True


def process_url(
    url: str,
    output: Path | None,
    from_enc: str | None,
    detect_only: bool,
    verbose: bool,
) -> bool:
    """URLを取得して処理する。"""
    try:
        raw = fetch_url(url)
    except urllib.error.URLError as e:
        print(f"ERROR: {url}: {e}", file=sys.stderr)
        return False

    detected_enc, confidence = detect_encoding(raw)
    conf_pct = f"{confidence * 100:.0f}%"

    if detect_only:
        print(f"{url}: {detected_enc} (confidence: {conf_pct})")
        return True

    text, used_enc = convert(raw, from_enc)

    if output:
        try:
            output.write_text(text, encoding="utf-8")
            if verbose:
                print(f"  {url} [{used_enc} → UTF-8] → {output}")
        except OSError as e:
            print(f"ERROR: write {output}: {e}", file=sys.stderr)
            return False
    else:
        # 出力先未指定の場合は標準出力に出力
        print(text)

    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Shift-JIS/EUC-JP/CP932 → UTF-8 変換ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Usage:")[1].strip() if "Usage:" in __doc__ else "",
    )
    parser.add_argument("source", help="変換するファイルパス、ディレクトリ、またはURL")
    parser.add_argument("-o", "--output", type=Path, default=None,
                        help="出力先ファイルパス（省略時はファイルを上書き、URLは標準出力）")
    parser.add_argument("--from-encoding", default=None,
                        help="入力エンコーディングを手動指定（例: shift_jis, euc_jp, cp932）")
    parser.add_argument("--recursive", "-r", action="store_true",
                        help="ディレクトリを再帰的に処理（.html, .htm, .txt, .csv対象）")
    parser.add_argument("--detect-only", action="store_true",
                        help="エンコーディングを検出するだけ（変換しない）")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="変換結果の詳細を表示しない")
    parser.add_argument("--extensions", default="html,htm,txt,csv",
                        help="再帰処理時の対象拡張子（カンマ区切り、デフォルト: html,htm,txt,csv）")

    args = parser.parse_args()
    verbose = not args.quiet

    # URL判定
    if args.source.startswith(("http://", "https://")):
        success = process_url(
            args.source, args.output, args.from_encoding,
            args.detect_only, verbose,
        )
        return 0 if success else 1

    src = Path(args.source)

    # ディレクトリ処理
    if src.is_dir():
        if not args.recursive:
            print(f"ERROR: {src} はディレクトリです。--recursive を指定してください。",
                  file=sys.stderr)
            return 1

        exts = {f".{e.strip().lstrip('.')}" for e in args.extensions.split(",")}
        files = [f for f in src.rglob("*") if f.is_file() and f.suffix.lower() in exts]

        if not files:
            print(f"WARNING: {src} に対象ファイルが見つかりませんでした。", file=sys.stderr)
            return 0

        if not args.quiet:
            print(f"{len(files)} ファイルを処理します...")

        errors = 0
        for f in sorted(files):
            ok = process_file(f, None, args.from_encoding, args.detect_only, verbose)
            if not ok:
                errors += 1

        if not args.quiet:
            ok_count = len(files) - errors
            print(f"\n完了: {ok_count}/{len(files)} ファイル変換" +
                  (f"（{errors} エラー）" if errors else ""))
        return 0 if errors == 0 else 1

    # 単一ファイル処理
    if not src.exists():
        print(f"ERROR: ファイルが見つかりません: {src}", file=sys.stderr)
        return 1

    success = process_file(src, args.output, args.from_encoding, args.detect_only, verbose)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
