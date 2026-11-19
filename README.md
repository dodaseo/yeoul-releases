# 여울 (Yeoul) — 내 구독 AI로 번역하는 Windows 빠른 번역기

**가볍고 빠르게, 그러나 마음먹으면 본격 작업도.**

어느 프로그램에서든 글을 선택하고 **Ctrl 을 누른 채 C 를 두 번** 누르면 커서 옆 작은 창에 번역이 나오고, 낱말을 선택하고 **Ctrl 을 누른 채 D 를 두 번** 누르면 사전이 뜨며 찾아본 낱말은 단어장에 쌓입니다.
번역 엔진은 이 PC 의 **구독 AI**(Claude, ChatGPT/Codex, Google Antigravity)를 그대로 쓰거나, API 키(OpenAI 호환 · Anthropic · Gemini) 또는 로컬 모델(Ollama, LM Studio)을 씁니다.
**설정 › 사전** 에서 오프라인 사전 DB 를 받아 두면 AI 호출·대기 시간 없이 **1~3ms 만에** 영한·영영·국어·한영·일한·중한 뜻풀이와 발음을 바로 볼 수 있습니다.

> ‘여울’은 물살이 빠르고 얕아 건너기 좋은 곳을 뜻하는 우리말입니다. 말과 말 사이를 빠르게 건넌다는 뜻으로 붙였습니다.

<div align="center">

