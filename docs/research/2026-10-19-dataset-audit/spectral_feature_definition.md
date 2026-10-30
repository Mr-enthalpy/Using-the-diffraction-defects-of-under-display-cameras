> Historical D1 interface checks: the unlabelled 290 candidate curves are distinct from the later D1-Data production. Current label acceptance is reported in [quality_report.md](quality_report.md). No N1 training has started.

> Public audit edition. Local filenames mentioned below are evidence references, not files included in this publication. See [audit index](README.md).

# 21点曲线定义与验收

波长坐标固定 `450,460,...,650 nm`。UWA原始F_06…F_26与作者名义波段定义对应；文件不包含独立实测波长响应函数，10nm只是采样。原始归档和所有像素保持不变。

给定同一空间支持R及21个波段I，定义：

`s[b] = sum(I[b,y,x] for (y,x) in R) / |R|`

本轮`s`单位是UWA原始8bit强度DN，**不是反射率或已辐射校准的场景能谱**。正式数据可获得辐射标定后再建立有明确单位的新目标版本，不能悄悄替换当前语义。

相对曲线为 `q[b]=s[b]/sum(s)`，仅对有限、非负且总和>0的有效目标定义。零总和应返回无效状态，不用任意epsilon伪造有效谱。原始均值与相对曲线同时导出，不把归一化覆盖原值。此次290条曲线均为有限正总和。

## 导出契约

未来N1主输出 `[batch,21]`，波长顺序固定；必须配置声明输出为 `mean_intensity` 或 `relative_sum1`，监督目标严格同一策略。推荐当前研究以明确标注的相对强度为候选目标，同时保留raw mean供审核；尚不选定最终可训练目标。

每条曲线必须附：原始归档/文件SHA、sample_id、subject/session、sensor ROI `(x,y,width,height)` 半开区间、波长数组、处理版本/有效像素规则、量化/255比例、配准与辐射校准状态。`spectral_curves.json`包含这些实际来源信息和候选区域，`label=null`；不将网络embedding命名为光谱。

允许独立质量/不确定性输出，不把它藏进21维主曲线。不确定性需要未来独立重复或可靠噪声模型校准；本轮的量化区间不是置信区间。C1只消费明确曲线及事先声明的质量筛选；C2/C3不创建空模块。N1输出可以不调用C1而直接保存、绘图与检查。

## 实际敏感性检查

- 原始平均和sum-one曲线均已从145次采集的两个候选ROI提取，`spectral_curve_diagnostics.png`展示中位数与10–90%区间，图中组别不是类别。
- 量化检查假设未触顶像素为最近整数舍入，均值误差界±0.5DN（不假设独立误差随像素数缩小）。用逐band上下界传播到sum-one后，脸候选最大区间宽0.001908，角落0.003333。存在255时该界不覆盖真实截断误差；隐藏图像处理也可能不满足舍入假设。
- 使用全21波段共同的`I<255`空间mask，避免各band不同支持制造曲线差异；输出敏感性曲线但不替换原始目标。脸候选相对曲线最大L2变化0.008396。
- 数值测试确认全谱同一乘性缩放在sum-one下抵消。波长依赖照明、曝光、增益、加性偏置、clipping不会因此消除；本数据无法分离这些因素。同身份跨会话变化见可行性报告，不能归因于单一因素。
- 未做跨波段配准或暗场补偿，不假装ROI平均已解决配准。未来需保证所有band使用可比较空间支持，边界不因运动混入不同材料。

## 结构性限制

空间平均对任意共同像素置换保持不变，已用数值测试验证。因此一张人脸与其打乱空间布局的图像可以有相同21点均值，均值无法一般地编码“脸的结构”。谱曲线可提供材料/肤色相关线索，但不自动等于语义Face证据。本轮不改变用户架构，也不以此宣称任务必然失败；必须先用公平正负样本验证该瓶颈是否足以完成限定场景任务。

匹配RGB基线未来需已知共同光谱响应矩阵与明确辐射输入，或同次配准RGB。不能随意抽650/550/450三个band冒充相机RGB，也不能将不同场景的sRGB照片当公平对照。当前UWA这些条件尚不具备。
