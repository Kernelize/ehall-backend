# ehall-backend
ehall-backend是一个纯api式的服务端，使用Flask框架运行。该服务端可向不同学校的一站式事务大厅后端服务器获取各类数据。

## 学校支持情况
详见[学校支持列表](docs/school_support.md)
## API端点
- [CAS登录](#CAS登录)
- [用户信息](#用户信息)
- [用户成绩](#用户成绩)

### CAS登录

用于向学校后端cas服务器进行登录请求，保持登录状态以及获取登录token。

- **请求URL**:
  `/api/<school_name>/cas_login`

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
      "auth_token": "TGT-114514-xxxxxx"
  }
  ```


### 用户信息

用于获取用户信息。

- **请求URL**:
  `/api/<school_name>/user/info`

- **请求方法**:
  `GET`

#### URL参数

- `school_name`: 学校名称。

#### 请求头

- `Authorization`: `auth_token`

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
  `/api/<school_name>/user/score`

- **请求方法**:
  `GET`, `POST`

#### URL参数

- `school_name`: 学校名称。

#### 请求头

- `Authorization`: `auth_token`

#### 请求体（仅POST方法）
  ```json
  {
    "semester": "2022-2023-2,2023-2024-1",
    "amount": 10
  }
  ```
  - `semester`: 请求查询的学期，可同时含有多个学期，以逗号隔开，或者为`all`。默认值为`"2022-2023-2,2023-2024-1"`。
  - `amount`: 响应成绩的最大数量。默认值为`10`。

若使用`GET`方法，则上述两个参数均采用默认值。

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
        "courseId": "114514",
        "classId": "1919810",
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
        "semester": "2023-2024学年第1学期",
        "department": "和蔼学院"
        }
     ]
  }
  ```

## 特别响应
部分特殊错误可能需要客户端进行特定处理，其响应会有特定的状态码及`status`字段。

### 认证过期
请求头中的`auth_token`无效或过期。

- **代码**：401
- **响应示例**:
    ```json
    {
        "status": "invalid",
        "message": "Failed to get user info.auth_token is probably invalid"
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
