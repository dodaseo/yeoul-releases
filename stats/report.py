#!/usr/bin/env python3
"""다운로드 스냅숏(stats/downloads.csv) → 읽을 수 있는 요약·그래프(마크다운).

GitHub 은 **누적** 수만 주므로 일별 증가는 스냅숏 사이의 차분으로 계산한다.
표준 라이브러리만 쓴다(Actions 의 python3 로 바로 돌린다).

사용법:
  python3 stats/report.py [csv]                 전체 요약(stats/README.md 용, 표준출력)
  python3 stats/report.py [csv] --chart         README 하단 삽입용 짧은 블록만 출력
  python3 stats/report.py [csv] --write-readme  README.md 의 마커 사이를 직접 갱신

분석 주의 — 여울의 내려받기 동작:
  · setup.exe     : 새 설치 + 설치판 인앱 자동 업데이트가 함께 잡힌다
  · portable.zip  : 무설치 사용 + 압축판 인앱 자동 업데이트가 함께 잡힌다
  · *.db.gz       : 설정 › 사전 에서 내려받은 오프라인 사전 DB 팩
  · manifest.json : 설정 › 사전 목록을 새로고침할 때 내려받는다
  · SHA256SUMS.txt: 업데이트를 실제로 내려받을 때만 받는다(단순 확인은 API 조회만 수행)
"""
from __future__ import annotations

import csv
import html
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
CHART_ONLY = "--chart" in sys.argv[1:]
WRITE_README = "--write-readme" in sys.argv[1:]
CSV = Path(ARGS[0] if ARGS else "stats/downloads.csv")

README = Path("README.md") if Path("README.md").is_file() else (CSV.parent.parent / "README.md")
MARK_S = "<!-- DL-STATS:START -->"
MARK_E = "<!-- DL-STATS:END -->"
MARK_NOTE = (
    "<!-- 이 블록은 .github/workflows/dl-stats.yml 이 매일 생성합니다. "
    "직접 고치지 마세요. -->"
)

DICT_NAMES = {
    "en-ko": "영한 사전",
    "en-en-oewn": "영영 사전 · 경량",
    "en-en-wikt": "영영 사전 · 확장",
    "ko-ko-wikt": "국어 사전",
    "ko-en-wikt": "한영 사전",
    "ja-ko": "일한 사전",
    "zh-ko": "중한 사전",
    "ko-ko-std": "표준국어대사전",
    "ko-en-krdict": "한국어·한영 기초사전",
    "ko-ko-urimal": "우리말샘",
}

SVG_W, SVG_H = 760, 200
PAD_L, PAD_R, PAD_T, PAD_B = 36, 104, 14, 26
FONT = (
    "'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, "
    "'Segoe UI', 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif"
)

# 여울 UI(app.css / logo.svg) 팔레트
THEMES = {
    "light": {
        "setup": "#0B6B63",
        "zip": "#8A94A0",
        "dict": "#12897D",
        "grid": "#E1E4E9",
        "axis": "#CBD0D8",
        "text": "#636C78",
        "ink": "#1B1F24",
    },
    "dark": {
        "setup": "#4FD1C1",
        "zip": "#8B949E",
        "dict": "#7BE0D3",
        "grid": "#262A31",
        "axis": "#3A4049",
        "text": "#949DA8",
        "ink": "#E8EAED",
    },
}


def kind(asset: str) -> str:
    a = asset.lower()
    if a.endswith("setup.exe"):
        return "setup"
    if a.endswith("-portable.zip") or a.endswith(".zip"):
        return "zip"
    if a.endswith(".db.gz") or a.endswith(".db"):
        return "dict"
    if a == "manifest.json":
        return "manifest"
    if a == "sha256sums.txt" or a.endswith(".sha256"):
        return "checksum"
    return "other"


def dict_pack_id(asset: str) -> str:
    low = asset.lower()
    if low.endswith(".db.gz"):
        return asset[:-6]
    if low.endswith(".db"):
        return asset[:-3]
    return Path(asset).stem


def dict_label(asset: str) -> str:
    pid = dict_pack_id(asset)
    return DICT_NAMES.get(pid, pid)


def _fmt_delta(cur: int, prev_val: int | None) -> str:
    if prev_val is None:
        return "—"
    d = cur - prev_val
    return f"+{d}" if d > 0 else str(d)


