# 团队 GitHub 协作演练仓库

欢迎！这个仓库是给团队练手的沙盒，用来练习 GitHub 最核心的协作流程：

> **创建 Issue → 建分支 → 提交 → 推送 → 开 PR → 审阅 → 合并到 main**

> ⚠️ `main` 分支已开启保护，**不能直接推送**，所有改动必须走 PR（Pull Request）。这正是真实项目的做法，请放心按下面的流程练。

---

## 演练任务：添加你的自我介绍

每个成员完整走一遍下面的 10 步：

### 第 1 步 · 创建 Issue
点顶部 **Issues** → **New issue** → 选「**自我介绍**」模板 → 把标题改成「添加我的自我介绍：你的名字」→ **Submit new issue**。

### 第 2 步 · 认领任务
打开刚创建的 Issue，点右侧 **Assignees**（指派）→ 选你自己。

### 第 3 步 · 建分支
点 **Code** → 点分支下拉框 → 输入 `feature/你的名字`（如 `feature/zhangsan`）→ **Create branch**。

### 第 4 步 · 改文件
进入 `members/` 文件夹 → **Add file** → **Create new file** → 文件名写 `你的名字.md`（如 `zhangsan.md`），内容写一句自我介绍。

### 第 5 步 · 提交
拉到页面底部 **Commit changes**，写一句说明（如「添加我的自我介绍」），**确认分支选中你的 `feature/` 分支**，点 **Commit changes**。

### 第 6 步 · 推送
在网页上操作时，你的分支已经自动上传到 GitHub（这一步在网页端是自动完成的，等于「推送 push」）。

### 第 7 步 · 开 PR
点 **Pull requests** → **New pull request** → base 选 `main`，compare 选你的 `feature/` 分支 → 标题说明要做什么，描述里写 `Closes #1`（把 `#1` 换成你第 1 步的 Issue 编号）→ **Create pull request**。

### 第 8 步 · 审阅（队友完成）
请**另一位成员**打开你的 PR → 点 **Files changed** → **Review changes** → 选 **Approve** → **Submit review**。

### 第 9 步 · 合并到 main
回到 PR 页面 → **Merge pull request** → **Confirm merge**，改动合入 main。

### 第 10 步 · 收尾
点 **Delete branch** 删除已合并的分支；你的 Issue 会自动关闭 ✅

---

## 术语对照表

| 术语 | 大白话 |
|------|--------|
| 仓库 repository | 一个项目的「文件夹 + 全部历史记录」 |
| 分支 branch | 主干的分叉，各自改各自的，互不干扰 |
| 提交 commit | 一次「保存」，带一句说明 |
| 推送 push | 把本地改动上传到 GitHub |
| Issue | 任务/问题单，用来记录要做的事 |
| PR（Pull Request） | 「合并申请单」，请求把你的分支合进 main |
| 审阅 review | 队友检查你的改动，确认没问题 |
| 合并 merge | 批准后合入，分支的改动正式进入 main |
