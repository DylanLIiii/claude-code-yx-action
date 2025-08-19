# GetChangeRequest - 查询合并请求_云效(Alibaba Cloud DevOps)-阿里云帮助中心

请求语法
----

```
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}
```


请求头
---


|参数             |类型    |是否���填|描述     |示例值                         |
|---------------|------|------|-------|----------------------------|
|x-yunxiao-token|string|是     |个人访问令牌。|pt-0fh3****0fbG_35af****0484|


请求参数
----


|参数            |类型     |位置  |是否必填|描述                           |示例值                                  |
|--------------|-------|----|----|-----------------------------|-------------------------------------|
|organizationId|string |path|是   |组织 ID。                       |99d1****71d4                         |
|repositoryId  |string |path|是   |代码库 ID 或者 URL-Encoder 编码的全路径。|2835387 或 codeup-org-id%2Fcodeup-demo|
|localId       |integer|path|是   |局部 ID，表示代码库中第几个合并请求。         |1                                    |


**请求示例**
--------

```
curl -X 'GET' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```


返回参数
----



* 参数: -
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数:  ahead
  * 类型: integer
  * 描述: 源分支领先目标分支的 commit 数量。
  * 示例值: 1
* 参数:  allRequirementsPass
  * 类型: boolean
  * 描述: 是否所有卡点项通过。
  * 示例值: true
* 参数:  author
  * 类型: object
  * 描述: 用户信息。
  * 示例值: 
* 参数:  avatar
  * 类型: string
  * 描述: 用户头像地址。
  * 示例值: https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100
* 参数:  email
  * 类型: string
  * 描述: 用户邮箱。
  * 示例值: username@example.com
* 参数:  name
  * 类型: string
  * 描述: 用户名称。
  * 示例值: test-codeup
* 参数:  state
  * 类型: string
  * 描述: 用户状态：active - 激活可用；blocked - 阻��暂不可用。
  * 示例值: active
* 参数:  userId
  * 类型: string
  * 描述: 云效用户 ID。
  * 示例值: 62c795c9cf*****b468af8
* 参数:  username
  * 类型: string
  * 描述: 用户登录名。
  * 示例值: root-test-codeup
* 参数:  behind
  * 类型: integer
  * 描述: 目标分支领先源分支的 commit 数量。
  * 示例值: 1
* 参数:  canRevertOrCherryPick
  * 类型: boolean
  * 描述: 是否能 Revert 或者 CherryPick。
  * 示例值: false
* 参数:  conflictCheckStatus
  * 类型: string
  * 描述: 冲突检测状态：CHECKING - 检测中；HAS_CONFLICT - 有冲突；NO_CONFLICT - 无冲突；FAILED - 检测失败。
  * 示例值: NO_CONFLICT
* 参数:  createFrom
  * 类型: string
  * 描述: 创建来源：WEB - 页面创建；COMMAND_LINE - 命令行创建。
  * 示例值: WEB
* 参数:  createTime
  * 类型: string
  * 描述: 创建时间。
  * 示例值: 2023-05-30T02:53:36Z
* 参数:  description
  * 类型: string
  * 描述: 描述。
  * 示例值: 描述信息的具体内容
* 参数:  detailUrl
  * 类型: string
  * 描述: 合并请求详情地址。
  * 示例值: xxx
* 参数:  hasReverted
  * 类型: boolean
  * 描述: 是否 Revert 过。
  * 示例值: false
* 参数:  localId
  * 类型: integer
  * 描述: 局部 ID。
  * 示例值: 1
* 参数:  mergedRevision
  * 类型: string
  * 描述: 合并版本（提交 ID），仅已合并状态才有值。
  * 示例值: 1a072f5367c21f9de3464b8c0ee8546e47764d2d
* 参数:  mrType
  * 类型: string
  * 描述: 合并请求类型：CODE_REVIEW - 代码评审；REF_REVIEW - 分支标签评审。
  * 示例值: CODE_REVIEW
* 参数:  projectId
  * 类型: integer
  * 描述: 代码库 ID。
  * 示例值: 2369234
* 参数:  reviewers
  * 类型: array
  * 描述: 评审人列表。
  * 示例值: 
* 参数:  -
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数:  avatar
  * 类型: string
  * 描述: 用户头像地址。
  * 示例值: https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100
* 参数:  email
  * 类型: string
  * 描述: 用户邮箱。
  * 示例值: username@example.com
* 参数:  hasCommented
  * 类型: boolean
  * 描述: 是否已经评论过。
  * 示例值: true
* 参数:  hasReviewed
  * 类型: boolean
  * 描述: 是否评审过。
  * 示例值: false
* 参数:  name
  * 类型: string
  * 描述: 用户名称。
  * 示例值: test-codeup
* 参数:  reviewOpinionStatus
  * 类型: string
  * 描述: 评审意见：PASS - 通过；NOT_PASS - 不通过。
  * 示例值: NOT_PASS
* 参数:  reviewTime
  * 类型: string
  * 描述: 评审时间。
  * 示例值: 2023-05-30T02:53:36Z
* 参数:  state
  * 类型: string
  * 描述: 用户状态：active - 激活可用；blocked - 阻塞暂不可用。
  * 示例值: active
* 参数:  userId
  * 类型: string
  * 描述: 云效用户 ID。
  * 示例值: 62c795c9cf*****b468af8
* 参数:  username
  * 类型: string
  * 描述: 用户登录名。
  * 示例值: root-test-codeup
* 参数:  sourceBranch
  * 类型: string
  * 描述: 源分支。
  * 示例值: test-merge-request
* 参数:  sourceCommitId
  * 类型: string
  * 描述: 源提交 ID，当 createFrom=COMMAND_LINE 时，有值。
  * 示例值: 
* 参数:  sourceProjectId
  * 类型: integer
  * 描述: 源库 ID。
  * 示例值: 2369234
* 参数:  sourceRef
  * 类型: string
  * 描述: 源提交引用，当 createFrom=COMMAND_LINE 时，有值。
  * 示例值: 
* 参数:  status
  * 类型: string
  * 描述: 合并请求状态：UNDER_DEV - 开发中；UNDER_REVIEW - 评审中；TO_BE_MERGED - 待合并；CLOSED - 已关闭；MERGED - 已合并。
  * 示例值: UNDER_REVIEW
* 参数:  subscribers
  * 类型: array
  * 描述: 订阅人列表。
  * 示例值: 
* 参数:  -
  * 类型: object
  * 描述: 用户信息。
  * 示例值: 
* 参数:  avatar
  * 类型: string
  * 描述: 用户头像地址。
  * 示例值: https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100
* 参数:  email
  * 类型: string
  * 描述: 用户邮箱。
  * 示例值: username@example.com
* 参数:  name
  * 类型: string
  * 描述: 用户名称。
  * 示例值: test-codeup
* 参数:  state
  * 类型: string
  * 描述: 用户状态：active - 激活可用；blocked - 阻塞暂不可用。
  * 示例值: active
* 参数:  userId
  * 类型: string
  * 描述: 云效用户 ID。
  * 示例值: 62c795c9cf*****b468af8
* 参数:  username
  * 类型: string
  * 描述: 用户登录名。
  * 示例值: root-test-codeup
* 参数:  supportMergeFastForwardOnly
  * 类型: boolean
  * 描述: 是否支持 fast-forward-only。
  * 示例值: true
* 参数:  targetBranch
  * 类型: string
  * 描述: 目标分支。
  * 示例值: master
* 参数:  targetProjectId
  * 类型: integer
  * 描述: 目标库 ID。
  * 示例值: 2369234
* 参数:  targetProjectNameWithNamespace
  * 类型: string
  * 描述: 目标库名称（含完整父路径）。
  * 示例值: orgId / test-group / test-target-repo（斜杠两侧有空格）
* 参数:  targetProjectPathWithNamespace
  * 类型: string
  * 描述: 目标库路径（含完整父路径）。
  * 示例值: orgId/test-group/test-target-repo
* 参数:  title
  * 类型: string
  * 描述: 标题。
  * 示例值: test-合并请求标题
* 参数:  totalCommentCount
  * 类型: integer
  * 描述: 总评论数。
  * 示例值: 2
* 参数:  unResolvedCommentCount
  * 类型: integer
  * 描述: 未解决评论数。
  * 示例值: 1
