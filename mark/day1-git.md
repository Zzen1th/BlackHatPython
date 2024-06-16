# git 使用中遇到的问题
## 问题：因为第一次推送 github 时，将分支名写为 master 导致代码无法切换到主分支 main 上
### 报错内容
To https://github.com/Zzen1th/BlackHatPython.git
! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/Zzen1th/BlackHatPython.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. If you want to integrate the remote changes,
hint: use 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.

### 解决：
https://blog.csdn.net/m0_52316372/article/details/127446080

## 问题：删除分支
### 解决
// 删除本地分支
git branch -d localBranchName

// 删除远程分支
git push origin --delete remoteBranchName

 ## 问题：git远程管理
 ### 更新
 git pull https://github.com/xxx/xxx.git

 ### 推送
 git push origin main