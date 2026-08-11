import tkinter as tk
from tkinter import messagebox


ROUTINE = [
    {
        "name": "전날 문제 복습",
        "minutes": 5,
        "description": (
            "어제 풀었던 문제를 코드 없이 떠올려보세요.\n\n"
            "✓ 어떤 알고리즘/자료구조를 사용했는가?\n"
            "✓ 왜 그 방법을 사용했는가?\n"
            "✓ 처음 접근의 문제점은 무엇이었는가?\n"
            "✓ 시간복잡도는 어떻게 되는가?"
        ),
    },
    {
        "name": "새 문제 풀이",
        "minutes": 25,
        "description": (
            "정답이나 힌트를 보지 않고 먼저 문제를 풀어보세요.\n\n"
            "✓ 입력 크기 확인\n"
            "✓ 완전탐색이 가능한가?\n"
            "✓ Hash / Set을 사용할 수 있는가?\n"
            "✓ 정렬하면 문제가 단순해지는가?\n"
            "✓ Stack / Queue 문제인가?\n"
            "✓ DFS / BFS가 필요한가?\n\n"
            "25분 동안 진전이 없다면:\n"
            "문제 재분석 → 힌트 → 아이디어 → 정답 순서"
        ),
    },
    {
        "name": "풀이 분석",
        "minutes": 10,
        "description": (
            "내 풀이와 정석 풀이를 비교하세요.\n\n"
            "✓ 내 풀이의 시간복잡도는?\n"
            "✓ 정석 풀이의 시간복잡도는?\n"
            "✓ 불필요한 반복문이 있었는가?\n"
            "✓ 더 적절한 자료구조가 있는가?\n"
            "✓ 매번 같은 계산을 반복하고 있지 않은가?\n"
            "✓ O(N²)을 O(N) 또는 O(N log N)으로 줄일 수 있는가?"
        ),
    },
    {
        "name": "다시 구현",
        "minutes": 10,
        "description": (
            "정답 코드를 닫고 처음부터 다시 작성하세요.\n\n"
            "✓ 코드를 외우지 말 것\n"
            "✓ 풀이 아이디어를 먼저 말로 설명할 것\n"
            "✓ 자료구조를 선택한 이유를 생각할 것\n"
            "✓ 막히면 정답 전체가 아니라 필요한 부분만 확인"
        ),
    },
    {
        "name": "문제 기록",
        "minutes": 10,
        "description": (
            "오늘 푼 문제를 기록하세요.\n\n"
            "✓ 문제 이름 / 난이도\n"
            "✓ 알고리즘 유형\n"
            "✓ 혼자 풀었는가?\n"
            "✓ 힌트를 사용했는가?\n"
            "✓ 처음 생각한 접근\n"
            "✓ 정석 접근\n"
            "✓ 시간복잡도\n"
            "✓ 다시 풀어야 하는가?"
        ),
    },
]


