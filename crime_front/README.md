# jekedao_front

## Project setup

```
npm install
```

### Compiles and hot-reloads for development

```
npm run serve
```

### Compiles and minifies for production

```
npm run build
```

### Lints and fixes files

```
npm run lint
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

urban-crime-management/
├── node_modules/                # NPM包目录
├── public/                      # 公共资源目录
│   ├── index.html               # 入口 HTML 文件
│   └── favicon.ico              # 图标文件
├── src/                         # 源代码目录
│   ├── assets/                  # 静态资源（图片、样式等）
│   │   ├── images/              # 项目使用的图片
│   │   ├── styles/              # 全局样式（如CSS、SCSS等）
│   │   └── icons/               # 图标
│   ├── components/              # 公共组件
│   │   ├── Header.vue           # 头部组件
│   │   ├── Footer.vue           # 底部组件
│   │   ├── CrimeMap.vue         # 地图组件（展示犯罪热点）
│   │   └── CrimeChart.vue       # 图表组件（展示犯罪统计）
│   ├── views/                   # 页面视图
│   │   ├── Dashboard.vue        # 用户仪表盘页面
│   │   ├── UserLogin.vue        # 登录页面
│   │   ├── UserRegistration.vue # 注册页面
│   │   ├── UserProfile.vue      # 用户个人信息页面
│   │   ├── CrimeEventList.vue   # 犯罪事件列表页面
│   │   ├── CrimeEventDetail.vue # 犯罪事件详情页面
│   │   ├── CaseProgressList.vue # 案件进展页面
│   │   ├── ClueList.vue     # 证据列表页面
│   │   └── ClueUpload.vue   # 证据上传页面
│   ├── services/                # 与后端API的交互服务
│   │   ├── authService.js       # 用户认证服务
│   │   ├── crimeEventService.js # 犯罪事件数据服务
│   │   ├── caseService.js       # 案件进展服务
│   │   └── clueService.js   # 证据管理服务
│   ├── router/                  # 路由配置
│   │   └── index.js             # Vue Router 路由文件
│   ├── store/                   # Vuex状态管理
│   │   ├── index.js             # Vuex主文件
│   │   ├── modules/             # 模块化存放状态
│   │   │   ├── user.js          # 用户状态模块
│   │   │   ├── crimeEvent.js    # 犯罪事件状态模块
│   │   │   └── clue.js      # 证据状态模块
│   ├── App.vue                  # 根组件
│   └── main.js                  # Vue项目的入口文件
├── .env                         # 环境变量配置文件
├── babel.config.js              # Babel编译配置
├── package.json                 # 项目配置文件
├── vue.config.js                # Vue配置文件
└── README.md                    # 项目说明文档
