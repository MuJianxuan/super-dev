# 领域知识库: 移动端开发 (iOS & Android)

> **上下文**: 适用于 `platform="mobile"` 或 iOS/Android 开发场景。

## 1. 商店审核红线

### 1.1 Apple App Store (围墙花园)
- **审核指南**: 
    - 严禁隐藏功能（如热更开关控制的违规内容）。
    - 严禁外部支付链接（虚拟商品必须走 IAP 内购）。
    - 登录: 只要集成了第三方登录，就必须集成 "Sign in with Apple"。
- **硬件支持**: 必须支持最近 2 代 iPhone 和 iPad 分辨率。

### 1.2 Google Play Store
- **碎片化**: 必须支持动态长宽比（折叠屏适配）。
- **权限**: 运行时权限必须有合理的用途说明。
- **后台限制**: 严格限制后台保活（必须使用 WorkManager）。

## 2. UI/UX 标准

### 2.1 iOS (HIG 指南)
- **导航**: 底部 Tab Bar + 导航栈 (Push/Pop)。
- **字体**: San Francisco。
- **手势**: 必须支持"左侧边缘右滑返回"。
- **弹窗**: 优先使用 Action Sheet (底部弹出)，而非居中 Alert。

### 2.2 Android (Material Design 3)
- **导航**: 底部导航栏 或 侧边导航轨 (平板)。
- **字体**: Roboto。
- **手势**: 支持预测性返回手势 (Predictive Back)。
- **组件**: 核心操作使用悬浮按钮 (FAB)。

## 3. 架构模式 (Mobile)
- **Clean Architecture**: 严格分层 (Domain / Data / Presentation)。
- **MVVM / MVI**: 
    - iOS: SwiftUI (MVVM) 或 UIKit。
    - Android: Jetpack Compose (MVI/MVVM)。
- **离线优先**: 本地数据库 (Realm/Room) 是标配，必须设计同步逻辑。

## 4. 发布策略
- **Beta**: TestFlight (iOS) / Internal Test Track (Android)。
- **灰度发布**: 1% -> 5% -> 20% -> 100% 逐步放量，监控崩溃率。
- **热修复**: CodePush (RN) 或原生热修 SDK（需注意审核风险）。