[![Windows용 내려받기](https://img.shields.io/badge/%E2%AC%87%20Windows%EC%9A%A9%20%EB%82%B4%EB%A0%A4%EB%B0%9B%EA%B8%B0-setup.exe-0e7a5b?style=for-the-badge)](https://github.com/dodaseo/yeoul-releases/releases/latest) &nbsp; [![최신 릴리스](https://img.shields.io/github/v/release/dodaseo/yeoul-releases?style=for-the-badge&color=455a64&label=%EC%B5%9C%EC%8B%A0%20%ED%8C%90)](https://github.com/dodaseo/yeoul-releases/releases/latest)

[최신 판 받기](https://github.com/dodaseo/yeoul-releases/releases/latest) · [오프라인 사전 팩](https://github.com/dodaseo/yeoul-releases/releases/tag/dicts-v1) · [이용 조건](LICENSE) · [문제 제보 · 제안](https://github.com/dodaseo/yeoul-releases/issues/new)

</div>

## 이 저장소는 무엇인가

배포 전용 저장소입니다 — 설치본·압축판·체크섬(`SHA256SUMS.txt`), 오프라인 사전 DB 팩(`dicts-v1`), 안내 문서, 이슈 제보. 소스 코드는 비공개 저장소에 있습니다.

## 내려받기

**[Releases](https://github.com/dodaseo/yeoul-releases/releases/latest)** 에서 **`Yeoul-<버전>-setup.exe`** 를 받아 실행합니다.

- 사용자별 설치라 관리자 권한이 필요 없습니다(`%LOCALAPPDATA%\Programs\Yeoul`). 다시 설치하면 떠 있는 여울을 끝내고 덮어씁니다(설정·기록·단어장 유지).
- 설치 없이 쓰려면 `Yeoul-<버전>-portable.zip` 을 풀고 `Yeoul.exe` 를 실행합니다.
- 처음 실행할 때 「Windows의 PC 보호」(SmartScreen) 경고가 뜨면 **추가 정보 → 실행**을 누르세요. 코드 서명 전이라 나타나는 안내이며, 함께 올린 `SHA256SUMS.txt` 로 파일 무결성을 확인할 수 있습니다.
- 처음 설치 후 실행하면 **애니메이션 튜토리얼**이 핵심 단축키와 조작법을 안내합니다(언제든 **설정 › 일반 › 튜토리얼 다시 보기** 가능).
- 구독 AI CLI 를 쓰지 않던 일반 사용자도 첫 화면 온보딩 또는 **설정 › AI 엔진** 에서 클릭 한 번으로 공식 CLI 설치·OAuth 로그인·업데이트를 진행할 수 있습니다.
- 새 버전이 나오면 백그라운드에서 확인해 SHA-256 검증 뒤 자동 업데이트(설치판·압축판 모두 지원)를 안내합니다.

### 필요한 것

- Windows 10 · 11 (64비트)
- Microsoft Edge WebView2 런타임 — Windows 11 에는 기본 포함, Windows 10 은 없으면 설치 프로그램이 안내합니다.
- 번역·글 다듬기에는 구독 AI(Claude / Codex / Antigravity — 앱 안에서 원클릭 설치·로그인 지원) 또는 API 키·로컬 모델이 필요합니다. 오프라인 사전 DB(`Ctrl+D, D`)는 AI 없이도 단독으로 동작합니다.

## 쓰는 법

| 하고 싶은 일 | 방법 |
|---|---|
| 선택한 글 바로 번역 · 낱말 사전 | `Ctrl+C, C` (Ctrl 을 누른 채 C 두 번, 1초 안에) — 문장은 번역, 낱말·짧은 표현은 사전으로 알아서 |
| 사전 ↔ 번역 바꾸기 | 작은 창에서 `Ctrl+D` (또는 ‘사전으로 보기’ · ‘번역으로 보기’) |
| 번역문을 원문 자리에 넣기 | 작은 창에서 `Enter` 또는 `Ctrl+R` |
| 번역문(뜻) 복사 | 작은 창에서 `Ctrl+C` |
| 번역할 언어 바꾸기 | 작은 창에서 `Space` |
| 사전 탭 좌우 전환 | 사전 팝업에서 `←` / `→` |
| 메인 창에서 이어서 작업 | 작은 창에서 `Ctrl+E` |
| 닫기 | `Esc`, 또는 다른 곳을 클릭 (핀으로 고정 가능) |
| 메인 창에서 번역 | `Ctrl+Enter` |

- 번역 방향은 자동입니다. 내 언어(기본 한국어)로 쓴 글은 상대 언어(기본 영어)로, 그 밖의 글은 내 언어로 옮깁니다.
- 문체(기본 · 격식 · 구어 · 학술)를 고르면 그 문체로 다시 번역합니다. ‘다른 표현’은 대안 세 가지를 보여 줍니다.
- DeepL 처럼 `Ctrl+C, C` 를 쓰는 다른 프로그램과 겹치면 **설정 › 단축키**에서 조합을 바꿀 수 있습니다.

## 오프라인 사전 DB 와 단어장

**설정 › 사전** 에서 원하는 사전 DB 만 골라 원클릭(SHA-256 검증)으로 내려받을 수 있습니다.

| 사전 팩 | 언어 | 수록 내용 | 표제어 수 | 라이선스 |
|---|---|---|---|---|
| **영한 사전** | 영 → 한 | Wiktionary + WordNet 보강 (IPA·예문·유의어·활용형) | 37,788개 | CC BY-SA 4.0 |
| **영영 사전 · 경량** | 영 → 영 | Open English WordNet 2025 (정의·유의어·예문) | 153,888개 | CC BY 4.0 |
| **영영 사전 · 확장** | 영 → 영 | English Wiktionary (학술어·구동사·IPA·활용형) | 862,680개 | CC BY-SA 4.0 |
| **국어 사전** | 국 → 국 | Korean Wiktionary (표준 발음·품사·뜻풀이·유의어) | 68,290개 | CC BY-SA 4.0 |
| **한영 사전** | 국 → 영 | Wiktionary 한영 대역·발음·예문 | 51,714개 | CC BY-SA 4.0 |
| **일한 사전** | 일 → 한 | Korean Wiktionary 일본어 뜻·발음·활용형 | 12,247개 | CC BY-SA 4.0 |
| **중한 사전** | 중 → 한 | Korean Wiktionary 중국어 낱말·한자 뜻풀이 | 15,913개 | CC BY-SA 4.0 |

- 여러 사전이 설치되어 있으면 **우선순위 순으로 결과 있는 사전만 탭**으로 표시하며, 메인 창에서는 **`[전체 비교]`** 로 나란히 비교할 수 있습니다.
- 영어 활용형(`analyses`·`went`·`stopped`), 한국어 조사·어미(`성찰을`·`성찰했다`), 동음이의어·한자를 지원합니다.
- DB 에 없는 숙어나 뉘앙스 비교가 필요할 때만 **`[AI로 자세히]`** 를 누르면 보고 있는 탭 언어(영한·영영·국어)에 맞춰 AI 풀이를 덧보여 줍니다(설정에서 `로컬 DB만` 사용도 가능).
- 국립국어원 XML 등으로 직접 변환한 `.db`/`.db.gz` 파일도 **로컬 DB 가져오기…** 로 등록할 수 있습니다.

## 지원 번역 엔진

| 엔진 | 방식 | 속도 (2026-11 기준) |
|---|---|---|
| Claude 구독 | `claude -p` (stream-json 입출력), 프로세스 미리 준비 | 첫 글자 약 0.8초, 한 문장 1.5~2.5초 |
| ChatGPT 구독 (Codex) | `codex exec` (표준 입력, 읽기 전용 샌드박스) | 수 초 |
| Google 구독 (Antigravity) | `agy acp` (무도구·MCP 격리 상주 서버, 기본 `gemini-4-hydrogen-low`) | 미리 준비 시 한 문장 2.5~3.7초 (미준비 약 4.8~5.6초) |
| OpenAI 호환 API | `/chat/completions` 스트리밍 (OpenAI, OpenRouter, Ollama, LM Studio 등) | 서버에 따라 다름 |
| Anthropic API · Gemini API | API 키로 직접 호출, 스트리밍 | 서버에 따라 다름 |

- ‘실패하면 다른 엔진으로’를 켜면 한도 초과나 오류 때 대체 엔진으로 한 번 다시 시도합니다.

## 데이터와 개인정보

- **설정 · 번역 기록 · 단어장 · 용어집 · 사전 DB · API 키는 이 PC 에만 저장됩니다**(`%LOCALAPPDATA%\Yeoul`, 제거해도 남음).
- API 키는 Windows DPAPI(현재 사용자)로 암호화해 보관합니다.
- 오프라인 사전 조회는 네트워크를 전혀 쓰지 않습니다. 번역·AI 사전 요청 시에만 사용자가 고른 엔진으로 전송됩니다.

## 자매 제품

- **[Ibis](https://github.com/dodaseo/ibis-releases)** — 한국 연구자를 위한 문헌 관리 · 한글/Word 본문 인용
- **[에믹 (Emic)](https://github.com/dodaseo/emic-releases)** — 한국어 질적분석 스튜디오

## 사용 현황

<!-- DL-STATS:START -->
<!-- 이 블록은 .github/workflows/dl-stats.yml 이 매일 생성합니다. 직접 고치지 마세요. -->

기록이 아직 수집되지 않았습니다.

<!-- DL-STATS:END -->
