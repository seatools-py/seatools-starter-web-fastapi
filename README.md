# Seatools FastAPI Starter

This framework must be used in conjunction with the seatools-starter-server-* packages, using seatools-starter-server-uvicorn as an example here.

[中文文档](./README_zh.md)

## Usage Guide
1. Install with `poetry add fastapi seatools-starter-server-uvicorn seatools-starter-web-fastapi`
2. Configure `config/application.yml` as follows:
```yaml
seatools:
  server:
    # Here are the uvicorn parameter configurations
    uvicorn:
      host: 0.0.0.0
      port: 8000
      workers: 1
      reload: true
  # Here are the FastAPI configurations
  fastapi:
    title: xxxxx
    description: xxx
    docs_url: none
```
3. Usage, load by defining ioc container functions
```python
from seatools.ioc import Autowired, Bean
from fastapi import FastAPI

# Add middleware
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

# Add global exception handler
@Bean
def global_exception_handler(app: FastAPI):
    
    # Custom exception handling
    @app.exception_handler(AssertionError)
    async def assert_exception_handler(request, exc):
        ...

# Add route method
@Bean
def xxx_router(app: FastAPI):
    
    @app.get('/')
    async def hello():
        return "hello"

# Add route
from fastapi import APIRouter
custom_router = APIRouter(prefix='/custom')

@custom_router.get('/')
async def custom_hello():
    return "custom hello"

@Bean
def register_custom_router(app: FastAPI):
    app.include_router(custom_router)

# FastAPI integration with seatools ioc injection
@Bean
class ServiceA:
    
    async def hello(self):
        return "serviceA"


@Bean
def a_router(app: FastAPI):
    
    @app.get('/serviceA')
    async def serviceA(serviceA = Autowired(cls=ServiceA)): # Inject seatools.ioc in the controller parameter using Autowired, note that the type should not be explicitly declared here, FastAPI will fail on parameter type checking for unsupported types
        return await serviceA.hello()
    
# Or inject at the router level, this method is more recommended

@Bean
def a2_router(app: FastAPI, serviceA: ServiceA): # Specific injection method see seatools

    @app.get('/serviceA')
    async def serviceA():
        return await serviceA.hello()
```
3. Run, see `seatools-starter-server-*`, example [`seatools-starter-server-uvicorn`](https://gitee.com/seatools-py/seatools-starter-server-uvicorn)
