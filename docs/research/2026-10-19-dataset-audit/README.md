# D0 → D1 → D1-Data 审计入口

截至 2026-10-19，已完成公开数据调查、场景光谱目标定义与 UWA 标准化生产。当前任务为固定候选区域的 Face / Non-face，而不是身份识别或活体检测。**工程数据可用，通用二分类和超越 RGB 的科学结论尚未通过验收；未启动 N1 / Deep Unrolling。**

## 建议审计顺序

1. [数据来源与许可](dataset_survey.md)：五个候选，实际取得 UWA 完整归档与 CAVE 单场景；其余获取或用途限制保留。
2. [生产与质量报告](quality_report.md)：真实标签、分组、异常及处理方法。
3. [Oracle 基线](oracle_baseline.md)与[机器可读指标](oracle_metrics.json)：四组固定低容量逻辑回归，明确三波段代理不是真实 RGB。
4. [光谱目标定义](spectral_feature_definition.md)与[N1 数值接口记录](n1_interface.md)：历史 D1 检查及尚未满足的物理条件。
5. [配置模板](preprocessing_config.example.yaml)、[验证结果](validation_summary.json)、[本地证据哈希](local_evidence_hashes.json)、[源码审计快照](source_snapshot/README.md)。

## 当前数据账目

| 项目 | Train | Validation | Test | 合计 |
|---|---:|---:|---:|---:|
| 原始 Face ROI 接受 | 41 | 11 | 9 | 61 |
| 原始 Non-face ROI 接受 | 39 | 10 | 9 | 58 |
| 派生增强 | 80 | 0 | 0 | 80 |

119 个接受的原始 ROI 来自 **61 次采集**，不是 119 次独立观测。Oracle 仅使用正负均通过的 58 次采集（39/10/9），不使用增强。全清单286条含199条接受记录、80条待质量审核、1条待语义审核、6条越界拒绝。

正类来自眼点与视觉内容检查；负类来自同次采集左下衣物/背景区域，经 Agent 查看，**不是官方 Non-face 标签或独立人工复核**。受试者和采集隔离已验证，共同背景、位置、裁剪尺度及光照混杂仍在。测试集18个ROI仅9次成对采集；相对21点无误判不能证明泛化，更不能因比三波段少错1例而声称超越RGB。

## 实测 PSF 与版本边界

21波段实验 `spectral21_20261018_reset01` 的详细验收属于 optic_system，见[已发布的固定版本报告](https://github.com/Mr-enthalpy/optic_system/blob/4aed9b438b2c68ed6dd0e7d310c2c26f9ffb49df/docs/reports/2026-10-19-21-band-fixed-display-psf.md)。实际硬件采集版本为 `18dd598852b1d44ea80b4f6d53e1d2d5656f9e9b`。本次发布只整理研究证据，不重采、不部署、不推进 Submodule pin，也不把研究快照变为 optic_system 生产代码。

## 本次实际复核与公开边界

本地重新执行 `validate_build.py`：文件SHA、shape、有限值、21波段、均值/相对谱/伪RGB重算、受试者分组、父采集继承和训练增强重放均通过。重新执行 `oracle_check.py`，四个优化器收敛，78/20/18个训练/验证/测试ROI指标与报告一致。未执行新硬件测试，未重新运行历史 D1 operator 测试；其结果明确属于历史记录。

公开内容为作者撰写的报告、聚合指标、处理配置模板和无数据的源码审计快照。原始归档、派生人脸、预览、逐样本manifest、受试者划分、审核记录、逐样本预测和模型参数仍留本地。UWA目录许可与归档README存在冲突，按较严格的科研、不再分发边界处理。这里不是可下载的数据集，也不是仅凭clone即可复现结果的完整数据包。哈希用于有权访问本地证据时比对，不替代原始证据审核。

下一阶段先审核标签、背景捷径、RGB对照与辐射/空间模型限制，再决定是否开展PSF模拟或N1训练。此次提交不自动启动下一阶段。
