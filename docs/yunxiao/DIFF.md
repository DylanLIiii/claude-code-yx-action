# GetCompare - 查询代码比较内容_云效(Alibaba Cloud DevOps)-阿里云帮助中心
**说明**

可获取 branch、commit 或者 tag 之间的比较内容。from 和 to 的顺序应遵循 Git 命令行执行的顺序，这与 UI 页面的顺序相反。此外，在进行比较时，需确保比较的类型一致，例如 branch 与 branch 之间的比较，以及 commit 与 commit 之间的比较。

**请求语法**
--------

```
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/compares
```


**请求头**
-------


|参数             |类型    |是否必填|描述     |示例值                         |
|---------------|------|----|-------|----------------------------|
|x-yunxiao-token|string|是   |个人访问令牌。|pt-0fh3****0fbG_35af****0484|


**请求参数**
--------



* 参数: organizationId
  * 类型: string
  * 位置: path
  * 是否必填: 是
  * 描述: 组织 ID。
  * 示例值: 5ebbc0228123212b59xxxxx
* 参数: repositoryId
  * 类型: string
  * 位置: path
  * 是否必填: 是
  * 描述: 代码库 ID 或者 URL-Encoder 编码的全路径。
  * 示例值: 2369234
* 参数: from
  * 类型: string
  * 位置: query
  * 是否必填: 是
  * 描述: 可为 CommitSHA、分支名或者标签名。
  * 示例值: c9fb781f3d66ef6ee60bdd5c414f5106454b1426
* 参数: to
  * 类型: string
  * 位置: query
  * 是否必填: 是
  * 描述: 可为 CommitSHA、分支名或者标签名。
  * 示例值: b8f6f28520b1936aafe2e638373e19ccafa42b02
* 参数: sourceType
  * 类型: string
  * 位置: query
  * 是否必填: 否
  * 描述: 可选值：branch、tag；若是 commit 比较，可不传；若是分支比较，则需传入：branch，亦可不传，但需要确保不存在分支或 tag 重名的情况；若是 tag 比较，则需传入：tag；若是存在分支和标签同名的情况，则需要严格传入 branch 或者 tag。
  * 示例值: branch
* 参数: targetType
  * 类型: string
  * 位置: query
  * 是否必填: 否
  * 描述: 可选值：branch、tag；若是 commit 比较，可不传；若是分支比较，则需传入：branch，亦可不传，但需要确保不存在分支或 Tag 重名的情况；若是 tag 比较，则需传入：tag；若是存在分支和标签同名的情况，则需要严格传入 branch 或者 tag。
  * 示例值: branch
* 参数: straight
  * 类型: string
  * 位置: query
  * 是否必填: 否
  * 描述: 是否使用 Merge-Base：straight=false，表示使用 Merge-Base；straight=true，表示不使用 Merge-Base；默认为 false，即使用 Merge-Base。
  * 示例值: false


**请求示例**
--------

```
curl -X 'GET' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/compares?from=<from>&to=<to>&sourceType=<sourceType>&targetType=<targetType>&straight=<straight>' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```


**返回参数**
--------



* 参数: -
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数: commits
  * 类型: array
  * 描述: 差异提交列表。
  * 示例值: 
* 参数: -
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数: authorEmail
  * 类型: string
  * 描述: 作者邮箱。
  * 示例值: username@example.com
* 参数: authorName
  * 类型: string
  * 描述: 作者姓名。
  * 示例值: codeup-name
* 参数: authoredDate
  * 类型: string
  * 描述: 作者提交时间。
  * 示例值: 2024-10-05T15:30:45Z
* 参数: committedDate
  * 类型: string
  * 描述: 提交者提交时间。
  * 示例值: 2024-10-05T15:30:45Z
* 参数: committerEmail
  * 类型: string
  * 描述: 提交者邮箱。
  * 示例值: username@example.com
* 参数: committerName
  * 类型: string
  * 描述: 提交者姓名。
  * 示例值: codeup-name
