# Algorithm Study Timer

매일 1시간 동안 알고리즘 문제 풀이 루틴을 꾸준히 진행할 수 있도록 만든 Windows용 타이머 애플리케이션입니다.

Python의 `tkinter`를 사용해 구현했으며, PyInstaller를 이용해 Windows 실행 파일(`.exe`)로 빌드할 수 있습니다.

## 주요 기능

* 1시간 알고리즘 공부 루틴 자동 진행
* 단계별 카운트다운 타이머
* 현재 단계별 학습 가이드 표시
* 시작 / 일시정지 / 다음 단계 / 처음부터 기능
* 각 단계 종료 시 알림
* 마지막 단계 종료 시 전체 학습 완료 알림
* 별도 GUI 라이브러리 없이 Python 기본 `tkinter` 사용

## 공부 루틴

총 60분을 아래와 같이 구성합니다.

| 단계       |  시간 | 내용                          |
| -------- | --: | --------------------------- |
| 전날 문제 복습 |  10분 | 이전 문제의 알고리즘, 자료구조, 시간복잡도 복습 |
| 새 문제 풀이  | 25분 | 힌트 없이 새로운 문제 풀이             |
| 풀이 분석    | 10분 | 내 풀이와 정석 풀이 비교 및 시간복잡도 분석   |
| 다시 구현    | 15분 | 정답을 닫고 처음부터 직접 재구현          |
| 문제 기록    | - | 풀이 과정, 알고리즘 유형, 복습 필요 여부 기록 |

## 단계별 학습 가이드

### 1. 전날 문제 복습

* 어떤 알고리즘 또는 자료구조를 사용했는가?
* 왜 해당 방법을 사용했는가?
* 처음 접근의 문제점은 무엇이었는가?
* 시간복잡도는 어떻게 되는가?

### 2. 새 문제 풀이

문제를 읽고 다음 내용을 확인합니다.

* 입력 크기는 어느 정도인가?
* 완전탐색이 가능한가?
* Hash / Set을 활용할 수 있는가?
* 정렬하면 문제 구조가 단순해지는가?
* Stack / Queue 문제인가?
* DFS / BFS가 필요한가?

25분 동안 풀이 방향을 찾지 못했다면 다음 순서로 진행합니다.

```text
문제 재분석
→ 힌트 확인
→ 아이디어 확인
→ 정답 확인
```

### 3. 풀이 분석

* 내 풀이의 시간복잡도는?
* 정석 풀이의 시간복잡도는?
* 불필요한 반복문이 있었는가?
* 더 적절한 자료구조가 있는가?
* 동일한 계산을 반복하고 있지는 않은가?
* `O(N²)`을 `O(N)` 또는 `O(N log N)`으로 개선할 수 있는가?

### 4. 다시 구현

정답 코드를 그대로 따라 작성하지 않습니다.

* 정답 코드를 닫고 다시 작성
* 풀이 흐름을 먼저 말로 설명
* 자료구조를 선택한 이유 생각하기
* 막힌 경우 필요한 부분만 다시 확인

### 5. 문제 기록

문제를 풀고 다음 내용을 기록합니다.

* 문제 이름
* 난이도
* 알고리즘 유형
* 혼자 해결했는지
* 힌트를 사용했는지
* 처음 생각한 접근
* 정석 접근
* 시간복잡도
* 다시 풀 필요가 있는지

## 실행 화면

```text
┌──────────────────────────────────────┐
│          알고리즘 1시간 루틴          │
│                                      │
│             새 문제 풀이              │
│                                      │
│                24:31                 │
│                                      │
│              2 / 5 단계               │
│                                      │
│ [ 지금 할 일 ]                       │
│                                      │
│ ✓ 입력 크기 확인                     │
│ ✓ 완전탐색이 가능한가?               │
│ ✓ Hash / Set을 사용할 수 있는가?     │
│ ✓ 정렬하면 문제가 단순해지는가?      │
│ ✓ Stack / Queue 문제인가?            │
│ ✓ DFS / BFS가 필요한가?              │
│                                      │
│ [시작] [일시정지] [다음 단계]        │
│            [처음부터]                 │
└──────────────────────────────────────┘
```

## 프로젝트 구조

```text
algorithm-study-timer/
├── algorithm_timer.py
├── README.md
└── .gitignore
```

PyInstaller로 빌드하면 다음 파일들이 추가될 수 있습니다.

```text
algorithm-study-timer/
├── algorithm_timer.py
├── README.md
├── .gitignore
├── AlgorithmTimer.spec
├── build/
└── dist/
    └── AlgorithmTimer.exe
```

`build/`, `dist/`, `.spec` 파일은 필요에 따라 Git에서 제외할 수 있습니다.

## 실행 환경

* Python 3.x
* Windows
* tkinter

`tkinter`는 일반적인 Windows용 Python 설치 환경에 기본 포함되어 있습니다.

## 실행 방법

Repository를 clone합니다.

```bash
git clone https://github.com/yonghwan1998/python-algorithm-study-timer.git
```

프로젝트 폴더로 이동합니다.

```bash
cd python-algorithm-study-timer
```

프로그램을 실행합니다.

```bash
python algorithm_timer.py
```

또는 Windows 환경에서는 다음 명령어를 사용할 수 있습니다.

```bash
py algorithm_timer.py
```

## Windows 실행 파일 만들기

PyInstaller를 설치합니다.

```bash
py -m pip install pyinstaller
```

실행 파일을 생성합니다.

```bash
pyinstaller --onefile --windowed --name AlgorithmTimer algorithm_timer.py
```

빌드가 완료되면 다음 경로에 실행 파일이 생성됩니다.

```text
dist/AlgorithmTimer.exe
```

`--windowed` 옵션을 사용하기 때문에 실행 시 별도의 콘솔 창이 나타나지 않습니다.

## 추천 `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo

# Virtual Environment
.venv/
venv/

# PyInstaller
build/
dist/
*.spec

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

## 향후 추가 예정 기능

* 전체 60분 진행률 Progress Bar
* 완료된 단계 체크 표시
* 현재까지 공부한 실제 시간 표시
* 오늘의 공부 기록 CSV 저장
* 공부 기록 통계
* 항상 위에 표시 옵션
* 단계별 시간 사용자 설정
* 문제 기록 페이지 바로가기
* Windows 실행 파일 배포

## 목적

이 프로젝트의 목적은 단순히 시간을 측정하는 것이 아니라,

> 문제 풀이 → 분석 → 재구현 → 기록

과정을 매일 반복해 알고리즘 문제 해결 패턴을 익히는 것입니다.

문제를 많이 푸는 것보다 문제를 보고 적절한 자료구조와 알고리즘을 떠올릴 수 있도록 만드는 것을 목표로 합니다.

## License

This project is for personal study and learning purposes.
