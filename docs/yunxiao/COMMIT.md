#  查询提交信息_云效(Alibaba Cloud DevOps)-阿里云帮助中心


**请求语法**
--------

```
GET https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/commits/{sha}
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
  * 示例值: 99d1****71d4
* 参数: repositoryId
  * 类型: string
  * 位置: path
  * 是否必填: 是
  * 描述: 代码库 ID 或者 URL-Encoder 编码的全路径。
  * 示例值: 2825387
* 参数: sha
  * 类型: string
  * 位置: path
  * 是否必填: 是
  * 描述: 提交 ID，即 Commit SHA 值。
  * 示例值: ff4fb5ac6d1f44f452654336d2dba468ae6c8d04


**请求示例**
--------

```
curl -X 'GET' \
  'https://test.rdc.aliyuncs.com/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/commits/{sha}' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484'
```


**返回参数**
--------


|参数             |类型           |描述          |示例值                                      |
|---------------|-------------|------------|-----------------------------------------|
|-              |object       |            |                                         |
| authorEmail   |string       |作者邮箱。       |username@example.com                     |
| authorName    |string       |作者姓名。       |committer-codeup                         |
| authoredDate  |string       |作者提交时间。     |2022-08-08 18:09:09                      |
| committedDate |string       |提交者提交时间。    |2022-03-18 15:00:02                      |
| committerEmail|string       |提交者邮箱。      |username@example.com                     |
| committerName |string       |提交者姓名。      |committer-codeup                         |
| id            |string       |提交 ID。      |ff4fb5ac6d1f44f452654336d2dba468ae6c8d04 |
| message       |string       |提交内容。       |提交的具体内容                                  |
| parentIds     |array[string]|父提交 ID。     |                                         |
| shortId       |string       |代码组路径。      |ff4fb5ac                                 |
| stats         |object       |变更行数统计。     |false                                    |
| additions     |integer      |增加行数。       |5                                        |
| deletions     |integer      |删除行数。       |2                                        |
| total         |integer      |总变动行数。      |10                                       |
| title         |string       |标题，提交的第一行内容。|提交标题                                     |
| webUrl        |string       |页面访问地址。     | ""                                      |


**返回示例**
--------

```
{
    "authorEmail": "username@example.com",
    "authorName": "committer-codeup",
    "authoredDate": "2022-08-08 18:09:09",
    "committedDate": "2022-03-18 15:00:02",
    "committerEmail": "username@example.com",
    "committerName": "committer-codeup",
    "id": "ff4fb5ac6d1f44f452654336d2dba468ae6c8d04 ",
    "message": "提交的具体内容",
    "parentIds": [
        
    ],
    "shortId": "ff4fb5ac",
    "stats": {
        "additions": 5,
        "deletions": 2,
        "total": 10
    },
    "title": "提交的具体内容",
    "webUrl": "\"\""
}
```


**错���码**
---------

 

# CreateCommitComment - 给单个提交添加评论-阿里云帮助中心

    

### **请求语法**

```
POST https://{domain}/oapi/v1/codeup/organizations/{organizationId}/repositories/{repositoryId}/commits/{sha}/comments
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
  * 示例值: 60de7a6852743a5162b5f957
* 参数: repositoryId
  * 类型: string
  * 位置: path
  * 是否必填: 是
  * 描述: 代码库 ID 或者 URL-Encoder 编码的全路径。
  * 示例值: 2813489或者60de7a6852743a5162b5f957%2FDemoRepo
* 参数: sha
  * 类型: string
  * 位置: path
  * 是否必填: 是
  * 描述: 提交的 SHA 值。
  * 示例值: 2b4f8fc38bdf464359c3a05334654fa27e15a704
* 参数: -
  * 类型: object
  * 位置: body
  * 是否必填: 否
  * 描述: commit 的评论。
  * 示例值: 
* 参数: content
  * 类型: string
  * 位置: body
  * 是否必填: 是
  * 描述: commit 的评论内容。
  * 示例值: comment content


### **请求示例**

```
curl -X 'POST' \
  'https://{domain}/oapi/v1/codeup/organizations/60de7a6852743a5162b5f957/repositories/2813489或者60de7a6852743a5162b5f957%2FDemoRepo/commits/2b4f8fc38bdf464359c3a05334654fa27e15a704/comments' \
  -H 'Content-Type: application/json' \
  -H 'x-yunxiao-token: pt-0fh3****0fbG_35af****0484' \
  --data '
    {
        "content": "comment content"
    }'

```


### **返回参数**

无

### **��误码**

 