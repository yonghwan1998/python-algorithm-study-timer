import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


# =========================================================
# Study Routine
# =========================================================

ROUTINE = [
    {
        "name": "전날 문제 복습",
        "short_name": "복습",
        "minutes": 5,
        "description": (
            "어제 풀었던 문제를 코드 없이 떠올려보세요.\n\n"
            "• 어떤 알고리즘 / 자료구조를 사용했는가?\n"
            "• 왜 그 방법을 사용했는가?\n"
            "• 처음 접근의 문제점은 무엇이었는가?\n"
            "• 시간복잡도는 어떻게 되는가?"
        ),
    },
    {
        "name": "새 문제 풀이",
        "short_name": "문제 풀이",
        "minutes": 25,
        "description": (
            "정답이나 힌트를 보지 않고 먼저 문제를 풀어보세요.\n\n"
            "• 입력 크기 확인\n"
            "• 완전탐색이 가능한가?\n"
            "• Hash / Set을 사용할 수 있는가?\n"
            "• 정렬하면 문제가 단순해지는가?\n"
            "• Stack / Queue 문제인가?\n"
            "• DFS / BFS가 필요한가?\n\n"
            "25분 동안 진전이 없다면\n"
            "문제 재분석 → 힌트 → 아이디어 → 정답"
        ),
    },
    {
        "name": "풀이 분석",
        "short_name": "풀이 분석",
        "minutes": 10,
        "description": (
            "내 풀이와 정석 풀이를 비교하세요.\n\n"
            "• 내 풀이의 시간복잡도는?\n"
            "• 정석 풀이의 시간복잡도는?\n"
            "• 불필요한 반복문이 있었는가?\n"
            "• 더 적절한 자료구조가 있는가?\n"
            "• 같은 계산을 반복하고 있지 않은가?\n"
            "• O(N²)을 O(N) 또는 O(N log N)으로 줄일 수 있는가?"
        ),
    },
    {
        "name": "다시 구현",
        "short_name": "재구현",
        "minutes": 10,
        "description": (
            "정답 코드를 닫고 처음부터 다시 작성하세요.\n\n"
            "• 코드를 외우지 말 것\n"
            "• 풀이 아이디어를 먼저 말로 설명할 것\n"
            "• 자료구조를 선택한 이유를 생각할 것\n"
            "• 막히면 정답 전체가 아니라 필요한 부분만 확인"
        ),
    },
    {
        "name": "문제 기록",
        "short_name": "기록",
        "minutes": 10,
        "description": (
            "오늘 푼 문제를 기록하세요.\n\n"
            "• 문제 이름 / 난이도\n"
            "• 알고리즘 유형\n"
            "• 혼자 풀었는가?\n"
            "• 힌트를 사용했는가?\n"
            "• 처음 생각한 접근\n"
            "• 정석 접근\n"
            "• 시간복잡도\n"
            "• 다시 풀어야 하는가?"
        ),
    },
]


# =========================================================
# Colors
# =========================================================

BG = "#111318"
CARD = "#191C22"
CARD_ALT = "#20242C"

TEXT = "#F4F4F5"
SUB_TEXT = "#9CA3AF"

ACCENT = "#7C6CF2"
ACCENT_HOVER = "#6D5EE7"

BORDER = "#2D323C"


# =========================================================
# Application
# =========================================================

