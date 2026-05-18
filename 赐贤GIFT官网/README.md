# GIFT Titanium 产品管理后台

为赐贤GIFT钛杯B2B官网创建的产品管理后台，简单易用，无需技术背景即可管理产品信息。

---

## 快速开始

### 1. 启动服务器

```bash
cd 用户上传/赐贤GIFT官网
python3 server.py
```

启动后显示：
```
GIFT Titanium Product Management Server

  Local URL:    http://localhost:8899
  Admin Panel:  http://localhost:8899/admin.html

  API Endpoints:
    GET  /api/products - Get all products
    POST /api/products - Save products
    POST /api/build    - Generate HTML pages
```

### 2. 打开管理后台

在浏览器中打开：**http://localhost:8899/admin.html**

---

## 管理后台功能

### 主页概览
- 顶部工具栏：导出JSON、导入JSON、保存更改、生成网站
- 左侧导航：按系列/分类筛选产品
- 顶部统计：产品总数、系列数量、价格区间

### 编辑产品

1. **快速编辑**（在产品卡片上直接修改）：
   - 产品标题
   - 产品描述
   - 最低/最高价格
   - 主图路径
   - 特性标签（点击添加/删除）

2. **完整编辑**（点击"编辑详情"按钮）：
   - 修改系列名称
   - 修改分类
   - 修改URL别名
   - 修改徽章
   - 添加/删除特性

### 添加新产品

1. 点击右上角 **"Add Product"** 按钮
2. 填写表单：
   - Series：系列编号（如 G1, G2）
   - Series Name：系列名称（如 Premium Thermos）
   - Title：产品标题
   - Description：产品描述
   - Min/Max Price：价格区间
   - Category：分类（Thermos/Outdoor/Office/Kids/Other）
   - Slug：URL别名（如 titanium-thermos）
   - Main Image：主图路径
   - Badge：徽章文字（Bestseller/New/Safe等）
   - Features：特性标签
3. 点击 **"Save Product"**

### 删除产品

1. 点击产品卡片右下角的 **"Delete"** 按钮
2. 确认删除

---

## 产品数据文件

### products.json 结构

```json
{
  "products": [
    {
      "id": "g1-thermos",
      "series": "G1",
      "seriesName": "Premium Thermos Collection",
      "category": "thermos",
      "slug": "titanium-thermos",
      "title": "Premium Pure Titanium Thermos Collection",
      "description": "产品描述...",
      "priceMin": 70,
      "priceMax": 350,
      "priceDisplay": "$70-350",
      "badge": "Bestseller",
      "features": ["Ti>99.8%", "600-1500ml", "12H Heat"],
      "mainImage": "images/g1-thermos-main.jpg",
      "detailImages": ["images/g1-detail-1.jpg"],
      "specs": { "材质": "纯钛", "容量": "600ml" },
      "subProducts": [...]
    }
  ],
  "siteInfo": {
    "email": "faisalhalim4637733624@gmail.com",
    "phone": "+86 13085622387"
  }
}
```

---

## 图片文件规范

### 存放位置
所有产品图片放在 `images/` 目录下

### 命名规范
```
images/
├── g1-thermos-main.jpg      # G1系列主图
├── g1-detail-1.jpg          # G1系列详情图1
├── g1-detail-2.jpg          # G1系列详情图2
├── g2-outdoor-main.jpg      # G2系列主图
├── g3-office-main.jpg       # G3系列主图
├── g4-kids-main.jpg         # G4系列主图
├── g5-glass-main.jpg        # G5系列主图
└── g8-container-main.jpg    # G8系列主图
```

### 更换图片步骤

1. 将新图片上传到 `images/` 目录
2. 在管理后台修改产品的主图路径
3. 点击"Save Changes"保存
4. 点击"Generate Website"重新生成网站

---

## 生成网站

### 方式一：管理后台按钮
点击右上角绿色 **"Generate Website"** 按钮

### 方式二：命令行
```bash
python3 build.py
```

### 生成的文件
- `index.html` - 首页产品区域更新
- `products.html` - 产品列表页更新
- `products/titanium-thermos.html` - G1详情页
- `products/outdoor-flask.html` - G2详情页
- `products/office-tea-coffee.html` - G3详情页
- `products/kids-titanium.html` - G4详情页
- `products/titanium-glass.html` - G5详情页
- `products/titanium-food-container.html` - G8详情页

---

## 保留信息（不可修改）

以下信息在代码中已固定，修改 products.json 不会改变它们：

- **邮箱**: faisalhalim4637733624@gmail.com
- **电话**: +86 13085622387
- **WhatsApp**: 8613085622387
- **GA追踪ID**: G-395164520

---

## API 接口

服务器提供以下 REST API：

### 获取产品数据
```bash
GET /api/products
```

### 保存产品数据
```bash
POST /api/products
Content-Type: application/json

{ ... products.json 内容 ... }
```

### 生成网站
```bash
POST /api/build
```

---

## 常见问题

### Q: 服务器无法启动？
确保：
1. 端口 8899 未被占用
2. Python3 已安装
3. 当前目录正确

### Q: 图片无法显示？
1. 检查图片路径是否正确
2. 确认图片文件存在于 `images/` 目录
3. 路径区分大小写

### Q: 修改没有保存？
1. 点击"Save Changes"按钮
2. 查看是否有错误提示
3. 可使用"Export JSON"导出备份

### Q: 生成网站后页面错乱？
检查 products.json 格式是否正确，可使用"Import JSON"导入备份文件恢复。

---

## 备份与恢复

### 导出备份
点击"Export JSON"下载 products.json 文件

### 导入恢复
1. 点击"Import JSON"
2. 选择备份的 JSON 文件
3. 点击"Save Changes"
4. 点击"Generate Website"

---

## 技术信息

- **服务器**: Python3 内置 http.server
- **数据格式**: JSON
- **不需要数据库**: 所有数据存储在 products.json
- **无需构建工具**: 生成的是纯静态 HTML

---

**更新时间**: 2025年
