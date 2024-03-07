# API文档
- [登录](#登录)
  - [CAS登录](#CAS登录)
- [用户](#用户)
  - [用户信息](#用户信息)
  - [用户成绩](#用户成绩)
  - [学科成绩排名](#学科成绩排名)
  - [课程表](#课程表)
- [特别响应](#特别响应)

## 登录
### CAS登录

用于向学校后端cas服务器进行登录请求，保持登录状态以及获取登录token。

- **请求URL**:
  `/<school_name>/cas_login`

- **请求方法**:
  `POST`

#### URL参数

- `school_name`: 学校名称。

#### 请求体（json）

  ```json
  {
      "username": "114514",
      "password": "password"
  }
  ```

#### 成功响应

- **代码**：200
- **响应示例**：
  ```json
  {
      "status": "OK",
      "message": "Login successful",
      "authToken": "TGT-114514-xxxxxx"
  }
  ```

## 用户
### 用户信息

用于获取用户信息。

- **请求URL**:
  `/<school_name>/user/info`

- **请求方法**:
  `GET`

#### URL参数

- `school_name`: 学校名称。

#### 请求头

- `Authorization`: `authToken`

#### 成功响应

- **代码**：200
- **响应示例**：
  ```json
  {
      "status": "OK",
      "message": "User info retrieved successfully",
      "data": {
          "userName": "李田所",
          "userId": "114514",
          "userType": "学生",
          "userDepartment": "计算机科学与技术学院",
          "userSex": "男"
      }
  }
  ```

### 用户成绩
用于查询用户成绩信息。

- **请求URL**:
  `/<school_name>/user/score`

- **请求方法**:
  `GET`, `POST`

#### URL参数

- `school_name`: 学校名称。

#### 请求头

- `Authorization`: `authToken`

#### 请求体（仅POST方法）
  ```json
  {
    "semester": "2022-2023-2,2023-2024-1",
    "amount": 10,
    "isNeedRank": "true"
  }
  ```
  - `semester`: 请求查询的学期，可同时含有多个学期，以逗号隔开，或者为`all`。默认值为`"2022-2023-2,2023-2024-1"`。
  - `amount`: 响应成绩的最大数量。默认值为`10`。
  - `isNeedRank`: 是否需要排名信息，值只能为`true`或者`false`。默认值为`false`。

上述参数若请求中不含有则采用默认值。若使用`GET`方法，则上述三个参数均采用默认值。

#### 成功响应

- **代码**：200
  - **响应示例**：
  ```json
  {
    "status": "OK",
    "message": "User score retrieved successfully",
    "totalCount": 42,
    "data": [
      {
        "courseName": "绳之以法的正确姿势概论",
        "examTime": "2024-01-17",
        "courseID": "114514",
        "classID": "1919810",
        "totalScore": 100,
        "gradePoint": "5.0",
        "regularScore": "100",
        "midScore": "100",
        "finalScore": "100",
        "regularPercent": "30",
        "midPercent": "30",
        "finalPercent": "40",
        "courseType": "必修课",
        "courseCate": "公共必修课程",
        "isRetake": "初修",
        "credits": 3.0,
        "gradeType": "百分制",
        "semester": "2023-2024-1",
        "department": "和蔼学院",
        "courseRank": {
              "abc": "def"
            }
        }
     ]
  }
  ```
  **注：**
- 此处省略了`isNeedRank`为`true`时的排名信息，若指定为`true`，则对应学科的数据中将出现`courseRank`字段，具体格式详见`学科成绩排名`的响应示例。

### 学科成绩排名
- **请求URL**:
  `/<school_name>/user/score_rank`
- **请求方法**: `POST`

#### URL参数

- `school_name`: 学校名称。

#### 请求头

- `Authorization`: `authToken`

#### 请求体

  ```json
  {
    "courseID": "114514",
    "classID": "1919810",
    "semester": "2023-2024-1"
  }
  ```
所有字段均为必填字段，格式与`用户成绩`的响应中的对应字段格式相同。
  - `courseid`: 课程ID。
  - `classid`: 教学班ID。
  - `semester`: 学期。

#### 成功响应
- **响应示例**:
  ```json
  {
  "status": "OK",
  "message": "Score rank retrieved successfully",
  "data":{
    "class": {
      "rank": 49,
      "totalPeopleNum": 96,
      "lowScore": 70,
      "highScore": 98,
      "averageScore": 90,
      "numAbove90": 60,
      "numAbove80": 26,
      "numAbove70": 10
    },
    "school": {
      "rank": 1149,
      "totalPeopleNum": 4827,
      "lowScore": 39,
      "highScore": 100,
      "averageScore": 80,
      "numAbove90": 4000,
      "numAbove80": 800,
      "numAbove70": 25,
      "numAbove60": 1,
      "numBelow60": 1
    }
  }
  }
  ```
  **注：**
- 分数段为10分一个区间，如`numAbove80`表示80-90分的人数。
- 低分数段若是没有人，则不会出现在响应数据中。如该学科最低分为70分，则不会出现`numAbove60`和`numBelow60`字段。

###  课程表
- **请求URL**:
  `/<school_name>/user/course_table`
- **请求方法**: `GET`, `POST`

#### URL参数

- `school_name`: 学校名称。

#### 请求头

- `Authorization`: `authToken`

#### 请求体(仅POST方法)
  ```json
  {
    "semester": "2022-2023-2"
  }
  ```
  - `semester`: 学期,默认值为当前学期。
若使用`GET`方法，则采用默认值。

#### 成功响应
- **响应示例**:
  ```json
    {
    "message": "Course table retrieved successfully",
    "status": "OK",
    "data": {
      "arranged": [
        {
          "courseName": "品史",
          "classID": "114514",
          "courseID": "1919810",
          "credit": 2,
          "creditHour": 36,
          "semester": "2023-2024-2",
          "teacher": "李田所",
          "time": "4:1-2",
          "week": "1-18周",
          "classroom": "会员制餐厅112"
        }
      ],
      "not_arranged": [
        {
          "courseName": "拉史",
          "classID": "514114",
          "courseID": "8109191",
          "credit": 0,
          "creditHour": 9,
          "semester": "2023-2024-2",
          "teacher": "浩二",
          "week": "1-18周"
        }
      ]
    }
  }

  ```
  **注：**
- `time`字段表示上课时间，格式为`周数`:`节数`，例如1:1-2表示周一的1-2节。如果一节课有多个时间段，则用逗号隔开，例如1:1-2,2:3-4表示周一的1-2节和周二的3-4节。

## 特别响应
部分特殊错误可能需要客户端进行特定处理，其响应会有特定的状态码及`status`字段。

### 认证过期
请求头中的`authToken`无效或过期。

- **代码**：401
- **响应示例**:
    ```json
    {
        "status": "invalid",
        "message": "Failed to get user info.authToken is probably invalid"
    }
    ```
  
### 意外错误
产生了意外错误，且可能是后端服务器产生的问题，建议客户端进行重试。

- **代码**：402
- **响应示例**:
    ```json
    {
        "status": "retry",
        "message": "Unexpected behavior happened.Please try again"
    }
    ```