* 参数:  updateTime
  * 类型: string
  * 描述: 更新时间。
  * 示例值: 2023-05-30T02:53:36Z
* 参数:  webUrl
  * 类型: string
  * 描述: 页面地址。
  * 示例值: xxx


返回示例
----

```
{
    "ahead": 0,
    "allRequirementsPass": false,
    "author": {
        "avatar": "https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100",
        "email": "username@example.com",
        "name": "test-codeup",
        "state": "active",
        "userId": "62c795c9cf*****b468af8",
        "username": "root-test-codeup"
    },
    "behind": 0,
    "canRevertOrCherryPick": false,
    "conflictCheckStatus": "NO_CONFLICT",
    "createFrom": "WEB",
    "createTime": "2023-05-30T02:53:36Z",
    "description": "描述信息的具体内容",
    "detailUrl": "xxx",
    "hasReverted": false,
    "localId": 0,
    "mergedRevision": "1a072f5367c21f9de3464b8c0ee8546e47764d2d",
    "mrType": "CODE_REVIEW",
    "projectId": 0,
    "reviewers": [
        {
            "avatar": "https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100",
            "email": "username@example.com",
            "hasCommented": false,
            "hasReviewed": false,
            "name": "test-codeup",
            "reviewOpinionStatus": "NOT_PASS",
            "reviewTime": "2023-05-30T02:53:36Z",
            "state": "active",
            "userId": "62c795c9cf*****b468af8",
            "username": "root-test-codeup"
        }
    ],
    "sourceBranch": "test-merge-request",
    "sourceCommitId": "",
    "sourceProjectId": 0,
    "sourceRef": "",
    "status": "UNDER_REVIEW",
    "subscribers": [
        {
            "avatar": "https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100",
            "email": "username@example.com",
            "name": "test-codeup",
            "state": "active",
            "userId": "62c795c9cf*****b468af8",
            "username": "root-test-codeup"
        }
    ],
    "supportMergeFastForwardOnly": false,
    "targetBranch": "master",
    "targetProjectId": 0,
    "targetProjectNameWithNamespace": "orgId / test-group / test-target-repo（斜杠两侧有空格）",
    "targetProjectPathWithNamespace": "orgId/test-group/test-target-repo",
    "title": "test-合并请求标题",
    "totalCommentCount": 2,
    "unResolvedCommentCount": 1,
    "updateTime": "2023-05-30T02:53:36Z",
    "webUrl": "\"\""
}
```


# GetChangeRequestTree - 查询合并请求的变更文件树_云效(Alibaba Cloud DevOps)-阿里云帮助中心

    

请求语法
----

```
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}/diffs/changeTree
```


请求头
---


|参数             |类型    |是否必填|描述     |示例值                         |
|---------------|------|----|-------|----------------------------|
|x-yunxiao-token|string|是   |个人访问令牌。|pt-0fh3****0fbG_35af****0484|


请求参数
----



* 参数: organizationId
  * 类型: string
  * 位置: path
  * 是否必填: 是
  * 描述: 组织 ID。
  * 示例值: 6270e731cfea268afc21ccac
* 参数: repositoryId
  * 类型: string
  * 位置: path
  * 是否必填: 是
  * 描述: 代码库 ID 或者 URL-Encoder 编码的全路径。
  * 示例值: 2835387 或 codeup-org-id%2Fcodeup-demo
* 参数: localId
  * 类型: integer
  * 位置: path
  * 是否必填: 是
  * 描述: 局部 ID。
  * 示例值: 1
* 参数: fromPatchSetId
  * 类型: string
  * 位置: query
  * 是否必填: 是
  * 描述: 合并目标对应的版本唯一 ID（from 和 to，是 Git 的对比顺序，与通常的源分支和目标分支的顺序相反）。
  * 示例值: 5e733xxxxxxxxb04a6aa0e23d4ff72b8
* 参数: toPatchSetId
  * 类型: string
  * 位置: query
  * 是否必填: 是
  * 描述: 合并源对应的版本唯一 ID（from 和 to，是 Git 的对比顺序，与通常的源分支和目标分支的顺序相反）。
  * 示例值: 513fcxxxxxxxx2d2bb0db4f72c0aa15b


**请求示例**
--------

```
curl -X 'GET' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}/diffs/changeTree?fromPatchSetId=<fromPatchSetId>&toPatchSetId=<toPatchSetId>' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```


返回参数
----


|参数               |类型     |描述                 |示例值     |
|-----------------|-------|-------------------|--------|
|-                |object |                   |        |
| changedTreeItems|array  |变更文件列表。            |        |
| -               |object |                   |        |
| addLines        |integer|新增行数。              |10      |
| delLines        |integer|删除行数。              |0       |
| deletedFile     |boolean|是否是删除文件。           |false   |
| isBinary        |boolean|是否是二进制文件。          |false   |
| newFile         |boolean|是否是新建文件。           |true    |
| newObjectId     |string |新文件 git object id。 |        |
| newPath         |string |新文件路径。             |test.txt|
| oldObjectId     |string |旧文�� git object id。|        |
| oldPath         |string |旧文件路径。             |test.txt|
| renamedFile     |boolean|是否是重命名文件。          |false   |
| count           |integer|总变更文件数。            |20      |
| totalAddLines   |integer|总增加行数。             |100     |
| totalDelLines   |integer|总删除行数。             |50      |


返回示例
----

```
{
    "changedTreeItems": [
        {
            "addLines": 10,
            "delLines": 0,
            "deletedFile": false,
            "isBinary": false,
            "newFile": false,
            "newObjectId": "",
            "newPath": "test.txt",
            "oldObjectId": "",
            "oldPath": "test.txt",
            "renamedFile": false
        }
    ],
    "count": 20,
    "totalAddLines": 100,
    "totalDelLines": 50
}
```


 
---

 

# ListChangeRequests - 查询合并请求列表_云效(Alibaba Cloud DevOps)-阿里云帮助中心
    
 

    

请求语法
----

```
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/changeRequests
```


请求头
---


|参数             |类型    |是否必填|描述     |示例值                         |
|---------------|------|----|-------|----------------------------|
|x-yunxiao-token|string|是   |个人访问令牌。|pt-0fh3****0fbG_35af****0484|


请求参数
----



* 参数: organizationId
  * 类型: string
  * 位置: path
  * 是否必填: 是
  * 描述: 组织 ID。
  * 示例值: 99d1****71d4
* 参数: page
  * 类型: integer
  * 位置: query
  * 是否必填: 否
  * 描述: 页码。
  * 示例值: 1
* 参数: perPage
  * 类型: integer
  * 位置: query
  * 是否必填: 否
  * 描述: 每页大小。
  * 示例值: 10
* 参数: projectIds
  * 类型: string
  * 位置: query
  * 是否必填: 否
  * 描述: 代码库 ID 或者路径列表，多个以逗号分隔。
  * 示例值: 2308912, 2308913
* 参数: authorIds
  * 类型: string
  * 位置: query
  * 是否必填: 否
  * 描述: 创建者用户 ID 列表，多个以逗号分隔。
  * 示例值: 1234567890
* 参数: reviewerIds
  * 类型: string
  * 位置: query
  * 是否必填: 否
  * 描述: 评审人用户 ID 列表，多个以逗号分隔。
  * 示例值: 1234567890123
* 参数: state
  * 类型: string
  * 位置: query
  * 是否必填: 否
  * 描述: 合并请求筛选状态：opened，merged，closed，默认为 null，即查询全部状态。
  * 示例值: opened
* 参数: search
  * 类型: string
  * 位置: query
  * 是否必填: 否
  * 描述: 标题关键字搜索。
  * 示例值: test-search
* 参数: orderBy
  * 类型: string
  * 位置: query
  * 是否必填: 否
  * 描述: 排序字段，仅支持：created_at - 创建时间；updated_at - 更新时间，默认排序字段。
  * 示例值: updated_at
* 参数: sort
  * 类型: string
  * 位置: query
  * 是否必填: 否
  * 描述: 排序方式：asc - 升序；desc - 降序，默认排序方式。
  * 示例值: desc
* 参数: createdBefore
  * 类型: string
  * 位置: query
  * 是否必填: 否
  * 描述: 起始创建时间，时间格式为 ISO 8601。
  * 示例值: 2019-03-15T08:00:00Z
