## {{ section_number }}. 移动端特定需求 (Mobile Specifics)

### {{ section_number }}.1 应用商店合规
- **Apple App Store**:
    - **隐私标签**: 必须披露数据收集情况（位置、联系信息等）。
    - **账户注销**: App 内必须提供"注销账户"的显性入口。
    - **登录**: 如果集成了微信/Google登录，则必须提供 "Sign in with Apple"。
- **Google Play Store**:
    - **数据安全**: 必须填写与隐私协议一致的数据安全部分。
    - **API 级别**: 必须支持 Android 14+ (Target SDK)。

### {{ section_number }}.2 设备兼容性
- **屏幕适配**: 支持刘海屏、灵动岛以及不同长宽比。
- **方向**: 默认竖屏；视频/图表等特定场景支持横屏。
- **权限管理**:
    - 运行时权限 (Runtime Permission)：相机、定位、通知。
    - **理由说明**: 必须在弹窗中解释"为什么"需要此权限。

### {{ section_number }}.3 离线能力
- **策略**: 离线优先 (Offline-First) 或 优雅降级。
- **数据同步**: 冲突解决策略（最后写入优先 / 手动合并）。