class AlgorithmTimer:
    NORMAL_WIDTH = 680
    NORMAL_HEIGHT = 720

    MINI_WIDTH = 320
    MINI_HEIGHT = 190

    def __init__(self, root):
        self.root = root

        self.root.title("Algorithm Study Timer")
        self.root.geometry(
            f"{self.NORMAL_WIDTH}x{self.NORMAL_HEIGHT}"
        )
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # 기본값: 항상 위
        self.root.attributes("-topmost", True)

        self.current_step = 0
        self.remaining_seconds = self.get_current_duration()

        self.running = False
        self.after_id = None
        self.mini_mode = False

        self.topmost_var = tk.BooleanVar(value=True)

        self.setup_style()

        # 일반 화면 / 미니 화면 분리
        self.normal_frame = tk.Frame(
            self.root,
            bg=BG,
        )

        self.mini_frame = tk.Frame(
            self.root,
            bg=BG,
        )

        self.create_normal_view()
        self.create_mini_view()

        self.show_normal_view()
        self.update_screen()

    # =====================================================
    # Style
    # =====================================================

    def setup_style(self):
        self.style = ttk.Style()

        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure(
            "Study.Horizontal.TProgressbar",
            troughcolor=CARD_ALT,
            background=ACCENT,
            bordercolor=CARD_ALT,
            lightcolor=ACCENT,
            darkcolor=ACCENT,
            thickness=8,
        )

    # =====================================================
    # Helpers
    # =====================================================

    def get_current_duration(self):
        return ROUTINE[self.current_step]["minutes"] * 60

    def create_button(
        self,
        parent,
        text,
        command,
        primary=False,
        width=12,
    ):
        background = ACCENT if primary else CARD_ALT
        hover = ACCENT_HOVER if primary else "#292E38"

        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=background,
            fg=TEXT,
            activebackground=hover,
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=(
                "맑은 고딕",
                10,
                "bold" if primary else "normal",
            ),
            width=width,
            height=2,
            anchor="center",
            justify="center",
            cursor="hand2",
        )

        def on_enter(_):
            button.configure(bg=hover)

        def on_leave(_):
            button.configure(bg=background)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        return button

    # =====================================================
    # Normal View
    # =====================================================

    def create_normal_view(self):
        # ---------------------------------------------
        # Header
        # ---------------------------------------------

        header = tk.Frame(
            self.normal_frame,
            bg=BG,
        )
        header.pack(
            fill="x",
            padx=32,
            pady=(26, 16),
        )

        title_area = tk.Frame(
            header,
            bg=BG,
        )
        title_area.pack(side="left")

        tk.Label(
            title_area,
            text="Algorithm Study",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 24, "bold"),
        ).pack(anchor="w")

        tk.Label(
            title_area,
            text="Daily 60-minute routine",
            bg=BG,
            fg=SUB_TEXT,
            font=("Segoe UI", 10),
        ).pack(
            anchor="w",
            pady=(3, 0),
        )

        self.mini_button = self.create_button(
            header,
            "미니 모드",
            self.show_mini_view,
            width=10,
        )
        self.mini_button.pack(
            side="right",
            pady=5,
        )

        # ---------------------------------------------
        # Options
        # ---------------------------------------------

        option_card = tk.Frame(
            self.normal_frame,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        option_card.pack(
            fill="x",
            padx=32,
            pady=(0, 16),
        )

        option_inner = tk.Frame(
            option_card,
            bg=CARD,
        )
        option_inner.pack(
            fill="x",
            padx=18,
            pady=12,
        )

        self.topmost_switch = tk.Checkbutton(
            option_inner,
            text="항상 위에 표시",
            variable=self.topmost_var,
            command=self.toggle_topmost,
            bg=CARD,
            fg=TEXT,
            activebackground=CARD,
            activeforeground=TEXT,
            selectcolor=ACCENT,
            font=("맑은 고딕", 10),
            cursor="hand2",
            bd=0,
            highlightthickness=0,
        )
        self.topmost_switch.pack(side="left")

        tk.Label(
            option_inner,
            text="다른 창을 선택해도 타이머를 앞에 유지합니다.",
            bg=CARD,
            fg=SUB_TEXT,
            font=("맑은 고딕", 9),
        ).pack(side="right")

        # ---------------------------------------------
        # Timer Card
        # ---------------------------------------------

        timer_card = tk.Frame(
            self.normal_frame,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        timer_card.pack(
            fill="x",
            padx=32,
        )

        timer_inner = tk.Frame(
            timer_card,
            bg=CARD,
        )
        timer_inner.pack(
            fill="x",
            padx=24,
            pady=22,
        )

        top_line = tk.Frame(
            timer_inner,
            bg=CARD,
        )
        top_line.pack(fill="x")

        self.step_label = tk.Label(
            top_line,
            bg=CARD,
            fg=TEXT,
            font=("맑은 고딕", 17, "bold"),
        )
        self.step_label.pack(side="left")

        self.progress_label = tk.Label(
            top_line,
            bg=CARD,
            fg=SUB_TEXT,
            font=("Segoe UI", 10),
        )
        self.progress_label.pack(side="right")

        self.timer_label = tk.Label(
            timer_inner,
            bg=CARD,
            fg=TEXT,
            font=("Consolas", 58, "bold"),
        )
        self.timer_label.pack(
            pady=(18, 12)
        )

        self.progress_bar = ttk.Progressbar(
            timer_inner,
            style="Study.Horizontal.TProgressbar",
            maximum=100,
        )
        self.progress_bar.pack(fill="x")

        # ---------------------------------------------
        # Description
        # ---------------------------------------------

        description_card = tk.Frame(
            self.normal_frame,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1,
            height=220,
        )

        description_card.pack(
            fill="x",
            padx=32,
            pady=16,
        )

        # 내용 길이에 따라 카드 크기가 변하지 않음
        description_card.pack_propagate(False)

        description_header = tk.Label(
            description_card,
            text="지금 할 일",
            bg=CARD,
            fg=SUB_TEXT,
            font=("맑은 고딕", 9, "bold"),
        )
        description_header.pack(
            anchor="w",
            padx=20,
            pady=(15, 5),
        )

        description_content = tk.Frame(
            description_card,
            bg=CARD,
        )
        description_content.pack(
            fill="both",
            expand=True,
            padx=(20, 12),
            pady=(0, 15),
        )

        description_scrollbar = tk.Scrollbar(
            description_content,
            orient="vertical",
            bg=CARD_ALT,
            troughcolor=CARD,
            activebackground=ACCENT,
            bd=0,
            highlightthickness=0,
        )
        description_scrollbar.pack(
            side="right",
            fill="y",
        )

        self.description_text = tk.Text(
            description_content,
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT,
            selectbackground=ACCENT,
            relief="flat",
            bd=0,
            highlightthickness=0,
            wrap="word",
            font=("맑은 고딕", 10),
            yscrollcommand=description_scrollbar.set,
            padx=0,
            pady=0,
        )
        self.description_text.pack(
            side="left",
            fill="both",
            expand=True,
        )

        description_scrollbar.config(
            command=self.description_text.yview
        )

        self.description_text.config(
            state="disabled"
        )

        # ---------------------------------------------
        # Controls
        # ---------------------------------------------

        controls = tk.Frame(
            self.normal_frame,
            bg=BG,
        )
        controls.pack(
            fill="x",
            padx=32,
            pady=(2, 16),
        )

        # 4개의 버튼 영역을 동일한 크기로
        for i in range(4):
            controls.grid_columnconfigure(
                i,
                weight=1,
                uniform="control",
            )

        self.start_button = self.create_button(
            controls,
            "시작",
            self.start,
            primary=True,
        )
        self.start_button.grid(
            row=0,
            column=0,
            padx=(0, 4),
            sticky="ew",
        )

        self.pause_button = self.create_button(
            controls,
            "일시정지",
            self.pause,
        )
        self.pause_button.grid(
            row=0,
            column=1,
            padx=4,
            sticky="ew",
        )

        self.next_button = self.create_button(
            controls,
            "다음 단계",
            self.next_step,
        )
        self.next_button.grid(
            row=0,
            column=2,
            padx=4,
            sticky="ew",
        )

        self.reset_button = self.create_button(
            controls,
            "처음부터",
            self.reset,
        )
        self.reset_button.grid(
            row=0,
            column=3,
            padx=(4, 0),
            sticky="ew",
        )

        # ---------------------------------------------
        # Footer
        # ---------------------------------------------

        self.routine_label = tk.Label(
            self.normal_frame,
            text=(
                "복습 5m   ·   문제 풀이 25m   ·   "
                "분석 10m   ·   재구현 10m   ·   기록 10m"
            ),
            bg=BG,
            fg=SUB_TEXT,
            font=("Segoe UI", 9),
        )
        self.routine_label.pack(
            pady=(0, 15)
        )

    # =====================================================
    # Mini View
    # =====================================================

    def create_mini_view(self):
        container = tk.Frame(
            self.mini_frame,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        container.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8,
        )

        top = tk.Frame(
            container,
            bg=CARD,
        )
        top.pack(
            fill="x",
            padx=14,
            pady=(10, 0),
        )

        self.mini_step_label = tk.Label(
            top,
            bg=CARD,
            fg=SUB_TEXT,
            font=("맑은 고딕", 9, "bold"),
        )
        self.mini_step_label.pack(side="left")

        self.restore_button = tk.Button(
            top,
            text="전체 보기",
            command=self.show_normal_view,
            bg=CARD_ALT,
            fg=TEXT,
            activebackground="#292E38",
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=("맑은 고딕", 8),
            cursor="hand2",
            padx=8,
            pady=4,
        )
        self.restore_button.pack(side="right")

        self.mini_timer_label = tk.Label(
            container,
            bg=CARD,
            fg=TEXT,
            font=("Consolas", 36, "bold"),
        )
        self.mini_timer_label.pack(
            pady=(8, 5)
        )

        mini_controls = tk.Frame(
            container,
            bg=CARD,
        )
        mini_controls.pack(
            fill="x",
            padx=14,
            pady=(2, 10),
        )

        for i in range(3):
            mini_controls.grid_columnconfigure(
                i,
                weight=1,
                uniform="mini_control",
            )

        self.mini_start_button = self.create_button(
            mini_controls,
            "시작",
            self.start,
            primary=True,
            width=8,
        )
        self.mini_start_button.grid(
            row=0,
            column=0,
            padx=(0, 3),
            sticky="ew",
        )

        self.mini_pause_button = self.create_button(
            mini_controls,
            "정지",
            self.pause,
            width=8,
        )
        self.mini_pause_button.grid(
            row=0,
            column=1,
            padx=3,
            sticky="ew",
        )

        self.mini_next_button = self.create_button(
            mini_controls,
            "다음",
            self.next_step,
            width=8,
        )
        self.mini_next_button.grid(
            row=0,
            column=2,
            padx=(3, 0),
            sticky="ew",
        )

    # =====================================================
    # View Switching
    # =====================================================

    def show_normal_view(self):
        self.mini_mode = False

        self.mini_frame.pack_forget()

        self.root.geometry(
            f"{self.NORMAL_WIDTH}x{self.NORMAL_HEIGHT}"
        )

        self.normal_frame.pack(
            fill="both",
            expand=True,
        )

        self.update_screen()

    def show_mini_view(self):
        self.mini_mode = True

        self.normal_frame.pack_forget()

        self.root.geometry(
            f"{self.MINI_WIDTH}x{self.MINI_HEIGHT}"
        )

        self.mini_frame.pack(
            fill="both",
            expand=True,
        )

        self.update_screen()

    # =====================================================
    # Always On Top
    # =====================================================

    def toggle_topmost(self):
        self.root.attributes(
            "-topmost",
            self.topmost_var.get(),
        )

    # =====================================================
    # Timer
    # =====================================================

    def start(self):
        if self.running:
            return

        if self.remaining_seconds <= 0:
            return

        self.running = True

        self.update_button_text()
        self.tick()

    def pause(self):
        if not self.running:
            return

        self.running = False

        if self.after_id is not None:
            self.root.after_cancel(
                self.after_id
            )
            self.after_id = None

        self.update_button_text()

    def tick(self):
        if not self.running:
            return

        if self.remaining_seconds <= 0:
            self.running = False
            self.after_id = None

            self.update_screen()

            self.root.bell()
            self.complete_step()
            return

        self.remaining_seconds -= 1

        self.update_screen()

        self.after_id = self.root.after(
            1000,
            self.tick,
        )

    # =====================================================
    # Step Management
    # =====================================================

    def complete_step(self):
        current_name = ROUTINE[self.current_step]["name"]

        if self.current_step == len(ROUTINE) - 1:
            messagebox.showinfo(
                "오늘 공부 완료",
                (
                    "오늘의 알고리즘 1시간 루틴을 완료했습니다.\n\n"
                    "복습이 필요한 문제는 따로 표시해두세요."
                ),
            )

            self.update_button_text(
                completed=True
            )
            return

        next_name = ROUTINE[
            self.current_step + 1
        ]["name"]

        messagebox.showinfo(
            "단계 완료",
            (
                f"{current_name} 완료\n\n"
                f"다음 단계: {next_name}"
            ),
        )

        self.current_step += 1

        self.remaining_seconds = (
            self.get_current_duration()
        )

        self.update_screen()

        # 다음 단계 자동 시작
        self.start()

    def next_step(self):
        if self.current_step >= len(ROUTINE) - 1:
            messagebox.showinfo(
                "마지막 단계",
                "현재가 마지막 단계입니다.",
            )
            return

        self.stop_current_timer()

        self.current_step += 1
        self.remaining_seconds = (
            self.get_current_duration()
        )

        self.update_screen()
        self.update_button_text()

    def reset(self):
        self.stop_current_timer()

        self.current_step = 0
        self.remaining_seconds = (
            self.get_current_duration()
        )

        self.update_screen()
        self.update_button_text()

    def stop_current_timer(self):
        self.running = False

        if self.after_id is not None:
            self.root.after_cancel(
                self.after_id
            )
            self.after_id = None

    # =====================================================
    # Screen Update
    # =====================================================

    def update_screen(self):
        routine = ROUTINE[self.current_step]

        minutes = (
            self.remaining_seconds // 60
        )
        seconds = (
            self.remaining_seconds % 60
        )

        time_text = (
            f"{minutes:02d}:{seconds:02d}"
        )

        # ---------------------------------------------
        # Normal View
        # ---------------------------------------------

        self.step_label.config(
            text=routine["name"]
        )

        self.progress_label.config(
            text=(
                f"{self.current_step + 1}"
                f" / {len(ROUTINE)}"
            )
        )

        self.timer_label.config(
            text=time_text
        )

        # 설명 업데이트
        self.description_text.config(
            state="normal"
        )

        self.description_text.delete(
            "1.0",
            tk.END
        )

        self.description_text.insert(
            tk.END,
            routine["description"]
        )

        # 단계 변경 시 항상 최상단
        self.description_text.yview_moveto(0)

        self.description_text.config(
            state="disabled"
        )

        # 현재 단계 진행률
        duration = (
            routine["minutes"] * 60
        )

        elapsed = (
            duration
            - self.remaining_seconds
        )

        if duration > 0:
            percentage = (
                elapsed / duration
            ) * 100
        else:
            percentage = 0

        self.progress_bar["value"] = (
            percentage
        )

        # ---------------------------------------------
        # Mini View
        # ---------------------------------------------

        self.mini_step_label.config(
            text=(
                f"{self.current_step + 1}/"
                f"{len(ROUTINE)}  "
                f"{routine['short_name']}"
            )
        )

        self.mini_timer_label.config(
            text=time_text
        )

        self.update_button_text()

    def update_button_text(
        self,
        completed=False,
    ):
        if completed:
            normal_text = "완료"
            mini_text = "완료"

        elif self.running:
            normal_text = "진행 중"
            mini_text = "진행"

        elif (
            self.remaining_seconds
            == self.get_current_duration()
        ):
            normal_text = "시작"
            mini_text = "시작"

        else:
            normal_text = "계속"
            mini_text = "계속"

        self.start_button.config(
            text=normal_text
        )

        self.mini_start_button.config(
            text=mini_text
        )


# =========================================================
# Run
# =========================================================

if __name__ == "__main__":
    root = tk.Tk()

    app = AlgorithmTimer(root)

    root.mainloop()