* 参数: createdAfter
  * 类型: string
  * 位置: query
  * 是否必填: 否
  * 描述: 截止创建时间，时间格式为 ISO 8601。
  * 示例值: 2019-03-15T08:00:00Z


**请求示例**
--------

```
curl -X 'GET' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/{organizationId}/changeRequests?page=<page>&perPage=<perPage>&projectIds=<projectIds>&authorIds=<authorIds>&reviewerIds=<reviewerIds>&state=<state>&search=<search>&orderBy=<orderBy>&sort=<sort>&createdBefore=<createdBefore>&createdAfter=<createdAfter>' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```


返回参数
----



* 参数: -
  * 类型: array
  * 描述: 
  * 示例值: 
* 参数:  -
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数:  author
  * 类型: object
  * 描述: 用户信息。
  * 示例值: 
* 参数:  avatar
  * 类型: string
  * 描述: 用户头像地址。
  * 示例值: https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100
* 参数:  email
  * 类型: string
  * 描述: 用户邮箱。
  * 示例值: username@example.com
* 参数:  name
  * 类型: string
  * 描述: 用户名称。
  * 示例值: test-review-user
* 参数:  state
  * 类型: string
  * 描述: 用户状态：active - 激活可用；blocked - 阻塞暂不可用。
  * 示例值: active
* 参数:  userId
  * 类型: string
  * 描述: 云效用户 ID。
  * 示例值: 62c795c9cf*****b468af8
* 参数:  username
  * 类型: string
  * 描述: 用户登录名。
  * 示例值: root-test-review-user
* 参数:  createdAt
  * 类型: string
  * 描述: 创建时间。
  * 示例值: 2023-05-30T02:53:36Z
* 参数:  creationMethod
  * 类型: string
  * 描述: 合并请求的创建方式：WEB - 页面创建；COMMAND_LINE - 命令行创建。
  * 示例值: WEB
* 参数:  description
  * 类型: string
  * 描述: 描述。
  * 示例值: 新的特性或需求
* 参数:  detailUrl
  * 类型: string
  * 描述: 合并请求详情地址。
  * 示例值: xxx
* 参数:  hasConflict
  * 类型: boolean
  * 描述: 是否有冲突。
  * 示例值: false
* 参数:  localId
  * 类型: integer
  * 描述: 合并请求局部 ID，表示当前代码库中第几个合并请求 ID。
  * 示例值: 1
* 参数:  mergedRevision
  * 类型: string
  * 描述: 合并版本（提交 ID），仅已合并状态才有值。
  * 示例值: 1a072f5367c21f9de3464b8c0ee8546e47764d2d
* 参数:  projectId
  * 类型: integer
  * 描述: 代码库 ID。
  * 示例值: 2369234
* 参数:  reviewers
  * 类型: array
  * 描述: 评审人列表。
  * 示例值: 
* 参数:  -
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数:  avatar
  * 类型: string
  * 描述: 用户头像地址。
  * 示例值: https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100
* 参数:  email
  * 类型: string
  * 描述: 用户邮箱。
  * 示例值: username@example.com
* 参数:  hasCommented
  * 类型: boolean
  * 描述: 是否已经评论过。
  * 示例值: false
* 参数:  hasReviewed
  * 类型: boolean
  * 描述: 是否评审过。
  * 示例值: false
* 参数:  name
  * 类型: string
  * 描述: 用户名称。
  * 示例值: test-codeup
* 参数:  reviewOpinionStatus
  * 类型: string
  * 描述: 评审意见：PASS - 通过；NOT_PASS - 不通过。
  * 示例值: PASS
* 参数:  reviewTime
  * 类型: string
  * 描述: 评审时间。
  * 示例值: 2023-05-30T02:53:36Z
* 参数:  state
  * 类型: string
  * 描述: 用户状态：active - 激活可用；blocked - 阻塞暂不可用。
  * 示例值: active
* 参数:  userId
  * 类型: string
  * 描述: 云效用户 ID。
  * 示例值: 62c795c9cf*****b468af8
* 参数:  username
  * 类型: string
  * 描述: 用户登录名。
  * 示例值: root-test-codeup
* 参数:  sourceBranch
  * 类型: string
  * 描述: 源分支。
  * 示例值: test-merge-source-branch
* 参数:  sourceProjectId
  * 类型: integer
  * 描述: 评审分支所在的代码库 ID。
  * 示例值: 2876119
* 参数:  sourceType
  * 类型: string
  * 描述: 评审分支类型：BRANCH、COMMIT。
  * 示例值: BRANCH
* 参数:  sshUrl
  * 类型: string
  * 描述: 仓库 SSH 克隆地址。
  * 示例值: git@xxx:xxx/test/test.git
* 参数:  state
  * 类型: string
  * 描述: 合并请求状态：UNDER_DEV - 开发中；UNDER_REVIEW - 评审中；TO_BE_MERGED - 待合并；CLOSED - 已关闭；MERGED - 已合并。
  * 示例值: UNDER_DEV
* 参数:  supportMergeFFOnly
  * 类型: boolean
  * 描述: 是否支持 fast-forward-only 合并方式。
  * 示例值: false
* 参数:  targetBranch
  * 类型: string
  * 描述: 目标分支。
  * 示例值: test-merge-target-branch
* 参数:  targetProjectId
  * 类型: integer
  * 描述: 目标分支所在的代码库 ID。
  * 示例值: 2876119
* 参数:  targetType
  * 类型: string
  * 描述: 目标分支类型：BRANCH、COMMIT。
  * 示例值: BRANCH
* 参数:  title
  * 类型: string
  * 描述: 标题。
  * 示例值: 测试标题
* 参数:  totalCommentCount
  * 类型: integer
  * 描述: 总评论数。
  * 示例值: 10
* 参数:  unResolvedCommentCount
  * 类型: integer
  * 描述: 未解决评论数。
  * 示例值: 1
* 参数:  updatedAt
  * 类型: string
  * 描述: 更新时间。
  * 示例值: 2023-05-30T02:53:36Z
* 参数:  webUrl
  * 类型: string
  * 描述: Web 地址。
  * 示例值: ""
* 参数:  workInProgress
  * 类型: boolean
  * 描述: WIP 标识，即是否在开发中。
  * 示例值: false


返回示例
----

```
[
    {
        "author": {
            "avatar": "https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100",
            "email": "username@example.com",
            "name": "test-codeup",
            "state": "active",
            "userId": "62c795c9cf*****b468af8",
            "username": "root-test-codeup"
        },
        "createdAt": "2023-05-30T02:53:36Z",
        "creationMethod": "WEB",
        "description": "新的特性或需求",
        "detailUrl": "xxx",
        "hasConflict": false,
        "localId": 1,
        "mergedRevision": "1a072f5367c21f9de3464b8c0ee8546e47764d2d",
        "projectId": 2876119,
        "reviewers": [
            {
                "avatar": "https://tcs-devops.aliyuncs.com/thumbnail/112afcb7a6a35c3f67f1bea827c4/w/100/h/100",
                "email": "username@example.com",
                "hasCommented": false,
                "hasReviewed": false,
                "name": "test-review-user",
                "reviewOpinionStatus": "PASS",
                "reviewTime": "2023-05-30T02:53:36Z",
                "state": "active",
                "userId": "62c795c9cf*****b468af8",
                "username": "root-test-review-user"
            }
        ],
        "sourceBranch": "test-merge-source-branch",
        "sourceProjectId": 2876119,
        "sourceType": "BRANCH",
        "sshUrl": "git@xxx:xxx/test/test.git",
        "state": "UNDER_DEV",
        "supportMergeFFOnly": false,
        "targetBranch": "test-merge-source-branch",
        "targetProjectId": 2876119,
        "targetType": "BRANCH",
        "title": "test-合并请求标题",
        "totalCommentCount": 10,
        "unResolvedCommentCount": 1,
        "updatedAt": "2023-05-30T02:53:36Z",
        "webUrl": "xxx",
        "workInProgress": false
    }
]
```


响应头
---