def _axis(maxv: int, want: int = 5) -> tuple[int, int]:
    """(위끝, 눈금 간격). 정수 간격을 먼저 고르고 위끝을 그 배수로 올린다."""
    raw = max(maxv, 1) / want
    mag = 10 ** (len(str(int(raw))) - 1) if raw >= 1 else 1
    step = max(1, int(raw) + 1)
    for m in (1, 2, 2.5, 5, 10):
        cand = mag * m
        if cand >= raw and cand == int(cand):
            step = int(cand)
            break
    return (maxv // step + 1) * step, step


def _x_positions(days: list[str]) -> list[float]:
    """날짜 간격에 비례해 x 를 놓는다 — 스냅숏이 빠진 날이 사실대로 벌어진다."""
    def ordinal(d: str) -> int:
        y, m, dd = (int(x) for x in d.split("-"))
        return date(y, m, dd).toordinal()

    o = [ordinal(d) for d in days]
    span = max(o[-1] - o[0], 1)
    w = SVG_W - PAD_L - PAD_R
    return [PAD_L + w * (v - o[0]) / span for v in o]


def _render_line_svg(
    days: list[str],
    series: list[tuple[list[int], str, str, float]],
    aria_label: str,
    theme: str,
) -> str:
    """공통 누적 선 그래프 SVG 렌더러.

    series: [(값 목록, 색상 키, 선 끝 라벨, 선 두께), ...] — 먼저 나온 항목이 아래에 깔린다.
    """
    c = THEMES[theme]
    all_vals = [v for vals, _, _, _ in series for v in vals]
    top, step = _axis(max([*all_vals, 1]))
    xs = _x_positions(days)
    h = SVG_H - PAD_T - PAD_B

    def y(v: int) -> float:
        return PAD_T + h * (1 - v / top)

    def path(vals: list[int]) -> str:
        return " ".join(f"{x:.1f},{y(v):.1f}" for x, v in zip(xs, vals))

    esc_aria = html.escape(aria_label, quote=True)
    o: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{SVG_H}" '
        f'viewBox="0 0 {SVG_W} {SVG_H}" role="img" aria-label="{esc_aria}">',
        f'<g font-family="{FONT}" font-size="11">',
    ]

    for v in range(0, top + 1, step):
        yy = y(v)
        o.append(
            f'<line x1="{PAD_L}" y1="{yy:.1f}" x2="{SVG_W - PAD_R}" y2="{yy:.1f}" '
            f'stroke="{c["grid"]}" stroke-width="1"/>'
        )
        o.append(
            f'<text x="{PAD_L - 8}" y="{yy + 3.5:.1f}" fill="{c["text"]}" '
            f'font-size="10" text-anchor="end">{v}</text>'
        )

    for vals, key, _, width in series:
        o.append(
            f'<polyline points="{path(vals)}" fill="none" stroke="{c[key]}" '
            f'stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>'
        )

    ends = sorted(
        ((vals[-1], key, label) for vals, key, label, _ in series),
        key=lambda t: -t[0],
    )
    prev_y: float | None = None
    for val, key, label in ends:
        yy = y(val)
        if prev_y is not None and abs(yy - prev_y) < 13:
            yy = prev_y + 13
        prev_y = yy
        esc_label = html.escape(f"{label} {val}", quote=False)
        o.append(f'<circle cx="{xs[-1]:.1f}" cy="{y(val):.1f}" r="2.6" fill="{c[key]}"/>')
        o.append(
            f'<text x="{xs[-1] + 8:.1f}" y="{yy + 4:.1f}" fill="{c[key]}" '
            f'font-size="12" font-weight="600">{esc_label}</text>'
        )

    picks = {0, len(days) // 2, len(days) - 1}
    for i in sorted(picks):
        anchor = "start" if i == 0 else ("end" if i == len(days) - 1 else "middle")
        date_lbl = html.escape(days[i][5:].replace("-", "."), quote=False)
        o.append(
            f'<text x="{xs[i]:.1f}" y="{SVG_H - 8}" fill="{c["text"]}" '
            f'font-size="10" text-anchor="{anchor}">{date_lbl}</text>'
        )

    o += ["</g>", "</svg>", ""]
    return "\n".join(o)


def svg_downloads(days: list[str], per_day, theme: str) -> str:
    setup = [per_day[d].get("setup", 0) for d in days]
    zipd = [per_day[d].get("zip", 0) for d in days]
    aria = f"누적 다운로드 추이 — 설치 프로그램 {setup[-1]}건, 압축판 {zipd[-1]}건"
    return _render_line_svg(
        days,
        [(zipd, "zip", "압축판", 1.6), (setup, "setup", "설치", 2.0)],
        aria,
        theme,
    )


def svg_dicts(days: list[str], per_day, theme: str) -> str:
    dicts = [per_day[d].get("dict", 0) for d in days]
    aria = f"오프라인 사전 팩 누적 다운로드 추이 — 총 {dicts[-1]}건"
    return _render_line_svg(
        days,
        [(dicts, "dict", "사전 팩", 2.0)],
        aria,
        theme,
    )


def write_svgs(days: list[str], per_day) -> list[str]:
    """라이트·다크 두 벌을 쓴다. README 는 <picture> 로 갈라 쓴다."""
    if len(days) < 2:
        return []
    out: list[str] = []
    dict_max = max((per_day[d].get("dict", 0) for d in days), default=0)
    for theme in ("light", "dark"):
        p = CSV.parent / f"downloads-{theme}.svg"
        p.write_text(svg_downloads(days, per_day, theme), encoding="utf-8", newline="\n")
        out.append(p.name)
        if dict_max > 0:
            q = CSV.parent / f"dicts-{theme}.svg"
            q.write_text(svg_dicts(days, per_day, theme), encoding="utf-8", newline="\n")
            out.append(q.name)
    return out


def chart_block(days: list[str], base: str = "stats/downloads") -> list[str]:
    """README 에 넣을 앱 다운로드 그래프 조각."""
    if len(days) < 2:
        return ["> 스냅숏이 하나뿐이라 아직 그래프를 그릴 수 없습니다 — 내일부터 채워집니다.", ""]
    return [
        "<picture>",
        f'  <source media="(prefers-color-scheme: dark)" srcset="{base}-dark.svg">',
        f'  <img alt="누적 다운로드 추이 — 설치 프로그램과 무설치 압축판" src="{base}-light.svg" width="760">',
        "</picture>",
        "",
        "> 설치판과 압축판 모두 앱 안 자동 업데이트가 해당 파일을 내려받으므로, 신규 설치와 업데이트가 함께 잡힙니다.",
        "",
    ]


def dict_chart_block(days: list[str], base: str = "dicts") -> list[str]:
    """오프라인 사전 팩 누적 그래프 조각."""
    if len(days) < 2:
        return []
    return [
        "<picture>",
        f'  <source media="(prefers-color-scheme: dark)" srcset="{base}-dark.svg">',
        f'  <img alt="오프라인 사전 팩 누적 다운로드 추이" src="{base}-light.svg" width="760">',
        "</picture>",
        "",
        "> **설정 › 사전** 에서 원클릭으로 내려받은 오프라인 사전 DB 팩(`*.db.gz`) 누적 건수입니다.",
        "",
    ]


def load():
    with CSV.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    per_day: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    per_asset: dict[str, dict[tuple[str, str], int]] = defaultdict(dict)
    for r in rows:
        d, tag, asset = r["date"], r["tag"], r["asset"]
        n = int(r["downloads"])
        per_day[d][kind(asset)] += n
        per_asset[d][(tag, asset)] = n
    return rows, per_day, per_asset


def load_repo(path: Path) -> dict[str, dict[str, int]]:
    if not path.is_file():
        return {}
    out: dict[str, dict[str, int]] = {}
    with path.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            d = (r.get("date") or "").strip()
            if not d:
                continue
            out[d] = {
                "stars": int(r.get("stars") or 0),
                "forks": int(r.get("forks") or 0),
                "watchers": int(r.get("watchers") or 0),
                "open_issues": int(r.get("open_issues") or 0),
            }
    return out


def short_block(days: list[str], per_day, last: str) -> str:
    """README 하단 '사용 현황' 에 넣을 짧은 블록(요약 한 줄 + 차트 + 링크)."""
    setup_n = per_day[last].get("setup", 0)
    zip_n = per_day[last].get("zip", 0)
    dict_n = per_day[last].get("dict", 0)
    app_tot = setup_n + zip_n
    head = (
        f"최신 기록 **{last}** · 앱 누적 **{app_tot}건** "
        f"(설치 {setup_n} · 압축판 {zip_n}) · 오프라인 사전 팩 **{dict_n}건**"
    )
    tail = (
        "자세한 표는 [stats/README.md](stats/README.md), "
        "원본은 [stats/downloads.csv](stats/downloads.csv)."
    )
    return "\n".join([head, ""] + chart_block(days, base="stats/downloads") + [tail])


def write_readme(block: str) -> None:
    """마커 사이만 바꿔치운다 — 워크플로가 매일 부르므로 나머지 문서를 건드리면 안 된다."""
    if not README.is_file():
        print("README.md 없음 — 건너뜀")
        return
    t = README.read_text(encoding="utf-8")
    if MARK_S not in t or MARK_E not in t:
        print("README 에 DL-STATS 마커가 없음 — 건너뜀")
        return
    new = "\n".join([MARK_S, MARK_NOTE, "", block.strip(), "", MARK_E])
    head, rest = t.split(MARK_S, 1)
    _, tail = rest.split(MARK_E, 1)
    README.write_text(head + new + tail, encoding="utf-8", newline="\n")
    print("README '사용 현황' 갱신")


def main() -> int:
    if not CSV.is_file():
        print("스냅숏이 아직 없습니다.")
        return 0
    rows, per_day, per_asset = load()
    if not rows:
        print("스냅숏이 비어 있습니다.")
        return 0
    days = sorted(per_day)
    last, prev = days[-1], (days[-2] if len(days) > 1 else None)
    write_svgs(days, per_day)

    if CHART_ONLY or WRITE_README:
        block = short_block(days, per_day, last)
        if WRITE_README:
            write_readme(block)
        else:
            print(block)
        return 0

    repo = load_repo(CSV.parent / "repo.csv")

    out: list[str] = ["# 다운로드 추이", ""]
    out.append(f"- 기록 시작 **{days[0]}** · 최신 스냅숏 **{last}** · 스냅숏 {len(days)}개")
    sources = ["[`downloads.csv`](downloads.csv)"]
    if repo:
        sources.append("[`repo.csv`](repo.csv)")
    out.append(f"- 이 파일은 매일 자동 생성됩니다. 원본은 {' · '.join(sources)}.")
    out.append("")

    # ── 누적 표 ──
    out += ["## 누적", "", "| 구분 | 누적 | 전일 대비 |", "|---|---:|---:|"]

    def cur_val(k: str) -> int:
        return per_day[last].get(k, 0)

    def prev_val(k: str) -> int | None:
        return per_day[prev].get(k, 0) if prev is not None else None

    s_cur, z_cur = cur_val("setup"), cur_val("zip")
    s_prev, z_prev = prev_val("setup"), prev_val("zip")
    app_cur = s_cur + z_cur
    app_prev = (s_prev + z_prev) if (s_prev is not None and z_prev is not None) else None

    out.append(f"| 설치 프로그램 (`setup.exe` — 새 설치 + 설치판 자동 업데이트) | {s_cur} | {_fmt_delta(s_cur, s_prev)} |")
    out.append(f"| 무설치 압축판 (`portable.zip` — 무설치 + 압축판 자동 업데이트) | {z_cur} | {_fmt_delta(z_cur, z_prev)} |")
    out.append(f"| **앱 내려받기 소계** | **{app_cur}** | **{_fmt_delta(app_cur, app_prev)}** |")

    for k, label in (
        ("dict", "오프라인 사전 팩 (`*.db.gz`)"),
        ("manifest", "사전 카탈로그 (`manifest.json` — 설정 › 사전 목록 조회)"),
        ("checksum", "체크섬 (`SHA256SUMS.txt` — 업데이트 검증 등)"),
    ):
        c_v, p_v = cur_val(k), prev_val(k)
        out.append(f"| {label} | {c_v} | {_fmt_delta(c_v, p_v)} |")

    o_cur, o_prev = cur_val("other"), prev_val("other")
    if o_cur > 0 or (o_prev is not None and o_prev > 0):
        out.append(f"| 기타 (`LICENSES-DICTS.txt` 등) | {o_cur} | {_fmt_delta(o_cur, o_prev)} |")

    all_keys = ("setup", "zip", "dict", "manifest", "checksum", "other")
    tot_cur = sum(cur_val(k) for k in all_keys)
    tot_prev = sum(per_day[prev].get(k, 0) for k in all_keys) if prev is not None else None
    out += [
        f"| **전체 자산 합계** | **{tot_cur}** | **{_fmt_delta(tot_cur, tot_prev)}** |",
        "",
        "- 여울의 인앱 자동 업데이트(`updater.py`)는 설치판에서는 `-setup.exe`, 무설치 압축판에서는 `-portable.zip` 을 내려받으므로 두 항목 모두 신규 다운로드와 자동 업데이트가 함께 집계됩니다.",
        "- 배포 스크립트(`publish.ps1`)가 새 릴리스를 올린 직후 체크섬 검증을 위해 자산을 1회 내려받으므로 릴리스 직후 초기 +1건이 포함됩니다.",
        "- `SHA256SUMS.txt` 는 업데이트를 실제로 내려받을 때만 받으므로(단순 최신 버전 확인은 API 조회만 수행) 일별 실행 횟수 지표로 쓰지 않습니다.",
        "- `manifest.json` 은 앱의 **설정 › 사전** 카탈로그를 새로고침할 때 내려받습니다.",
        "",
    ]

    # ── 저장소 현황 ──
    if repo:
        repo_days = sorted(repo)
        r_last = repo_days[-1]
        r_prev = repo_days[-2] if len(repo_days) > 1 else None
        out += ["## 저장소 현황", "", "| 항목 | 현재 | 전일 대비 |", "|---|---:|---:|"]
        for k, label in (
            ("stars", "스타 (Stars)"),
            ("forks", "포크 (Forks)"),
            ("watchers", "워처 (Watchers)"),
            ("open_issues", "열린 이슈 (Open Issues)"),
        ):
            rc = repo[r_last][k]
            rp = repo[r_prev][k] if r_prev is not None else None
            out.append(f"| {label} | {rc} | {_fmt_delta(rc, rp)} |")
        out.append("")

    # ── 누적 그래프 ──
    out += ["## 누적 그래프", ""] + chart_block(days, base="downloads")
    dict_max = max((per_day[d].get("dict", 0) for d in days), default=0)
    if len(days) >= 2 and dict_max > 0:
        out += dict_chart_block(days, base="dicts")

    # ── 일별 증가 ──
    if len(days) > 1:
        out += ["## 일별 증가", "", "| 날짜 | 설치 | 압축판 | 앱 합계 | 사전 팩 |", "|---|---:|---:|---:|---:|"]
        for i in range(1, len(days)):
            a, b = days[i - 1], days[i]
            ds = per_day[b].get("setup", 0) - per_day[a].get("setup", 0)
            dz = per_day[b].get("zip", 0) - per_day[a].get("zip", 0)
            dd = per_day[b].get("dict", 0) - per_day[a].get("dict", 0)
            out.append(f"| {b} | {ds:+d} | {dz:+d} | {ds + dz:+d} | {dd:+d} |")
        out.append("")

    # ── 릴리스별 (앱 릴리스만) ──
    by_tag: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for (tag, asset), n in per_asset[last].items():
        k = kind(asset)
        if k in ("setup", "zip"):
            by_tag[tag][k] += n
        elif tag.lower().startswith("v"):
            by_tag.setdefault(tag, defaultdict(int))
    app_tags = {
        tag: v for tag, v in by_tag.items()
        if (v.get("setup", 0) + v.get("zip", 0) > 0) or tag.lower().startswith("v")
    }
    if app_tags:
        out += ["## 릴리스별 (최신 스냅숏)", "", "| 릴리스 | 설치 | 압축판 | 합계 |", "|---|---:|---:|---:|"]
        ranked = sorted(app_tags.items(), key=lambda kv: kv[0], reverse=True)
        ranked.sort(key=lambda kv: -(kv[1].get("setup", 0) + kv[1].get("zip", 0)))
        for tag, v in ranked[:10]:
            s_n, z_n = v.get("setup", 0), v.get("zip", 0)
            out.append(f"| {tag} | {s_n} | {z_n} | {s_n + z_n} |")
        if len(ranked) > 10:
            out.append(f"| … 외 {len(ranked) - 10}개 | | | |")
        out.append("")

    # ── 오프라인 사전 팩별 ──
    dict_cur: dict[str, int] = defaultdict(int)
    for (_, asset), n in per_asset[last].items():
        if kind(asset) == "dict":
            dict_cur[asset] += n
    dict_prev: dict[str, int] = defaultdict(int)
    if prev is not None:
        for (_, asset), n in per_asset[prev].items():
            if kind(asset) == "dict":
                dict_prev[asset] += n
    if dict_cur:
        out += ["## 오프라인 사전 팩별 (최신 스냅숏)", "", "| 사전 팩 | 파일 | 누적 | 전일 대비 |", "|---|---|---:|---:|"]
        for asset, n in sorted(dict_cur.items(), key=lambda kv: (-kv[1], kv[0])):
            p_n = dict_prev[asset] if prev is not None else None
            out.append(f"| {dict_label(asset)} | `{asset}` | {n} | {_fmt_delta(n, p_n)} |")
        m_cur = cur_val("manifest")
        m_delta = _fmt_delta(m_cur, prev_val("manifest"))
        out.append("")
        if prev is not None:
            out.append(f"- 사전 카탈로그(`manifest.json`) 누적 조회: **{m_cur}건** (전일 대비 {m_delta})")
        else:
            out.append(f"- 사전 카탈로그(`manifest.json`) 누적 조회: **{m_cur}건**")
        out.append("")

    print("\n".join(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
