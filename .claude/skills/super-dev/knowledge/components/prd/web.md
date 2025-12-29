## {{ section_number }}. Web 端特定需求 (Web Specifics)

### {{ section_number }}.1 SEO 与 社交分享
- **Meta 策略**: 所有公开页面必须包含动态 OpenGraph 标签 (Title, Image, Desc)。
- **Sitemap**: 每小时自动更新。
- **Robots**: 默认允许抓取，封禁 `/admin` 等路径。

### {{ section_number }}.2 浏览器兼容性
- **桌面端**: Chrome (Latest-2), Firefox (Latest-2), Safari (Latest-2), Edge.
- **移动 Web**: iOS Safari (iOS 16+), Android Chrome.

### {{ section_number }}.3 性能指标 (Core Web Vitals)
- **LCP (最大内容绘制)**: < 2.5s
- **CLS (累积布局偏移)**: < 0.1
- **FID (首次输入延迟)**: < 100ms