|参数           |描述    |示例值                                 |
|-------------|------|------------------------------------|
|x-next-page  |下一页。  |2                                   |
|x-page       |当前页。  |1                                   |
|x-per-page   |每页大小。 |20                                  |
|x-prev-page  |前一页。  |0                                   |
|x-request-id |请求 ID。|37294673-00CA-5B8B-914F-A8B35511E90A|
|x-total      |总数。   |10                                  |
|x-total-pages|总分页数。 |1                                   |


 
---

 


# UpdateChangeRequest - 更新合并请求基本信息_云效(Alibaba Cloud DevOps)-阿里云帮助中心
    

请求语法
----

```
PUT https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}
```


请求头
---


|参数             |类型    |是否必填|描述     |示例值                         |
|---------------|------|----|-------|----------------------------|
|x-yunxiao-token|string|是   |个人访问令牌。|pt-0fh3****0fbG_35af****0484|


请求参数
----


|参数            |类型     |位置  |是否必填|描述                           |示例值                                  |
|--------------|-------|----|----|-----------------------------|-------------------------------------|
|organizationId|string |path|是   |组织 ID。                       |99d1****71d4                         |
|repositoryId  |string |path|是   |代码库 ID 或者 URL-Encoder 编码的全路径。|2835387 或 codeup-org-id%2Fcodeup-demo|
|localId       |integer|path|是   |局部 ID，表示代码库中第几个合并请求。         |1                                    |
|-             |object |body|否   |                             |                                     |
| description  |string |body|否   |描述。                          |test-描述信息                            |
| title        |string |body|否   |标题。                          |test-更新标题                            |


**请求示例**
--------

```
curl -X 'PUT' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "description": "test-描述信息",
        "title": "test-更新标题"
    }'
```


返回参数
----


|参数     |类型     |描述     |示例值  |
|-------|-------|-------|-----|
|-      |object |       |     |
| result|boolean|是否执行成功。|false|


返回示例
----

```
{
    "result": false
}
```


 
---

 


# CreateChangeRequestComment,创建合并请求评论_云效(Alibaba Cloud DevOps)-阿里云帮助中心

请求语法
----

```
POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}/comments
```


请求头
---


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
  * 示例值: 60d54f3daccf2bbd6659f3ad
* 参数: repositoryId
  * 类型: string
  * 位置: path
  * 是否必填: 是
  * 描述: 代码库 ID 或者 URL-Encoder 编码的全路径。
  * 示例值: 2813489或者60de7a6852743a5162b5f957%2FDemoRepo
* 参数: localId
  * 类型: integer
  * 位置: path
  * 是否必填: 是
  * 描述: 局部 ID，表示代码库中第几个合并请求。
  * 示例值: 1
* 参数: -
  * 类型: object
  * 位置: body
  * 是否必填: 否
  * 描述: 
  * 示例值: 
* 参数: comment_type
  * 类型: string
  * 位置: body
  * 是否必填: 是
  * 描述: 评论类型。
  * 示例值: GLOBAL_COMMENT,INLINE_COMMENT
* 参数: content
  * 类型: string
  * 位置: body
  * 是否必填: 是
  * 描述: 评论内容，长度必须在 1 到 65535 之间。
  * 示例值: This is a comment content.
* 参数: draft
  * 类型: boolean
  * 位置: body
  * 是否必填: 是
  * 描述: 是否草稿评论。
  * 示例值: true
* 参数: file_path
  * 类型: string
  * 位置: body
  * 是否必填: 否
  * 描述: 文件名称，只有行内评论才有。
  * 示例值: /src/main/java/com/example/MyClass.java
* 参数: from_patchset_biz_id
  * 类型: string
  * 位置: body
  * 是否必填: 否
  * 描述: 比较的起始版本 id，INLINE_COMMENT 类型的评论必传。
  * 示例值: bf117304dfe44d5d9b1132f348edf92e
* 参数: line_number
  * 类型: integer
  * 位置: body
  * 是否必填: 否
  * 描述: 行号，只有行内评论才有。
  * 示例值: 42
* 参数: parent_comment_biz_id
  * 类型: string
  * 位置: body
  * 是否必填: 否
  * 描述: 父评论 id。
  * 示例值: 12345
* 参数: patchset_biz_id
  * 类型: string
  * 位置: body
  * 是否必填: 是
  * 描述: 关联版本 id，如果是 INLINE_COMMENT，则选择 from_patchset_biz_id 或 to_patchset_biz_id 中的一个。
  * 示例值: bf117304dfe44d5d9b1132f348edf92e
* 参数: resolved
  * 类型: boolean
  * 位置: body
  * 是否必填: 是
  * 描述: 是否标记已解决。
  * 示例值: false
* 参数: to_patchset_biz_id
  * 类型: string
  * 位置: body
  * 是否必填: 否
  * 描述: 比较的目标版本 id， INLINE_COMMENT 类型的评论必传。
  * 示例值: bf117304dfe44d5d9b1132f348edf92e


**请求示例**
--------

```
curl -X 'POST' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/changeRequests/1/comments' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "comment_type": "GLOBAL_COMMENT,INLINE_COMMENT",
        "content": "This is a comment content.",
        "draft": true,
        "file_path": "/src/main/java/com/example/MyClass.java",
        "from_patchset_biz_id": "bf117304dfe44d5d9b1132f348edf92e",
        "line_number": 42,
        "parent_comment_biz_id": "12345",
        "patchset_biz_id": "bf117304dfe44d5d9b1132f348edf92e",
        "resolved": false,
        "to_patchset_biz_id": "bf117304dfe44d5d9b1132f348edf92e"
    }'
```


**返回参数**
--------



* 参数: -
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数: author
  * 类型: object
  * 描述: 用户信息。
  * 示例值: 
* 参数: avatar
  * 类型: string
  * 描述: 用户头像地址。
  * 示例值: https://example/example/w/100/h/100
* 参数: email
  * 类型: string
  * 描述: 用户邮箱。
  * 示例值: username@example.com
* 参数: name
  * 类型: string
  * 描述: 用户名称。
  * 示例值: codeup-name
* 参数: state
  * 类型: string
  * 描述: 用户状态：active - 激活可用；blocked - 阻塞暂不可用。
  * 示例值: active
* 参数: userId
  * 类型: string
  * 描述: 云效用户 ID。
  * 示例值: 62c795xxxb468af8
* 参数: username
  * 类型: string
  * 描述: 用户登录名。
  * 示例值: codeup-username
* 参数: child_comments_list
  * 类型: array
  * 描述: 子评论。
  * 示例值: []
* 参数: -
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数: author
  * 类型: object
  * 描述: 用户信息。
  * 示例值: 
* 参数: avatar
  * 类型: string
  * 描述: 用户头像地址。
  * 示例值: https://example/example/w/100/h/100
* 参数: email
  * 类型: string
  * 描述: 用户邮箱。
  * 示例值: username@example.com
* 参数: name
  * 类型: string
  * 描述: 用户名称。
  * 示例值: codeup-name
* 参数: state
  * 类型: string
  * 描述: 用户状态：active - 激活可用；blocked - 阻塞暂不可用。
  * 示例值: active
* 参数: userId
  * 类型: string
  * 描述: 云效用户 ID。
  * 示例值: 62c795xxxb468af8
* 参数: username
  * 类型: string
  * 描述: 用户登录名。
  * 示例值: codeup-username
* 参数: comment_biz_id
  * 类型: string
  * 描述: 评论 bizId。
  * 示例值: bf117304dfe44d5d9b1132f348edf92e
* 参数: comment_time
  * 类型: string
  * 描述: 评论时间。
  * 示例值: 2023-08-21T14:30:00Z
* 参数: comment_type
  * 类型: string
  * 描述: 评论类型。
  * 示例值: INLINE_COMMENT
* 参数: content
  * 类型: string
  * 描述: 评论内容。
  * 示例值: This is a comment content.
* 参数: expression_reply_list
  * 类型: array
  * 描述: 表态回复。
  * 示例值: []
* 参数: -
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数: emoji
  * 类型: string
  * 描述: emoji 表情符。
  * 示例值: 
* 参数: reply_user_list
  * 类型: array
  * 描述: 表态用户列表。
  * 示例值: 
* 参数: -
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数: reply_biz_id
  * 类型: string
  * 描述: 回复业务 ID。
  * 示例值: 1d8171cf0cc2453197fae0e0a27d5ece
* 参数: reply_user
  * 类型: object
  * 描述: 用户信息。
  * 示例值: 