* 参数: id
  * 类型: string
  * 描述: 提交 ID。
  * 示例值: 6da8c14b5a9102998148b7ea35f96507d5304f74
* 参数: message
  * 类型: string
  * 描述: 提交内容。
  * 示例值: commit message detail
* 参数: parentIds
  * 类型: array[string]
  * 描述: 父提交 ID。
  * 示例值: [“3fdaf119cf76539c1a47de0074ac02927ef4c8e1”]
* 参数: shortId
  * 类型: string
  * 描述: 提交短 ID。
  * 示例值: 6da8c14b
* 参数: stats
  * 类型: object
  * 描述: 变更行数。
  * 示例值: 
* 参数: additions
  * 类型: integer
  * 描述: 增加行数。
  * 示例值: 1
* 参数: deletions
  * 类型: integer
  * 描述: 删除行数。
  * 示例值: 1
* 参数: total
  * 类型: integer
  * 描述: 总变动行数。
  * 示例值: 2
* 参数: title
  * 类型: string
  * 描述: 标题，提交的第一行内容。
  * 示例值: commit msg title
* 参数: webUrl
  * 类型: string
  * 描述: 页面访问地址。
  * 示例值: http://exmaple.com/example_repo/commit/commit_sha
* 参数: diffs
  * 类型: array
  * 描述: 差异内容。
  * 示例值: 
* 参数: -
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数: aMode
  * 类型: string
  * 描述: 旧文件的模式标识，包含文件类型、权限等信息。
  * 示例值: 0
* 参数: bMode
  * 类型: string
  * 描述: 新文件的模式标识，包含文件类型、权限等信息。
  * 示例值: 100644
* 参数: deletedFile
  * 类型: boolean
  * 描述: 是否是删除文件。
  * 示例值: false
* 参数: diff
  * 类型: string
  * 描述: 比较内容。
  * 示例值: — /dev/null\n+++ b/asda\n@@ -0,0 +1 @@\n+asdasd\n\ No newline at end of file\n
* 参数: isBinary
  * 类型: boolean
  * 描述: 是否是二进制文件。
  * 示例值: false
* 参数: newFile
  * 类型: boolean
  * 描述: 是否是新增文件。
  * 示例值: true
* 参数: newId
  * 类型: string
  * 描述: 新文件的 git object id。
  * 示例值: 911***********660d7b
* 参数: newPath
  * 类型: string
  * 描述: 新文件路径。
  * 示例值: src/test/main.java
* 参数: oldId
  * 类型: string
  * 描述: 旧文件的 git object id。
  * 示例值: 8a9***********fdd82a2c1
* 参数: oldPath
  * 类型: string
  * 描述: 旧文件路径。
  * 示例值: src/test/main.java
* 参数: renamedFile
  * 类型: boolean
  * 描述: 是否是重命名文件。
  * 示例值: false


**返回示例**
--------

```
{
    "commits": [
        {
            "authorEmail": "username@example.com",
            "authorName": "云效Codeup",
            "authoredDate": "2023-01-03T15:41:26+08:00",
            "committedDate": "2023-01-03T15:41:26+08:00",
            "committerEmail": "username@example.com",
            "committerName": "云效CodeupCommitter",
            "id": "b8f6f28520b1936aafe2e638373e19ccafa42b02",
            "message": "",
            "parentIds": [
                "b8f6f"
            ],
            "shortId": "b8f6f285",
            "stats": {
                "additions": 0,
                "deletions": 0,
                "total": 0
            },
            "title": "提交标题",
            "webUrl": ""
        }
    ],
    "diffs": [
        {
            "aMode": "0",
            "bMode": "100644",
            "deletedFile": false,
            "diff": "--- /dev/null\n+++ b/asda\n@@ -0,0 +1 @@\n+asdasd\n\\ No newline at end of file\n",
            "isBinary": false,
            "newFile": true,
            "newId": "9118d6c90d********4a50ff660d7b",
            "newPath": "new_test.txt",
            "oldId": "8a9***********fdd82a2c1",
            "oldPath": "test.txt",
            "renamedFile": false
        }
    ]
}
```