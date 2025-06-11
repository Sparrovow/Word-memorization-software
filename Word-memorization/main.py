import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import random
from datetime import datetime, timedelta


class VocabularyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("背单词软件")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)

        # 设置中文字体
        self.font_family = "SimHei"

        # 用户数据
        self.user_data = {
            "username": "",
            "password": "",
            "learning_goal": "",
            "starred_words": [],
            "learning_history": [],
            "settings": {
                "font_size": 12,
                "theme_color": "#4a7abc",
                "dark_mode": False
            }
        }

        # 单词库（示例数据）
        try:
            with open('word_banks.json', 'r', encoding='utf-8') as file:
                self.word_banks = json.load(file)
        except:
            # 如果文件不存在或出错，使用备用数据
            self.word_banks = {
                "high_school": [
                    {"word": "abandon", "meaning": "放弃，抛弃", "example": "She had to abandon her dream."},
                    {"word": "absorb", "meaning": "吸收，理解", "example": "Plants absorb sunlight."},
                    {"word": "academic", "meaning": "学术的，学院的", "example": "She has excellent academic records."},
                    {"word": "accumulate", "meaning": "积累，积聚", "example": "He accumulated a fortune."},
                    {"word": "adapt", "meaning": "适应，改编", "example": "We must adapt to new conditions."}
                ],
                "cet4": [
                    {"word": "adequate", "meaning": "足够的，适当的", "example": "We have adequate resources."},
                    {"word": "ambiguous", "meaning": "模棱两可的", "example": "His answer was ambiguous."},
                    {"word": "annual", "meaning": "每年的，年度的", "example": "The annual meeting is in December."},
                    {"word": "anticipate", "meaning": "预期，期望", "example": "We anticipate good results."},
                    {"word": "appeal", "meaning": "呼吁，上诉", "example": "The charity appeal raised millions."}
                ],
                "cet6": [
                    {"word": "aberration", "meaning": "偏差，脱离常轨", "example": "This behavior is an aberration."},
                    {"word": "abjure", "meaning": "发誓放弃，宣誓弃绝", "example": "He abjured his old beliefs."},
                    {"word": "abdicate", "meaning": "退位，放弃", "example": "The king abdicated the throne."},
                    {"word": "aberrant", "meaning": "异常的，脱离常轨的", "example": "His aberrant behavior surprised everyone."},
                    {"word": "abide", "meaning": "遵守，忍受", "example": "Abide by the rules."}
                ]
            }
        # 当前单词列表
        self.current_words = []

        # 创建主框架
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 初始显示登录界面
        self.show_login()

    def show_login(self):
        # 清空主框架
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # 创建登录框架
        login_frame = tk.Frame(self.main_frame, padx=20, pady=20)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # 标题
        tk.Label(login_frame, text="背单词软件", font=(self.font_family, 24, "bold")).grid(row=0, column=0,
                                                                                       columnspan=2, pady=20)

        # 用户名
        tk.Label(login_frame, text="用户名:", font=(self.font_family, 12)).grid(row=1, column=0, sticky="w", pady=10)
        self.username_entry = tk.Entry(login_frame, font=(self.font_family, 12), width=20)
        self.username_entry.grid(row=1, column=1, pady=10)

        # 密码
        tk.Label(login_frame, text="密码:", font=(self.font_family, 12)).grid(row=2, column=0, sticky="w", pady=10)
        self.password_entry = tk.Entry(login_frame, font=(self.font_family, 12), width=20, show="*")
        self.password_entry.grid(row=2, column=1, pady=10)

        # 登录按钮
        login_btn = tk.Button(login_frame, text="登录", font=(self.font_family, 12),
                             command=self.login, width=10)
        login_btn.grid(row=3, column=0, pady=20, padx=5)

        # 注册按钮
        register_btn = tk.Button(login_frame, text="注册", font=(self.font_family, 12),
                                command=self.show_register, width=10)
        register_btn.grid(row=3, column=1, pady=20, padx=5)

    def show_register(self):
        # 清空主框架
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # 创建注册框架
        register_frame = tk.Frame(self.main_frame, padx=20, pady=20)
        register_frame.place(relx=0.5, rely=0.5, anchor="center")

        # 标题
        tk.Label(register_frame, text="新用户注册", font=(self.font_family, 24, "bold")).grid(row=0, column=0,
                                                                                        columnspan=2, pady=20)

        # 用户名
        tk.Label(register_frame, text="用户名:", font=(self.font_family, 12)).grid(row=1, column=0, sticky="w", pady=10)
        self.register_username = tk.Entry(register_frame, font=(self.font_family, 12), width=20)
        self.register_username.grid(row=1, column=1, pady=10)

        # 密码
        tk.Label(register_frame, text="密码:", font=(self.font_family, 12)).grid(row=2, column=0, sticky="w", pady=10)
        self.register_password = tk.Entry(register_frame, font=(self.font_family, 12), width=20, show="*")
        self.register_password.grid(row=2, column=1, pady=10)

        # 确认密码
        tk.Label(register_frame, text="确认密码:", font=(self.font_family, 12)).grid(row=3, column=0, sticky="w", pady=10)
        self.register_confirm_password = tk.Entry(register_frame, font=(self.font_family, 12), width=20, show="*")
        self.register_confirm_password.grid(row=3, column=1, pady=10)

        # 学习目标
        tk.Label(register_frame, text="学习目标:", font=(self.font_family, 12)).grid(row=4, column=0, sticky="w", pady=10)
        self.learning_goal = tk.StringVar(value="high_school")
        goal_frame = tk.Frame(register_frame)
        goal_frame.grid(row=4, column=1, pady=10, sticky="w")

        goals = [("高中", "high_school"), ("四级", "cet4"), ("六级", "cet6")]
        for i, (text, value) in enumerate(goals):
            tk.Radiobutton(goal_frame, text=text, variable=self.learning_goal, value=value,
                          font=(self.font_family, 12)).grid(row=0, column=i, padx=5)

        # 注册按钮
        tk.Button(register_frame, text="注册", font=(self.font_family, 12),
                  command=self.register, width=15).grid(row=5, column=0, columnspan=2, pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("错误", "用户名和密码不能为空")
            return

        # 检查用户文件是否存在
        user_file = f"{username}.json"
        if not os.path.exists(user_file):
            messagebox.showerror("错误", "用户不存在")
            return

        # 读取用户数据
        try:
            with open(user_file, "r", encoding="utf-8") as f:
                self.user_data = json.load(f)

            if self.user_data["password"] != password:
                messagebox.showerror("错误", "密码错误")
                return

            messagebox.showinfo("成功", f"欢迎回来，{username}!")
            self.load_word_bank()
            self.show_main_menu()
        except Exception as e:
            messagebox.showerror("错误", f"登录失败: {str(e)}")

    def register(self):
        username = self.register_username.get()
        password = self.register_password.get()
        confirm_password = self.register_confirm_password.get()
        learning_goal = self.learning_goal.get()

        if not username or not password:
            messagebox.showerror("错误", "用户名和密码不能为空")
            return

        if password != confirm_password:
            messagebox.showerror("错误", "两次输入的密码不一致")
            return

        # 检查用户文件是否已存在
        user_file = f"{username}.json"
        if os.path.exists(user_file):
            messagebox.showerror("错误", "用户名已存在")
            return

        # 创建新用户数据
        self.user_data["username"] = username
        self.user_data["password"] = password
        self.user_data["learning_goal"] = learning_goal

        # 保存用户数据
        try:
            with open(user_file, "w", encoding="utf-8") as f:
                json.dump(self.user_data, f, ensure_ascii=False, indent=4)

            messagebox.showinfo("成功", "注册成功，请登录")
            self.show_login()
        except Exception as e:
            messagebox.showerror("错误", f"注册失败: {str(e)}")

    def load_word_bank(self):
        # 根据学习目标加载单词库
        goal = self.user_data["learning_goal"]
        if goal in self.word_banks:
            self.current_words = self.word_banks[goal]
        else:
            # 如果目标词库不存在，默认加载高中词库
            self.current_words = self.word_banks.get("high_school", [])
            self.user_data["learning_goal"] = "high_school"

            # 保存用户数据
            try:
                user_file = f"{self.user_data['username']}.json"
                with open(user_file, "w", encoding="utf-8") as f:
                    json.dump(self.user_data, f, ensure_ascii=False, indent=4)
            except Exception as e:
                messagebox.showerror("错误", f"加载词库失败: {str(e)}")

    def calculate_weekly_stats(self):
        """计算本周的学习统计数据"""
        # 获取当前日期和一周前的日期
        today = datetime.now()
        week_ago = today - timedelta(days=7)

        # 初始化统计变量
        learning_days = 0
        new_words = 0
        review_words = 0
        quiz_correct = 0
        quiz_total = 0

        # 遍历学习历史记录
        for entry in self.user_data.get("learning_history", []):
            try:
                entry_date = datetime.strptime(entry["date"], "%Y-%m-%d")
                if week_ago <= entry_date <= today:
                    learning_days += 1
                    new_words += entry.get("new_words", 0)
                    review_words += entry.get("review_words", 0)
                    quiz_correct += entry.get("quiz_correct_answers", 0)
                    quiz_total += entry.get("quiz_total_questions", 0)
            except:
                continue

        # 计算平均测验正确率
        avg_quiz_accuracy = "0%"
        if quiz_total > 0:
            accuracy = (quiz_correct / quiz_total) * 100
            avg_quiz_accuracy = f"{accuracy:.0f}%"

        return {
            "学习天数": learning_days,
            "新学单词": new_words,
            "复习单词": review_words,
            "测验正确率": avg_quiz_accuracy
        }

    def check_answer(self):
        user_answer = self.quiz_entry.get().strip()
        correct_answer = self.current_quiz_word["word"]

        is_correct = user_answer == correct_answer
        if is_correct:
            self.quiz_correct += 1
            messagebox.showinfo("正确", "回答正确！")
        else:
            messagebox.showerror("错误", f"回答错误，正确答案是: {correct_answer}")

        self.quiz_progress += 1

        if self.quiz_progress < self.quiz_total:
            # 清空测验区域，保留顶部导航栏
            for widget in self.main_frame.winfo_children():
                if widget != self.main_frame.winfo_children()[0]:  # 跳过顶部导航栏
                    widget.destroy()

            # 更新顶部导航栏的进度
            top_bar = self.main_frame.winfo_children()[0]
            for widget in top_bar.winfo_children():
                if isinstance(widget, tk.Label) and "测验进度" in widget.cget("text"):
                    widget.config(text=f"测验进度: {self.quiz_progress}/{self.quiz_total}")

            # 创建新的测验区域，保持一致的布局
            quiz_frame = tk.Frame(self.main_frame, padx=20, pady=20)
            quiz_frame.pack(fill=tk.BOTH, expand=True)

            # 显示下一个单词的释义
            self.current_quiz_word = self.quiz_words[self.quiz_progress]
            tk.Label(quiz_frame, text=f"释义: {self.current_quiz_word['meaning']}", font=(self.font_family, 24)).pack(
                pady=40)

            # 用户输入框
            self.quiz_entry = tk.Entry(quiz_frame, font=(self.font_family, 16), width=20)
            self.quiz_entry.pack(pady=20)

            # 提交按钮
            submit_btn = tk.Button(quiz_frame, text="提交", font=(self.font_family, 16),
                                   command=self.check_answer)
            submit_btn.pack(pady=20)
        else:
            # 测验结束，显示结果
            accuracy = (self.quiz_correct / self.quiz_total) * 100
            messagebox.showinfo("测验结束", f"测验结束，你的正确率是: {accuracy:.0f}%")

            # 记录测验历史
            today = datetime.now().strftime("%Y-%m-%d")
            for entry in self.user_data["learning_history"]:
                if entry["date"] == today:
                    entry["quiz_total_questions"] = entry.get("quiz_total_questions", 0) + self.quiz_total
                    entry["quiz_correct_answers"] = entry.get("quiz_correct_answers", 0) + self.quiz_correct
                    break
            else:
                self.user_data["learning_history"].append({
                    "date": today,
                    "words": 0,
                    "new_words": 0,
                    "review_words": 0,
                    "quiz_correct_answers": self.quiz_correct,
                    "quiz_total_questions": self.quiz_total
                })

            # 保存用户数据
            try:
                user_file = f"{self.user_data['username']}.json"
                with open(user_file, "w", encoding="utf-8") as f:
                    json.dump(self.user_data, f, ensure_ascii=False, indent=4)
            except Exception as e:
                messagebox.showerror("错误", f"保存学习记录失败: {str(e)}")

            self.show_main_menu()

    def record_learning(self):
        today = datetime.now().strftime("%Y-%m-%d")
        # 查找今天是否已有记录
        for entry in self.user_data["learning_history"]:
            if entry["date"] == today:
                entry["words"] = entry.get("words", 0) + 1
                entry["review_words"] = entry.get("review_words", 0) + 1
                return

        # 如果没有，创建新记录（注意这里不包含正确率统计）
        self.user_data["learning_history"].append({
            "date": today,
            "words": 1,
            "new_words": 1,  # 简化处理，实际可区分新学/复习
            "review_words": 0,
            "quiz_correct_answers": 0,  # 初始化测验统计
            "quiz_total_questions": 0  # 初始化测验统计
        })

        # 保存用户数据
        try:
            user_file = f"{self.user_data['username']}.json"
            with open(user_file, "w", encoding="utf-8") as f:
                json.dump(self.user_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("错误", f"保存学习记录失败: {str(e)}")

    def show_main_menu(self):
        # 清空主框架
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # 创建顶部导航栏
        top_bar = tk.Frame(self.main_frame, bg=self.user_data["settings"]["theme_color"], height=40)
        top_bar.pack(fill=tk.X)

        # 用户名
        tk.Label(top_bar, text=f"用户: {self.user_data['username']}", font=(self.font_family, 12),
                 bg=self.user_data["settings"]["theme_color"], fg="white").pack(side=tk.LEFT, padx=10, pady=10)

        # 设置按钮
        tk.Button(top_bar, text="设置", font=(self.font_family, 10),
                  command=self.show_settings, bg=self.user_data["settings"]["theme_color"],
                  fg="white", bd=0).pack(side=tk.RIGHT, padx=10, pady=10)

        # 登出按钮
        tk.Button(top_bar, text="登出", font=(self.font_family, 10),
                  command=self.logout, bg=self.user_data["settings"]["theme_color"],
                  fg="white", bd=0).pack(side=tk.RIGHT, padx=10, pady=10)

        # 创建内容区域
        content_frame = tk.Frame(self.main_frame, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧面板 - 学习统计
        stats_frame = tk.LabelFrame(content_frame, text="学习统计", font=(self.font_family, 14), padx=10, pady=10)
        stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 学习目标
        goal_text = "高中" if self.user_data["learning_goal"] == "high_school" else \
            "四级" if self.user_data["learning_goal"] == "cet4" else "六级"
        tk.Label(stats_frame, text=f"学习目标: {goal_text}", font=(self.font_family, 12)).pack(anchor="w", pady=5)

        # 总单词数
        total_words = len(self.current_words)
        tk.Label(stats_frame, text=f"总单词数: {total_words}", font=(self.font_family, 12)).pack(anchor="w", pady=5)

        # 星标单词数
        starred_count = len(self.user_data["starred_words"])
        tk.Label(stats_frame, text=f"星标单词: {starred_count}", font=(self.font_family, 12)).pack(anchor="w", pady=5)

        # 本周学习统计
        tk.Label(stats_frame, text="本周学习:", font=(self.font_family, 12, "bold")).pack(anchor="w", pady=10)

        # 计算本周学习数据
        weekly_data = self.calculate_weekly_stats()

        for key, value in weekly_data.items():
            tk.Label(stats_frame, text=f"{key}: {value}", font=(self.font_family, 12)).pack(anchor="w", pady=3)

        # 右侧面板 - 功能按钮
        functions_frame = tk.Frame(content_frame)
        functions_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 开始学习按钮
        tk.Button(functions_frame, text="开始学习", font=(self.font_family, 16),
                  command=self.start_learning, height=2, width=20).pack(pady=20)

        # 查看星标单词
        tk.Button(functions_frame, text="星标单词", font=(self.font_family, 16),
                  command=self.show_starred_words, height=2, width=20).pack(pady=20)

        # 学习记录
        tk.Button(functions_frame, text="学习记录", font=(self.font_family, 16),
                  command=self.show_learning_history, height=2, width=20).pack(pady=20)

        # 新增：切换词库按钮
        tk.Button(functions_frame, text="切换词库", font=(self.font_family, 16),
                  command=self.show_switch_bank, height=2, width=20).pack(pady=20)

        # 新增：开始测验按钮
        tk.Button(functions_frame, text="开始测验", font=(self.font_family, 16),
                  command=self.start_quiz, height=2, width=20).pack(pady=20)

        # 底部按钮 - 退出程序
        tk.Button(self.main_frame, text="退出程序", font=(self.font_family, 14),
                  command=self.exit_program, bg="#e74c3c", fg="white").pack(side=tk.BOTTOM, pady=20)

    def show_settings(self):
        # 创建设置对话框
        settings_window = tk.Toplevel(self.root)
        settings_window.title("设置")
        settings_window.geometry("400x350")
        settings_window.resizable(False, False)

        # 设置标题
        tk.Label(settings_window, text="软件设置", font=(self.font_family, 18, "bold")).pack(pady=20)

        # 学习目标
        tk.Label(settings_window, text="学习目标:", font=(self.font_family, 12)).pack(anchor="w", padx=30, pady=5)
        learning_goal = tk.StringVar(value=self.user_data["learning_goal"])
        goal_frame = tk.Frame(settings_window)
        goal_frame.pack(pady=5)

        goals = [("高中", "high_school"), ("四级", "cet4"), ("六级", "cet6")]
        for i, (text, value) in enumerate(goals):
            tk.Radiobutton(goal_frame, text=text, variable=learning_goal, value=value,
                          font=(self.font_family, 12)).grid(row=0, column=i, padx=10)

        # 字体大小
        tk.Label(settings_window, text="字体大小:", font=(self.font_family, 12)).pack(anchor="w", padx=30, pady=5)
        font_size = tk.IntVar(value=self.user_data["settings"]["font_size"])
        font_size_scale = tk.Scale(settings_window, from_=10, to=20, orient=tk.HORIZONTAL,
                                  variable=font_size, length=300)
        font_size_scale.pack(pady=5)

        # 主题颜色
        tk.Label(settings_window, text="主题颜色:", font=(self.font_family, 12)).pack(anchor="w", padx=30, pady=5)
        theme_color = tk.StringVar(value=self.user_data["settings"]["theme_color"])

        color_frame = tk.Frame(settings_window)
        color_frame.pack(pady=5)

        colors = ["#4a7abc", "#2ecc71", "#e74c3c", "#f39c12", "#9b59b6"]
        for color in colors:
            tk.Radiobutton(color_frame, variable=theme_color, value=color,
                          bg=color, width=3, height=1).pack(side=tk.LEFT, padx=5)

        # 深色模式
        tk.Label(settings_window, text="深色模式:", font=(self.font_family, 12)).pack(anchor="w", padx=30, pady=5)
        dark_mode = tk.BooleanVar(value=self.user_data["settings"]["dark_mode"])
        tk.Checkbutton(settings_window, variable=dark_mode).pack(anchor="w", padx=50)

        # 保存设置按钮
        def save_settings():
            # 更新学习目标
            self.user_data["learning_goal"] = learning_goal.get()
            # 更新其他设置
            self.user_data["settings"]["font_size"] = font_size.get()
            self.user_data["settings"]["theme_color"] = theme_color.get()
            self.user_data["settings"]["dark_mode"] = dark_mode.get()

            # 重新加载单词库
            self.load_word_bank()

            # 保存用户数据
            try:
                user_file = f"{self.user_data['username']}.json"
                with open(user_file, "w", encoding="utf-8") as f:
                    json.dump(self.user_data, f, ensure_ascii=False, indent=4)

                messagebox.showinfo("成功", "设置已保存")
                settings_window.destroy()
                self.show_main_menu()  # 刷新主界面
            except Exception as e:
                messagebox.showerror("错误", f"保存设置失败: {str(e)}")

        tk.Button(settings_window, text="保存设置", font=(self.font_family, 12),
                  command=save_settings).pack(pady=20)

    def show_switch_bank(self):
        # 清空主框架
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # 创建顶部导航栏
        top_bar = tk.Frame(self.main_frame, bg=self.user_data["settings"]["theme_color"], height=40)
        top_bar.pack(fill=tk.X)

        # 返回按钮
        tk.Button(top_bar, text="返回", font=(self.font_family, 10),
                  command=self.show_main_menu, bg=self.user_data["settings"]["theme_color"],
                  fg="white", bd=0).pack(side=tk.LEFT, padx=10, pady=10)

        # 创建词库选择区域
        bank_frame = tk.Frame(self.main_frame, padx=20, pady=20)
        bank_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        tk.Label(bank_frame, text="选择词库", font=(self.font_family, 24, "bold")).pack(pady=40)

        # 当前词库显示
        current_goal = self.user_data["learning_goal"]
        current_text = "高中" if current_goal == "high_school" else \
                      "四级" if current_goal == "cet4" else "六级"
        tk.Label(bank_frame, text=f"当前词库: {current_text}", font=(self.font_family, 14)).pack(pady=20)

        # 词库选择
        goal_var = tk.StringVar(value=current_goal)

        # 高中词库
        high_school_frame = tk.Frame(bank_frame)
        high_school_frame.pack(fill=tk.X, pady=10)
        tk.Radiobutton(high_school_frame, text="高中词库", variable=goal_var, value="high_school",
                      font=(self.font_family, 14)).pack(side=tk.LEFT)
        tk.Label(high_school_frame, text=f"共 {len(self.word_banks.get('high_school', []))} 个单词",
                font=(self.font_family, 12)).pack(side=tk.LEFT, padx=20)

        # 四级词库
        cet4_frame = tk.Frame(bank_frame)
        cet4_frame.pack(fill=tk.X, pady=10)
        tk.Radiobutton(cet4_frame, text="四级词库", variable=goal_var, value="cet4",
                      font=(self.font_family, 14)).pack(side=tk.LEFT)
        tk.Label(cet4_frame, text=f"共 {len(self.word_banks.get('cet4', []))} 个单词",
                font=(self.font_family, 12)).pack(side=tk.LEFT, padx=20)

        # 六级词库
        cet6_frame = tk.Frame(bank_frame)
        cet6_frame.pack(fill=tk.X, pady=10)
        tk.Radiobutton(cet6_frame, text="六级词库", variable=goal_var, value="cet6",
                      font=(self.font_family, 14)).pack(side=tk.LEFT)
        tk.Label(cet6_frame, text=f"共 {len(self.word_banks.get('cet6', []))} 个单词",
                font=(self.font_family, 12)).pack(side=tk.LEFT, padx=20)

        # 确认按钮
        def confirm_switch():
            new_goal = goal_var.get()
            if new_goal != current_goal:
                self.user_data["learning_goal"] = new_goal
                self.load_word_bank()  # 重新加载词库

                # 保存用户数据
                try:
                    user_file = f"{self.user_data['username']}.json"
                    with open(user_file, "w", encoding="utf-8") as f:
                        json.dump(self.user_data, f, ensure_ascii=False, indent=4)

                    messagebox.showinfo("成功", f"已切换到 {current_text} 词库")
                except Exception as e:
                    messagebox.showerror("错误", f"切换词库失败: {str(e)}")

            self.show_main_menu()  # 返回主菜单

        tk.Button(bank_frame, text="确认切换", font=(self.font_family, 16),
                  command=confirm_switch, height=2, width=15).pack(pady=40)

    def start_learning(self):
        # 清空主框架
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # 创建顶部导航栏
        top_bar = tk.Frame(self.main_frame, bg=self.user_data["settings"]["theme_color"], height=40)
        top_bar.pack(fill=tk.X)

        # 返回按钮
        tk.Button(top_bar, text="返回", font=(self.font_family, 10),
                  command=self.show_main_menu, bg=self.user_data["settings"]["theme_color"],
                  fg="white", bd=0).pack(side=tk.LEFT, padx=10, pady=10)


        # 获取完整词库
        all_words = self.word_banks.get(self.user_data["learning_goal"], [])

        # 为每个单词设置权重（星标单词权重3，普通单词权重1）
        weighted_words = []
        for word_dict in all_words:
            weight = 3 if word_dict["word"] in self.user_data["starred_words"] else 1
            weighted_words.extend([word_dict] * weight)

        # 随机选择一个单词
        if not weighted_words:
            messagebox.showinfo("提示", "没有可用的单词")
            self.show_main_menu()
            return

        current_word = random.choice(weighted_words)

        # 创建单词学习区域
        word_frame = tk.Frame(self.main_frame, padx=20, pady=20)
        word_frame.pack(fill=tk.BOTH, expand=True)

        # 单词
        tk.Label(word_frame, text=current_word["word"], font=(self.font_family, 36, "bold")).pack(pady=40)

        # 隐藏的词义
        meaning_var = tk.StringVar(value="点击显示词义")
        tk.Label(word_frame, textvariable=meaning_var, font=(self.font_family, 24), fg="gray").pack(pady=20)

        # 显示词义按钮
        def show_meaning():
            meaning_var.set(current_word["meaning"])
            show_meaning_btn.pack_forget()
            next_word_btn.pack(pady=20)
            star_btn.pack(pady=10)

        show_meaning_btn = tk.Button(word_frame, text="显示词义", font=(self.font_family, 16),
                                    command=show_meaning)
        show_meaning_btn.pack(pady=20)

        # 例句
        tk.Label(word_frame, text=f"例句: {current_word['example']}", font=(self.font_family, 14),
                wraplength=500).pack(pady=20)

        # 星标按钮
        is_starred = current_word["word"] in self.user_data["starred_words"]
        star_var = tk.StringVar(value="★" if is_starred else "☆")

        def toggle_star():
            if star_var.get() == "☆":
                star_var.set("★")
                if current_word["word"] not in self.user_data["starred_words"]:
                    self.user_data["starred_words"].append(current_word["word"])
            else:
                star_var.set("☆")
                if current_word["word"] in self.user_data["starred_words"]:
                    self.user_data["starred_words"].remove(current_word["word"])

            # 保存用户数据
            try:
                user_file = f"{self.user_data['username']}.json"
                with open(user_file, "w", encoding="utf-8") as f:
                    json.dump(self.user_data, f, ensure_ascii=False, indent=4)
            except Exception as e:
                messagebox.showerror("错误", f"保存星标失败: {str(e)}")

        star_btn = tk.Button(word_frame, textvariable=star_var, font=(self.font_family, 20),
                            command=toggle_star, fg="orange")

        # 下一个单词按钮
        next_word_btn = tk.Button(word_frame, text="下一个", font=(self.font_family, 16),
                                command=self.start_learning)

        # 记录学习历史
        def record_learning():
            today = datetime.now().strftime("%Y-%m-%d")
            # 查找今天是否已有记录
            for entry in self.user_data["learning_history"]:
                if entry["date"] == today:
                    entry["words"] = entry.get("words", 0) + 1
                    entry["review_words"] = entry.get("review_words", 0) + 1
                    return

            # 如果没有，创建新记录
            self.user_data["learning_history"].append({
                "date": today,
                "words": 1,
                "new_words": 1,  # 简化处理，实际可区分新学/复习
                "review_words": 0,
                "correct_answers": 1,
                "total_questions": 1
            })

            # 保存用户数据
            try:
                user_file = f"{self.user_data['username']}.json"
                with open(user_file, "w", encoding="utf-8") as f:
                    json.dump(self.user_data, f, ensure_ascii=False, indent=4)
            except Exception as e:
                messagebox.showerror("错误", f"保存学习记录失败: {str(e)}")

        record_learning()

        # 显示按钮（初始只显示"显示词义"）
        show_meaning_btn.pack(pady=20)

    def show_starred_words(self):
        # 清空主框架
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # 创建顶部导航栏
        top_bar = tk.Frame(self.main_frame, bg=self.user_data["settings"]["theme_color"], height=40)
        top_bar.pack(fill=tk.X)

        # 返回按钮
        tk.Button(top_bar, text="返回", font=(self.font_family, 10),
                  command=self.show_main_menu, bg=self.user_data["settings"]["theme_color"],
                  fg="white", bd=0).pack(side=tk.LEFT, padx=10, pady=10)

        # 星标单词数量
        count = len(self.user_data["starred_words"])
        tk.Label(top_bar, text=f"星标单词: {count}", font=(self.font_family, 12),
                 bg=self.user_data["settings"]["theme_color"], fg="white").pack(side=tk.RIGHT, padx=10, pady=10)

        # 创建星标单词列表区域
        starred_frame = tk.Frame(self.main_frame, padx=20, pady=20)
        starred_frame.pack(fill=tk.BOTH, expand=True)

        # 创建列表框
        listbox = tk.Listbox(starred_frame, font=(self.font_family, 14), width=50, height=15)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 添加滚动条
        scrollbar = tk.Scrollbar(starred_frame, orient=tk.VERTICAL, command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)

        # 添加星标单词到列表
        for word in self.user_data["starred_words"]:
            # 查找单词详情
            word_data = next((item for item in self.current_words if item["word"] == word), None)
            if word_data:
                listbox.insert(tk.END, f"{word} - {word_data['meaning']}")

        # 如果没有星标单词
        if not self.user_data["starred_words"]:
            listbox.insert(tk.END, "暂无星标单词")

    def show_learning_history(self):
        # 清空主框架
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # 创建顶部导航栏
        top_bar = tk.Frame(self.main_frame, bg=self.user_data["settings"]["theme_color"], height=40)
        top_bar.pack(fill=tk.X)

        # 返回按钮
        tk.Button(top_bar, text="返回", font=(self.font_family, 10),
                  command=self.show_main_menu, bg=self.user_data["settings"]["theme_color"],
                  fg="white", bd=0).pack(side=tk.LEFT, padx=10, pady=10)

        # 创建学习记录区域
        history_frame = tk.Frame(self.main_frame, padx=20, pady=20)
        history_frame.pack(fill=tk.BOTH, expand=True)

        # 创建列表框
        listbox = tk.Listbox(history_frame, font=(self.font_family, 14), width=50, height=15)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 添加滚动条
        scrollbar = tk.Scrollbar(history_frame, orient=tk.VERTICAL, command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)

        # 添加学习记录到列表
        if not self.user_data["learning_history"]:
            listbox.insert(tk.END, "暂无学习记录")
        else:
            # 按日期排序（最新的在前）
            history_sorted = sorted(self.user_data["learning_history"], key=lambda x: x["date"], reverse=True)

            for entry in history_sorted:
                listbox.insert(tk.END, f"{entry['date']} - 学习了 {entry['words']} 个单词")

        # 学习汇总
        total_days = len(self.user_data["learning_history"])
        total_words = sum(entry["words"] for entry in self.user_data["learning_history"]) if total_days > 0 else 0

        summary_frame = tk.Frame(self.main_frame, padx=20, pady=10)
        summary_frame.pack(fill=tk.X)

        tk.Label(summary_frame, text=f"累计学习: {total_days} 天", font=(self.font_family, 14)).pack(side=tk.LEFT, padx=20)
        tk.Label(summary_frame, text=f"累计学习单词: {total_words} 个", font=(self.font_family, 14)).pack(side=tk.LEFT, padx=20)

    def logout(self):
        if messagebox.askyesno("确认", "确定要登出吗?"):
            self.user_data = {
                "username": "",
                "password": "",
                "learning_goal": "",
                "starred_words": [],
                "learning_history": [],
                "settings": {
                    "font_size": 12,
                    "theme_color": "#4a7abc",
                    "dark_mode": False
                }
            }
            self.show_login()

    def exit_program(self):
        if messagebox.askyesno("确认", "确定要退出程序吗?"):
            self.root.destroy()

    def start_quiz(self):
        # 清空主框架
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # 创建顶部导航栏
        top_bar = tk.Frame(self.main_frame, bg=self.user_data["settings"]["theme_color"], height=40)
        top_bar.pack(fill=tk.X)

        # 返回按钮
        tk.Button(top_bar, text="返回", font=(self.font_family, 10),
                  command=self.show_main_menu, bg=self.user_data["settings"]["theme_color"],
                  fg="white", bd=0).pack(side=tk.LEFT, padx=10, pady=10)

        # 当前测验进度
        self.quiz_progress = 0
        self.quiz_total = 10  # 测验题目数量
        self.quiz_correct = 0
        self.quiz_words = random.sample(self.current_words, min(self.quiz_total, len(self.current_words)))

        tk.Label(top_bar, text=f"测验进度: {self.quiz_progress}/{self.quiz_total}", font=(self.font_family, 12),
                 bg=self.user_data["settings"]["theme_color"], fg="white").pack(side=tk.RIGHT, padx=10, pady=10)

        # 创建测验区域
        quiz_frame = tk.Frame(self.main_frame, padx=20, pady=20)
        quiz_frame.pack(fill=tk.BOTH, expand=True)

        # 显示第一个单词的释义
        self.current_quiz_word = self.quiz_words[self.quiz_progress]
        tk.Label(quiz_frame, text=f"释义: {self.current_quiz_word['meaning']}", font=(self.font_family, 24)).pack(pady=40)

        # 用户输入框
        self.quiz_entry = tk.Entry(quiz_frame, font=(self.font_family, 16), width=20)
        self.quiz_entry.pack(pady=20)

        # 提交按钮
        submit_btn = tk.Button(quiz_frame, text="提交", font=(self.font_family, 16),
                               command=self.check_answer)
        submit_btn.pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyApp(root)
    root.mainloop()