* 参数: avatar
  * 类型: string
  * 描述: 用户头像地址。
  * 示例值: https://example/example/w/100/h/100
* 参数: email
  * 类型: string
  * 描述: 用户邮箱。
  * 示例值: username@example.com
* 参数: name
  * 类型: string
  * 描述: 用户名称。
  * 示例值: codeup-name
* 参数: state
  * 类型: string
  * 描述: 用户状态：active - 激活可用；blocked - 阻塞暂不可用。
  * 示例值: active
* 参数: userId
  * 类型: string
  * 描述: 云效用户 ID。
  * 示例值: 62c795xxxb468af8
* 参数: username
  * 类型: string
  * 描述: 用户登录名。
  * 示例值: codeup-username
* 参数: filePath
  * 类型: string
  * 描述: 所在文件。
  * 示例值: /src/main/java/com/example/MyClass.java
* 参数: from_patchset_biz_id
  * 类型: string
  * 描述: from 版本 id。
  * 示例值: c341efc7fa38425eb575ad6ab6e95e76
* 参数: is_deleted
  * 类型: boolean
  * 描述: 是否已经删除。
  * 示例值: false
* 参数: last_edit_time
  * 类型: string
  * 描述: 上次编辑时间。
  * 示例值: 2023-08-21T15:00:00Z
* 参数: last_edit_user
  * 类型: object
  * 描述: 用户信息。
  * 示例值: 
* 参数: avatar
  * 类型: string
  * 描述: 用户头像地址。
  * 示例值: https://example/example/w/100/h/100
* 参数: email
  * 类型: string
  * 描述: 用���邮箱。
  * 示例值: username@example.com
* 参数: name
  * 类型: string
  * 描述: 用户名称。
  * 示例值: codeup-name
* 参数: state
  * 类型: string
  * 描述: 用户状态：active - 激活可用；blocked - 阻塞暂不可用。
  * 示例值: active
* 参数: userId
  * 类型: string
  * 描述: 云效用户 ID。
  * 示例值: 62c795xxxb468af8
* 参数: username
  * 类型: string
  * 描述: 用户登录名。
  * 示例值: codeup-username
* 参数: last_resolved_status_change_time
  * 类型: string
  * 描述: 最后解决状态更改时间。
  * 示例值: 2023-08-21T16:00:00Z
* 参数: last_resolved_status_change_user
  * 类型: object
  * 描述: 用户信息。
  * 示例值: 
* 参数: avatar
  * 类型: string
  * 描述: 用户头像地址。
  * 示例值: https://example/example/w/100/h/100
* 参数: email
  * 类型: string
  * 描述: 用户邮箱。
  * 示例值: username@example.com
* 参数: name
  * 类型: string
  * 描述: 用户名称。
  * 示例值: codeup-name
* 参数: state
  * 类型: string
  * 描述: 用户状态：active - 激活可用；blocked - 阻塞暂不可用。
  * 示例值: active
* 参数: userId
  * 类型: string
  * 描述: 云效用户 ID。
  * 示例值: 62c795xxxb468af8
* 参数: username
  * 类型: string
  * 描述: 用户登录名。
  * 示例值: codeup-username
* 参数: line_number
  * 类型: integer
  * 描述: 所在行号。
  * 示例值: 42
* 参数: location
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数: can_located
  * 类型: boolean
  * 描述: 是否可以定位。
  * 示例值: true
* 参数: located_file_path
  * 类型: string
  * 描述: 定位的文件路径。
  * 示例值: /src/main/java/com/example/Example.java
* 参数: located_line_number
  * 类型: integer
  * 描述: 定位的行号。
  * 示例值: 100
* 参数: located_patch_set_biz_id
  * 类型: string
  * 描述: 定位的补丁集业务 ID。
  * 示例值: 1d8171cf0cc2453197fae0e0a27d5ece
* 参数: mr_biz_id
  * 类型: string
  * 描述: 所属 mrBizId。
  * 示例值: bf117304dfe44d5d9b1132f348edf92e
* 参数: out_dated
  * 类型: boolean
  * 描述: 是否过期评论。
  * 示例值: false
* 参数: parent_comment_biz_id
  * 类型: string
  * 描述: 父评论 bizID。
  * 示例值: 1d8171cf0cc2453197fae0e0a27d5ece
* 参数: project_id
  * 类型: integer
  * 描述: 代码库 ID。
  * 示例值: 123456
* 参数: related_patchset
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数: commitId
  * 类型: string
  * 描述: 版本对应的提交 ID。
  * 示例值: 45ede4680536406d793e0e629bc771cb9fcaa153
* 参数: createTime
  * 类型: string
  * 描述: 版本创建时间。
  * 示例值: 2024-10-05T15:30:45Z
* 参数: patchSetBizId
  * 类型: string
  * 描述: 版本 ID，具有唯一性。
  * 示例值: bf117304dfe44d5d9b1132f348edf92e
* 参数: patchSetName
  * 类型: string
  * 描述: 版本名称。
  * 示例值: 版本1
* 参数: ref
  * 类型: string
  * 描述: 版本对应的 ref 信息。
  * 示例值: null
* 参数: relatedMergeItemType
  * 类型: string
  * 描述: 关联的类型：MERGE_SOURCE - 合并源；MERGE_TARGET - 合并目标。
  * 示例值: MERGE_SOURCE
* 参数: shortId
  * 类型: string
  * 描述: 提交 ID 对应的短 ID，通常为8位。
  * 示例值: 45ede468
* 参数: versionNo
  * 类型: integer
  * 描述: 版本号。
  * 示例值: 1
* 参数: resolved
  * 类型: boolean
  * 描述: 是否已解决。
  * 示例值: false
* 参数: root_comment_biz_id
  * 类型: string
  * 描述: 根评论 bizId。
  * 示例值: 1d8171cf0cc2453197fae0e0a27d5ece
* 参数: state
  * 类型: string
  * 描述: 评论状态。
  * 示例值: OPENED,DRAFT
* 参数: to_patchset_biz_id
  * 类型: string
  * 描述: to 版本 id。
  * 示例值: c341efc7fa38425eb575ad6ab6e95e76
* 参数: comment_biz_id
  * 类型: string
  * 描述: 评论 bizId。
  * 示例值: bf117304dfe44d5d9b1132f348edf92e
* 参数: comment_time
  * 类型: string
  * 描述: 评论时间。
  * 示例值: 2023-08-21T14:30:00Z
* 参数: comment_type
  * 类型: string
  * 描述: 评论类型。
  * 示例值: INLINE_COMMENT
* 参数: content
  * 类型: string
  * 描述: 评论内容。
  * 示例值: This is a comment content.
* 参数: expression_reply_list
  * 类型: array
  * 描述: 表态回复。
  * 示例值: []
* 参数: -
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数: emoji
  * 类型: string
  * 描述: emoji 表情符。
  * 示例值: 
* 参数: reply_user_list
  * 类型: array
  * 描述: 表态用户列表。
  * 示例值: 
* 参数: -
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数: reply_biz_id
  * 类型: string
  * 描述: 回复业务 ID。
  * 示例值: 1d8171cf0cc2453197fae0e0a27d5ece
* 参数: reply_user
  * 类型: object
  * 描述: 用户信息。
  * 示例值: 
* 参数: avatar
  * 类型: string
  * 描述: 用户头像地址。
  * 示例值: https://example/example/w/100/h/100
* 参数: email
  * 类型: string
  * 描述: 用户邮箱。
  * 示例值: username@example.com
* 参数: name
  * 类型: string
  * 描述: 用户名称。
  * 示例值: codeup-name
* 参数: state
  * 类型: string
  * 描述: 用户状态：active - 激活可用；blocked - 阻塞暂不可用。
  * 示例值: active
* 参数: userId
  * 类型: string
  * 描述: 云效用户 ID。
  * 示例值: 62c795xxxb468af8
* 参数: username
  * 类型: string
  * 描述: 用户登录名。
  * 示例值: codeup-username
* 参数: filePath
  * 类型: string
  * 描述: 所在文件。
  * 示例值: /src/main/java/com/example/MyClass.java
* 参数: from_patchset_biz_id
  * 类型: string
  * 描述: from 版本 id。
  * 示例值: c341efc7fa38425eb575ad6ab6e95e76
