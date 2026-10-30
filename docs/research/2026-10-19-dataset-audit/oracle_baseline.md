> Public audit edition. Local filenames mentioned below are evidence references, not files included in this publication. See [audit index](README.md).

# 受限数据oracle检查

本次不是一般人脸检测验收。任务仅为本次人工可视内容审核后的“UWA完整脸ROI vs 同采集衣物/背景ROI”。负类是真实同域测量，但固定位置/背景/空间尺度混杂仍在。

只取双方都通过粗筛的58次采集：train39对=78 ROI，val10对=20 ROI，test9对=18 ROI。严格受试者分组，全部会话/派生物同组；使用原始ROI，**不使用80份增强**。实际样本ID固定于 `oracle_sample_ids.json`。

采用固定低容量L2 Logistic Regression：SciPy成熟L-BFGS-B求解标准二元交叉熵，mean loss +0.01/2×权重平方和，截距不惩罚；训练集均值/标准差标准化，阈值0.5，最多1000迭代，无超参数搜索、无测试集选择。四个预先定义输入都完整报告，不按测试表现挑选发布。当前OpenCV安装不含ml、没有sklearn；未为此添加训练框架，使用SciPy优化器实现薄的标准逻辑回归目标。

| 输入 | Val Balanced Accuracy | Val Macro-F1 | Test Balanced Accuracy | Test Macro-F1 |
|---|---:|---:|---:|---:|
| 原始21点均值 | 0.9500 | 0.9499 | 0.9444 | 0.9443 |
| sum-one相对21点 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 原始650/550/450三波段代理 | 0.9500 | 0.9499 | 0.9444 | 0.9443 |
| sum-one三波段代理 | 1.0000 | 1.0000 | 0.9444 | 0.9443 |

测试混淆矩阵，行是真类、列是预测类，顺序 `[non_face, face]`：

- 原始21点：`[[8,1],[0,9]]`
- 相对21点：`[[9,0],[0,9]]`
- 原始三波段代理：`[[8,1],[0,9]]`
- 相对三波段代理：`[[8,1],[0,9]]`

失败记录：原始21点及原始三波段均将validation的[local sample ID withheld]与test的[local sample ID withheld]误判为face；相对三波段将test的[local sample ID withheld]误判为face。可视内容为衣物/背景，说明简单谱均值也可能受服饰材料/照明影响；本轮未根据错误样本改标签、调参或修改划分。完整预测及概率在 `oracle_predictions.json`，参数和验证集矩阵在 `oracle_results.json`。

**RGB边界：这里是同ROI、同split的三窄波段伪RGB代理，不是匹配的真实相机RGB基线。** UWA没有本轮可确认的同步标定RGB及谱响应，所以真正RGB比较仍未完成；不能把此表称为光谱优于RGB。三波段投影已按要求保留供定位/工程对照，并明确其来源。

18个测试ROI只有9次成对采集，且可能共享受试者的不同会话；不是18个完全独立实验。100%只是此小集合无错误，不是稳定识别人脸的证据。固定幕布跨split、脸与负类位置及裁剪尺度差异都可能解释高分。归一化21点比三波段少错1个样本，不足以建立可靠信息增益。

结论：当前谱曲线能分开这批受限正负ROI，足以作为工程数据流检查，但尚不能据此启动以“普适Face识别/超越RGB”为科学目标的N1训练。本轮停止在数据交付，不训练Deep Unrolling、不做新采集。
