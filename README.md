# 여울 (Yeoul) — 내 구독 AI로 번역하는 Windows 빠른 번역기

**가볍고 빠르게, 그러나 마음먹으면 본격 작업도.**

어느 프로그램에서든 글을 선택하고 **Ctrl 을 누른 채 C 를 두 번** 누르면 커서 옆 작은 창에 번역이 나오고, 낱말을 선택하고 **Ctrl 을 누른 채 D 를 두 번** 누르면 학습용 사전이 뜨며 찾아본 낱말은 단어장에 쌓입니다.
번역 엔진은 이 PC 에 로그인해 둔 **구독 AI**(Claude, ChatGPT/Codex, Google Antigravity)를 그대로 쓰거나, API 키(OpenAI 호환 · Anthropic · Gemini) 또는 로컬 모델(Ollama, LM Studio)을 씁니다.

> ‘여울’은 물살이 빠르고 얕아 건너기 좋은 곳을 뜻하는 우리말입니다. 말과 말 사이를 빠르게 건넌다는 뜻으로 붙였습니다.

<div align="center">

[![Windows용 내려받기](https://img.shields.io/badge/%E2%AC%87%20Windows%EC%9A%A9%20%EB%82%B4%EB%A0%A4%EB%B0%9B%EA%B8%B0-setup.exe-0e7a5b?style=for-the-badge)](https://github.com/dodaseo/yeoul-releases/releases/latest) &nbsp; [![최신 릴리스](https://img.shields.io/github/v/release/dodaseo/yeoul-releases?style=for-the-badge&color=455a64&label=%EC%B5%9C%EC%8B%A0%20%ED%8C%90)](https://github.com/dodaseo/yeoul-releases/releases/latest)

[최신 판 받기](https://github.com/dodaseo/yeoul-releases/releases/latest) · [이용 조건](LICENSE) · [문제 제보 · 제안](https://github.com/dodaseo/yeoul-releases/issues/new)

</div>

## 이 저장소는 무엇인가

배포 전용 저장소입니다 — 설치본·압축판·체크섬(`SHA256SUMS.txt`), 안내 문서, 이슈 제보. 소스 코드는 비공개 저장소에 있습니다.

## 내려받기

**[Releases](https://github.com/dodaseo/yeoul-releases/releases/latest)** 에서 **`Yeoul-<버전>-setup.exe`** 를 받아 실행합니다.

- 사용자별 설치라 관리자 권한이 필요 없습니다(`%LOCALAPPDATA%\Programs\Yeoul`). 다시 설치하면 떠 있는 여울을 끝내고 덮어씁니다(설정·기록·단어장 유지).
- 설치 없이 쓰려면 `Yeoul-<버전>-portable.zip` 을 풀고 `Yeoul.exe` 를 실행합니다.
- 처음 실행할 때 「Windows의 PC 보호」(SmartScreen) 경고가 뜨면 **추가 정보 → 실행**을 누르세요. 코드 서명 전이라 나타나는 안내이며, 함께 올린 `SHA256SUMS.txt` 로 파일 무결성을 확인할 수 있습니다.
- 새 버전이 나오면 백그라운드에서 확인해 SHA-256 검증 뒤 자동 업데이트(설치판·압축판 모두 지원)를 안내합니다. 앱의 **설정 › 일반** 또는 트레이 아이콘 메뉴에서도 바로 확인할 수 있습니다.

### 필요한 것

- Windows 10 · 11 (64비트)
- Microsoft Edge WebView2 런타임 — Windows 11 에는 기본 포함, Windows 10 은 없으면 설치 프로그램이 안내합니다.
- 구독 AI 엔진을 쓰려면 해당 CLI 를 설치하고 로그인해 둡니다(예: Claude Code CLI, Codex CLI, Antigravity `agy` CLI). API 키나 로컬 모델(Ollama, LM Studio)을 쓸 때는 CLI 가 없어도 됩니다.

## 쓰는 법

| 하고 싶은 일 | 방법 |
|---|---|
| 선택한 글 바로 번역 | `Ctrl+C, C` (Ctrl 을 누른 채 C 두 번, 1초 안에) |
| 선택한 낱말 사전 찾기 | `Ctrl+D, D` (Ctrl 을 누른 채 D 를 빠르게 두 번) |
| 번역문을 원문 자리에 넣기 | 작은 창에서 `Enter` 또는 `Ctrl+R` |
| 번역문(뜻) 복사 | 작은 창에서 `Ctrl+C` |
| 번역할 언어 바꾸기 | 작은 창에서 `Space` |
| 메인 창에서 이어서 작업 | 작은 창에서 `Ctrl+E` |
| 닫기 | `Esc`, 또는 다른 곳을 클릭 (핀으로 고정 가능) |
| 메인 창에서 번역 | `Ctrl+Enter` |

- 번역 방향은 자동입니다. 내 언어(기본 한국어)로 쓴 글은 상대 언어(기본 영어)로, 그 밖의 글은 내 언어로 옮깁니다.
- 문체(기본 · 격식 · 구어 · 학술)를 고르면 그 문체로 다시 번역합니다. ‘다른 표현’은 대안 세 가지를 보여 줍니다.
- 5,000자(설정에서 변경)를 넘는 글은 작은 창 대신 메인 창에서 번역합니다. 6,000자를 넘으면 문단 경계에서 나눠 차례로 번역하고, 누락이나 미번역이 의심되면 한 번 다시 시도한 뒤 안내합니다.
- DeepL 처럼 `Ctrl+C, C` 를 쓰는 다른 프로그램과 겹치면 **설정 › 단축키**에서 조합을 바꿀 수 있습니다.

### 사전과 단어장

- 사전 항목: 표제어, 발음(영어 IPA, 일본어 읽기), 품사별 뜻과 짧은 설명, 예문 두 개와 그 번역, 비슷한 말, 함께 쓰는 말, 쓰임 설명. 비슷한 말·함께 쓰는 말을 누르면 다시 찾고, 🔊 단추는 Windows 음성으로 읽어 줍니다.
- 내 언어로 된 낱말(예: ‘성찰’)을 고르면 상대 언어 대응 표현과 쓰임 차이를 알려 줍니다(거꾸로 찾기). 틀린 철자도 바로잡아 찾습니다.
- `Ctrl+D` 를 한 번만 누르면 0.4초 뒤 원래 프로그램에 그대로 전달되며(북마크 등), 두 번 누를 때만 사전이 뜹니다.
- 80자(설정에서 변경)가 넘는 글을 `Ctrl+D, D` 로 고르면 사전 대신 번역합니다.
- 메인 창 **사전**에서 단어장을 다시 보고 ‘뜻 가리기’로 복습할 수 있습니다.

## 지원 번역 엔진

| 엔진 | 방식 | 속도 (2026-11 기준) |
|---|---|---|
| Claude 구독 | `claude -p` (stream-json 입출력), 프로세스 미리 준비 | 첫 글자 약 0.8초, 한 문장 1.5~2.5초 |
| ChatGPT 구독 (Codex) | `codex exec` (표준 입력, 읽기 전용 샌드박스) | 수 초 |
| Google 구독 (Antigravity) | `agy acp` (무도구·MCP 격리 상주 서버, 기본 `gemini-4-hydrogen-low`) | 미리 준비 시 한 문장 2.5~3.7초 (미준비 약 4.8~5.6초) |
| OpenAI 호환 API | `/chat/completions` 스트리밍 (OpenAI, OpenRouter, Ollama, LM Studio 등) | 서버에 따라 다름 |
| Anthropic API · Gemini API | API 키로 직접 호출, 스트리밍 | 서버에 따라 다름 |

- 엔진을 따로 고르지 않으면 설치된 구독 CLI 가운데 첫 번째(Claude → Codex → Antigravity)를 씁니다.
- ‘실패하면 다른 엔진으로’를 켜면 한도 초과나 오류 때 대체 엔진으로 한 번 다시 시도합니다.

## 데이터와 개인정보

- **설정 · 번역 기록 · 단어장 · 용어집 · API 키는 이 PC 에만 저장됩니다**(`%LOCALAPPDATA%\Yeoul`, 제거해도 남음).
- API 키는 Windows DPAPI(현재 사용자)로 암호화해 보관합니다.
- 번역·사전을 실행할 때만 해당 텍스트가 사용자가 고른 엔진(구독 CLI 또는 API 제공자)으로 전송됩니다. 자동 업데이트 확인은 GitHub Releases 공개 메타데이터만 조회합니다.

## 자매 제품

- **[Ibis](https://github.com/dodaseo/ibis-releases)** — 한국 연구자를 위한 문헌 관리 · 한글/Word 본문 인용
- **[에믹 (Emic)](https://github.com/dodaseo/emic-releases)** — 한국어 질적분석 스튜디오