* 参数: is_deleted
  * 类型: boolean
  * 描述: 是否已经删除。
  * 示例值: false
* 参数: last_edit_time
  * 类型: string
  * 描述: 上次编辑时间。
  * 示例值: 2023-08-21T15:00:00Z
* 参数: last_edit_user
  * 类型: object
  * 描述: 用户信息。
  * 示例值: 
* 参数: avatar
  * 类型: string
  * 描述: 用户头像地址。
  * 示例值: https://example/example/w/100/h/100
* 参数: email
  * 类型: string
  * 描述: 用户邮箱。
  * 示例值: username@example.com
* 参数: name
  * 类型: string
  * 描述: 用户名称。
  * 示例值: codeup-name
* 参数: state
  * 类型: string
  * 描述: 用户状态：active - 激活可用；blocked - 阻塞暂不可用。
  * 示例值: active
* 参数: userId
  * 类型: string
  * 描述: 云效用户 ID。
  * 示例值: 62c795xxxb468af8
* 参数: username
  * 类型: string
  * 描述: 用户登录名。
  * 示例值: codeup-username
* 参数: last_resolved_status_change_time
  * 类型: string
  * 描述: 最后解决状态更改时间。
  * 示例值: 2023-08-21T16:00:00Z
* 参数: last_resolved_status_change_user
  * 类型: object
  * 描述: 用户信息。
  * 示例值: 
* 参数: avatar
  * 类型: string
  * 描述: 用户头像地址。
  * 示例值: https://example/example/w/100/h/100
* 参数: email
  * 类型: string
  * 描述: 用户邮箱。
  * 示例值: username@example.com
* 参数: name
  * 类型: string
  * 描述: 用户名称。
  * 示例值: codeup-name
* 参数: state
  * 类型: string
  * 描述: 用户状态：active - 激活可用；blocked - 阻塞暂不可用。
  * 示例值: active
* 参数: userId
  * 类型: string
  * 描述: 云效用户 ID。
  * 示例值: 62c795xxxb468af8
* 参数: username
  * 类型: string
  * 描述: 用户登录名。
  * 示例值: codeup-username
* 参数: line_number
  * 类型: integer
  * 描述: 所在行号。
  * 示例值: 42
* 参数: location
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数: can_located
  * 类型: boolean
  * 描述: 是否可以定位。
  * 示例值: true
* 参数: located_file_path
  * 类型: string
  * 描述: 定位的文件路径。
  * 示例值: /src/main/java/com/example/Example.java
* 参数: located_line_number
  * 类型: integer
  * 描述: 定位的行号。
  * 示例值: 100
* 参数: located_patch_set_biz_id
  * 类型: string
  * 描述: 定位的补丁集业务 ID。
  * 示例值: 1d8171cf0cc2453197fae0e0a27d5ece
* 参数: mr_biz_id
  * 类型: string
  * 描述: 所属 mrBizId。
  * 示例值: bf117304dfe44d5d9b1132f348edf92e
* 参数: out_dated
  * 类型: boolean
  * 描述: 是否过期评论。
  * 示例值: false
* 参数: parent_comment_biz_id
  * 类型: string
  * 描述: 父评论 bizID。
  * 示例值: 1d8171cf0cc2453197fae0e0a27d5ece
* 参数: project_id
  * 类型: integer
  * 描述: 代码库 ID。
  * 示例值: 123456
* 参数: related_patchset
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数: commitId
  * 类型: string
  * 描述: 版本对应的提交 ID。
  * 示例值: 45ede4680536406d793e0e629bc771cb9fcaa153
* 参数: createTime
  * 类型: string
  * 描述: 版本创建时间。
  * 示例值: 2024-10-05T15:30:45Z
* 参数: patchSetBizId
  * 类型: string
  * 描述: 版本 ID，具有唯一性。
  * 示例值: bf117304dfe44d5d9b1132f348edf92e
* 参数: patchSetName
  * 类型: string
  * 描述: 版本名称。
  * 示例值: 版本1
* 参数: ref
  * 类型: string
  * 描述: 版本对应的 ref 信息。
  * 示例值: null
* 参数: relatedMergeItemType
  * 类型: string
  * 描述: 关联的类型：MERGE_SOURCE - 合并源；MERGE_TARGET - 合并目标。
  * 示例值: MERGE_SOURCE
* 参数: shortId
  * 类型: string
  * 描述: 提交 ID 对应的短 ID，通常为8位。
  * 示例值: 45ede468
* 参数: versionNo
  * 类型: integer
  * 描述: 版本号。
  * 示例值: 1
* 参数: resolved
  * 类型: boolean
  * 描述: 是否已解决。
  * 示例值: false
* 参数: root_comment_biz_id
  * 类型: string
  * 描述: 根评论 bizId。
  * 示例值: 1d8171cf0cc2453197fae0e0a27d5ece
* 参数: state
  * 类型: string
  * 描述: 评���状态。
  * 示例值: OPENED,DRAFT
* 参数: to_patchset_biz_id
  * 类型: string
  * 描述: to 版本 id。
  * 示例值: c341efc7fa38425eb575ad6ab6e95e76


**返回示例**
--------

```
{
    "author": {
        "avatar": "https://example/example/w/100/h/100",
        "email": "username@example.com",
        "name": "codeup-name",
        "state": "active",
        "userId": "62c795xxxb468af8",
        "username": "codeup-username"
    },
    "child_comments_list": [],
    "comment_biz_id": "bf117304dfe44d5d9b1132f348edf92e",
    "comment_time": "2023-08-21T14:30:00Z",
    "comment_type": "INLINE_COMMENT",
    "content": "This is a comment content.",
    "expression_reply_list": [],
    "filePath": "/src/main/java/com/example/MyClass.java",
    "from_patchset_biz_id": "c341efc7fa38425eb575ad6ab6e95e76",
    "is_deleted": false,
    "last_edit_time": "2023-08-21T15:00:00Z",
    "last_edit_user": {
        "avatar": "https://example/example/w/100/h/100",
        "email": "username@example.com",
        "name": "codeup-name",
        "state": "active",
        "userId": "62c795xxxb468af8",
        "username": "codeup-username"
    },
    "last_resolved_status_change_time": "2023-08-21T16:00:00Z",
    "last_resolved_status_change_user": {
        "avatar": "https://example/example/w/100/h/100",
        "email": "username@example.com",
        "name": "codeup-name",
        "state": "active",
        "userId": "62c795xxxb468af8",
        "username": "codeup-username"
    },
    "line_number": 42,
    "location": {
        "can_located": true,
        "located_file_path": "/src/main/java/com/example/Example.java",
        "located_line_number": 100,
        "located_patch_set_biz_id": "1d8171cf0cc2453197fae0e0a27d5ece"
    },
    "mr_biz_id": "bf117304dfe44d5d9b1132f348edf92e",
    "out_dated": false,
    "parent_comment_biz_id": "1d8171cf0cc2453197fae0e0a27d5ece",
    "project_id": 123456,
    "related_patchset": {
        "commitId": "45ede4680536406d793e0e629bc771cb9fcaa153",
        "createTime": "2024-10-05T15:30:45Z",
        "patchSetBizId": "bf117304dfe44d5d9b1132f348edf92e",
        "patchSetName": "版本1",
        "ref": "null",
        "relatedMergeItemType": "MERGE_SOURCE",
        "shortId": "45ede468",
        "versionNo": 1
    },
    "resolved": false,
    "root_comment_biz_id": "1d8171cf0cc2453197fae0e0a27d5ece",
    "state": "OPENED,DRAFT",
    "to_patchset_biz_id": "c341efc7fa38425eb575ad6ab6e95e76"
}
```


 
-------

 


# UpdateChangeRequestComment,更新合并请求评论_云效(Alibaba Cloud DevOps)-阿里云帮助中心

    

### **请求语法**

```
PUT https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}/comments/{commentBizId}
```


### **请求头**


|参数             |类型    |是否必填|描述     |示例值                         |
|---------------|------|----|-------|----------------------------|
|x-yunxiao-token|string|是   |个人访问令牌。|pt-0fh3****0fbG_35af****0484|


### **请求参数**



* 参数: organizationId
  * 类型: string
  * 位置: path
  * 是否必填: 是
  * 描述: 组织 ID。
  * 示例值: 60d54f3daccf2bbd6659f3ad
