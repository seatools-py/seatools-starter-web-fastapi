# seatools fastapi 启动器

该框架必须和`seatools-starter-server-*`的包集成配合使用, 这里以`seatools-starter-server-uvicorn`为例

## 使用指南
1. 安装, `poetry add fastapi seatools-starter-server-uvicorn seatools-starter-web-fastapi`
2. 配置`config/application.yml`如下:
```yaml

seatools:
  server:
    # 此处为uvicorn参数配置
    uvicorn:
      host: 0.0.0.0
      port: 8000
      workers: 1
      reload: true
  # 此处为fastapi配置
  fastapi:
    title: xxxxx
    description: xxx
    docs_url: none
```
3. 使用, 通过定义ioc容器函数加载
```python
from seatools.ioc import Autowired, Bean
from fastapi import FastAPI

# 添加中间件, 
@Bean
def xxx_middleware(app: FastAPI):
    from fastapi.middleware.cors import CORSMiddleware
    
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加全局异常处理
@Bean
def global_exception_handler(app: FastAPI):
    
    # 自定义异常处理
    @app.exception_handler(AssertionError)
    async def assert_exception_handler(request, exc):
        ...

# 添加路由方法
@Bean
def xxx_router(app: FastAPI):
    
    @app.get('/')
    async def hello():
        return "hello"

# 添加路由
from fastapi import APIRouter
custom_router = APIRouter(prefix='/custom')

@custom_router.get('/')
async def custom_hello():
    return "custom hello"

@Bean
def register_custom_router(app: FastAPI):
    app.include_router(custom_router)


# fastapi 与 seatools 的集成注入
@Bean
class ServiceA:
    
    async def hello(self):
        return "serviceA"


@Bean
def a_router(app: FastAPI):
    
    @app.get('/serviceA')
    async def serviceA(serviceA = Autowired(cls=ServiceA)): # 在控制器参数中使用Autowired方式注入seatools.ioc, 注意此处不能主动声明类型, fastapi会对参数类型校验不支持的类型将失败
        return await serviceA.hello()
    
# 或者在router层注入, 更推荐该方式

@Bean
def a2_router(app: FastAPI, serviceA: ServiceA): # 具体注入方式见seatools

    @app.get('/serviceA')
    async def serviceA():
        return await serviceA.hello()
```
3. 运行, 具体见`seatools-starter-server-*`, [`seatools-starter-server-uvicorn`](https://gitee.com/seatools-py/seatools-starter-server-uvicorn)