class AlgorithmTimer:
    def __init__(self, root):
        self.root = root

        self.root.title("Algorithm Study Timer")
        self.root.geometry("650x680")
        self.root.resizable(False, False)

        self.current_step = 0
        self.remaining_seconds = self.get_current_duration()

        self.running = False
        self.after_id = None

        self.create_widgets()
        self.update_screen()

    def get_current_duration(self):
        return ROUTINE[self.current_step]["minutes"] * 60

    def create_widgets(self):
        # 제목
        self.title_label = tk.Label(
            self.root,
            text="알고리즘 1시간 루틴",
            font=("맑은 고딕", 23, "bold"),
        )
        self.title_label.pack(pady=(25, 8))

        self.total_label = tk.Label(
            self.root,
            text="5분 + 25분 + 10분 + 10분 + 10분 = 60분",
            font=("맑은 고딕", 10),
        )
        self.total_label.pack()

        # 현재 단계
        self.step_label = tk.Label(
            self.root,
            font=("맑은 고딕", 17, "bold"),
        )
        self.step_label.pack(pady=(20, 5))

        self.progress_label = tk.Label(
            self.root,
            font=("맑은 고딕", 10),
        )
        self.progress_label.pack()

        # 타이머
        self.timer_label = tk.Label(
            self.root,
            font=("Consolas", 55, "bold"),
        )
        self.timer_label.pack(pady=15)

        # 현재 단계 설명 영역
        description_frame = tk.LabelFrame(
            self.root,
            text=" 지금 할 일 ",
            font=("맑은 고딕", 11, "bold"),
            padx=15,
            pady=12,
        )
        description_frame.pack(
            padx=30,
            pady=5,
            fill="both",
        )

        self.description_label = tk.Label(
            description_frame,
            justify="left",
            anchor="w",
            font=("맑은 고딕", 10),
            wraplength=540,
        )
        self.description_label.pack(
            fill="both",
        )

        # 버튼
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        self.start_button = tk.Button(
            button_frame,
            text="시작",
            width=11,
            height=2,
            command=self.start,
        )
        self.start_button.grid(
            row=0,
            column=0,
            padx=5,
        )

        self.pause_button = tk.Button(
            button_frame,
            text="일시정지",
            width=11,
            height=2,
            command=self.pause,
        )
        self.pause_button.grid(
            row=0,
            column=1,
            padx=5,
        )

        self.next_button = tk.Button(
            button_frame,
            text="다음 단계",
            width=11,
            height=2,
            command=self.next_step,
        )
        self.next_button.grid(
            row=0,
            column=2,
            padx=5,
        )

        self.reset_button = tk.Button(
            button_frame,
            text="처음부터",
            width=11,
            height=2,
            command=self.reset,
        )
        self.reset_button.grid(
            row=1,
            column=1,
            padx=5,
            pady=10,
        )

        # 전체 루틴
        self.routine_label = tk.Label(
            self.root,
            text=(
                "복습 5분  →  문제 풀이 25분  →  분석 10분\n"
                "→  재구현 10분  →  기록 10분"
            ),
            font=("맑은 고딕", 10),
        )
        self.routine_label.pack(pady=5)

    def start(self):
        if self.running:
            return

        # 이미 시간이 끝난 상태에서 시작하는 것 방지
        if self.remaining_seconds <= 0:
            return

        self.running = True
        self.start_button.config(text="진행 중")

        self.tick()

    def pause(self):
        self.running = False

        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        self.start_button.config(text="계속")

    def tick(self):
        if not self.running:
            return

        self.update_screen()

        if self.remaining_seconds <= 0:
            self.running = False
            self.after_id = None

            self.root.bell()

            self.complete_step()
            return

        self.remaining_seconds -= 1

        self.after_id = self.root.after(
            1000,
            self.tick,
        )

    def complete_step(self):
        current_name = ROUTINE[self.current_step]["name"]

        # 마지막 단계
        if self.current_step == len(ROUTINE) - 1:
            messagebox.showinfo(
                "오늘 공부 완료 🎉",
                (
                    "오늘의 알고리즘 1시간 루틴을 완료했습니다.\n\n"
                    "오늘 풀었던 문제 중 다시 풀어야 할 문제가 있다면\n"
                    "복습 대상으로 표시해두세요."
                ),
            )

            self.start_button.config(text="완료")
            return

        next_name = ROUTINE[self.current_step + 1]["name"]

        messagebox.showinfo(
            "단계 완료",
            (
                f"✅ {current_name} 완료!\n\n"
                f"다음 단계\n"
                f"👉 {next_name}"
            ),
        )

        self.current_step += 1
        self.remaining_seconds = self.get_current_duration()

        self.update_screen()

        # 자동으로 다음 단계 시작
        self.start()

    def next_step(self):
        self.pause()

        if self.current_step >= len(ROUTINE) - 1:
            messagebox.showinfo(
                "마지막 단계",
                "현재가 마지막 단계입니다.",
            )
            return

        self.current_step += 1
        self.remaining_seconds = self.get_current_duration()

        self.start_button.config(text="시작")

        self.update_screen()

    def reset(self):
        self.pause()

        self.current_step = 0
        self.remaining_seconds = self.get_current_duration()

        self.start_button.config(text="시작")

        self.update_screen()

    def update_screen(self):
        routine = ROUTINE[self.current_step]

        step_name = routine["name"]
        description = routine["description"]

        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60

        self.step_label.config(
            text=step_name
        )

        self.description_label.config(
            text=description
        )

        self.timer_label.config(
            text=f"{minutes:02d}:{seconds:02d}"
        )

        self.progress_label.config(
            text=(
                f"{self.current_step + 1} / "
                f"{len(ROUTINE)} 단계 · "
                f"{routine['minutes']}분"
            )
        )


if __name__ == "__main__":
    root = tk.Tk()

    app = AlgorithmTimer(root)

    root.mainloop()