* 参数: repositoryId
  * 类型: string
  * 位置: path
  * 是否必填: 是
  * 描述: 代码库 ID 或者 URL-Encoder 编码的全路径。
  * 示例值: 2813489或者60de7a6852743a5162b5f957%2FDemoRepo
* 参数: localId
  * 类型: integer
  * 位置: path
  * 是否必填: 是
  * 描述: 局部 ID，表示代码库中第几个合并请求。
  * 示例值: 1
* 参数: commentBizId
  * 类型: string
  * 位置: path
  * 是否必填: 是
  * 描述: 评论 bizId。
  * 示例值: bf117304dfe44d5d9b1132f348edf92e
* 参数: -
  * 类型: object
  * 位置: body
  * 是否必填: 否
  * 描述: 
  * 示例值: 
* 参数: content
  * 类型: string
  * 位置: body
  * 是否必填: 否
  * 描述: 内容。
  * 示例值: your new comment
* 参数: resolved
  * 类型: boolean
  * 位置: body
  * 是否必填: 否
  * 描述: 是否已解决。
  * 示例值: false


### **请求示例**

```
curl -X 'PUT' \
  'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/changeRequests/1/comments/bf117304dfe44d5d9b1132f348edf92e' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "content": "your new comment",
        "resolved": false
    }'

```


### **返回参数**


|参数    |类型     |描述   |示例值 |
|------|-------|-----|----|
|-     |object |     |    |
|result|boolean|执行结果。|true|


### **返回示例**

```
{
    "result": true
}

```

# UpdateChangeRequest - 更新合并请求基本信息_云效(Alibaba Cloud DevOps)-阿里云帮助中心

请求语法
----

```
PUT https://{domain}/oapiz`/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}
```


请求头
---


|参数             |类型    |是否必填|描述     |示例值                         |
|---------------|------|----|-------|----------------------------|
|x-yunxiao-token|string|是   |个人访问令牌。|pt-0fh3****0fbG_35af****0484|


请求参数
----


|参数            |类型     |位置  |是否必填|描述                           |示例值                                  |
|--------------|-------|----|----|-----------------------------|-------------------------------------|
|organizationId|string |path|是   |组织 ID。                       |99d1****71d4                         |
|repositoryId  |string |path|是   |代码库 ID 或者 URL-Encoder 编码的全路径。|2835387 或 codeup-org-id%2Fcodeup-demo|
|localId       |integer|path|是   |局部 ID，表示代码库中第几个合并请求。         |1                                    |
|-             |object |body|否   |                             |                                     |
| description  |string |body|否   |描述。                          |test-描述信息                            |
| title        |string |body|否   |标题。                          |test-更新标题                            |


**请求示例**
--------

```
curl -X 'PUT' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "description": "test-描述信息",
        "title": "test-更新标题"
    }'
```


返回参数
----


|参数     |类型     |描述     |示例值  |
|-------|-------|-------|-----|
|-      |object |       |     |
| result|boolean|是否执行成功。|false|


返回示例
----

```
{
    "result": false
}
```


# ListMergeRequestComments,查询评论列表_云效(Alibaba Cloud DevOps)-阿里云帮助中心
### **请求语法**

```
POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/changeRequests/{localId}/comments/list
```


### **请求头**


|参数             |类型    |是否必填|描述     |示例值                         |
|---------------|------|----|-------|----------------------------|
|x-yunxiao-token|string|是   |个人访问令牌。|pt-0fh3****0fbG_35af****0484|


### **请求参数**



* 参数: organizationId
  * 类型: string
  * 位置: path
  * 是否必填: 是
  * 描述: 组织 ID。
  * 示例值: 60d54f3daccf2bbd6659f3ad
* 参数: repositoryId
  * 类型: string
  * 位置: path
  * 是否必填: 是
  * 描述: 代码库 ID 或者 URL-Encoder 编码的全路径。
  * 示例值: 2813489或者60de7a6852743a5162b5f957%2FDemoRepo
* 参数: localId
  * 类型: integer
  * 位置: path
  * 是否必填: 是
  * 描述: 局部 ID，表示代码库中第几个合并请求。
  * 示例值: 1
* 参数: -
  * 类型: object
  * 位置: body
  * 是否必填: 否
  * 描述: 
  * 示例值: 
* 参数: comment_biz_id_list
  * 类型: array[string]
  * 位置: body
  * 是否必填: 否
  * 描述: 所需评论 ID 列表，从根评论开始返回。
  * 示例值: 
* 参数: comment_type
  * 类型: string
  * 位置: body
  * 是否必填: 否
  * 描述: 评论类型。
  * 示例值: GLOBAL_COMMENT,INLINE_COMMENT
* 参数: file_path
  * 类型: string
  * 位置: body
  * 是否必填: 否
  * 描述: 文件路径。
  * 示例值: /src/main/test.java
* 参数: patchset_biz_id_list
  * 类型: array[string]
  * 位置: body
  * 是否必填: 否
  * 描述: 版本业务 ID 列表。
  * 示例值: 
* 参数: resolved
  * 类型: boolean
  * 位置: body
  * 是否必填: 
  * 描述: 是否已解决。
  * 示例值: false
* 参数: state
  * 类型: string
  * 位置: body
  * 是否必填: 
  * 描述: 评论状态。
  * 示例值: DRAFT,OPENED


### **请求示例**

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/organizations/60d54f3daccf2bbd6659f3ad/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/changeRequests/1/comments/list' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "comment_biz_id_list": [
            
        ],
        "comment_type": "GLOBAL_COMMENT,INLINE_COMMENT",
        "file_path": "/src/main/test.java",
        "patchset_biz_id_list": [
            
        ],
        "resolved": false,
        "state": "DRAFT,OPENED"
    }'

```


### **返回参数**



* 参数: -
  * 类型: array
  * 描述: 
  * 示例值: 
* 参数: -
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数: author
  * 类型: object
  * 描述: 用户信息。
  * 示例值: 
* 参数: avatar
  * 类型: string
  * 描述: 用户头像地址。
  * 示例值: https://example/example/w/100/h/100
* 参数: email
  * 类型: string
  * 描述: 用户邮箱。
  * 示例值: username@example.com
* 参数: name
  * 类型: string
  * 描述: 用户名称。
  * 示例值: codeup-name
* 参数: state
  * 类型: string
  * 描述: 用户状态：active - 激活可用；blocked - 阻塞暂不可用。
  * 示例值: active
* 参数: userId
  * 类型: string
  * 描述: 云效用户 ID。
  * 示例值: 62c795xxxb468af8
* 参数: username
  * 类型: string
  * 描述: 用户登录名。
  * 示例值: codeup-username
* 参数: child_comments_list
  * 类型: array[string]
  * 描述: 子评论。
  * 示例值: []
* 参数: comment_time
  * 类型: string
  * 描述: 评论时间。
  * 示例值: 2023-08-21T14:30:00Z
* 参数: comment_type
  * 类型: string
  * 描述: 评论类型。
  * 示例值: INLINE_COMMENT
* 参数: content
  * 类型: string
  * 描述: 评论内容。
  * 示例值: This is a comment content.
* 参数: expression_reply_list
  * 类型: array
  * 描述: 表态回复。
  * 示例值: []
* 参数: -
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数: emoji
  * 类型: string
  * 描述: emoji 表情符。
  * 示例值: 
* 参数: reply_user_list
  * 类型: array
  * 描述: 表态用户列表。
  * 示例值: 
* 参数: -
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数: reply_biz_id
  * 类型: string
  * 描述: 回复业务 ID。
  * 示例值: 1d8171cf0cc2453197fae0e0a27d5ece
* 参数: reply_user
  * 类型: object
  * 描述: 用户信息。
  * 示例值: 
* 参数: avatar
  * 类型: string
  * 描述: 用户头像地址。
  * 示例值: https://example/example/w/100/h/100
* 参数: email
  * 类型: string
  * 描述: 用户邮箱。
  * 示例值: username@example.com
* 参数: name
  * 类型: string
  * 描述: 用户名称。
  * 示例值: codeup-name
* 参数: state
  * 类型: string
  * 描述: 用户状态：active - 激活��用；blocked - 阻塞暂不可用。
  * 示例值: active
