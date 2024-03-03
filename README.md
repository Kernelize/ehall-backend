# ehall-backend
ehall-backend是一个纯api式的服务端，使用Flask框架运行。该服务端可向不同学校的一站式事务大厅后端服务器获取各类数据。

## 部署
您可从[Actions构建](https://github.com/Kernelize/ehall-backend/actions)中下载最新的可执行文件，或者自行构建。  
Actions构建的可执行文件已包含`waitress`WSGI服务器，可直接运行。  
默认的监听地址为`0.0.0.0:8080`，可通过环境变量`HOST`与`PORT`修改。

## API端点
详见[API文档](docs/api.md)

## 学校支持情况
详见[学校支持列表](docs/school_support.md)

## 前端实现
此处展示由其他开发者开发的前端实现，供学习交流之用。如果您有自己的实现，欢迎提交PR。
- [ehall-swift](https://github.com/Kernelize/ehall-swift): iOS, iPadOS, macOS端实现

## 开发
环境要求：Python 3.10+

1. 安装依赖
```shell
pip install -r requirements.txt
```
2. 运行
```shell
flask run
```
仅供开发使用，生产环境请使用WSGI服务器。
