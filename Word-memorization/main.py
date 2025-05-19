import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import random
from datetime import datetime


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
        self.word_banks = {
            "high_school": [
                {"word": "abandon", "meaning": "放弃，抛弃", "example": "She had to abandon her dream."},
                {"word": "absorb", "meaning": "吸收，理解", "example": "Plants absorb sunlight."},
                # 更多单词...
            ],
            "cet4": [
                {"word": "adequate", "meaning": "足够的，适当的", "example": "We have adequate resources."},
                {"word": "ambiguous", "meaning": "模棱两可的", "example": "His answer was ambiguous."},
                # 更多单词...
            ],
            "cet6": [
                {"word": "aberration", "meaning": "偏差，脱离常轨", "example": "This behavior is an aberration."},
                {"word": "abjure", "meaning": "发誓放弃，宣誓弃绝", "example": "He abjured his old beliefs."},
                # 更多单词...
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
        tk.Label(register_frame, text="确认密码:", font=(self.font_family, 12)).grid(row=3, column=0, sticky="w",
                                                                                     pady=10)
        self.register_confirm_password = tk.Entry(register_frame, font=(self.font_family, 12), width=20, show="*")
        self.register_confirm_password.grid(row=3, column=1, pady=10)

        # 学习目标
        tk.Label(register_frame, text="学习目标:", font=(self.font_family, 12)).grid(row=4, column=0, sticky="w",
                                                                                     pady=10)
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

        # 模拟学习数据
        weekly_data = {
            "学习天数": 5,
            "新学单词": 30,
            "复习单词": 50,
            "平均正确率": "85%"
        }

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

        # 底部按钮 - 退出程序
        tk.Button(self.main_frame, text="退出程序", font=(self.font_family, 14),
                  command=self.exit_program, bg="#e74c3c", fg="white").pack(side=tk.BOTTOM, pady=20)

    def show_settings(self):
        # 创建设置对话框
        settings_window = tk.Toplevel(self.root)
        settings_window.title("设置")
        settings_window.geometry("400x300")
        settings_window.resizable(False, False)

        # 设置标题
        tk.Label(settings_window, text="软件设置", font=(self.font_family, 18, "bold")).pack(pady=20)

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
            self.user_data["settings"]["font_size"] = font_size.get()
            self.user_data["settings"]["theme_color"] = theme_color.get()
            self.user_data["settings"]["dark_mode"] = dark_mode.get()

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

        # 当前学习进度
        tk.Label(top_bar, text="学习进度: 1/20", font=(self.font_family, 12),
                 bg=self.user_data["settings"]["theme_color"], fg="white").pack(side=tk.RIGHT, padx=10, pady=10)

        # 随机选择一个单词
        if not self.current_words:
            messagebox.showinfo("提示", "没有可用的单词")
            self.show_main_menu()
            return

        current_word = random.choice(self.current_words)

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
                self.user_data["starred_words"].append(current_word["word"])
            else:
                star_var.set("☆")
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
                    entry["words"] += 1
                    return

            # 如果没有，创建新记录
            self.user_data["learning_history"].append({
                "date": today,
                "words": 1
            })

            # 保存用户数据
            try:
                user_file = f"{self.user_data['username']}.json"
                with open(user_file, "w", encoding="utf-8") as f:
                    json.dump(self.user_data, f, ensure_ascii=False, indent=4)
            except Exception as e:
                messagebox.showerror("错误", f"保存学习记录失败: {str(e)}")

        record_learning()

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

        tk.Label(summary_frame, text=f"累计学习: {total_days} 天", font=(self.font_family, 14)).pack(side=tk.LEFT,
                                                                                                     padx=20)
        tk.Label(summary_frame, text=f"累计学习单词: {total_words} 个", font=(self.font_family, 14)).pack(side=tk.LEFT,
                                                                                                          padx=20)

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


if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyApp(root)
    root.mainloop()