* 参数: userId
  * 类型: string
  * 描述: 云效用户 ID。
  * 示例值: 62c795xxxb468af8
* 参数: username
  * 类型: string
  * 描述: 用户登录名。
  * 示例值: codeup-username
* 参数: filePath
  * 类型: string
  * 描述: 所在文件。
  * 示例值: /src/main/java/com/example/MyClass.java
* 参数: from_patchset_biz_id
  * 类型: string
  * 描述: from 版本 id。
  * 示例值: c341efc7fa38425eb575ad6ab6e95e76
* 参数: is_deleted
  * 类型: boolean
  * 描述: 是否已经删除。
  * 示例值: false
* 参数: last_edit_time
  * 类型: string
  * 描述: 上次编辑时间。
  * 示例值: 2023-08-21T15:00:00Z
* 参数: last_edit_user
  * 类型: object
  * 描述: 用户信息。
  * 示例值: 
* 参数: avatar
  * 类型: string
  * 描述: 用户头像地址。
  * 示例值: https://example/example/w/100/h/100
* 参数: email
  * 类型: string
  * 描述: 用户邮箱。
  * 示例值: username@example.com
* 参数: name
  * 类型: string
  * 描述: 用户名称。
  * 示例值: codeup-name
* 参数: state
  * 类型: string
  * 描述: 用户状态：active - 激活可用；blocked - 阻塞暂不可用。
  * 示例值: active
* 参数: userId
  * 类型: string
  * 描述: 云效用户 ID。
  * 示例值: 62c795xxxb468af8
* 参数: username
  * 类型: string
  * 描述: 用户登录名。
  * 示例值: codeup-username
* 参数: last_resolved_status_change_time
  * 类型: string
  * 描述: 最后解决状态更改时间。
  * 示例值: 2023-08-21T16:00:00Z
* 参数: last_resolved_status_change_user
  * 类型: object
  * 描述: 用户信息。
  * 示例值: 
* 参数: avatar
  * 类型: string
  * 描述: 用户头像地址。
  * 示例值: https://example/example/w/100/h/100
* 参数: email
  * 类型: string
  * 描述: 用户邮箱。
  * 示例值: username@example.com
* 参数: name
  * 类型: string
  * 描述: 用户名称。
  * 示例值: codeup-name
* 参数: state
  * 类型: string
  * 描述: 用户状态：active - 激活可用；blocked - 阻塞暂不可用。
  * 示例值: active
* 参数: userId
  * 类型: string
  * 描述: 云效用户 ID。
  * 示例值: 62c795xxxb468af8
* 参数: username
  * 类型: string
  * 描述: 用户登录名。
  * 示例值: codeup-username
* 参数: line_number
  * 类型: integer
  * 描述: 所在行号。
  * 示例值: 42
* 参数: location
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数: can_located
  * 类型: boolean
  * 描述: 是否可以定位。
  * 示例值: true
* 参数: located_file_path
  * 类型: string
  * 描述: 定位的文件路径。
  * 示例值: /src/main/java/com/example/Example.java
* 参数: located_line_number
  * 类型: integer
  * 描述: 定位的行号。
  * 示例值: 100
* 参数: located_patch_set_biz_id
  * 类型: string
  * 描述: 定位的补丁集业务 ID。
  * 示例值: 1d8171cf0cc2453197fae0e0a27d5ece
* 参数: mr_biz_id
  * 类型: string
  * 描述: 所属 mrBizId。
  * 示例值: bf117304dfe44d5d9b1132f348edf92e
* 参数: out_dated
  * 类型: boolean
  * 描述: 是否过期评论。
  * 示例值: false
* 参数: parent_comment_biz_id
  * 类型: string
  * 描述: 父评论 bizID。
  * 示例值: 1d8171cf0cc2453197fae0e0a27d5ece
* 参数: project_id
  * 类型: integer
  * 描述: 代码库 ID。
  * 示例值: 123456
* 参数: related_patchset
  * 类型: object
  * 描述: 
  * 示例值: 
* 参数: commitId
  * 类型: string
  * 描述: 版本对应的提交 ID。
  * 示例值: 45ede4680536406d793e0e629bc771cb9fcaa153
* 参数: createTime
  * 类型: string
  * 描述: 版本创建时间。
  * 示例值: 2024-10-05T15:30:45Z
* 参数: patchSetBizId
  * 类型: string
  * 描述: 版本 ID，具有唯一性。
  * 示例值: bf117304dfe44d5d9b1132f348edf92e
* 参数: patchSetName
  * 类型: string
  * 描述: 版本名称。
  * 示例值: 版本1
* 参数: ref
  * 类型: string
  * 描述: 版本对应的 ref 信息。
  * 示例值: null
* 参数: relatedMergeItemType
  * 类型: string
  * 描述: 关联的类型：MERGE_SOURCE - 合并源；MERGE_TARGET - 合并目标。
  * 示例值: MERGE_SOURCE
* 参数: shortId
  * 类型: string
  * 描述: 提交 ID 对应的短 ID，通常为8位。
  * 示例值: 45ede468
* 参数: versionNo
  * 类型: integer
  * 描述: 版本号。
  * 示例值: 1
* 参数: resolved
  * 类型: boolean
  * 描述: 是否已解决。
  * 示例值: false
* 参数: root_comment_biz_id
  * 类型: string
  * 描述: 根评论 bizId。
  * 示例值: 1d8171cf0cc2453197fae0e0a27d5ece
* 参数: state
  * 类型: string
  * 描述: 评论状态。
  * 示例值: OPENED,DRAFT
* 参数: to_patchset_biz_id
  * 类型: string
  * 描述: to 版本 id。
  * 示例值: c341efc7fa38425eb575ad6ab6e95e76


### **返回示例**

```
[
    {
        "author": {
            "avatar": "https://example/example/w/100/h/100",
            "email": "username@example.com",
            "name": "codeup-name",
            "state": "active",
            "userId": "62c795xxxb468af8",
            "username": "codeup-username"
        },
        "child_comments_list": [],
        "comment_biz_id": "bf117304dfe44d5d9b1132f348edf92e",
        "comment_time": "2023-08-21T14:30:00Z",
        "comment_type": "INLINE_COMMENT",
        "content": "This is a comment content.",
        "expression_reply_list": [],
        "filePath": "/src/main/java/com/example/MyClass.java",
        "from_patchset_biz_id": "c341efc7fa38425eb575ad6ab6e95e76",
        "is_deleted": false,
        "last_edit_time": "2023-08-21T15:00:00Z",
        "last_edit_user": {
            "avatar": "https://example/example/w/100/h/100",
            "email": "username@example.com",
            "name": "codeup-name",
            "state": "active",
            "userId": "62c795xxxb468af8",
            "username": "codeup-username"
        },
        "last_resolved_status_change_time": "2023-08-21T16:00:00Z",
        "last_resolved_status_change_user": {
            "avatar": "https://example/example/w/100/h/100",
            "email": "username@example.com",
            "name": "codeup-name",
            "state": "active",
            "userId": "62c795xxxb468af8",
            "username": "codeup-username"
        },
        "line_number": 42,
        "location": {
            "can_located": true,
            "located_file_path": "/src/main/java/com/example/Example.java",
            "located_line_number": 100,
            "located_patch_set_biz_id": "1d8171cf0cc2453197fae0e0a27d5ece"
        },
        "mr_biz_id": "bf117304dfe44d5d9b1132f348edf92e",
        "out_dated": false,
        "parent_comment_biz_id": "1d8171cf0cc2453197fae0e0a27d5ece",
        "project_id": 123456,
        "related_patchset": {
            "commitId": "45ede4680536406d793e0e629bc771cb9fcaa153",
            "createTime": "2024-10-05T15:30:45Z",
            "patchSetBizId": "bf117304dfe44d5d9b1132f348edf92e",
            "patchSetName": "版本1",
            "ref": "null",
            "relatedMergeItemType": "MERGE_SOURCE",
            "shortId": "45ede468",
            "versionNo": 1
        },
        "resolved": false,
        "root_comment_biz_id": "1d8171cf0cc2453197fae0e0a27d5ece",
        "state": "OPENED,DRAFT",
        "to_patchset_biz_id": "c341efc7fa38425eb575ad6ab6e95e76"
    }
]

```

