# 领域知识库: Web 开发 (商业级)

> **上下文**: 适用于 `platform="web"` 的场景。

## 1. 技术约束与标准

### 1.1 SEO 与 可发现性
- **SSR/SSG**: 面向公众的页面必须使用服务端渲染 (Next.js/Nuxt)。
- **Meta 标签**:
    - `og:image`: 1200x630px
    - `twitter:card`: summary_large_image
    - `robots.txt`:以此控制允许/禁止抓取的路径
    - `sitemap.xml`: 自动生成
- **核心 Web 指标 (Core Web Vitals)**:
    - LCP: < 2.5s
    - FID: < 100ms
    - CLS: < 0.1

### 1.2 性能红线
- **包体积**: 初始 JS 包 < 200KB (gzip)。
- **图片格式**: AVIF/WebP，带回退机制。
- **缓存策略**: 
    - 静态资源: CDN 永久缓存 (`max-age=31536000, immutable`)
    - API: 读多写少使用 `stale-while-revalidate` 模式。

### 1.3 渐进式 Web 应用 (PWA)
- **Manifest**: 必须包含 `display: standalone`。
- **Service Worker**: 处理离线回退页。
- **可安装性**: 自定义"添加到主屏幕"引导逻辑。

## 2. 安全 (OWASP Top 10 Web)
- **CORS**: 严格限制允许的 Origin (禁用 `*`)。
- **CSP (内容安全策略)**:
    - `script-src`: 仅限 'self' (禁止内联脚本)。
- **Cookie**: 配置 `HttpOnly`, `Secure`, `SameSite=Strict`。
- **XSS**: 对所有 HTML 输入进行清洗 (DOMPurify)。

## 3. 架构模式
- **BFF (Backend for Frontend)**: 如果存在微服务，必须通过 BFF 聚合数据。
- **状态管理**:
    - 服务端状态: React Query / SWR (避免在全局 Store 存 API 数据)。
    - 客户端状态: Zustand / Pinia (保持最小化)。

## 4. 设计系统 (Web 特有)
- **响应式断点**:
    - 手机: < 640px
    - 平板: 640px - 1024px
    - 桌面: > 1024px
    - 宽屏: > 1440px
- **交互状态**: 所有可交互元素必须设计 Hover 和 Focus 态 (无障碍要求)。
