GitHub Actions 中确实存在与 Jenkins Build Number 类似的概念，但默认行为可能导致不同分支的 Run Number 重复。以下是详细解释和解决方案：

---

### 1. GitHub Actions 的默认计数器
- **`GITHUB_RUN_NUMBER`**  
  这是仓库级别的全局递增计数器，**所有分支共享同一个序列**（但实测发现不同分支可能独立计数，这取决于 Workflow 文件的触发方式）。  
  若你的 Workflow 文件存在于多个分支且被分别触发，不同分支的 Run Number 可能会独立递增，导致重复。

- **`GITHUB_RUN_ID`**  
  每个 Workflow Run 的全局唯一 ID（如 `1658821493`），全平台唯一且递增，适合用作绝对唯一标识。

---

### 2. 为何不同分支的 Run Number 可能重复？
- 如果 Workflow 文件在**不同分支中存在不同版本**（如通过 `push` 或 `pull_request` 触发），GitHub 会为每个分支维护独立的 `GITHUB_RUN_NUMBER` 计数，导致重复。

---

### 3. 解决方案：生成唯一且一致的 Build Identifier

#### 方案一：使用 `GITHUB_RUN_ID`
```yaml
steps:
  - name: Get Unique ID
    run: echo "Unique Build ID: ${{ github.run_id }}"
```
- **优点**：绝对唯一，全平台递增。
- **缺点**：数字较长，不易人类阅读。

#### 方案二：组合分支名和 Run Number
```yaml
env:
  BUILD_ID: ${{ github.ref_name }}-${{ github.run_number }}
```
- 示例：`main-15` 或 `feature/login-3`
- **优点**：直观区分分支和构建次数。

#### 方案三：手动生成递增版本号（推荐）
通过调用 GitHub API 获取历史 Run 总数并手动递增：
```yaml
- name: Calculate Build Number
  id: buildnum
  run: |
    TOTAL_RUNS=$(curl -s -H "Authorization: Bearer ${{ secrets.GITHUB_TOKEN }}" \
      "https://api.github.com/repos/${{ github.repository }}/actions/runs?branch=${{ github.ref_name }}" \
      | jq '[.workflow_runs[] | select(.name == "${{ github.workflow }}")] | length')
    echo "build_number=$(($TOTAL_RUNS + 1))" >> $GITHUB_OUTPUT
```
- **优点**：完全自定义，跨分支统一递增。
- **限制**：需处理 API 分页，建议使用更精确的查询参数。

#### 方案四：利用 Git 标签或 Commit SHA
```yaml
env:
  BUILD_TAG: ${{ github.ref_name }}-${{ github.run_number }}-${{ github.sha }}
```
- 示例：`main-15-a1b2c3d`
- **优点**：包含提交信息，便于追溯。

---

### 4. 最佳实践
- **跨分支统一版本号**：推荐使用 **`GITHUB_RUN_ID`** 或 **手动生成递增 ID**。
- **产物版本化**：结合 `git tag` 和 Actions 自动打标签（如 SemVer）。
- **日志可读性**：在日志中同时输出 `GITHUB_RUN_NUMBER` 和分支名称。

---

通过上述方法，你可以有效避免不同分支的 Build Number 冲突，同时保留与 Jenkins 类似的递增标识功能。根据实际需求选择最适合的方案即可。

GitHub Actions 确实有 run_number，但它是针对整个 repository 的，而不是针对特定的 branch。因此，不同分支的 build job 可能会有相同的 run_number，因为它是基于整个 workflow 运行次数的。

如果你想要一个类似 Jenkins BUILD_NUMBER 的编号，可以考虑以下几种方法：

方法 1: 使用 run_id

run_id 是唯一的，但它是一个较长的数字。例如：

echo "Run ID: ${{ github.run_id }}"

这个值在整个 repository 中是唯一的，但它可能不是连续的。

⸻

方法 2: 使用 GITHUB_RUN_NUMBER 并结合分支名

如果你想要在不同分支上维护不同的 build 计数，可以使用 run_number + branch_name 组合：

echo "Build Number: ${{ github.run_number }}-${{ github.ref_name }}"

这可以确保在不同分支上不会有重复的编号。

⸻

方法 3: 使用 Repository Dispatch + 生成自定义 Build Number

如果你希望每个分支都有独立的 build 计数，可以使用 repository_dispatch 触发 workflow，并在某个存储（比如 GitHub Artifacts 或外部数据库）中维护一个计数。

或者你可以使用 GitHub Actions 的 create-or-update-artifact 来存储并递增一个 build number。

示例：

- name: Read Build Number
  run: |
    BUILD_NUM=$(cat build_number.txt || echo 0)
    BUILD_NUM=$((BUILD_NUM + 1))
    echo "BUILD_NUMBER=$BUILD_NUM" >> $GITHUB_ENV
- name: Save Build Number
  run: echo "$BUILD_NUMBER" > build_number.txt
- name: Upload Build Number
  uses: actions/upload-artifact@v3
  with:
    name: build_number
    path: build_number.txt

这种方法确保了每个分支的 build number 是独立递增的。

⸻

方法 4: 使用 Git Tags 作为 Build Number

你也可以使用 Git tags 来管理 build number。例如，每次构建成功后，创建一个新的 tag：

- name: Generate Build Number from Tags
  run: |
    BUILD_NUM=$(git tag --list 'build-*' | wc -l)
    BUILD_NUM=$((BUILD_NUM + 1))
    echo "BUILD_NUMBER=$BUILD_NUM" >> $GITHUB_ENV
- name: Create New Build Tag
  run: |
    git tag "build-${{ env.BUILD_NUMBER }}"
    git push origin "build-${{ env.BUILD_NUMBER }}"

这种方式可以确保 build number 持续递增，但需要 GitHub Actions 有 push 权限。

⸻

总结
	•	如果要保证唯一性，可以使用 run_id。
	•	如果希望不同分支编号不同，可以使用 run_number + branch_name 组合。
	•	如果希望独立递增，可以用 artifact 存储 build number 或者用 Git tags。

你想要哪种方式？